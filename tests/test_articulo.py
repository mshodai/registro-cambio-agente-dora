"""Los ejemplos del artículo (docs/index.md) son reproducibles.

- Cada ejemplo de docs/ejemplos/ da el resultado esperado escrito a mano en su
  `.esperado.json`.
- Cada ejemplo difiere del caso del corpus del que parte solo en lo que dice.
- Lo que el artículo cita de la salida de la orden es la salida real: cada línea
  aparece en el mismo orden, y dos líneas seguidas en el artículo son seguidas
  en la salida, salvo que las separe «[...]». Una línea que acaba en « [...]»
  está recortada: cuenta como prefijo.
"""

import copy
import json
import re

import pytest

from ayudas import G, RAIZ
from registro_cambio.carga import cargar_fichero
from registro_cambio.cli import main
from registro_cambio.salida import como_dict, informe

EJEMPLOS = RAIZ / "docs" / "ejemplos"
ARTICULO = (RAIZ / "docs" / "index.md").read_text(encoding="utf-8")
URL = "https://github.com/mshodai/registro-cambio-agente-dora/blob/main/"

# Lo que cambia cada ejemplo respecto del caso del corpus del que parte.
DIFERENCIAS = {
    "sin-revision": lambda c: c.update(revisiones_codigo=[]),
    "flujo": lambda c: c["solicitud"].update(actores=["P-3"]),
}


def _esperado(nombre):
    return json.loads((EJEMPLOS / f"{nombre}.esperado.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("nombre", sorted(DIFERENCIAS))
def test_cada_ejemplo_da_su_resultado_esperado(nombre):
    obtenido = G.resumen(como_dict(informe(cargar_fichero(EJEMPLOS / f"{nombre}.json"))))
    assert obtenido == _esperado(nombre)["resultado"]


@pytest.mark.parametrize("nombre", sorted(DIFERENCIAS))
def test_cada_ejemplo_solo_cambia_lo_que_dice(nombre):
    origen = json.loads((RAIZ / _esperado(nombre)["parte_de"]).read_text(encoding="utf-8"))
    esperado = copy.deepcopy(origen)
    DIFERENCIAS[nombre](esperado["cambio"])
    assert esperado != origen
    assert json.loads((EJEMPLOS / f"{nombre}.json").read_text(encoding="utf-8")) == esperado


BLOQUES = re.findall(r"```\n\$ registro-cambio-agente (\S+)\n(.*?)\n```", ARTICULO, re.S)


def test_el_articulo_cita_los_dos_ejemplos():
    assert sorted(f for f, _ in BLOQUES) == ["docs/ejemplos/flujo.json", "docs/ejemplos/sin-revision.json"]
    for nombre in DIFERENCIAS:
        assert f"{URL}docs/ejemplos/{nombre}.json" in ARTICULO
        assert f"{URL}docs/ejemplos/{nombre}.esperado.json" in ARTICULO
        assert f"{URL}{_esperado(nombre)['parte_de']}" in ARTICULO


@pytest.mark.parametrize("fichero,citada", BLOQUES, ids=[f for f, _ in BLOQUES])
def test_lo_que_cita_el_articulo_es_la_salida_real(fichero, citada, capsys, monkeypatch):
    monkeypatch.chdir(RAIZ)
    codigo = main([fichero])
    real = capsys.readouterr().out.splitlines()
    assert codigo == 1
    i, seguida = 0, False
    for linea in citada.splitlines():
        if linea == "[...]":
            seguida = False
            continue
        prefijo = linea.removesuffix(" [...]")
        recortada = prefijo != linea
        j = next(
            (k for k in range(i, len(real)) if (real[k].startswith(prefijo) if recortada else real[k] == linea)),
            None,
        )
        assert j is not None, f"no está en la salida real, o no en este orden: {linea}"
        assert not seguida or j == i, f"falta «[...]» antes de: {linea}"
        i, seguida = j + 1, True
