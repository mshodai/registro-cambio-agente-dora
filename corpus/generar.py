"""Genera el corpus de registros de cambios con su resultado esperado.

Uso, desde la raíz del repositorio:

    python corpus/generar.py

Cada caso parte de una base limpia (el ejemplo del §1.1 de docs/modelo-datos.md
con una revisión hecha por una persona, para que no lleve el aviso A-01) o de
una base de emergencia (el ejemplo del §1.2), y rompe un solo requisito o
provoca un solo aviso. Los casos que dan un aviso de lectura propia (A-03)
llevan en el nombre «aviso» y la lectura de la que sale (D-n, DI-n o la
sección del modelo).
El nombre de cada caso lleva el artículo que rompe.

Los resultados esperados están escritos a mano a partir de docs/modelo-datos.md.
Antes de escribir los ficheros, el script comprueba cada caso con el código de
src/ y se detiene si alguno no da lo esperado. Todos los datos son inventados
(modelo, §0.2, regla 3).
"""

import copy
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

RAIZ = Path(__file__).resolve().parent.parent
CORPUS = RAIZ / "corpus"
sys.path.insert(0, str(RAIZ / "src"))

from registro_cambio.carga import cargar  # noqa: E402
from registro_cambio.salida import como_dict, informe  # noqa: E402


def ejemplos_del_modelo():
    """Los tres bloques JSON de docs/modelo-datos.md, compuestos como dice el modelo.

    El §1.2 y el fragmento del D-1 solo muestran los campos de `cambio` que
    cambian; «los demás serían como allí» (§1.2).
    """
    texto = (RAIZ / "docs" / "modelo-datos.md").read_text(encoding="utf-8")
    bloques = [json.loads(b) for b in re.findall(r"```json\n(.*?)```", texto, re.S)]
    base = bloques[0]
    emergencia = copy.deepcopy(base)
    emergencia["cambio"].update(bloques[1])
    d1 = copy.deepcopy(base)
    d1["cambio"].update(bloques[2])
    return {"1.1": base, "1.2": emergencia, "D-1": d1}


def base_limpia():
    e = copy.deepcopy(ejemplos_del_modelo()["1.1"])
    # Sin autorrevisión: la revisión estática la hace la persona responsable del agente.
    e["cambio"]["revisiones_codigo"][0]["realizada_por"] = ["P-3"]
    return e


def base_emergencia():
    e = base_limpia()
    emergencia = ejemplos_del_modelo()["1.2"]["cambio"]
    for clave in ("aprobacion", "emergencia", "implantacion", "verificacion_posterior", "acciones"):
        e["cambio"][clave] = copy.deepcopy(emergencia[clave])
    return e


AGENTE_APROBADOR = {
    "id": "AG-2",
    "tipo": "agente_ia",
    "funcion": "FUNCION-APROBACION-EJEMPLO",
    "cuenta": "CUENTA-EJEMPLO-5",
    "herramienta": "HERRAMIENTA-EJEMPLO-2",
    "modelo": "MODELO-EJEMPLO-2",
    "version": "0.0-ejemplo",
    "persona_responsable": "P-2",
}


@dataclass(frozen=True)
class Caso:
    nombre: str
    articulo: str
    descripcion: str
    base: Callable
    mutar: Callable
    # {régimen: (incumplimientos, avisos, informativos)}
    completo: tuple
    simplificado: tuple

    def entrada(self):
        e = self.base()
        self.mutar(e)
        return e

    @property
    def esperado(self):
        def r(t):
            return {"incumplimientos": list(t[0]), "avisos": list(t[1]), "informativos": list(t[2])}

        # 1 si hay un incumplimiento o un aviso de lectura propia (A-03) en algún régimen.
        def exige(t):
            return bool(t[0]) or any(a.startswith("A-03") for a in t[1])

        codigo = 1 if exige(self.completo) or exige(self.simplificado) else 0
        return {"completo": r(self.completo), "simplificado": r(self.simplificado), "codigo_salida": codigo}


