"""Lectura y validación de la entrada, según docs/modelo-datos.md (versión 1).

`cargar` lee el JSON y devuelve un ResultadoCarga con la entrada validada (o
None si hay errores) y los errores del §15 del modelo. No calcula nada, y la
validación no depende del régimen (modelo, §0.1, principio 3): que falte un
dato exigible no es un error de entrada, sino un resultado del cálculo.

La validación va en dos pasadas. La primera lee la estructura y anota ERR-01.
Si hay algún ERR-01, la segunda no se hace, porque depende de datos que no se
han podido leer. La segunda comprueba repetidos, referencias y coherencia
(ERR-02 a ERR-05). En cada pasada se recogen todos los errores.
"""

import json
from datetime import datetime
from pathlib import Path

from registro_cambio.modelo import (
    AGENTE_IA,
    DATOS,
    ELEMENTOS,
    ENTORNOS,
    ESTADOS_SEGUIMIENTO,
    ETAPAS,
    FASES,
    ORIGENES_CODIGO,
    PERSONA,
    RESULTADOS_IMPLANTACION,
    RESULTADOS_PRUEBA,
    RESULTADOS_VERIFICACION,
    RESULTADOS_VERIFICACION_SEGURIDAD,
    TECNICAS,
    TIPOS_ACTOR,
    TIPOS_EMERGENCIA,
    TIPOS_PRUEBA,
    VERSION_MODELO,
    Accion,
    Actor,
    Cambio,
    Comunicacion,
    ControlIntegridad,
    EjecucionVueltaAtras,
    Emergencia,
    Entrada,
    Evaluacion,
    Evidencia,
    ExcepcionDatosProduccion,
    Hallazgo,
    Implantacion,
    Incidencia,
    Medida,
    Paso,
    PlanAccion,
    Prueba,
    Responsabilidades,
    ResultadoCarga,
    RevisionCodigo,
    RevisionPosterior,
    Seguimiento,
    VerificacionPosterior,
    VerificacionSeguridad,
    VueltaAtras,
)

# §3.2: los campos propios del agente.
CAMPOS_AGENTE = ("herramienta", "modelo", "version", "persona_responsable")


def cargar(texto: str) -> ResultadoCarga:
    """Lee y valida una entrada en JSON."""
    return _Carga().ejecutar(texto)


def cargar_fichero(ruta) -> ResultadoCarga:
    return cargar(Path(ruta).read_text(encoding="utf-8"))


def _leer_json(texto):
    """Devuelve (datos, claves repetidas). Rechaza NaN e Infinity."""
    repetidas = []

    def objeto(pares):
        resultado = {}
        for clave, valor in pares:
            if clave in resultado:
                repetidas.append(clave)
            resultado[clave] = valor
        return resultado

    def constante(nombre):
        raise ValueError(f"{nombre} no es un número JSON válido")

    return json.loads(texto, parse_constant=constante, object_pairs_hook=objeto), repetidas


def _ruta(base, clave):
    return f"{base}.{clave}" if base else str(clave)


# Valor centinela de un dato que no se ha podido leer. Con algún ERR-01 la
# entrada se descarta, así que nunca llega al cálculo.
_MAL = object()


