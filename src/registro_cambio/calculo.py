"""Cálculo: qué resulta de cada requisito con cada régimen.

El régimen (`completo` o `simplificado`) es un parámetro, no un dato de la
entrada (modelo, §0.1, principio 2). Para cada requisito del catálogo, el
cálculo da un resultado con su cita:

- `cumple`: el registro tiene lo que el requisito pide. En R-01, R-04, R-08 y
  R-24 lo garantiza ya la validación de entrada, y el resultado lo dice;
- `incumplimiento`: le falta algo, o lo contradice, y lo sostiene el texto de
  la norma aplicado al registro (modelo, §0.1 bis, principio 2);
- `aviso`: el texto no sostiene un incumplimiento, pero una lectura propia
  (una decisión D-n, otra decisión propia del modelo o una duda DI-n) dice que
  falta algo. El resultado lleva un aviso A-03 que remite a esa lectura;
- `sin_indicio_de_incumplimiento`: en los requisitos que dependen de un
  mecanismo de la entidad (modelo, §0.1 bis, principio 1; D-1), en lugar de
  `cumple` y de `aviso`. El registro de un cambio puede probar que el
  mecanismo falló, pero no que existe;
- `no_aplica`: el régimen no lo exige, o no se da la condición de la que
  depende. El motivo se dice siempre.

Los avisos (A-n) y los datos informativos (I-n) van aparte de los requisitos.
Las dudas de implementación se citan como «dudas, DI-n»
(docs/dudas-implementacion.md).
"""

from dataclasses import dataclass, field
from typing import Callable, Optional

from registro_cambio.modelo import (
    APLICADO,
    DATOS_PRODUCCION,
    FASES_HASTA_INTEGRACION,
    NO_CUMPLE,
    NO_PRODUCCION,
    ORIGENES_DE_TERCEROS,
    SEGURIDAD_PAQUETES,
    TECNICAS,
    Entrada,
)

COMPLETO = "completo"
SIMPLIFICADO = "simplificado"
REGIMENES = (COMPLETO, SIMPLIFICADO)

CUMPLE = "cumple"
INCUMPLIMIENTO = "incumplimiento"
AVISO = "aviso"
SIN_INDICIO = "sin_indicio_de_incumplimiento"
NO_APLICA = "no_aplica"
ESTADOS = (CUMPLE, INCUMPLIMIENTO, AVISO, SIN_INDICIO, NO_APLICA)

GARANTIZADO = "Garantizado por la validación de entrada."
SIN_BASE_TITULO_III = "El título III del Reglamento Delegado no tiene equivalente (modelo, §0.3 y §13)."

# Aviso de lectura propia: con esa lectura, falta algo. Activa el código 1.
AVISO_LECTURA = "A-03"


@dataclass(frozen=True)
class Resultado:
    id: str
    nombre: str
    estado: str
    cita: str
    motivos: tuple[str, ...] = ()
    notas: tuple[str, ...] = ()
    garantizado: bool = False


@dataclass(frozen=True)
class Aviso:
    """Un aviso (A-n) o un dato informativo (I-n). No es un incumplimiento.

    Los avisos A-03 vienen de una lectura propia (`lectura`) aplicada a un
    requisito (`requisito`) y dicen que, con esa lectura, falta algo.
    """

    codigo: str
    mensaje: str
    cita: str
    requisito: Optional[str] = None
    lectura: Optional[str] = None

    @property
    def exige_actuar(self) -> bool:
        return self.codigo == AVISO_LECTURA


@dataclass(frozen=True)
class ResultadoRegimen:
    regimen: str
    resultados: tuple[Resultado, ...]
    avisos: tuple[Aviso, ...]
    informativos: tuple[Aviso, ...]

    @property
    def incumplimientos(self) -> tuple[Resultado, ...]:
        return tuple(r for r in self.resultados if r.estado == INCUMPLIMIENTO)

    @property
    def avisos_de_lectura(self) -> tuple[Aviso, ...]:
        return tuple(a for a in self.avisos if a.exige_actuar)

    @property
    def activadores(self) -> tuple[str, ...]:
        """Qué exige actuar en este régimen: el texto o una lectura propia."""
        return tuple(f"{r.id} (texto: {r.cita})" for r in self.incumplimientos) + tuple(
            f"{a.requisito} (lectura propia: {a.lectura})" for a in self.avisos_de_lectura
        )


# --- Utilidades ------------------------------------------------------------------


def _vacio(texto: Optional[str]) -> bool:
    # Dudas, DI-1: una cadena vacía o solo con espacios cuenta como dato ausente.
    # No es una lectura jurídica: sigue la base del requisito al que pertenece.
    return texto is None or not texto.strip()


