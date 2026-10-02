"""Estructuras de datos de la entrada, según docs/modelo-datos.md (versión 1).

Describen la entrada ya validada y no contienen ninguna regla de cálculo. No
hay régimen: es un parámetro del cálculo (modelo, §0.1, principio 2). Todas
las fechas son `datetime` con zona horaria (modelo, §2).

Del agente de IA solo hay su identidad (herramienta, modelo, versión y persona
responsable) y lo que hizo: nada interno (modelo, §0.2, regla 2).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

VERSION_MODELO = 1

# §3
PERSONA = "persona"
AGENTE_IA = "agente_ia"
TIPOS_ACTOR = (PERSONA, AGENTE_IA)

# §4
ELEMENTOS = ("software", "hardware", "firmware", "sistema", "parametros_seguridad")
DESARROLLO_INTERNO = "desarrollo_interno"
ORIGENES_CODIGO = (DESARROLLO_INTERNO, "proveedor_tercero", "software_propietario", "codigo_abierto")
# Art. 16.8: los orígenes que deben revisarse antes de la implantación en producción (D-3).
ORIGENES_DE_TERCEROS = ("proveedor_tercero", "software_propietario", "codigo_abierto")

# §5.2
APLICADO = "aplicado"
RESULTADOS_IMPLANTACION = (APLICADO, "abortado", "revertido")

# §6.1
NO_CUMPLE = "no_cumple"
RESULTADOS_VERIFICACION_SEGURIDAD = ("cumple", NO_CUMPLE)

# §7.1
SEGURIDAD_PAQUETES = "seguridad_paquetes"
TIPOS_PRUEBA = ("idoneidad", "calidad_software", "seguridad_expuesto_internet", SEGURIDAD_PAQUETES, "otra")
FASES = ("desarrollo", "integracion", "preproduccion", "produccion")
# Art. 16.4: «a más tardar en la fase de integración».
FASES_HASTA_INTEGRACION = ("desarrollo", "integracion")
NO_PRODUCCION = "no_produccion"
ENTORNOS = ("produccion", NO_PRODUCCION)
DATOS_PRODUCCION = "produccion"
DATOS = ("sin_datos_produccion", "produccion_anonimizados", DATOS_PRODUCCION)
RESULTADOS_PRUEBA = ("superada", "no_superada")

# §7.2
TECNICAS = ("estatica", "dinamica")
ESTADOS_SEGUIMIENTO = ("pendiente", "completado")

# §9
TIPOS_EMERGENCIA = ("cambio", "solucion_alternativa", "parche")

# §10
RESULTADOS_VERIFICACION = ("conforme", "no_conforme")

# §11
ETAPAS = (
    "solicitud",
    "especificacion",
    "pruebas",
    "revision_codigo",
    "implantacion",
    "vuelta_atras",
    "verificacion",
    "otra",
)

# Modelo, §15.
ERRORES = {
    "ERR-01": "JSON mal formado o con claves repetidas, campo obligatorio ausente, tipo o valor no válido, "
    "fecha sin la forma del §2, `version_modelo` distinto de 1, o campo `regimen` u otro desconocido",
    "ERR-02": "`id` repetido en `actores`, en `pruebas`, en `revisiones_codigo` o en los `hallazgos` de una revisión",
    "ERR-03": "Una referencia apunta a un `id` que no existe",
    "ERR-04": "`persona_responsable` que no es una persona, o campos del §3.2 en un actor `persona`",
    "ERR-05": "`implantacion.fin` anterior a `implantacion.inicio`",
}


@dataclass(frozen=True)
class Actor:
    id: str
    tipo: str
    funcion: str
    cuenta: Optional[str]
    herramienta: Optional[str] = None
    modelo: Optional[str] = None
    version: Optional[str] = None
    persona_responsable: Optional[str] = None

    @property
    def es_persona(self) -> bool:
        return self.tipo == PERSONA


@dataclass(frozen=True)
class Paso:
    """Un paso del cambio con sus actores y su fecha (modelo, §2)."""

    actores: tuple[str, ...]
    fecha: datetime


@dataclass(frozen=True)
class Evidencia:
    referencia: str
    descripcion: Optional[str]


@dataclass(frozen=True)
class Comunicacion:
    fecha: datetime
    destinatarios: str


@dataclass(frozen=True)
class Responsabilidades:
    especificacion_planificacion: tuple[str, ...]
    diseno_transicion: tuple[str, ...]
    pruebas_ultimacion: tuple[str, ...]
    aseguramiento_calidad: tuple[str, ...]


@dataclass(frozen=True)
class VerificacionSeguridad:
    actores: tuple[str, ...]
    fecha: datetime
    resultado: str
    evidencias: tuple[Evidencia, ...]


@dataclass(frozen=True)
class Evaluacion:
    actores: tuple[str, ...]
    fecha: datetime
    repercusion_seguridad: Optional[str]
    requiere_medidas_adicionales: Optional[bool]
    medidas_adicionales: tuple[str, ...]
    riesgos: Optional[str]


@dataclass(frozen=True)
class ControlIntegridad:
    descripcion: str
    evidencias: tuple[Evidencia, ...]


@dataclass(frozen=True)
class ExcepcionDatosProduccion:
    aprobacion: Paso
    hasta: datetime
    notificacion_funcion_riesgo_tic: datetime


@dataclass(frozen=True)
class Prueba:
    id: str
    tipo: str
    descripcion: str
    realizada_por: tuple[str, ...]
    fecha: datetime
    fase: str
    entorno: str
    datos: str
    excepcion_datos_produccion: Optional[ExcepcionDatosProduccion]
    resultado: str
    evidencias: tuple[Evidencia, ...]


@dataclass(frozen=True)
class Hallazgo:
    id: str
    descripcion: str


@dataclass(frozen=True)
class Medida:
    hallazgos: tuple[str, ...]
    descripcion: str


@dataclass(frozen=True)
class PlanAccion:
    adoptado_por: tuple[str, ...]
    fecha: datetime
    medidas: tuple[Medida, ...]


@dataclass(frozen=True)
class Seguimiento:
    actores: tuple[str, ...]
    fecha: datetime
    estado: str
    descripcion: Optional[str]


@dataclass(frozen=True)
class RevisionCodigo:
    id: str
    realizada_por: tuple[str, ...]
    fecha: datetime
    tecnicas: tuple[str, ...]
    hallazgos: tuple[Hallazgo, ...]
    plan_accion: Optional[PlanAccion]
    seguimiento: tuple[Seguimiento, ...]
    evidencias: tuple[Evidencia, ...]


@dataclass(frozen=True)
class EjecucionVueltaAtras:
    actores: tuple[str, ...]
    fecha: datetime
    motivo: str


@dataclass(frozen=True)
class VueltaAtras:
    responsables: tuple[str, ...]
    procedimiento: str
    ejecucion: Optional[EjecucionVueltaAtras]


@dataclass(frozen=True)
class RevisionPosterior:
    documentacion: Optional[Paso]
    reexamen: Optional[Paso]
    evaluacion: Optional[Paso]
    aprobacion: Optional[Paso]


@dataclass(frozen=True)
class Emergencia:
    tipo: str
    motivo: str
    procedimiento: str
    salvaguardias: str
    revision_posterior: RevisionPosterior


@dataclass(frozen=True)
class Implantacion:
    actores: tuple[str, ...]
    inicio: datetime
    fin: Optional[datetime]
    resultado: str


@dataclass(frozen=True)
class VerificacionPosterior:
    actores: tuple[str, ...]
    fecha: datetime
    resultado: str
    descripcion: Optional[str]


@dataclass(frozen=True)
class Accion:
    actor: str
    fecha: datetime
    etapa: str
    descripcion: str


@dataclass(frozen=True)
class Cambio:
    id: str
    elementos: tuple[str, ...]
    objeto: str
    alcance_descripcion: str
    alcance_sistemas: tuple[str, ...]
    inicio_previsto: datetime
    fin_previsto: datetime
    resultados_esperados: str
    comunicaciones: tuple[Comunicacion, ...]
    incluye_codigo_fuente: bool
    origen_codigo: tuple[str, ...]
    cambio_importante: Optional[bool]
    solicitud: Paso
    responsabilidades: Responsabilidades
    verificacion_seguridad: Optional[VerificacionSeguridad]
    evaluacion: Optional[Evaluacion]
    controles_integridad: tuple[ControlIntegridad, ...]
    pruebas: tuple[Prueba, ...]
    revisiones_codigo: tuple[RevisionCodigo, ...]
    vuelta_atras: Optional[VueltaAtras]
    aprobacion: Optional[Paso]
    emergencia: Optional[Emergencia]
    implantacion: Implantacion
    verificacion_posterior: Optional[VerificacionPosterior]
    acciones: tuple[Accion, ...]


@dataclass(frozen=True)
class Entrada:
    actores: tuple[Actor, ...]
    cambio: Cambio

    def actor(self, id_: str) -> Actor:
        return next(a for a in self.actores if a.id == id_)


@dataclass(frozen=True)
class Incidencia:
    """Un error de validación de la entrada (modelo, §15)."""

    codigo: str
    mensaje: str
    ruta: str = ""


@dataclass(frozen=True)
class ResultadoCarga:
    entrada: Optional[Entrada]
    errores: tuple[Incidencia, ...]

    @property
    def valida(self) -> bool:
        return not self.errores