class _Carga:
    def __init__(self):
        self.errores: list[Incidencia] = []

    def error(self, codigo, mensaje, ruta=""):
        self.errores.append(Incidencia(codigo, mensaje, ruta))

    def ejecutar(self, texto):
        try:
            datos, repetidas = _leer_json(texto)
        except ValueError as e:
            self.error("ERR-01", f"El JSON no es válido: {e}")
            return self._resultado(None)
        for clave in repetidas:
            self.error("ERR-01", f"La clave «{clave}» aparece repetida en un mismo objeto")
        if isinstance(datos, dict) and "regimen" in datos:
            # Modelo, §2: no hay campo de régimen (§0.1, principio 2).
            self.error("ERR-01", "La entrada no lleva régimen: es un parámetro del cálculo (modelo, §0.1 y §2)", "regimen")
        entrada = self._entrada(datos)
        if any(e.codigo == "ERR-01" for e in self.errores):
            return self._resultado(None)
        _Coherencia(self, entrada).comprobar()
        return self._resultado(None if self.errores else entrada)

    def _resultado(self, entrada):
        return ResultadoCarga(entrada=entrada, errores=tuple(sorted(self.errores, key=lambda i: i.codigo)))

    # --- Lectores básicos ----------------------------------------------------

    def _objeto(self, valor, ruta, obligatorios, opcionales=()):
        """Comprueba que `valor` es un objeto con exactamente esas claves."""
        if not isinstance(valor, dict):
            self.error("ERR-01", "Debe ser un objeto", ruta)
            return None
        for clave in obligatorios:
            if clave not in valor:
                self.error("ERR-01", f"Falta el campo obligatorio «{clave}»", _ruta(ruta, clave))
        for clave in valor:
            if clave not in obligatorios and clave not in opcionales and not (ruta == "" and clave == "regimen"):
                self.error("ERR-01", f"Campo desconocido «{clave}»", _ruta(ruta, clave))
        return valor

    def _campo(self, obj, clave, ruta, lector, nulo=False):
        if obj is None or clave not in obj:
            return _MAL
        valor = obj[clave]
        r = _ruta(ruta, clave)
        if valor is None:
            if nulo:
                return None
            self.error("ERR-01", "No puede ser null", r)
            return _MAL
        return lector(valor, r)

    def _cadena(self, valor, ruta):
        if not isinstance(valor, str):
            self.error("ERR-01", "Debe ser una cadena", ruta)
            return _MAL
        return valor

    def _booleano(self, valor, ruta):
        if not isinstance(valor, bool):
            self.error("ERR-01", "Debe ser true o false", ruta)
            return _MAL
        return valor

    def _enum(self, opciones):
        def lector(valor, ruta):
            if valor not in opciones:
                self.error("ERR-01", f"Valor no válido; debe ser uno de: {', '.join(opciones)}", ruta)
                return _MAL
            return valor

        return lector

    def _fecha(self, valor, ruta):
        # Modelo, §2: fecha y hora ISO 8601 con desfase horario.
        if not isinstance(valor, str) or "T" not in valor:
            self.error("ERR-01", "Debe ser fecha y hora ISO 8601 con desfase horario (AAAA-MM-DDThh:mm:ss±hh:mm)", ruta)
            return _MAL
        try:
            fecha = datetime.fromisoformat(valor)
        except ValueError:
            fecha = None
        if fecha is None or fecha.tzinfo is None:
            self.error("ERR-01", "Debe ser fecha y hora ISO 8601 con desfase horario (AAAA-MM-DDThh:mm:ss±hh:mm)", ruta)
            return _MAL
        return fecha

    def _lista(self, lector, no_vacia=False):
        def leer(valor, ruta):
            if not isinstance(valor, list):
                self.error("ERR-01", "Debe ser una lista", ruta)
                return _MAL
            if no_vacia and not valor:
                self.error("ERR-01", "No puede estar vacía", ruta)
            return tuple(lector(v, f"{ruta}[{i}]") for i, v in enumerate(valor))

        return leer

    # --- Objetos del modelo --------------------------------------------------

    def _entrada(self, datos):
        obj = self._objeto(datos, "", ("version_modelo", "actores", "cambio"))
        if obj is not None and "version_modelo" in obj:
            v = obj["version_modelo"]
            if not (isinstance(v, int) and not isinstance(v, bool) and v == VERSION_MODELO):
                self.error("ERR-01", f"Debe ser {VERSION_MODELO}", "version_modelo")
        actores = self._campo(obj, "actores", "", self._lista(self._actor, no_vacia=True))
        cambio = self._campo(obj, "cambio", "", self._cambio)
        return Entrada(actores=actores, cambio=cambio)

    def _actor(self, valor, ruta):
        es_agente = isinstance(valor, dict) and valor.get("tipo") == AGENTE_IA
        obligatorios = ("id", "tipo", "funcion", "cuenta") + (CAMPOS_AGENTE if es_agente else ())
        # Los campos del agente en una persona son ERR-04, no ERR-01 (modelo, §15).
        obj = self._objeto(valor, ruta, obligatorios, opcionales=() if es_agente else CAMPOS_AGENTE)
        c = lambda clave, lector, nulo=False: self._campo(obj, clave, ruta, lector, nulo)  # noqa: E731
        return Actor(
            id=c("id", self._cadena),
            tipo=c("tipo", self._enum(TIPOS_ACTOR)),
            funcion=c("funcion", self._cadena),
            cuenta=c("cuenta", self._cadena, nulo=True),
            herramienta=c("herramienta", self._cadena) if es_agente else (obj or {}).get("herramienta"),
            modelo=c("modelo", self._cadena) if es_agente else (obj or {}).get("modelo"),
            version=c("version", self._cadena) if es_agente else (obj or {}).get("version"),
            persona_responsable=c("persona_responsable", self._cadena)
            if es_agente
            else (obj or {}).get("persona_responsable"),
        )

    def _ids(self, no_vacia=False):
        return self._lista(self._cadena, no_vacia=no_vacia)

    def _paso(self, valor, ruta):
        # Modelo, §2: `actores` es una lista no vacía.
        obj = self._objeto(valor, ruta, ("actores", "fecha"))
        return Paso(
            actores=self._campo(obj, "actores", ruta, self._ids(no_vacia=True)),
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
        )

    def _evidencia(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("referencia", "descripcion"))
        return Evidencia(
            referencia=self._campo(obj, "referencia", ruta, self._cadena),
            descripcion=self._campo(obj, "descripcion", ruta, self._cadena, nulo=True),
        )

    def _evidencias(self, obj, ruta):
        return self._campo(obj, "evidencias", ruta, self._lista(self._evidencia))

    def _cambio(self, valor, ruta):
        ruta = "cambio"
        campos = (
            "id",
            "elementos",
            "objeto",
            "alcance",
            "calendario",
            "resultados_esperados",
            "comunicaciones",
            "incluye_codigo_fuente",
            "origen_codigo",
            "cambio_importante",
            "solicitud",
            "responsabilidades",
            "verificacion_seguridad",
            "evaluacion",
            "controles_integridad",
            "pruebas",
            "revisiones_codigo",
            "vuelta_atras",
            "aprobacion",
            "emergencia",
            "implantacion",
            "verificacion_posterior",
            "acciones",
        )
        obj = self._objeto(valor, ruta, campos)
        c = lambda clave, lector, nulo=False: self._campo(obj, clave, ruta, lector, nulo)  # noqa: E731
        alcance = self._objeto(obj.get("alcance") if obj else None, "cambio.alcance", ("descripcion", "sistemas")) if obj and "alcance" in obj else None
        calendario = (
            self._objeto(obj["calendario"], "cambio.calendario", ("inicio_previsto", "fin_previsto"))
            if obj and "calendario" in obj
            else None
        )
        return Cambio(
            id=c("id", self._cadena),
            elementos=c("elementos", self._lista(self._enum(ELEMENTOS))),
            objeto=c("objeto", self._cadena),
            alcance_descripcion=self._campo(alcance, "descripcion", "cambio.alcance", self._cadena),
            alcance_sistemas=self._campo(alcance, "sistemas", "cambio.alcance", self._ids()),
            inicio_previsto=self._campo(calendario, "inicio_previsto", "cambio.calendario", self._fecha),
            fin_previsto=self._campo(calendario, "fin_previsto", "cambio.calendario", self._fecha),
            resultados_esperados=c("resultados_esperados", self._cadena),
            comunicaciones=c("comunicaciones", self._lista(self._comunicacion)),
            incluye_codigo_fuente=c("incluye_codigo_fuente", self._booleano),
            origen_codigo=c("origen_codigo", self._lista(self._enum(ORIGENES_CODIGO))),
            cambio_importante=c("cambio_importante", self._booleano, nulo=True),
            solicitud=c("solicitud", self._paso),
            responsabilidades=c("responsabilidades", self._responsabilidades),
            verificacion_seguridad=c("verificacion_seguridad", self._verificacion_seguridad, nulo=True),
            evaluacion=c("evaluacion", self._evaluacion, nulo=True),
            controles_integridad=c("controles_integridad", self._lista(self._control)),
            pruebas=c("pruebas", self._lista(self._prueba)),
            revisiones_codigo=c("revisiones_codigo", self._lista(self._revision)),
            vuelta_atras=c("vuelta_atras", self._vuelta_atras, nulo=True),
            aprobacion=c("aprobacion", self._paso, nulo=True),
            emergencia=c("emergencia", self._emergencia, nulo=True),
            implantacion=c("implantacion", self._implantacion),
            verificacion_posterior=c("verificacion_posterior", self._verificacion_posterior, nulo=True),
            acciones=c("acciones", self._lista(self._accion)),
        )

    def _comunicacion(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("fecha", "destinatarios"))
        return Comunicacion(
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
            destinatarios=self._campo(obj, "destinatarios", ruta, self._cadena),
        )

    def _responsabilidades(self, valor, ruta):
        claves = ("especificacion_planificacion", "diseno_transicion", "pruebas_ultimacion", "aseguramiento_calidad")
        obj = self._objeto(valor, ruta, claves)
        return Responsabilidades(**{k: self._campo(obj, k, ruta, self._ids()) for k in claves})

    def _verificacion_seguridad(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("actores", "fecha", "resultado", "evidencias"))
        return VerificacionSeguridad(
            actores=self._campo(obj, "actores", ruta, self._ids(no_vacia=True)),
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
            resultado=self._campo(obj, "resultado", ruta, self._enum(RESULTADOS_VERIFICACION_SEGURIDAD)),
            evidencias=self._evidencias(obj, ruta),
        )

    def _evaluacion(self, valor, ruta):
        claves = (
            "actores",
            "fecha",
            "repercusion_seguridad",
            "requiere_medidas_adicionales",
            "medidas_adicionales",
            "riesgos",
        )
        obj = self._objeto(valor, ruta, claves)
        return Evaluacion(
            actores=self._campo(obj, "actores", ruta, self._ids(no_vacia=True)),
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
            repercusion_seguridad=self._campo(obj, "repercusion_seguridad", ruta, self._cadena, nulo=True),
            requiere_medidas_adicionales=self._campo(obj, "requiere_medidas_adicionales", ruta, self._booleano, nulo=True),
            medidas_adicionales=self._campo(obj, "medidas_adicionales", ruta, self._lista(self._cadena)),
            riesgos=self._campo(obj, "riesgos", ruta, self._cadena, nulo=True),
        )

    def _control(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("descripcion", "evidencias"))
        return ControlIntegridad(
            descripcion=self._campo(obj, "descripcion", ruta, self._cadena), evidencias=self._evidencias(obj, ruta)
        )

    def _excepcion(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("aprobacion", "hasta", "notificacion_funcion_riesgo_tic"))
        return ExcepcionDatosProduccion(
            aprobacion=self._campo(obj, "aprobacion", ruta, self._paso),
            hasta=self._campo(obj, "hasta", ruta, self._fecha),
            notificacion_funcion_riesgo_tic=self._campo(obj, "notificacion_funcion_riesgo_tic", ruta, self._fecha),
        )

    def _prueba(self, valor, ruta):
        claves = (
            "id",
            "tipo",
            "descripcion",
            "realizada_por",
            "fecha",
            "fase",
            "entorno",
            "datos",
            "excepcion_datos_produccion",
            "resultado",
            "evidencias",
        )
        obj = self._objeto(valor, ruta, claves)
        c = lambda clave, lector, nulo=False: self._campo(obj, clave, ruta, lector, nulo)  # noqa: E731
        return Prueba(
            id=c("id", self._cadena),
            tipo=c("tipo", self._enum(TIPOS_PRUEBA)),
            descripcion=c("descripcion", self._cadena),
            realizada_por=c("realizada_por", self._ids()),
            fecha=c("fecha", self._fecha),
            fase=c("fase", self._enum(FASES)),
            entorno=c("entorno", self._enum(ENTORNOS)),
            datos=c("datos", self._enum(DATOS)),
            excepcion_datos_produccion=c("excepcion_datos_produccion", self._excepcion, nulo=True),
            resultado=c("resultado", self._enum(RESULTADOS_PRUEBA)),
            evidencias=self._evidencias(obj, ruta),
        )

    def _hallazgo(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("id", "descripcion"))
        return Hallazgo(id=self._campo(obj, "id", ruta, self._cadena), descripcion=self._campo(obj, "descripcion", ruta, self._cadena))

    def _medida(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("hallazgos", "descripcion"))
        return Medida(
            hallazgos=self._campo(obj, "hallazgos", ruta, self._ids()),
            descripcion=self._campo(obj, "descripcion", ruta, self._cadena),
        )

    def _plan(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("adoptado_por", "fecha", "medidas"))
        return PlanAccion(
            adoptado_por=self._campo(obj, "adoptado_por", ruta, self._ids()),
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
            medidas=self._campo(obj, "medidas", ruta, self._lista(self._medida)),
        )

    def _seguimiento(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("actores", "fecha", "estado", "descripcion"))
        return Seguimiento(
            actores=self._campo(obj, "actores", ruta, self._ids(no_vacia=True)),
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
            estado=self._campo(obj, "estado", ruta, self._enum(ESTADOS_SEGUIMIENTO)),
            descripcion=self._campo(obj, "descripcion", ruta, self._cadena, nulo=True),
        )

    def _revision(self, valor, ruta):
        claves = ("id", "realizada_por", "fecha", "tecnicas", "hallazgos", "plan_accion", "seguimiento", "evidencias")
        obj = self._objeto(valor, ruta, claves)
        c = lambda clave, lector, nulo=False: self._campo(obj, clave, ruta, lector, nulo)  # noqa: E731
        return RevisionCodigo(
            id=c("id", self._cadena),
            realizada_por=c("realizada_por", self._ids()),
            fecha=c("fecha", self._fecha),
            # Dudas, DI-8: «una técnica o las dos» (modelo, §7.2) se lee como lista no vacía.
            tecnicas=c("tecnicas", self._lista(self._enum(TECNICAS), no_vacia=True)),
            hallazgos=c("hallazgos", self._lista(self._hallazgo)),
            plan_accion=c("plan_accion", self._plan, nulo=True),
            seguimiento=c("seguimiento", self._lista(self._seguimiento)),
            evidencias=self._evidencias(obj, ruta),
        )

    def _vuelta_atras(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("responsables", "procedimiento", "ejecucion"))
        return VueltaAtras(
            responsables=self._campo(obj, "responsables", ruta, self._ids()),
            procedimiento=self._campo(obj, "procedimiento", ruta, self._cadena),
            ejecucion=self._campo(obj, "ejecucion", ruta, self._ejecucion, nulo=True),
        )

    def _ejecucion(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("actores", "fecha", "motivo"))
        return EjecucionVueltaAtras(
            actores=self._campo(obj, "actores", ruta, self._ids(no_vacia=True)),
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
            motivo=self._campo(obj, "motivo", ruta, self._cadena),
        )

    def _emergencia(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("tipo", "motivo", "procedimiento", "salvaguardias", "revision_posterior"))
        rp_ruta = _ruta(ruta, "revision_posterior")
        claves = ("documentacion", "reexamen", "evaluacion", "aprobacion")
        rp = self._objeto(obj["revision_posterior"], rp_ruta, claves) if obj and "revision_posterior" in obj else None
        return Emergencia(
            tipo=self._campo(obj, "tipo", ruta, self._enum(TIPOS_EMERGENCIA)),
            motivo=self._campo(obj, "motivo", ruta, self._cadena),
            procedimiento=self._campo(obj, "procedimiento", ruta, self._cadena),
            salvaguardias=self._campo(obj, "salvaguardias", ruta, self._cadena),
            revision_posterior=RevisionPosterior(**{k: self._campo(rp, k, rp_ruta, self._paso, nulo=True) for k in claves}),
        )

    def _implantacion(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("actores", "inicio", "fin", "resultado"))
        return Implantacion(
            actores=self._campo(obj, "actores", ruta, self._ids(no_vacia=True)),
            inicio=self._campo(obj, "inicio", ruta, self._fecha),
            fin=self._campo(obj, "fin", ruta, self._fecha, nulo=True),
            resultado=self._campo(obj, "resultado", ruta, self._enum(RESULTADOS_IMPLANTACION)),
        )

    def _verificacion_posterior(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("actores", "fecha", "resultado", "descripcion"))
        return VerificacionPosterior(
            actores=self._campo(obj, "actores", ruta, self._ids(no_vacia=True)),
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
            resultado=self._campo(obj, "resultado", ruta, self._enum(RESULTADOS_VERIFICACION)),
            descripcion=self._campo(obj, "descripcion", ruta, self._cadena, nulo=True),
        )

    def _accion(self, valor, ruta):
        obj = self._objeto(valor, ruta, ("actor", "fecha", "etapa", "descripcion"))
        return Accion(
            actor=self._campo(obj, "actor", ruta, self._cadena),
            fecha=self._campo(obj, "fecha", ruta, self._fecha),
            etapa=self._campo(obj, "etapa", ruta, self._enum(ETAPAS)),
            descripcion=self._campo(obj, "descripcion", ruta, self._cadena),
        )