class _Contexto:
    def __init__(self, entrada: Entrada):
        self.e = entrada
        self.c = entrada.cambio
        self.actores = {a.id: a for a in entrada.actores}

    def es_persona(self, id_):
        return self.actores[id_].es_persona

    def hay_persona(self, ids):
        return any(self.es_persona(i) for i in ids)

    def funciones(self, id_):
        """D-1: un agente cuenta con su función y con la de su persona responsable."""
        a = self.actores[id_]
        fs = {a.funcion}
        if not a.es_persona:
            fs.add(self.actores[a.persona_responsable].funcion)
        return fs

    def personas(self, id_):
        """El actor y, si es un agente, su persona responsable (D-1; modelo, §3.2)."""
        a = self.actores[id_]
        return {a.id} if a.es_persona else {a.id, a.persona_responsable}

    @property
    def inicio(self):
        return self.c.implantacion.inicio


@dataclass(frozen=True)
class Requisito:
    id: str
    nombre: str
    # Cita en cada régimen; None si el régimen no lo exige.
    cita: dict
    # Depende de un mecanismo de la entidad: nunca da `cumple` (modelo, §0.1 bis; D-1).
    mecanismo: bool
    comprobar: Callable
    # Motivo de `no_aplica` en el régimen sin cita.
    sin_cita: dict = field(default_factory=dict)
    # La carga ya exige todo lo que el requisito pide.
    garantizado: bool = False


@dataclass(frozen=True)
class _Salida:
    """Lo que devuelve la comprobación de un requisito."""

    estado: str
    motivos: tuple[str, ...] = ()
    notas: tuple[str, ...] = ()
    # (lectura, mensaje): lo que falta con una lectura propia.
    lecturas: tuple[tuple[str, str], ...] = ()


def _no_aplica(motivo):
    return _Salida(NO_APLICA, (motivo,))


def _evaluar(faltas=(), lecturas=(), notas=(), ok=()):
    """Texto antes que lectura: con faltas textuales, incumplimiento; si solo hay
    lecturas, aviso; si nada, cumple (modelo, §0.1 bis, principio 2)."""
    if faltas:
        return _Salida(INCUMPLIMIENTO, tuple(faltas), tuple(notas), tuple(lecturas))
    if lecturas:
        return _Salida(AVISO, tuple(f"Con la lectura {ref}: {msg}" for ref, msg in lecturas), tuple(notas), tuple(lecturas))
    return _Salida(CUMPLE, tuple(ok), tuple(notas))


# --- Requisitos ------------------------------------------------------------------


def _garantizado(x, regimen):
    return _Salida(CUMPLE, (GARANTIZADO,))


def _elementos(x, regimen):
    # Dudas, DI-8: una «lista no vacía» fuera de los pasos se juzga aquí, no en la carga.
    return _evaluar(faltas=[] if x.c.elementos else ["`cambio.elementos` está vacía: no dice qué se cambia."])


def _que_actuaron(x):
    """Dudas, DI-2: los actores que actúan en los sistemas de TIC."""
    c = x.c
    ids = list(c.implantacion.actores)
    for p in c.pruebas:
        ids += p.realizada_por
    for r in c.revisiones_codigo:
        ids += r.realizada_por
    if c.vuelta_atras is not None and c.vuelta_atras.ejecucion is not None:
        ids += c.vuelta_atras.ejecucion.actores
    ids += [a.actor for a in c.acciones]
    return list(dict.fromkeys(ids))


def _identificacion(x, regimen):
    # Lectura propia: los arts. 21.c) y 33.b) regulan la política de acceso; que cada
    # registro lleve la cuenta, o diga quién hizo cada prueba, lo pide el modelo (§3.1).
    lecturas = [
        ("modelo §3.1; dudas, DI-2", f"el actor {i} actuó en los sistemas de TIC y no tiene `cuenta`.")
        for i in _que_actuaron(x)
        if x.actores[i].cuenta is None
    ]
    lecturas += [
        ("modelo §7.1; dudas, DI-8", f"la prueba {p.id} no dice quién la hizo (`realizada_por` vacía).")
        for p in x.c.pruebas
        if not p.realizada_por
    ]
    lecturas += [
        ("modelo §7.2; dudas, DI-8", f"la revisión {r.id} no dice quién la hizo (`realizada_por` vacía).")
        for r in x.c.revisiones_codigo
        if not r.realizada_por
    ]
    return _evaluar(lecturas=lecturas)


