"""Cálculo: qué resulta de cada requisito con cada régimen.

El régimen (`completo` o `simplificado`) es un parámetro, no un dato de la
entrada (modelo, §0.1, principio 2). Para cada requisito del catálogo, el
cálculo da un resultado con su cita:

- `cumple`: el registro tiene lo que el requisito pide;
- `incumplimiento`: le falta, o lo que tiene lo contradice;
- `sin_indicio_de_incumplimiento`: en los requisitos que dependen de un
  mecanismo de la entidad (modelo, §0.3 y D-1), el registro de un cambio puede
  probar que el mecanismo falló, pero no que existe. Esos requisitos nunca dan
  `cumple`;
- `no_aplica`: el régimen no lo exige, o no se da la condición de la que
  depende. El motivo se dice siempre.

Los avisos (A-n) y los datos informativos (I-n) van aparte y no son
incumplimientos. Las dudas de implementación se citan como «dudas, DI-n»
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
    Paso,
)

COMPLETO = "completo"
SIMPLIFICADO = "simplificado"
REGIMENES = (COMPLETO, SIMPLIFICADO)

CUMPLE = "cumple"
INCUMPLIMIENTO = "incumplimiento"
SIN_INDICIO = "sin_indicio_de_incumplimiento"
NO_APLICA = "no_aplica"
ESTADOS = (CUMPLE, INCUMPLIMIENTO, SIN_INDICIO, NO_APLICA)

SIN_BASE_TITULO_III = "El título III del Reglamento Delegado no tiene equivalente (modelo, §0.3 y §13)."


@dataclass(frozen=True)
class Resultado:
    id: str
    nombre: str
    estado: str
    cita: str
    motivos: tuple[str, ...] = ()
    notas: tuple[str, ...] = ()


@dataclass(frozen=True)
class Aviso:
    """Un aviso (A-n) o un dato informativo (I-n). No es un incumplimiento."""

    codigo: str
    mensaje: str
    cita: str


@dataclass(frozen=True)
class ResultadoRegimen:
    regimen: str
    resultados: tuple[Resultado, ...]
    avisos: tuple[Aviso, ...]
    informativos: tuple[Aviso, ...]

    @property
    def incumplimientos(self) -> tuple[Resultado, ...]:
        return tuple(r for r in self.resultados if r.estado == INCUMPLIMIENTO)


# --- Utilidades ------------------------------------------------------------------


def _vacio(texto: Optional[str]) -> bool:
    # Dudas, DI-1: una cadena vacía o solo con espacios cuenta como dato ausente.
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
        """La persona o, si es un agente, su persona responsable (D-1)."""
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
    # Depende de un mecanismo de la entidad: nunca da `cumple` (modelo, §0.3; D-1).
    mecanismo: bool
    comprobar: Callable
    # Motivo de `no_aplica` en el régimen sin cita.
    sin_cita: dict = field(default_factory=dict)


def _r(estado, motivos=(), notas=()):
    return estado, tuple(motivos), tuple(notas)


def _por_faltas(faltas, notas=()):
    return _r(INCUMPLIMIENTO, faltas, notas) if faltas else _r(CUMPLE, (), notas)


# --- Requisitos ------------------------------------------------------------------
#
# Cada función recibe el contexto y el régimen, y devuelve (estado, motivos,
# notas). Un requisito de mecanismo devuelve CUMPLE cuando no encuentra nada;
# `evaluar` lo convierte en SIN_INDICIO.


def _registro(x, regimen):
    return _r(CUMPLE, ("El cambio tiene registro.",))


def _elementos(x, regimen):
    # Dudas, DI-8: una «lista no vacía» fuera de los pasos se juzga aquí, no en la carga.
    return _por_faltas([] if x.c.elementos else ["`cambio.elementos` está vacía: no dice qué se cambia."])


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
    sin = [i for i in _que_actuaron(x) if x.actores[i].cuenta is None]
    faltas = [f"El actor {i} actuó en los sistemas de TIC y no tiene `cuenta`." for i in sin]
    faltas += [f"La prueba {p.id} no dice quién la hizo (`realizada_por` vacía)." for p in x.c.pruebas if not p.realizada_por]
    faltas += [
        f"La revisión {r.id} no dice quién la hizo (`realizada_por` vacía)." for r in x.c.revisiones_codigo if not r.realizada_por
    ]
    return _por_faltas(faltas)


def _solicitud(x, regimen):
    return _r(CUMPLE, (f"Solicitado por {', '.join(x.c.solicitud.actores)}.",))


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

    Devuelve dos listas de mensajes: las de la misma persona (incluida la
    persona responsable de un agente) y las de personas distintas de la misma
    función, que dependen de la lectura del considerando 17.
    """
    misma_persona, misma_funcion = [], []
    otros = [("solicita", i) for i in x.c.solicitud.actores] + [("aplica", i) for i in x.c.implantacion.actores]
    for ruta, paso in _aprobaciones(x):
        for a in paso.actores:
            for papel, o in otros:
                comunes = x.personas(a) & x.personas(o)
                if comunes:
                    misma_persona.append(
                        f"{a} aprueba ({ruta}) y {o} {papel}: coincide la persona {', '.join(sorted(comunes))}."
                    )
                elif x.funciones(a) & x.funciones(o):
                    funciones = ", ".join(sorted(x.funciones(a) & x.funciones(o)))
                    misma_funcion.append(f"{a} aprueba ({ruta}) y {o} {papel}: son de la misma función ({funciones}).")
    return misma_persona, misma_funcion