# --- Segunda pasada: repetidos, referencias y coherencia (ERR-02 a ERR-05) -----


class _Coherencia:
    def __init__(self, carga: _Carga, entrada: Entrada):
        self.carga = carga
        self.e = entrada
        self.ids_actores = {a.id for a in entrada.actores}

    def comprobar(self):
        self._repetidos()
        self._referencias()
        self._agentes()
        imp = self.e.cambio.implantacion
        if imp.fin is not None and imp.fin < imp.inicio:
            self.carga.error("ERR-05", "`implantacion.fin` es anterior a `implantacion.inicio`", "cambio.implantacion.fin")

    def _repetidos(self):
        c = self.e.cambio
        listas = [("actores", [a.id for a in self.e.actores])]
        listas.append(("cambio.pruebas", [p.id for p in c.pruebas]))
        listas.append(("cambio.revisiones_codigo", [r.id for r in c.revisiones_codigo]))
        for i, r in enumerate(c.revisiones_codigo):
            listas.append((f"cambio.revisiones_codigo[{i}].hallazgos", [h.id for h in r.hallazgos]))
        for ruta, ids in listas:
            vistos = set()
            for id_ in ids:
                if id_ in vistos:
                    self.carga.error("ERR-02", f"`id` repetido: {id_}", ruta)
                vistos.add(id_)

    def _ref(self, id_, ruta):
        if id_ not in self.ids_actores:
            self.carga.error("ERR-03", f"No existe el actor {id_}", ruta)

    def _refs(self, ids, ruta):
        for i, id_ in enumerate(ids):
            self._ref(id_, f"{ruta}[{i}]")

    def _paso(self, paso, ruta):
        if paso is not None:
            self._refs(paso.actores, f"{ruta}.actores")

    def _referencias(self):
        c = self.e.cambio
        self._paso(c.solicitud, "cambio.solicitud")
        for k in ("especificacion_planificacion", "diseno_transicion", "pruebas_ultimacion", "aseguramiento_calidad"):
            self._refs(getattr(c.responsabilidades, k), f"cambio.responsabilidades.{k}")
        self._paso(c.verificacion_seguridad, "cambio.verificacion_seguridad")
        self._paso(c.evaluacion, "cambio.evaluacion")
        for i, p in enumerate(c.pruebas):
            self._refs(p.realizada_por, f"cambio.pruebas[{i}].realizada_por")
            if p.excepcion_datos_produccion is not None:
                self._paso(p.excepcion_datos_produccion.aprobacion, f"cambio.pruebas[{i}].excepcion_datos_produccion.aprobacion")
        for i, r in enumerate(c.revisiones_codigo):
            ruta = f"cambio.revisiones_codigo[{i}]"
            self._refs(r.realizada_por, f"{ruta}.realizada_por")
            hallazgos = {h.id for h in r.hallazgos}
            if r.plan_accion is not None:
                self._refs(r.plan_accion.adoptado_por, f"{ruta}.plan_accion.adoptado_por")
                for j, m in enumerate(r.plan_accion.medidas):
                    for k, h in enumerate(m.hallazgos):
                        if h not in hallazgos:
                            self.carga.error("ERR-03", f"No existe el hallazgo {h} en esta revisión", f"{ruta}.plan_accion.medidas[{j}].hallazgos[{k}]")
            for j, s in enumerate(r.seguimiento):
                self._paso(s, f"{ruta}.seguimiento[{j}]")
        if c.vuelta_atras is not None:
            self._refs(c.vuelta_atras.responsables, "cambio.vuelta_atras.responsables")
            self._paso(c.vuelta_atras.ejecucion, "cambio.vuelta_atras.ejecucion")
        self._paso(c.aprobacion, "cambio.aprobacion")
        if c.emergencia is not None:
            rp = c.emergencia.revision_posterior
            for k in ("documentacion", "reexamen", "evaluacion", "aprobacion"):
                self._paso(getattr(rp, k), f"cambio.emergencia.revision_posterior.{k}")
        self._paso(c.implantacion, "cambio.implantacion")
        self._paso(c.verificacion_posterior, "cambio.verificacion_posterior")
        for i, a in enumerate(c.acciones):
            self._ref(a.actor, f"cambio.acciones[{i}].actor")

    def _agentes(self):
        for i, a in enumerate(self.e.actores):
            ruta = f"actores[{i}]"
            if a.tipo == PERSONA:
                presentes = [k for k in CAMPOS_AGENTE if getattr(a, k) is not None]
                if presentes:
                    self.carga.error("ERR-04", f"Una persona no lleva los campos del agente: {', '.join(presentes)}", ruta)
            else:
                r = a.persona_responsable
                if r not in self.ids_actores:
                    self.carga.error("ERR-03", f"No existe el actor {r}", f"{ruta}.persona_responsable")
                elif self.e.actor(r).tipo != PERSONA:
                    self.carga.error("ERR-04", "`persona_responsable` debe ser una persona", f"{ruta}.persona_responsable")