def _aprobaciones(x):
    """Los pasos de aprobación del cambio: la previa y la posterior de emergencia."""
    pasos = []
    if x.c.aprobacion is not None:
        pasos.append(("cambio.aprobacion", x.c.aprobacion))
    if x.c.emergencia is not None and x.c.emergencia.revision_posterior.aprobacion is not None:
        pasos.append(("cambio.emergencia.revision_posterior.aprobacion", x.c.emergencia.revision_posterior.aprobacion))
    return pasos


def coincidencias_independencia(x):
    """D-1: coincidencias entre quien aprueba y quien solicita o aplica.

    Devuelve tres listas de mensajes:
    - el mismo actor: lo sostiene el texto del art. 17.1.b);
    - la persona responsable de un agente: lectura propia (modelo, §3.2; D-1);
    - personas distintas de la misma función: lectura propia (considerando 17; D-1).
    """
    mismo_actor, responsable, misma_funcion = [], [], []
    otros = [("solicita", i) for i in x.c.solicitud.actores] + [("aplica", i) for i in x.c.implantacion.actores]
    for ruta, paso in _aprobaciones(x):
        for a in paso.actores:
            for papel, o in otros:
                if a == o:
                    mismo_actor.append(f"{a} aprueba ({ruta}) y también {papel}.")
                elif x.personas(a) & x.personas(o):
                    comunes = ", ".join(sorted(x.personas(a) & x.personas(o)))
                    responsable.append(f"{a} aprueba ({ruta}) y {o} {papel}: responde de los dos la persona {comunes}.")
                elif x.funciones(a) & x.funciones(o):
                    funciones = ", ".join(sorted(x.funciones(a) & x.funciones(o)))
                    misma_funcion.append(f"{a} aprueba ({ruta}) y {o} {papel}: son de la misma función ({funciones}).")
    return mismo_actor, responsable, misma_funcion


def _independencia(x, regimen):
    if not _aprobaciones(x):
        # Dudas, DI-9: sin aprobación no hay indicio de dependencia; la falta la dan R-23 y R-27.
        return _evaluar(ok=["No hay ninguna aprobación con la que comparar; ver R-23 y R-27 (dudas, DI-9)."])
    mismo_actor, responsable, misma_funcion = coincidencias_independencia(x)
    notas = []
    if mismo_actor:
        notas.append(
            "El mismo actor aprueba y solicita o aplica: el registro de este cambio muestra que el mecanismo del "
            "art. 17.1.b) no funcionó en él. Ninguna lectura lo salva (D-1)."
        )
    else:
        notas.append("El registro no puede probar que el mecanismo exista ni que funcione (D-1; modelo, §14).")
    lecturas = [("D-1 (persona responsable del agente, modelo §3.2)", m) for m in responsable]
    lecturas += [("D-1 (considerando 17: funciones «separadas»)", m) for m in misma_funcion]
    return _evaluar(
        faltas=mismo_actor,
        lecturas=lecturas,
        notas=notas,
        ok=["Ninguna función de quien aprueba coincide con las de quien solicita o aplica."],
    )


def _responsabilidades(x, regimen):
    r = x.c.responsabilidades
    incisos = {
        "especificacion_planificacion": "i",
        "diseno_transicion": "ii",
        "pruebas_ultimacion": "iii",
        "aseguramiento_calidad": "iv",
    }
    # Lectura propia: el art. 17.1.c) pide describirlas en el procedimiento; registrar
    # la asignación de cada cambio es una decisión del modelo (§5.1).
    lecturas = [
        ("modelo §5.1", f"`cambio.responsabilidades.{k}` está vacía (art. 17.1.c.{inciso}).")
        for k, inciso in incisos.items()
        if not getattr(r, k)
    ]
    return _evaluar(lecturas=lecturas)


def _objeto_alcance(x, regimen):
    faltas = []
    if _vacio(x.c.objeto):
        faltas.append("Falta `cambio.objeto`.")
    if _vacio(x.c.alcance_descripcion):
        faltas.append("Falta `cambio.alcance.descripcion`.")
    if not x.c.alcance_sistemas:
        faltas.append("`cambio.alcance.sistemas` está vacía.")
    return _evaluar(faltas=faltas)


def _resultados_esperados(x, regimen):
    return _evaluar(faltas=["Falta `cambio.resultados_esperados`."] if _vacio(x.c.resultados_esperados) else [])


def _comunicacion(x, regimen):
    return _evaluar(faltas=[] if x.c.comunicaciones else ["`cambio.comunicaciones` está vacía."])