def _independencia(x, regimen):
    if not _aprobaciones(x):
        # Dudas, DI-9: sin aprobación no hay indicio de dependencia; la falta la dan R-23 y R-27.
        return _r(CUMPLE, ("No hay ninguna aprobación con la que comparar; ver R-23 y R-27 (dudas, DI-9).",))
    misma_persona, misma_funcion = coincidencias_independencia(x)
    notas = []
    if misma_persona:
        notas.append(
            "Misma persona: el registro de este cambio muestra que el mecanismo del art. 17.1.b) no funcionó en él. "
            "Ninguna lectura lo salva (D-1)."
        )
    if misma_funcion:
        notas.append(
            "Misma función con personas distintas: es incumplimiento con la lectura del considerando 17 "
            "(funciones «separadas») que adopta el modelo; con otra lectura de los «mecanismos» del art. 17.1.b) "
            "podría no serlo (D-1)."
        )
    if misma_persona or misma_funcion:
        return _r(INCUMPLIMIENTO, misma_persona + misma_funcion, notas)
    return _r(
        CUMPLE,
        ("Ninguna función de quien aprueba coincide con las de quien solicita o aplica.",),
        ("El registro no puede probar que el mecanismo exista ni que funcione (D-1; modelo, §14).",),
    )


def _responsabilidades(x, regimen):
    r = x.c.responsabilidades
    incisos = {
        "especificacion_planificacion": "i",
        "diseno_transicion": "ii",
        "pruebas_ultimacion": "iii",
        "aseguramiento_calidad": "iv",
    }
    faltas = [
        f"`cambio.responsabilidades.{k}` está vacía (art. 17.1.c.{inciso})."
        for k, inciso in incisos.items()
        if not getattr(r, k)
    ]
    return _por_faltas(faltas)


def _objeto_alcance(x, regimen):
    faltas = []
    if _vacio(x.c.objeto):
        faltas.append("Falta `cambio.objeto`.")
    if _vacio(x.c.alcance_descripcion):
        faltas.append("Falta `cambio.alcance.descripcion`.")
    if not x.c.alcance_sistemas:
        faltas.append("`cambio.alcance.sistemas` está vacía.")
    return _por_faltas(faltas)


def _calendario(x, regimen):
    return _r(CUMPLE, ("El calendario tiene inicio y fin previstos.",))


def _resultados_esperados(x, regimen):
    return _por_faltas(["Falta `cambio.resultados_esperados`."] if _vacio(x.c.resultados_esperados) else [])


def _comunicacion(x, regimen):
    return _por_faltas([] if x.c.comunicaciones else ["`cambio.comunicaciones` está vacía."])