def _c(e):
    return e["cambio"]


def _nada(e):
    pass


def _poner(**campos):
    def mutar(e):
        _c(e).update(campos)

    return mutar


def _misma_funcion(e):
    e["actores"].append({"id": "P-4", "tipo": "persona", "funcion": "FUNCION-APROBACION-EJEMPLO", "cuenta": None})
    _c(e)["solicitud"]["actores"] = ["P-4"]


def _sin_cuenta_el_agente(e):
    e["actores"][3]["cuenta"] = None


def _verificacion_negativa(e):
    _c(e)["verificacion_seguridad"]["resultado"] = "no_cumple"


def _medidas_sin_detallar(e):
    _c(e)["evaluacion"]["requiere_medidas_adicionales"] = True


def _importante_sin_riesgos(e):
    _c(e)["cambio_importante"] = True


def _pruebas_tardias(e):
    for p in _c(e)["pruebas"]:
        p["fecha"] = "2026-11-09T10:00:00+01:00"


def _paquetes_en_produccion(e):
    _c(e)["pruebas"][1]["fase"] = "produccion"


def _datos_produccion(e):
    _c(e)["pruebas"][0]["datos"] = "produccion"


def _excepcion_de_agente(e):
    e["actores"].append(copy.deepcopy(AGENTE_APROBADOR))
    p = _c(e)["pruebas"][0]
    p["datos"] = "produccion"
    p["excepcion_datos_produccion"] = {
        "aprobacion": {"actores": ["AG-2"], "fecha": "2026-11-04T09:00:00+01:00"},
        "hasta": "2026-11-06T00:00:00+01:00",
        "notificacion_funcion_riesgo_tic": "2026-11-04T09:30:00+01:00",
    }


def _sin_dinamica(e):
    _c(e)["revisiones_codigo"][1]["tecnicas"] = ["estatica"]


def _plan_de_agente(e):
    _c(e)["revisiones_codigo"][0]["plan_accion"]["adoptado_por"] = ["AG-1"]


def _hallazgo_sin_medida(e):
    _c(e)["revisiones_codigo"][0]["hallazgos"].append({"id": "H-2", "descripcion": "Hallazgo de ejemplo 2 (inventado)"})


def _seguimiento_de_agente(e):
    _c(e)["revisiones_codigo"][0]["seguimiento"][0]["actores"] = ["AG-1"]


def _abierto_revisado_despues(e):
    c = _c(e)
    c["origen_codigo"] = ["codigo_abierto"]
    for r in c["revisiones_codigo"]:
        r["fecha"] = "2026-11-09T10:00:00+01:00"


def _aprobacion_tardia(e):
    _c(e)["aprobacion"]["fecha"] = "2026-11-09T10:00:00+01:00"


def _aprobacion_de_agente(e):
    e["actores"].append(copy.deepcopy(AGENTE_APROBADOR))
    _c(e)["aprobacion"]["actores"] = ["AG-2"]


def _revertido_sin_ejecucion(e):
    _c(e)["implantacion"]["resultado"] = "revertido"


def _sin_salvaguardias(e):
    _c(e)["emergencia"]["salvaguardias"] = ""


def _revision_pendiente(e):
    _c(e)["emergencia"]["revision_posterior"]["aprobacion"] = None


def _reexamen_previo(e):
    _c(e)["emergencia"]["revision_posterior"]["reexamen"]["fecha"] = "2026-11-09T22:00:00+01:00"


def _aprobacion_posterior_de_agente(e):
    e["actores"].append(copy.deepcopy(AGENTE_APROBADOR))
    _c(e)["emergencia"]["revision_posterior"]["aprobacion"]["actores"] = ["AG-2"]


def _autorrevision_otra_instancia(e):
    otro = copy.deepcopy(e["actores"][3])
    otro.update({"id": "AG-3", "cuenta": "CUENTA-EJEMPLO-6"})
    e["actores"].append(otro)
    _c(e)["revisiones_codigo"][0]["realizada_por"] = ["AG-3"]