def _verificacion_seguridad(x, regimen):
    v = x.c.verificacion_seguridad
    if v is None:
        return _evaluar(faltas=["Falta `cambio.verificacion_seguridad`."])
    lecturas = []
    if v.resultado == NO_CUMPLE and x.c.implantacion.resultado == APLICADO:
        # Dudas, DI-3: lectura propia.
        lecturas.append(
            ("dudas, DI-3", "la verificación dice que el cambio no cumple los requisitos de seguridad, y el cambio se aplicó.")
        )
    return _evaluar(lecturas=lecturas)


def _evaluacion(x, regimen):
    ev = x.c.evaluacion
    if ev is None:
        return _evaluar(faltas=["Falta `cambio.evaluacion`."])
    if regimen == SIMPLIFICADO:
        return _evaluar()
    faltas, lecturas = [], []
    if _vacio(ev.repercusion_seguridad):
        faltas.append("Falta `cambio.evaluacion.repercusion_seguridad` (art. 17.1.h).")
    if ev.requiere_medidas_adicionales is None:
        faltas.append("Falta `cambio.evaluacion.requiere_medidas_adicionales` (art. 17.1.h).")
    elif ev.requiere_medidas_adicionales and not ev.medidas_adicionales:
        # Lectura propia: el art. 17.1.h) pide evaluar si hacen falta, no enumerarlas (modelo, §6.2).
        lecturas.append(("modelo §6.2", "la evaluación dice que hacen falta medidas adicionales y no dice cuáles."))
    return _evaluar(faltas=faltas, lecturas=lecturas)


def _cambio_importante(x, regimen):
    c = x.c
    if c.cambio_importante is None:
        # Lectura propia: la norma no define «importante»; la declaración la pide el modelo (§4).
        return _evaluar(lecturas=[("modelo §4", "la entidad no declara si el cambio es importante (`cambio_importante` es null).")])
    if not c.cambio_importante:
        return _no_aplica("La entidad declara que el cambio no es importante.")
    if c.evaluacion is None or _vacio(c.evaluacion.riesgos):
        return _evaluar(faltas=["El cambio es importante y falta `cambio.evaluacion.riesgos`."])
    return _evaluar()


def _pruebas_previas(x, regimen):
    c = x.c
    if not c.pruebas:
        return _evaluar(faltas=["`cambio.pruebas` está vacía."])
    previas = [p.id for p in c.pruebas if p.fecha < x.inicio]
    if previas:
        return _evaluar(ok=[f"Pruebas anteriores a la implantación: {', '.join(previas)}."])
    sin_previas = "Ninguna prueba es anterior a `cambio.implantacion.inicio`."
    if c.emergencia is not None and regimen == COMPLETO:
        # Dudas, DI-4: lectura propia; el art. 17.1.f) podría admitir pruebas posteriores.
        return _evaluar(lecturas=[("dudas, DI-4", f"cambio de emergencia: {sin_previas[0].lower()}{sin_previas[1:]}")])
    notas = []
    if c.emergencia is not None:
        notas.append("Art. 37.b) literal, sin excepción de emergencia. La D-5 documenta una lectura alternativa.")
    return _evaluar(faltas=[sin_previas], notas=notas)


def _seguridad_paquetes(x, regimen):
    paquetes = [p for p in x.c.pruebas if p.tipo == SEGURIDAD_PAQUETES]
    if not paquetes:
        # Dudas, DI-5: el modelo no exige una prueba de este tipo en cada cambio.
        return _no_aplica("No hay pruebas de tipo `seguridad_paquetes` (dudas, DI-5).")
    tardias = [p.id for p in paquetes if p.fase not in FASES_HASTA_INTEGRACION]
    return _evaluar(faltas=[f"La prueba {i} de seguridad de paquetes es posterior a la fase de integración." for i in tardias])


def _datos_produccion(x, regimen):
    no_prod = [p for p in x.c.pruebas if p.entorno == NO_PRODUCCION]
    if not no_prod:
        return _no_aplica("No hay pruebas en entornos distintos del de producción.")
    faltas, lecturas = [], []
    for p in no_prod:
        if p.datos != DATOS_PRODUCCION:
            continue
        ex = p.excepcion_datos_produccion
        if ex is None:
            faltas.append(f"La prueba {p.id} usa datos de producción sin excepción (art. 16.5.a).")
            continue
        if not x.hay_persona(ex.aprobacion.actores):
            lecturas.append(("D-4", f"la excepción de la prueba {p.id} no la aprueba ninguna persona."))
        if p.fecha > ex.hasta:
            faltas.append(f"La prueba {p.id} es posterior al límite de la excepción (art. 16.6: «durante un tiempo limitado»).")
    return _evaluar(faltas=faltas, lecturas=lecturas)