def _verificacion_seguridad(x, regimen):
    v = x.c.verificacion_seguridad
    if v is None:
        return _r(INCUMPLIMIENTO, ("Falta `cambio.verificacion_seguridad`.",))
    if v.resultado == NO_CUMPLE and x.c.implantacion.resultado == APLICADO:
        # Dudas, DI-3: lectura conservadora.
        return _r(
            INCUMPLIMIENTO,
            ("La verificación dice que el cambio no cumple los requisitos de seguridad, y el cambio se aplicó.",),
            ("Lectura conservadora: el modelo no dice qué pasa si se aplica un cambio que no los cumple (dudas, DI-3).",),
        )
    return _r(CUMPLE)


def _evaluacion(x, regimen):
    ev = x.c.evaluacion
    if ev is None:
        return _r(INCUMPLIMIENTO, ("Falta `cambio.evaluacion`.",))
    if regimen == SIMPLIFICADO:
        return _r(CUMPLE)
    faltas = []
    if _vacio(ev.repercusion_seguridad):
        faltas.append("Falta `cambio.evaluacion.repercusion_seguridad` (art. 17.1.h).")
    if ev.requiere_medidas_adicionales is None:
        faltas.append("Falta `cambio.evaluacion.requiere_medidas_adicionales` (art. 17.1.h).")
    elif ev.requiere_medidas_adicionales and not ev.medidas_adicionales:
        faltas.append("La evaluación dice que hacen falta medidas adicionales y no dice cuáles (art. 17.1.h).")
    return _por_faltas(faltas)


def _cambio_importante(x, regimen):
    c = x.c
    if c.cambio_importante is None:
        return _r(INCUMPLIMIENTO, ("Falta `cambio.cambio_importante`: la entidad no declara si el cambio es importante.",))
    if not c.cambio_importante:
        return _r(NO_APLICA, ("La entidad declara que el cambio no es importante.",))
    if c.evaluacion is None or _vacio(c.evaluacion.riesgos):
        return _r(INCUMPLIMIENTO, ("El cambio es importante y falta `cambio.evaluacion.riesgos`.",))
    return _r(CUMPLE)


def _pruebas_previas(x, regimen):
    c = x.c
    if not c.pruebas:
        return _r(INCUMPLIMIENTO, ("`cambio.pruebas` está vacía.",))
    previas = [p.id for p in c.pruebas if p.fecha < x.inicio]
    notas = []
    if c.emergencia is not None:
        # Dudas, DI-4: el modelo no exime de las pruebas previas a los cambios de emergencia.
        notas.append("Cambio de emergencia: se exigen igualmente pruebas previas (dudas, DI-4).")
    if not previas:
        return _r(INCUMPLIMIENTO, ("Ninguna prueba es anterior a `cambio.implantacion.inicio`.",), notas)
    return _r(CUMPLE, (f"Pruebas anteriores a la implantación: {', '.join(previas)}.",), notas)


def _seguridad_paquetes(x, regimen):
    paquetes = [p for p in x.c.pruebas if p.tipo == SEGURIDAD_PAQUETES]
    if not paquetes:
        # Dudas, DI-5: el modelo no exige una prueba de este tipo en cada cambio.
        return _r(NO_APLICA, ("No hay pruebas de tipo `seguridad_paquetes` (dudas, DI-5).",))
    tardias = [p.id for p in paquetes if p.fase not in FASES_HASTA_INTEGRACION]
    return _por_faltas([f"La prueba {i} de seguridad de paquetes es posterior a la fase de integración." for i in tardias])


def _datos_produccion(x, regimen):
    no_prod = [p for p in x.c.pruebas if p.entorno == NO_PRODUCCION]
    if not no_prod:
        return _r(NO_APLICA, ("No hay pruebas en entornos distintos del de producción.",))
    faltas = []
    for p in no_prod:
        if p.datos != DATOS_PRODUCCION:
            continue
        ex = p.excepcion_datos_produccion
        if ex is None:
            faltas.append(f"La prueba {p.id} usa datos de producción sin excepción (art. 16.5.a).")
            continue
        if not x.hay_persona(ex.aprobacion.actores):
            faltas.append(f"La excepción de la prueba {p.id} no la aprueba ninguna persona (art. 16.6; D-4).")
        if p.fecha > ex.hasta:
            faltas.append(f"La prueba {p.id} es posterior al límite de la excepción (art. 16.6: «durante un tiempo limitado»).")
    return _por_faltas(faltas)