def _sin_evidencias(e):
    _c(e)["pruebas"][0]["evidencias"] = []


def _pruebas_tras_emergencia(e):
    for p in _c(e)["pruebas"]:
        p["fecha"] = "2026-11-09T23:30:00+01:00"


def _revertido_sin_verificar(e):
    c = _c(e)
    c["implantacion"]["resultado"] = "revertido"
    c["vuelta_atras"]["ejecucion"] = {"actores": ["P-3"], "fecha": "2026-11-09T10:00:00+01:00", "motivo": "Motivo de ejemplo (inventado)"}
    c["verificacion_posterior"] = None


def _verificacion_previa(e):
    _c(e)["verificacion_posterior"]["fecha"] = "2026-11-09T09:00:00+01:00"


def _prueba_sin_autor(e):
    _c(e)["pruebas"][0]["realizada_por"] = []


def _sin_seguimiento(e):
    _c(e)["revisiones_codigo"][0]["seguimiento"] = []


I2 = ("I-02",)
I12 = ("I-01", "I-02")
NADA = ((), (), ())


def _a(*requisitos):
    """Avisos de lectura propia (A-03), uno por requisito."""
    return tuple(f"A-03 {r}" for r in requisitos)


CASOS = (
    Caso("01-base-limpia", "—", "Base limpia, sin incumplimientos ni avisos.", base_limpia, _nada, NADA, ((), (), I2)),
    Caso("02-art-17-1-d-i-sin-elementos", "Art. 17.1.d.i); art. 17.1, encabezado", "No dice qué se cambia: incumplimiento en el completo.", base_limpia, _poner(elementos=[]), (("R-02",), (), ()), ((), (), I2)),
    Caso("03-art-21-c-art-33-b-aviso-di-2-implantador-sin-cuenta", "Arts. 21.c) y 33.b); modelo §3.1; DI-2", "El agente que implanta no tiene cuenta. Registrar la cuenta lo pide el modelo: aviso en los dos regímenes.", base_limpia, _sin_cuenta_el_agente, ((), _a("R-03"), ()), ((), _a("R-03"), I2)),
    Caso("04-art-17-1-b-d-1-misma-persona-solicita-y-aprueba", "Art. 17.1.b); D-1", "El mismo actor solicita y aprueba: incumplimiento que sostiene el texto. En el simplificado es solo informativo.", base_limpia, lambda e: _c(e)["solicitud"].update(actores=["P-2"]), (("R-05",), (), ()), ((), (), I12)),
    Caso("05-art-17-1-b-aviso-d-1-considerando-17-misma-funcion", "Art. 17.1.b); considerando 17; D-1", "Solicita otra persona de la misma función que aprueba: sin indicio, con aviso de la D-1.", base_limpia, _misma_funcion, ((), _a("R-05"), ()), ((), (), I12)),
    Caso("06-art-17-1-b-aviso-d-1-aprueba-el-responsable-del-agente", "Art. 17.1.b); D-1; modelo §3.2", "Aprueba la persona responsable del agente que implanta: sin indicio, con aviso de la D-1.", base_limpia, lambda e: _c(e)["aprobacion"].update(actores=["P-3"]), ((), _a("R-05"), ()), ((), (), I12)),
    Caso("07-art-17-1-c-iv-aviso-modelo-5-1-aseguramiento-de-calidad-sin-asignar", "Art. 17.1.c.iv); modelo §5.1", "Nadie tiene asignado el aseguramiento de la calidad en el registro: sin indicio, con aviso.", base_limpia, lambda e: _c(e)["responsabilidades"].update(aseguramiento_calidad=[]), ((), _a("R-06"), ()), ((), (), I2)),
    Caso("08-art-17-1-d-i-sin-objeto", "Art. 17.1.d.i); dudas, DI-1", "El objeto es una cadena vacía.", base_limpia, _poner(objeto=""), (("R-07",), (), ()), ((), (), I2)),
    Caso("09-art-17-1-d-iii-sin-resultados-esperados", "Art. 17.1.d.iii)", "Faltan los resultados esperados.", base_limpia, _poner(resultados_esperados=" "), (("R-09",), (), ()), ((), (), I2)),
    Caso("10-art-17-1-d-sin-comunicaciones", "Art. 17.1.d), encabezado", "No se comunicaron los detalles.", base_limpia, _poner(comunicaciones=[]), (("R-10",), (), ()), ((), (), I2)),
    Caso("11-art-17-1-a-sin-verificacion-de-seguridad", "Art. 17.1.a)", "No se verificaron los requisitos de seguridad.", base_limpia, _poner(verificacion_seguridad=None), (("R-11",), (), ()), ((), (), I2)),
    Caso("12-art-17-1-a-aviso-di-3-verificacion-negativa-y-aplicado", "Art. 17.1.a); dudas, DI-3", "La verificación da no_cumple y el cambio se aplica: aviso.", base_limpia, _verificacion_negativa, ((), _a("R-11"), ()), ((), (), I2)),
    Caso("13-dora-art-9-4-e-art-38-2-sin-evaluacion", "DORA, art. 9.4.e); art. 38.2", "No se evaluó el cambio.", base_limpia, _poner(evaluacion=None), (("R-12",), (), ()), (("R-12",), (), I2)),
    Caso("14-art-17-1-h-aviso-modelo-6-2-medidas-adicionales-sin-detallar", "Art. 17.1.h); modelo §6.2", "Hacen falta medidas adicionales y no se dice cuáles: aviso.", base_limpia, _medidas_sin_detallar, ((), _a("R-12"), ()), ((), (), I2)),
    Caso("15-art-31-1-e-cambio-importante-sin-riesgos", "Art. 31.1.e)", "Cambio importante sin evaluación de riesgos: solo simplificado.", base_limpia, _importante_sin_riesgos, NADA, (("R-13",), (), I2)),
    Caso("16-art-31-1-e-aviso-modelo-4-sin-declarar-si-es-importante", "Art. 31.1.e); modelo §4", "La entidad no declara si el cambio es importante: aviso, solo simplificado.", base_limpia, _poner(cambio_importante=None), NADA, ((), _a("R-13"), I2)),
    Caso("17-art-16-2-art-37-b-pruebas-posteriores-a-la-implantacion", "Art. 16.2; art. 37.b)", "Todas las pruebas son posteriores a la implantación.", base_limpia, _pruebas_tardias, (("R-14",), (), ()), (("R-14",), (), I2)),
    Caso("18-art-16-2-art-37-b-sin-pruebas", "Art. 16.2; art. 37.b); dudas, DI-8", "No hay pruebas.", base_limpia, _poner(pruebas=[]), (("R-14",), (), ()), (("R-14",), (), I2)),
    Caso("19-art-16-4-seguridad-de-paquetes-en-produccion", "Art. 16.4", "La prueba de seguridad de paquetes se hace en producción.", base_limpia, _paquetes_en_produccion, (("R-15",), (), ()), ((), (), I2)),
    Caso("20-emergencia-bien-registrada-art-37-b-simplificado-d-5", "Art. 37.b); D-5", "Parche de emergencia bien registrado: el completo no tiene incumplimientos; el simplificado incumple el art. 37.b) literal (la D-5 documenta la lectura alternativa).", base_emergencia, _nada, NADA, (("R-23",), (), I2)),
    Caso("21-art-16-5-a-datos-de-produccion-sin-excepcion", "Art. 16.5.a)", "Una prueba fuera de producción usa datos de producción sin excepción.", base_limpia, _datos_produccion, (("R-16",), (), ()), ((), (), I2)),
    Caso("22-art-16-6-aviso-d-4-excepcion-aprobada-solo-por-un-agente", "Art. 16.6; D-4", "La excepción de datos de producción la aprueba solo un agente: aviso.", base_limpia, _excepcion_de_agente, ((), _a("R-16"), ()), ((), (), I2)),
    Caso("23-art-16-3-aviso-modelo-7-2-sin-revision-dinamica", "Art. 16.3; modelo §7.2", "Ninguna revisión usa la técnica dinámica: aviso.", base_limpia, _sin_dinamica, ((), _a("R-17"), ()), ((), (), I2)),
    Caso("24-art-16-3-b-aviso-d-2-plan-adoptado-solo-por-un-agente", "Art. 16.3.b); D-2, punto 2", "El plan de acción lo adopta solo un agente: aviso.", base_limpia, _plan_de_agente, ((), _a("R-18"), ()), ((), (), I2)),
    Caso("25-art-16-3-b-hallazgo-sin-medida", "Art. 16.3.b)", "Un hallazgo sin medida en el plan de acción.", base_limpia, _hallazgo_sin_medida, (("R-18",), (), ()), ((), (), I2)),
    Caso("26-art-16-3-c-aviso-d-2-seguimiento-solo-por-un-agente", "Art. 16.3.c); D-2, punto 3", "El seguimiento lo hace solo un agente: aviso.", base_limpia, _seguimiento_de_agente, ((), _a("R-19"), ()), ((), (), I2)),
    Caso("27-art-16-7-aviso-d-3-codigo-sin-origen", "Arts. 16.7 y 16.8; D-3", "El cambio incluye código y no declara su origen: aviso.", base_limpia, _poner(origen_codigo=[]), ((), _a("R-20"), ()), ((), (), I2)),
    Caso("28-art-16-8-d-3-codigo-abierto-revisado-despues", "Art. 16.8; D-3", "Código abierto revisado después de la implantación.", base_limpia, _abierto_revisado_despues, (("R-21",), (), ()), ((), (), I2)),
    Caso("29-art-16-1-c-art-37-c-aviso-modelo-6-3-sin-controles-de-integridad", "Art. 16.1.c); art. 37.c); modelo §6.3", "No hay medidas contra la manipulación en el registro: sin indicio, con aviso en los dos regímenes.", base_limpia, _poner(controles_integridad=[]), ((), _a("R-22"), ()), ((), _a("R-22"), I2)),
    Caso("30-dora-art-9-4-e-art-37-b-aprobacion-posterior-a-la-implantacion", "DORA, art. 9.4.e); art. 16.2; art. 37.b)", "La aprobación es posterior a la implantación.", base_limpia, _aprobacion_tardia, (("R-23",), (), ()), (("R-23",), (), I2)),
    Caso("31-art-37-b-aviso-d-4-aprobacion-solo-por-un-agente", "Art. 37.b); D-4", "Aprueba solo un agente: aviso en los dos regímenes.", base_limpia, _aprobacion_de_agente, ((), _a("R-23"), ()), ((), _a("R-23"), I2)),
    Caso("32-dora-art-9-4-e-art-37-b-sin-aprobacion", "DORA, art. 9.4.e); art. 37.b); dudas, DI-9", "Sin aprobación y sin emergencia.", base_limpia, _poner(aprobacion=None), (("R-23",), (), ()), (("R-23",), (), I2)),
    Caso("33-art-17-1-e-sin-vuelta-atras", "Art. 17.1.e)", "No hay procedimiento de vuelta atrás.", base_limpia, _poner(vuelta_atras=None), (("R-25",), (), ()), ((), (), I2)),
    Caso("34-art-17-1-e-aviso-modelo-8-revertido-sin-ejecucion", "Art. 17.1.e); modelo §8", "El cambio se revirtió y no consta cómo: aviso.", base_limpia, _revertido_sin_ejecucion, ((), _a("R-25"), ()), ((), (), I2)),
    Caso("35-art-17-1-f-aviso-modelo-9-emergencia-sin-salvaguardias", "Art. 17.1.f); modelo §9", "Cambio de emergencia sin salvaguardias en el registro: sin indicio, con aviso.", base_emergencia, _sin_salvaguardias, ((), _a("R-26"), ()), (("R-23",), (), I2)),
    Caso("36-art-17-1-g-aviso-di-6-revision-posterior-pendiente", "Art. 17.1.g); dudas, DI-6", "Falta la aprobación posterior del cambio de emergencia: pendiente, aviso.", base_emergencia, _revision_pendiente, ((), _a("R-27"), ()), (("R-23",), (), I2)),
    Caso("37-art-17-1-g-reexamen-anterior-a-la-aplicacion", "Art. 17.1.g)", "El reexamen es anterior a la aplicación.", base_emergencia, _reexamen_previo, (("R-27",), (), ()), (("R-23",), (), I2)),
    Caso("38-art-17-1-g-aviso-d-4-aprobacion-posterior-solo-por-un-agente", "Art. 17.1.g); D-4", "La aprobación posterior la da solo un agente: aviso.", base_emergencia, _aprobacion_posterior_de_agente, ((), _a("R-27"), ()), (("R-23",), (), I2)),
    Caso("39-dora-art-9-4-e-art-38-2-sin-verificacion-posterior", "DORA, art. 9.4.e); art. 38.2", "No se verificó un cambio aplicado.", base_limpia, _poner(verificacion_posterior=None), (("R-28",), (), ()), (("R-28",), (), I2)),
    Caso("40-art-17-1-c-iv-d-2-aviso-autorrevision", "Art. 17.1.c.iv); D-2, punto 4", "Revisa otro agente con la misma herramienta, modelo y versión que el que implanta: aviso A-01, no exige actuar.", base_limpia, _autorrevision_otra_instancia, ((), ("A-01",), ()), ((), (), I2)),
    Caso("41-modelo-7-3-aviso-sin-evidencias", "DORA, art. 9.4.e); art. 38.2; modelo, §7.3", "Una prueba sin evidencias: aviso A-02 en los dos regímenes, no exige actuar.", base_limpia, _sin_evidencias, ((), ("A-02",), ()), ((), ("A-02",), I2)),
    Caso("42-art-16-2-aviso-di-4-emergencia-sin-pruebas-previas", "Art. 16.2; art. 37.b); dudas, DI-4; D-5", "Cambio de emergencia sin pruebas previas: aviso en el completo (DI-4); incumplimiento del art. 37.b) literal en el simplificado.", base_emergencia, _pruebas_tras_emergencia, ((), _a("R-14"), ()), (("R-14", "R-23"), (), I2)),
    Caso("43-dora-art-9-4-e-aviso-di-10-revertido-sin-verificacion", "DORA, art. 9.4.e); art. 38.2; dudas, DI-10", "Cambio revertido sin verificación posterior: aviso en los dos regímenes.", base_limpia, _revertido_sin_verificar, ((), _a("R-28"), ()), ((), _a("R-28"), I2)),
    Caso("44-dora-art-9-4-e-aviso-modelo-10-verificacion-anterior-a-la-implantacion", "DORA, art. 9.4.e); art. 38.2; modelo §10", "La verificación posterior es anterior a la implantación: aviso en los dos regímenes.", base_limpia, _verificacion_previa, ((), _a("R-28"), ()), ((), _a("R-28"), I2)),
    Caso("45-art-21-c-art-33-b-aviso-di-8-prueba-sin-autor", "Arts. 21.c) y 33.b); modelo §7.1; DI-8", "Una prueba no dice quién la hizo: aviso en los dos regímenes.", base_limpia, _prueba_sin_autor, ((), _a("R-03"), ()), ((), _a("R-03"), I2)),
    Caso("46-art-16-3-c-sin-seguimiento", "Art. 16.3.c)", "El plan de acción no tiene seguimiento.", base_limpia, _sin_seguimiento, (("R-19",), (), ()), ((), (), I2)),
)