def _revision_codigo(x, regimen):
    c = x.c
    if not c.incluye_codigo_fuente:
        return _no_aplica("El cambio no incluye código fuente (`incluye_codigo_fuente` es false).")
    # Lectura propia: el art. 16.3 regula el procedimiento; que cada cambio tenga sus
    # revisiones, con las dos técnicas, lo pide el modelo (§7.2).
    if not c.revisiones_codigo:
        return _evaluar(lecturas=[("modelo §7.2", "el cambio incluye código fuente y no tiene revisiones de código.")])
    tecnicas = {t for r in c.revisiones_codigo for t in r.tecnicas}
    # D-2, punto 1: la revisión de un agente cuenta como revisión del art. 16.3.
    return _evaluar(lecturas=[("modelo §7.2", f"ninguna revisión usa la técnica {t}.") for t in TECNICAS if t not in tecnicas])


def _plan_accion(x, regimen):
    revisiones = [r for r in x.c.revisiones_codigo if r.hallazgos]
    if not revisiones:
        return _no_aplica("Ninguna revisión de código tiene hallazgos.")
    faltas, lecturas = [], []
    for r in revisiones:
        p = r.plan_accion
        if p is None:
            faltas.append(f"La revisión {r.id} tiene hallazgos y no tiene plan de acción.")
            continue
        if not x.hay_persona(p.adoptado_por):
            lecturas.append(("D-2, punto 2", f"el plan de acción de la revisión {r.id} no lo adopta ninguna persona."))
        cubiertos = {h for m in p.medidas for h in m.hallazgos}
        sin = [h.id for h in r.hallazgos if h.id not in cubiertos]
        if sin:
            faltas.append(f"El plan de acción de la revisión {r.id} no hace frente a: {', '.join(sin)}.")
    return _evaluar(faltas=faltas, lecturas=lecturas)


def _seguimiento(x, regimen):
    revisiones = [r for r in x.c.revisiones_codigo if r.plan_accion is not None]
    if not revisiones:
        return _no_aplica("Ninguna revisión de código tiene plan de acción.")
    faltas, lecturas = [], []
    for r in revisiones:
        if not r.seguimiento:
            faltas.append(f"El plan de acción de la revisión {r.id} no tiene seguimiento.")
        elif not any(x.hay_persona(s.actores) for s in r.seguimiento):
            lecturas.append(("D-2, punto 3", f"el seguimiento de la revisión {r.id} no tiene ninguna entrada con una persona."))
    return _evaluar(faltas=faltas, lecturas=lecturas)


def _origen_codigo(x, regimen):
    if not x.c.incluye_codigo_fuente:
        return _no_aplica("El cambio no incluye código fuente.")
    # Lectura propia: declarar el origen lo pide el modelo para aplicar los arts. 16.7 y 16.8 (D-3).
    return _evaluar(lecturas=[] if x.c.origen_codigo else [("D-3", "el cambio incluye código fuente y `origen_codigo` está vacía.")])


def _codigo_terceros(x, regimen):
    terceros = [o for o in x.c.origen_codigo if o in ORIGENES_DE_TERCEROS]
    if not terceros:
        return _no_aplica("La entidad no declara código de terceros, propietario ni abierto (D-3).")
    previas = [r.id for r in x.c.revisiones_codigo if r.fecha < x.inicio]
    if not previas:
        return _evaluar(faltas=[f"Origen declarado: {', '.join(terceros)}; ninguna revisión de código es anterior a la implantación."])
    return _evaluar(ok=[f"Revisiones anteriores a la implantación: {', '.join(previas)}."])


def _controles_integridad(x, regimen):
    # Lectura propia: los arts. 16.1.c), 16.7 y 37.c) regulan la política y el procedimiento;
    # registrar los controles aplicados a cada cambio lo pide el modelo (§6.3).
    return _evaluar(lecturas=[] if x.c.controles_integridad else [("modelo §6.3", "`cambio.controles_integridad` está vacía.")])