def _revision_codigo(x, regimen):
    c = x.c
    if not c.incluye_codigo_fuente:
        return _r(NO_APLICA, ("El cambio no incluye código fuente (`incluye_codigo_fuente` es false).",))
    if not c.revisiones_codigo:
        return _r(INCUMPLIMIENTO, ("El cambio incluye código fuente y no tiene revisiones de código.",))
    tecnicas = {t for r in c.revisiones_codigo for t in r.tecnicas}
    faltan = [t for t in TECNICAS if t not in tecnicas]
    # D-2, punto 1: la revisión de un agente cuenta como revisión del art. 16.3.
    return _por_faltas([f"Ninguna revisión usa la técnica {t}." for t in faltan])


def _con_hallazgos(x):
    return [r for r in x.c.revisiones_codigo if r.hallazgos]


def _plan_accion(x, regimen):
    revisiones = _con_hallazgos(x)
    if not revisiones:
        return _r(NO_APLICA, ("Ninguna revisión de código tiene hallazgos.",))
    faltas = []
    for r in revisiones:
        p = r.plan_accion
        if p is None:
            faltas.append(f"La revisión {r.id} tiene hallazgos y no tiene plan de acción.")
            continue
        if not x.hay_persona(p.adoptado_por):
            faltas.append(f"El plan de acción de la revisión {r.id} no lo adopta ninguna persona (D-2, punto 2).")
        cubiertos = {h for m in p.medidas for h in m.hallazgos}
        sin = [h.id for h in r.hallazgos if h.id not in cubiertos]
        if sin:
            faltas.append(f"El plan de acción de la revisión {r.id} no hace frente a: {', '.join(sin)}.")
    return _por_faltas(faltas)


def _seguimiento(x, regimen):
    revisiones = [r for r in x.c.revisiones_codigo if r.plan_accion is not None]
    if not revisiones:
        return _r(NO_APLICA, ("Ninguna revisión de código tiene plan de acción.",))
    faltas = []
    for r in revisiones:
        if not r.seguimiento:
            faltas.append(f"El plan de acción de la revisión {r.id} no tiene seguimiento.")
        elif not any(x.hay_persona(s.actores) for s in r.seguimiento):
            faltas.append(f"El seguimiento de la revisión {r.id} no tiene ninguna entrada con una persona (D-2, punto 3).")
    return _por_faltas(faltas)


def _origen_codigo(x, regimen):
    if not x.c.incluye_codigo_fuente:
        return _r(NO_APLICA, ("El cambio no incluye código fuente.",))
    return _por_faltas([] if x.c.origen_codigo else ["El cambio incluye código fuente y `origen_codigo` está vacía."])


def _codigo_terceros(x, regimen):
    terceros = [o for o in x.c.origen_codigo if o in ORIGENES_DE_TERCEROS]
    if not terceros:
        return _r(NO_APLICA, ("La entidad no declara código de terceros, propietario ni abierto (D-3).",))
    previas = [r.id for r in x.c.revisiones_codigo if r.fecha < x.inicio]
    if not previas:
        return _r(
            INCUMPLIMIENTO,
            (f"Origen declarado: {', '.join(terceros)}; ninguna revisión de código es anterior a la implantación.",),
        )
    return _r(CUMPLE, (f"Revisiones anteriores a la implantación: {', '.join(previas)}.",))


def _controles_integridad(x, regimen):
    return _por_faltas([] if x.c.controles_integridad else ["`cambio.controles_integridad` está vacía."])


def _aprobacion_valida(x, paso: Paso, ruta, antes_de_implantar=True):
    faltas = []
    if not x.hay_persona(paso.actores):
        faltas.append(f"`{ruta}` no la da ninguna persona (D-4).")
    if antes_de_implantar and paso.fecha >= x.inicio:
        faltas.append(f"`{ruta}` no es anterior a `cambio.implantacion.inicio`.")
    return faltas