def resumen(inf_dict):
    """Lo que se compara con el resultado esperado."""
    out = {}
    for regimen, r in inf_dict["regimenes"].items():
        out[regimen] = {
            "incumplimientos": r["incumplimientos"],
            "avisos": [f"{a['codigo']} {a['requisito']}" if a["codigo"] == "A-03" else a["codigo"] for a in r["avisos"]],
            "informativos": [a["codigo"] for a in r["informativos"]],
        }
    out["codigo_salida"] = inf_dict["codigo_salida"]
    return out


def calcular(entrada):
    carga = cargar(json.dumps(entrada, ensure_ascii=False))
    if not carga.valida:
        raise ValueError(f"entrada no válida: {carga.errores}")
    return resumen(como_dict(informe(carga)))


def comprobar(caso: Caso) -> list[str]:
    """Las diferencias entre lo calculado y lo esperado; vacía si coinciden."""
    obtenido = calcular(caso.entrada())
    return [
        f"{caso.nombre}: {clave}: esperado {caso.esperado[clave]}, obtenido {obtenido[clave]}"
        for clave in caso.esperado
        if caso.esperado[clave] != obtenido[clave]
    ]


def _json(datos):
    return json.dumps(datos, ensure_ascii=False, indent=2) + "\n"


def ficheros(caso: Caso) -> dict[str, str]:
    return {
        f"{caso.nombre}.json": _json(caso.entrada()),
        f"{caso.nombre}.esperado.json": _json(
            {"caso": caso.nombre, "articulo": caso.articulo, "descripcion": caso.descripcion, "resultado": caso.esperado}
        ),
    }