def _aprobacion(x, regimen):
    c = x.c
    notas = []
    if regimen == COMPLETO and c.emergencia is not None and c.aprobacion is None:
        return _no_aplica("Cambio de emergencia: la aprobación es posterior a la aplicación (art. 17.1.g); ver R-27.")
    if regimen == SIMPLIFICADO and c.emergencia is not None:
        notas.append(
            "Art. 37.b) literal: el título III no prevé excepción de emergencia. La D-5 documenta una lectura "
            "alternativa, basada en el «enfoque basado en el riesgo» del art. 37, que podría admitirla."
        )
    if c.aprobacion is None:
        return _evaluar(faltas=["Falta `cambio.aprobacion`."], notas=notas)
    faltas, lecturas = [], []
    if c.aprobacion.fecha >= x.inicio:
        faltas.append("`cambio.aprobacion` no es anterior a `cambio.implantacion.inicio`.")
    if not x.hay_persona(c.aprobacion.actores):
        lecturas.append(("D-4", "`cambio.aprobacion` no la da ninguna persona."))
    return _evaluar(faltas=faltas, lecturas=lecturas, notas=notas)


def _vuelta_atras(x, regimen):
    v = x.c.vuelta_atras
    if v is None:
        return _evaluar(faltas=["Falta `cambio.vuelta_atras`."])
    faltas, lecturas = [], []
    if not v.responsables:
        faltas.append("`cambio.vuelta_atras.responsables` está vacía.")
    if _vacio(v.procedimiento):
        faltas.append("Falta `cambio.vuelta_atras.procedimiento`.")
    if x.c.implantacion.resultado != APLICADO and v.ejecucion is None:
        # Lectura propia: el art. 17.1.e) pide procedimientos y responsabilidades, no
        # registrar la ejecución (modelo, §8).
        lecturas.append(
            ("modelo §8", f"el resultado de la implantación es «{x.c.implantacion.resultado}» y falta `cambio.vuelta_atras.ejecucion`.")
        )
    return _evaluar(faltas=faltas, lecturas=lecturas)


def _emergencia(x, regimen):
    e = x.c.emergencia
    if e is None:
        return _no_aplica("El cambio no siguió el procedimiento de emergencia (`emergencia` es null).")
    # Lectura propia: el art. 17.1.f) regula el procedimiento; que el registro lo nombre,
    # con sus salvaguardias, lo pide el modelo (§9).
    lecturas = []
    if _vacio(e.procedimiento):
        lecturas.append(("modelo §9", "falta `cambio.emergencia.procedimiento`."))
    if _vacio(e.salvaguardias):
        lecturas.append(("modelo §9", "falta `cambio.emergencia.salvaguardias`."))
    return _evaluar(lecturas=lecturas)


def _revision_posterior(x, regimen):
    e = x.c.emergencia
    if e is None:
        return _no_aplica("El cambio no es de emergencia.")
    rp = e.revision_posterior
    faltas, lecturas = [], []
    for k in ("documentacion", "reexamen", "evaluacion", "aprobacion"):
        paso = getattr(rp, k)
        ruta = f"cambio.emergencia.revision_posterior.{k}"
        if paso is None:
            # Dudas, DI-6: el art. 17.1.g) no fija plazo; «pendiente» es una lectura propia.
            lecturas.append(("dudas, DI-6", f"falta `{ruta}`: la revisión posterior está pendiente."))
        elif paso.fecha <= x.inicio:
            faltas.append(f"`{ruta}` no es posterior a la aplicación («tras su aplicación»).")
    if rp.aprobacion is not None and not x.hay_persona(rp.aprobacion.actores):
        lecturas.append(("D-4", "`cambio.emergencia.revision_posterior.aprobacion` no la da ninguna persona."))
    return _evaluar(faltas=faltas, lecturas=lecturas)


def _verificacion_posterior(x, regimen):
    v = x.c.verificacion_posterior
    if v is None:
        if x.c.implantacion.resultado != APLICADO:
            # Dudas, DI-10: lectura propia.
            return _evaluar(
                lecturas=[("dudas, DI-10", f"el cambio está «{x.c.implantacion.resultado}» y falta `cambio.verificacion_posterior`.")]
            )
        return _evaluar(faltas=["Falta `cambio.verificacion_posterior`."])
    if v.fecha <= x.inicio:
        # Lectura propia: «verifiquen» no fija el orden; lo fija el modelo (§10).
        return _evaluar(lecturas=[("modelo §10", "`cambio.verificacion_posterior` no es posterior a `cambio.implantacion.inicio`.")])
    return _evaluar(ok=[f"Resultado: {v.resultado}."])


# --- Catálogo --------------------------------------------------------------------


def _req(id_, nombre, completo, simplificado, comprobar, mecanismo=False, garantizado=False):
    sin_cita = {}
    if completo is None:
        sin_cita[COMPLETO] = "Solo lo exige el régimen simplificado."
    if simplificado is None:
        sin_cita[SIMPLIFICADO] = SIN_BASE_TITULO_III
    return Requisito(
        id_, nombre, {COMPLETO: completo, SIMPLIFICADO: simplificado}, mecanismo, comprobar, sin_cita, garantizado
    )


