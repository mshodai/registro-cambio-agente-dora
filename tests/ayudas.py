"""Utilidades comunes de los tests.

Las entradas de prueba parten del corpus (corpus/generar.py), que a su vez
parte de los ejemplos de docs/modelo-datos.md. Todos los datos son inventados
(modelo, §0.2, regla 3).
"""

import importlib.util
import json
from pathlib import Path

from registro_cambio.carga import cargar

RAIZ = Path(__file__).resolve().parent.parent
CORPUS = RAIZ / "corpus"

_spec = importlib.util.spec_from_file_location("generar", CORPUS / "generar.py")
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)


def carga_de(datos):
    return cargar(json.dumps(datos, ensure_ascii=False))


def codigos(carga):
    return sorted({e.codigo for e in carga.errores})
