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
    assert caso.articulo != "—"


@pytest.mark.parametrize("caso", G.CASOS[1:], ids=lambda c: c.nombre)
def test_cada_caso_roto_rompe_una_sola_cosa(caso):
    """Un incumplimiento o un aviso, en uno o en los dos regímenes (D-5 añade R-23 en el simplificado)."""
    completo, simplificado = caso.esperado["completo"], caso.esperado["simplificado"]
    roto_c = completo["incumplimientos"] + completo["avisos"]
    roto_s = [r for r in simplificado["incumplimientos"] + simplificado["avisos"]]
    if caso.base is G.base_emergencia:
        roto_s = [r for r in roto_s if r != "R-23"]
    assert len(set(roto_c) | set(roto_s)) == 1 or caso.nombre.startswith("20-"), (roto_c, roto_s)


def _todos(campo):
    for caso in G.CASOS:
        for r in como_dict(informe(cargar_fichero(CORPUS / f"{caso.nombre}.json")))["regimenes"].values():
            yield from r[campo]


def test_el_corpus_produce_todos_los_incumplimientos_posibles():
    # R-01, R-04, R-08 y R-24 no pueden dar incumplimiento: la carga ya exige sus datos.
    posibles = {f"R-{n:02}" for n in range(1, 29)} - {"R-01", "R-04", "R-08", "R-24"}
    producidos = {r["id"] for r in _todos("requisitos") if r["estado"] == "incumplimiento"}
    assert producidos == posibles


def test_el_corpus_produce_todos_los_avisos_e_informativos():
    assert {a["codigo"] for a in _todos("avisos")} == {"A-01", "A-02"}
    assert {a["codigo"] for a in _todos("informativos")} == {"I-01", "I-02"}


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