CATALOGO = (
    _req("R-01", "Registro del cambio", "DORA, art. 9.4.e) («se registren»); art. 12.2.c.iii)", "Art. 38.2 («se registre»); art. 34.f)", _garantizado, garantizado=True),
    _req("R-02", "Elementos que se cambian", "Art. 17.1.d.i); art. 17.1, encabezado", None, _elementos),
    _req("R-03", "Identificación de los actores en sus acciones", "Arts. 20.2.a) y 21.c)", "Art. 33.b)", _identificacion),
    _req("R-04", "Quién solicita", "Art. 17.1.b)", None, _garantizado, garantizado=True),
    _req("R-05", "Independencia entre quien aprueba y quien solicita o aplica", "Art. 17.1.b); considerando 17; D-1", None, _independencia, mecanismo=True),
    _req("R-06", "Funciones y responsabilidades del cambio", "Art. 17.1.c), incisos i) a iv)", None, _responsabilidades, mecanismo=True),
    _req("R-07", "Objeto y alcance", "Art. 17.1.d.i)", None, _objeto_alcance),
    _req("R-08", "Calendario", "Art. 17.1.d.ii)", None, _garantizado, garantizado=True),
    _req("R-09", "Resultados esperados", "Art. 17.1.d.iii)", None, _resultados_esperados),
    _req("R-10", "Comunicación de los detalles del cambio", "Art. 17.1.d), encabezado", None, _comunicacion),
    _req("R-11", "Verificación de los requisitos de seguridad", "Art. 17.1.a)", None, _verificacion_seguridad),
    _req("R-12", "Evaluación del cambio", "DORA, art. 9.4.e) («evalúen»); art. 17.1.h)", "Art. 38.2 («evalúe»)", _evaluacion),
    _req("R-13", "Riesgos de un cambio importante", None, "Art. 31.1.e)", _cambio_importante),
    _req("R-14", "Pruebas antes de la implantación", "DORA, art. 9.4.e); art. 16.2 («antes de su uso»)", "Art. 37.b); art. 38.2", _pruebas_previas),
    _req("R-15", "Seguridad de los paquetes a más tardar en integración", "Art. 16.4", None, _seguridad_paquetes),
    _req("R-16", "Datos de producción en entornos de prueba", "Art. 16.5.a) y 16.6; D-4", None, _datos_produccion),
    _req("R-17", "Revisión del código fuente, estática y dinámica", "Art. 16.3; D-2", None, _revision_codigo),
    _req("R-18", "Plan de acción ante los hallazgos", "Art. 16.3.b); D-2", None, _plan_accion),
    _req("R-19", "Seguimiento del plan de acción", "Art. 16.3.c); D-2", None, _seguimiento),
    _req("R-20", "Origen del código", "Art. 16.7 y 16.8; D-3", None, _origen_codigo),
    _req("R-21", "Revisión previa del código de terceros, propietario o abierto", "Art. 16.8; D-3", None, _codigo_terceros),
    _req("R-22", "Medidas contra la alteración o la manipulación", "Art. 16.1.c); art. 16.7", "Art. 37.c)", _controles_integridad, mecanismo=True),
    _req("R-23", "Aprobación", "DORA, art. 9.4.e) («aprueben»); art. 16.2; art. 17.1.b); D-4", "Art. 37.b); art. 38.2; D-4; D-5", _aprobacion),
    _req("R-24", "Aplicación", "DORA, art. 9.4.e) («apliquen»)", "Art. 38.2 («aplique»)", _garantizado, garantizado=True),
    _req("R-25", "Vuelta atrás", "Art. 17.1.e)", None, _vuelta_atras),
    _req("R-26", "Procedimiento de emergencia con salvaguardias", "Art. 17.1.f)", None, _emergencia, mecanismo=True),
    _req("R-27", "Revisión posterior del cambio de emergencia", "Art. 17.1.g); D-4", None, _revision_posterior),
    _req("R-28", "Verificación posterior", "DORA, art. 9.4.e) («verifiquen»)", "Art. 38.2 («verifique»)", _verificacion_posterior),
)

# Por el D-5, el régimen simplificado no tiene un requisito de emergencia: su
# R-26 y R-27 no aplican y la nota va en R-14 y R-23.