def _aprobacion(x, regimen):
    c = x.c
    notas = []
    if regimen == COMPLETO and c.emergencia is not None and c.aprobacion is None:
        return _r(
            NO_APLICA,
            ("Cambio de emergencia: la aprobación es posterior a la aplicación (art. 17.1.g); ver R-27.",),
        )
    if regimen == SIMPLIFICADO and c.emergencia is not None:
        notas.append(
            "El título III no prevé excepción de emergencia: el art. 37.b) exige la aprobación previa. "
            "Una lectura basada en el «enfoque basado en el riesgo» del art. 37 podría admitirla (D-5)."
        )
    if c.aprobacion is None:
        return _r(INCUMPLIMIENTO, ("Falta `cambio.aprobacion`.",), notas)
    return _por_faltas(_aprobacion_valida(x, c.aprobacion, "cambio.aprobacion"), notas)


def _aplicacion(x, regimen):
    return _r(CUMPLE, (f"Aplicado por {', '.join(x.c.implantacion.actores)}; resultado: {x.c.implantacion.resultado}.",))


def _vuelta_atras(x, regimen):
    v = x.c.vuelta_atras
    if v is None:
        return _r(INCUMPLIMIENTO, ("Falta `cambio.vuelta_atras`.",))
    faltas = []
    if not v.responsables:
        faltas.append("`cambio.vuelta_atras.responsables` está vacía.")
    if _vacio(v.procedimiento):
        faltas.append("Falta `cambio.vuelta_atras.procedimiento`.")
    if x.c.implantacion.resultado != APLICADO and v.ejecucion is None:
        faltas.append(f"El resultado de la implantación es «{x.c.implantacion.resultado}» y falta `cambio.vuelta_atras.ejecucion`.")
    return _por_faltas(faltas)


def _emergencia(x, regimen):
    e = x.c.emergencia
    if e is None:
        return _r(NO_APLICA, ("El cambio no siguió el procedimiento de emergencia (`emergencia` es null).",))
    faltas = []
    if _vacio(e.procedimiento):
        faltas.append("Falta `cambio.emergencia.procedimiento`.")
    if _vacio(e.salvaguardias):
        faltas.append("Falta `cambio.emergencia.salvaguardias`.")
    return _por_faltas(faltas)


def _revision_posterior(x, regimen):
    e = x.c.emergencia
    if e is None:
        return _r(NO_APLICA, ("El cambio no es de emergencia.",))
    rp = e.revision_posterior
    faltas = []
    for k in ("documentacion", "reexamen", "evaluacion", "aprobacion"):
        paso = getattr(rp, k)
        ruta = f"cambio.emergencia.revision_posterior.{k}"
        if paso is None:
            # Dudas, DI-6: «pendiente» se trata como incumplimiento mientras no se haga.
            faltas.append(f"Falta `{ruta}`: la revisión posterior está pendiente (dudas, DI-6).")
        elif paso.fecha <= x.inicio:
            faltas.append(f"`{ruta}` no es posterior a la aplicación («tras su aplicación»).")
    if rp.aprobacion is not None and not x.hay_persona(rp.aprobacion.actores):
        faltas.append("`cambio.emergencia.revision_posterior.aprobacion` no la da ninguna persona (D-4).")
    return _por_faltas(faltas)


def _verificacion_posterior(x, regimen):
    v = x.c.verificacion_posterior
    # Dudas, DI-10: se exige también si el cambio se abortó o se revirtió.
    if v is None:
        return _r(INCUMPLIMIENTO, ("Falta `cambio.verificacion_posterior`.",))
    if v.fecha <= x.inicio:
        return _r(INCUMPLIMIENTO, ("`cambio.verificacion_posterior` no es posterior a `cambio.implantacion.inicio`.",))
    return _r(CUMPLE, (f"Resultado: {v.resultado}.",))


# --- Catálogo --------------------------------------------------------------------


def _req(id_, nombre, completo, simplificado, comprobar, mecanismo=False):
    sin_cita = {}
    if completo is None:
        sin_cita[COMPLETO] = "Solo lo exige el régimen simplificado."
    if simplificado is None:
        sin_cita[SIMPLIFICADO] = SIN_BASE_TITULO_III
    return Requisito(id_, nombre, {COMPLETO: completo, SIMPLIFICADO: simplificado}, mecanismo, comprobar, sin_cita)


