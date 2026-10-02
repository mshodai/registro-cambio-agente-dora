"""El corpus de corpus/: cada caso da su resultado esperado, y los datos son sintéticos.

Los resultados esperados están escritos a mano en corpus/generar.py; aquí se
comprueba que los ficheros escritos son los que genera el script, que el
cálculo los reproduce y que la línea de órdenes devuelve el código esperado.
"""

import json
import re

import pytest

from ayudas import CORPUS, G
from registro_cambio.carga import cargar_fichero
from registro_cambio.cli import main as cli
from registro_cambio.salida import como_dict, informe

ESPERADOS = sorted(CORPUS.glob("*.esperado.json"))
IDS = [p.name.removesuffix(".esperado.json") for p in ESPERADOS]


def test_estan_todos_los_casos():
    assert IDS == [c.nombre for c in G.CASOS]


def test_readme_es_el_del_script():
    assert (CORPUS / "README.md").read_text(encoding="utf-8") == G.readme()


@pytest.mark.parametrize("caso", G.CASOS, ids=lambda c: c.nombre)
def test_los_ficheros_son_los_del_script(caso):
    for nombre, contenido in G.ficheros(caso).items():
        assert (CORPUS / nombre).read_text(encoding="utf-8") == contenido


@pytest.mark.parametrize("caso", G.CASOS, ids=lambda c: c.nombre)
def test_cada_caso_da_su_resultado(caso):
    assert G.comprobar(caso) == []
    assert G.resumen(como_dict(informe(cargar_fichero(CORPUS / f"{caso.nombre}.json")))) == caso.esperado


@pytest.mark.parametrize("esperado", ESPERADOS, ids=IDS)
def test_la_linea_de_ordenes_da_el_codigo_esperado(esperado, capsys):
    datos = json.loads(esperado.read_text(encoding="utf-8"))
    fichero = str(CORPUS / f"{datos['caso']}.json")
    assert cli([fichero]) == datos["resultado"]["codigo_salida"]
    assert cli([fichero, "--json"]) == datos["resultado"]["codigo_salida"]


@pytest.mark.parametrize("caso", G.CASOS[1:], ids=lambda c: c.nombre)
def test_cada_caso_roto_lleva_su_articulo_en_el_nombre(caso):
    assert re.search(r"-(art|dora|modelo)-", caso.nombre), caso.nombre
    if any(a.startswith("A-03") for t in (caso.completo, caso.simplificado) for a in t[1]):
        assert "-aviso-" in caso.nombre, caso.nombre
    assert caso.articulo != "—"


@pytest.mark.parametrize("caso", G.CASOS[1:], ids=lambda c: c.nombre)
def test_cada_caso_roto_rompe_una_sola_cosa(caso):
    """Un requisito o un aviso, en uno o en los dos regímenes.

    Un A-03 cuenta por su requisito, y en la base de emergencia no cuenta el R-23
    del simplificado, que viene de la base (D-5).
    """
    def requisitos(r):
        return {a.removeprefix("A-03 ") for a in r["incumplimientos"] + r["avisos"]}

    completo, simplificado = requisitos(caso.esperado["completo"]), requisitos(caso.esperado["simplificado"])
    if caso.base is G.base_emergencia:
        simplificado.discard("R-23")
    assert len(completo | simplificado) == 1 or caso.nombre.startswith("20-"), (completo, simplificado)


def _todos(campo):
    for caso in G.CASOS:
        for r in como_dict(informe(cargar_fichero(CORPUS / f"{caso.nombre}.json")))["regimenes"].values():
            yield from r[campo]


# Requisitos que solo pueden fallar por una lectura propia (modelo, §0.1 bis, principio 2).
SOLO_LECTURA = {"R-03", "R-06", "R-17", "R-20", "R-22", "R-26"}
GARANTIZADOS = {"R-01", "R-04", "R-08", "R-24"}


def test_el_corpus_produce_todos_los_incumplimientos_posibles():
    posibles = {f"R-{n:02}" for n in range(1, 29)} - GARANTIZADOS - SOLO_LECTURA
    producidos = {r["id"] for r in _todos("requisitos") if r["estado"] == "incumplimiento"}
    assert producidos == posibles


def test_el_corpus_produce_todos_los_avisos_de_lectura_posibles():
    posibles = {
        "R-03", "R-05", "R-06", "R-11", "R-12", "R-13", "R-14", "R-16", "R-17",
        "R-18", "R-19", "R-20", "R-22", "R-23", "R-25", "R-26", "R-27", "R-28",
    }
    assert {a["requisito"] for a in _todos("avisos") if a["codigo"] == "A-03"} == posibles


def test_el_corpus_produce_todos_los_avisos_e_informativos():
    assert {a["codigo"] for a in _todos("avisos")} == {"A-01", "A-02", "A-03"}
    assert {a["codigo"] for a in _todos("informativos")} == {"I-01", "I-02"}


def test_ningun_resultado_de_lectura_propia_sale_como_incumplimiento():
    """Modelo, §0.1 bis, principio 2: el incumplimiento solo lo da el texto."""
    for r in _todos("requisitos"):
        if r["estado"] == "incumplimiento":
            assert r["id"] not in SOLO_LECTURA
            assert not any(m.startswith("Con la lectura") for m in r["motivos"]), r


@pytest.mark.parametrize("caso", [c for c in G.CASOS if "-aviso-" in c.nombre and not c.nombre.startswith(("40-", "41-"))], ids=lambda c: c.nombre)
def test_un_caso_de_lectura_propia_da_aviso_y_no_incumplimiento(caso):
    datos = como_dict(informe(cargar_fichero(CORPUS / f"{caso.nombre}.json")))["regimenes"]
    for regimen, r in datos.items():
        for a in r["avisos"]:
            if a["codigo"] != "A-03":
                continue
            req = next(x for x in r["requisitos"] if x["id"] == a["requisito"])
            assert req["estado"] in ("aviso", "sin_indicio_de_incumplimiento"), (regimen, req)
    assert datos["completo"]["incumplimientos"] == []


def _ids_y_textos(valor):
    if isinstance(valor, dict):
        for clave, v in valor.items():
            if isinstance(v, str) and clave in (
                "id", "funcion", "cuenta", "herramienta", "modelo", "referencia", "objeto", "procedimiento",
                "salvaguardias", "motivo", "descripcion", "destinatarios", "resultados_esperados",
                "repercusion_seguridad",
            ):
                yield clave, v
            else:
                yield from _ids_y_textos(v)
    elif isinstance(valor, list):
        for v in valor:
            yield from _ids_y_textos(v)


@pytest.mark.parametrize("caso", G.CASOS, ids=lambda c: c.nombre)
def test_los_datos_son_sinteticos(caso):
    """Regla 3: nombres y textos genéricos e inventados."""
    for clave, v in _ids_y_textos(caso.entrada()):
        if clave == "id" or not v.strip():
            continue
        assert re.search(r"ejemplo|inventad", v, re.I), (clave, v)