def _evaluar_requisito(req: Requisito, x: _Contexto, regimen: str):
    """Devuelve (Resultado, avisos A-03)."""
    cita = req.cita[regimen]
    if cita is None:
        # Lo que no aplica también se cita: al artículo del otro régimen, que es el que lo exige.
        otro = SIMPLIFICADO if regimen == COMPLETO else COMPLETO
        return Resultado(req.id, req.nombre, NO_APLICA, f"{req.cita[otro]} (solo régimen {otro})", (req.sin_cita[regimen],)), []
    s = req.comprobar(x, regimen)
    estado = s.estado
    if req.mecanismo and estado in (CUMPLE, AVISO):
        # Asimetría del D-1: un requisito de mecanismo nunca da «cumple»; si solo falla
        # por una lectura propia, da «sin indicio» con su aviso.
        estado = SIN_INDICIO
    avisos = [
        Aviso(AVISO_LECTURA, f"{req.id}: con la lectura {ref}, {msg}", f"{ref}; {cita}", requisito=req.id, lectura=ref)
        for ref, msg in s.lecturas
    ]
    return Resultado(req.id, req.nombre, estado, cita, s.motivos, s.notas, req.garantizado), avisos


# --- Avisos e informativos ---------------------------------------------------------


def _mismo_agente(x, a, b):
    """D-2, punto 4: mismo `id`, o misma herramienta, modelo y versión."""
    if a == b:
        return True
    aa, bb = x.actores[a], x.actores[b]
    if aa.es_persona or bb.es_persona:
        return False
    return (aa.herramienta, aa.modelo, aa.version) == (bb.herramienta, bb.modelo, bb.version)


def _autorrevisiones(x):
    implantadores = [i for i in x.c.implantacion.actores if not x.es_persona(i)]
    avisos = []
    for r in x.c.revisiones_codigo:
        for revisor in r.realizada_por:
            if x.es_persona(revisor):
                continue
            for imp in implantadores:
                if _mismo_agente(x, revisor, imp):
                    avisos.append(
                        Aviso(
                            "A-01",
                            f"La revisión {r.id} la hace el agente {revisor}, que es el mismo agente que implanta ({imp}). "
                            "Cuenta para el art. 16.3, que no exige independencia del revisor.",
                            "Art. 17.1.c.iv); D-2, punto 4",
                        )
                    )
    return avisos


def _sin_evidencias(x, regimen):
    """Modelo, §7.3: la evidencia no es exigible; se avisa si falta en lo que el régimen usa (dudas, DI-11)."""
    c = x.c
    objetos = [(f"cambio.pruebas[{p.id}]", p.evidencias) for p in c.pruebas]
    objetos += [(f"cambio.controles_integridad[{i}]", ci.evidencias) for i, ci in enumerate(c.controles_integridad)]
    if regimen == COMPLETO:
        if c.verificacion_seguridad is not None:
            objetos.insert(0, ("cambio.verificacion_seguridad", c.verificacion_seguridad.evidencias))
        objetos += [(f"cambio.revisiones_codigo[{r.id}]", r.evidencias) for r in c.revisiones_codigo]
    cita = (
        "DORA, art. 9.4.e) («de forma controlada»); modelo, §7.3"
        if regimen == COMPLETO
        else "Art. 38.2 («de manera controlada»); modelo, §7.3"
    )
    return [Aviso("A-02", f"`{ruta}` no tiene evidencias.", cita) for ruta, ev in objetos if not ev]


def _informativos_simplificado(x):
    info = []
    if _aprobaciones(x):
        for m in sum(coincidencias_independencia(x), []):
            info.append(
                Aviso("I-01", f"{m} El título III no exige independencia: es un dato informativo.", "D-1; art. 28.4 (no aplicable)")
            )
    if x.c.revisiones_codigo:
        ids = ", ".join(r.id for r in x.c.revisiones_codigo)
        info.append(
            Aviso("I-02", f"Revisiones de código registradas ({ids}): el título III no exige revisión de código.", "D-2, punto 5; art. 37")
        )
    return info


def calcular(entrada: Entrada, regimen: str) -> ResultadoRegimen:
    if regimen not in REGIMENES:
        raise ValueError(f"Régimen desconocido: {regimen}")
    x = _Contexto(entrada)
    resultados, avisos_lectura = [], []
    for req in CATALOGO:
        resultado, avisos = _evaluar_requisito(req, x, regimen)
        resultados.append(resultado)
        avisos_lectura += avisos
    avisos = avisos_lectura + _sin_evidencias(x, regimen)
    if regimen == COMPLETO:
        avisos = _autorrevisiones(x) + avisos
        informativos = []
    else:
        informativos = _informativos_simplificado(x)
    return ResultadoRegimen(regimen, tuple(resultados), tuple(avisos), tuple(informativos))