CATALOGO = (
    _req("R-01", "Registro del cambio", "DORA, art. 9.4.e) («se registren»); art. 12.2.c.iii)", "Art. 38.2 («se registre»); art. 34.f)", _registro),
    _req("R-02", "Elementos que se cambian", "Art. 17.1, encabezado; DORA, art. 9.4.e)", None, _elementos),
    _req("R-03", "Identificación de los actores en sus acciones", "Arts. 20.2.a) y 21.c)", "Art. 33.b)", _identificacion),
    _req("R-04", "Quién solicita", "Art. 17.1.b)", None, _solicitud),
    _req("R-05", "Independencia entre quien aprueba y quien solicita o aplica", "Art. 17.1.b); considerando 17; D-1", None, _independencia, mecanismo=True),
    _req("R-06", "Funciones y responsabilidades del cambio", "Art. 17.1.c), incisos i) a iv)", None, _responsabilidades, mecanismo=True),
    _req("R-07", "Objeto y alcance", "Art. 17.1.d.i)", None, _objeto_alcance),
    _req("R-08", "Calendario", "Art. 17.1.d.ii)", None, _calendario),
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
    _req("R-20", "Origen del código", "Art. 16.7 y 16.8", None, _origen_codigo),
    _req("R-21", "Revisión previa del código de terceros, propietario o abierto", "Art. 16.8; D-3", None, _codigo_terceros),
    _req("R-22", "Medidas contra la alteración o la manipulación", "Art. 16.1.c); art. 16.7", "Art. 37.c)", _controles_integridad, mecanismo=True),
    _req("R-23", "Aprobación", "DORA, art. 9.4.e) («aprueben»); art. 17.1.b); D-4", "Art. 37.b); art. 38.2; D-4; D-5", _aprobacion),
    _req("R-24", "Aplicación", "DORA, art. 9.4.e) («apliquen»)", "Art. 38.2 («aplique»)", _aplicacion),
    _req("R-25", "Vuelta atrás", "Art. 17.1.e)", None, _vuelta_atras),
    _req("R-26", "Procedimiento de emergencia con salvaguardias", "Art. 17.1.f)", None, _emergencia, mecanismo=True),
    _req("R-27", "Revisión posterior del cambio de emergencia", "Art. 17.1.g); D-4", None, _revision_posterior),
    _req("R-28", "Verificación posterior", "DORA, art. 9.4.e) («verifiquen»)", "Art. 38.2 («verifique»)", _verificacion_posterior),
)

# Por el D-5, el régimen simplificado no tiene un requisito de emergencia: su
# R-26 y R-27 no aplican y la nota va en R-23.


def _evaluar_requisito(req: Requisito, x: _Contexto, regimen: str) -> Resultado:
    cita = req.cita[regimen]
    if cita is None:
        # Lo que no aplica también se cita: al artículo del otro régimen, que es el que lo exige.
        otro = SIMPLIFICADO if regimen == COMPLETO else COMPLETO
        cita_otro = f"{req.cita[otro]} (solo régimen {otro})"
        return Resultado(req.id, req.nombre, NO_APLICA, cita_otro, (req.sin_cita[regimen],))
    estado, motivos, notas = req.comprobar(x, regimen)
    if req.mecanismo and estado == CUMPLE:
        # Asimetría del D-1: un requisito de mecanismo nunca da «cumple».
        estado = SIN_INDICIO
    return Resultado(req.id, req.nombre, estado, cita, motivos, notas)


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
    cita = "DORA, art. 9.4.e) («de forma controlada»); modelo, §7.3" if regimen == COMPLETO else "Art. 38.2 («de manera controlada»); modelo, §7.3"
    return [Aviso("A-02", f"`{ruta}` no tiene evidencias.", cita) for ruta, ev in objetos if not ev]


def _informativos_simplificado(x):
    info = []
    if _aprobaciones(x):
        misma_persona, misma_funcion = coincidencias_independencia(x)
        for m in misma_persona + misma_funcion:
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
    resultados = tuple(_evaluar_requisito(req, x, regimen) for req in CATALOGO)
    avisos = _sin_evidencias(x, regimen)
    if regimen == COMPLETO:
        avisos = _autorrevisiones(x) + avisos
        informativos = []
    else:
        informativos = _informativos_simplificado(x)
    return ResultadoRegimen(regimen, resultados, tuple(avisos), tuple(informativos))