def readme() -> str:
    lineas = [
        "# Corpus",
        "",
        "Registros sintéticos de cambios con su resultado esperado. Lo genera `corpus/generar.py`, que comprueba cada caso "
        "con el código de `src/` antes de escribirlo. No se edita a mano.",
        "",
        "```",
        "python corpus/generar.py",
        "```",
        "",
        "Cada caso rompe un solo requisito o provoca un solo aviso, y su nombre lleva el artículo que rompe. Si el resultado "
        "es un aviso de lectura propia (A-03, modelo §0.1 bis), el nombre lleva además «aviso» y la lectura de la que sale. "
        "Parte de una base limpia (el ejemplo del §1.1 de `docs/modelo-datos.md`, con la revisión estática hecha por una "
        "persona) o de una base de emergencia (el ejemplo del §1.2). El código de salida es 1 si hay un incumplimiento o un "
        "A-03 en algún régimen. `I-02` aparece en el simplificado de todos los casos porque todos tienen revisiones de código, que el "
        "título III no exige.",
        "",
        "| Caso | Artículo | Completo | Simplificado | Código |",
        "|---|---|---|---|---|",
    ]

    def celda(t):
        partes = list(t[0]) + [f"aviso {a}" for a in t[1]] + [f"info {i}" for i in t[2]]
        return ", ".join(partes) or "—"

    for c in CASOS:
        lineas.append(f"| {c.nombre} | {c.articulo} | {celda(c.completo)} | {celda(c.simplificado)} | {c.esperado['codigo_salida']} |")
    lineas += ["", "## Qué demuestra cada caso", ""]
    lineas += [f"- **{c.nombre}.** {c.descripcion}" for c in CASOS]
    return "\n".join(lineas) + "\n"


def main():
    errores = [d for c in CASOS for d in comprobar(c)]
    if errores:
        print("\n".join(errores), file=sys.stderr)
        return 1
    for c in CASOS:
        for nombre, contenido in ficheros(c).items():
            (CORPUS / nombre).write_text(contenido, encoding="utf-8")
    (CORPUS / "README.md").write_text(readme(), encoding="utf-8")
    print(f"{len(CASOS)} casos escritos en {CORPUS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
