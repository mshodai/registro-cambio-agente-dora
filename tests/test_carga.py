"""Validación de la entrada (modelo, §15). No depende del régimen."""

import copy

from ayudas import G, carga_de, codigos
from registro_cambio.carga import cargar


def _base():
    return copy.deepcopy(G.base_limpia())


def test_la_base_es_valida():
    assert carga_de(_base()).valida


def test_json_mal_formado():
    assert codigos(cargar("{")) == ["ERR-01"]


def test_clave_repetida():
    assert codigos(cargar('{"version_modelo": 1, "version_modelo": 1}')) == ["ERR-01"]


def test_regimen_en_la_entrada():
    e = _base()
    e["regimen"] = "completo"
    carga = carga_de(e)
    assert codigos(carga) == ["ERR-01"]
    assert any(i.ruta == "regimen" for i in carga.errores)


def test_campo_desconocido():
    e = _base()
    e["cambio"]["prompt"] = "x"  # §0.2, regla 2: nada interno del agente.
    assert codigos(carga_de(e)) == ["ERR-01"]


def test_campo_obligatorio_ausente():
    e = _base()
    del e["cambio"]["vuelta_atras"]
    carga = carga_de(e)
    assert codigos(carga) == ["ERR-01"]
    assert any(i.ruta == "cambio.vuelta_atras" for i in carga.errores)


def test_version_distinta_de_1():
    e = _base()
    e["version_modelo"] = 2
    assert codigos(carga_de(e)) == ["ERR-01"]


def test_null_donde_no_se_admite():
    e = _base()
    e["cambio"]["implantacion"] = None
    assert codigos(carga_de(e)) == ["ERR-01"]


def test_fecha_sin_desfase_horario():
    e = _base()
    e["cambio"]["aprobacion"]["fecha"] = "2026-11-06T10:00:00"
    assert codigos(carga_de(e)) == ["ERR-01"]


def test_fecha_sin_hora():
    e = _base()
    e["cambio"]["aprobacion"]["fecha"] = "2026-11-06"
    assert codigos(carga_de(e)) == ["ERR-01"]


def test_valor_fuera_de_la_lista():
    e = _base()
    e["cambio"]["elementos"] = ["otro"]
    assert codigos(carga_de(e)) == ["ERR-01"]


def test_paso_sin_actores():
    # Modelo, §2: `actores` de un paso es una lista no vacía.
    e = _base()
    e["cambio"]["aprobacion"]["actores"] = []
    assert codigos(carga_de(e)) == ["ERR-01"]


def test_lista_vacia_fuera_de_un_paso_no_es_error():
    # Dudas, DI-8: la juzga su requisito.
    e = _base()
    e["cambio"]["elementos"] = []
    e["cambio"]["pruebas"][0]["realizada_por"] = []
    assert carga_de(e).valida


def test_id_repetido():
    e = _base()
    e["actores"].append(copy.deepcopy(e["actores"][0]))
    assert codigos(carga_de(e)) == ["ERR-02"]


def test_referencia_inexistente():
    e = _base()
    e["cambio"]["aprobacion"]["actores"] = ["P-9"]
    assert codigos(carga_de(e)) == ["ERR-03"]


def test_hallazgo_inexistente_en_el_plan():
    e = _base()
    e["cambio"]["revisiones_codigo"][0]["plan_accion"]["medidas"][0]["hallazgos"] = ["H-9"]
    assert codigos(carga_de(e)) == ["ERR-03"]


def test_persona_responsable_que_es_un_agente():
    e = _base()
    otro = copy.deepcopy(e["actores"][3])
    otro.update({"id": "AG-9", "persona_responsable": "AG-1"})
    e["actores"].append(otro)
    assert codigos(carga_de(e)) == ["ERR-04"]


def test_persona_con_campos_de_agente():
    e = _base()
    e["actores"][0]["modelo"] = "MODELO-EJEMPLO"
    assert codigos(carga_de(e)) == ["ERR-04"]


def test_agente_sin_sus_campos():
    e = _base()
    del e["actores"][3]["version"]
    assert codigos(carga_de(e)) == ["ERR-01"]


def test_fin_anterior_al_inicio():
    e = _base()
    e["cambio"]["implantacion"]["fin"] = "2026-11-09T08:00:00+01:00"
    assert codigos(carga_de(e)) == ["ERR-05"]


def test_se_recogen_todos_los_errores():
    e = _base()
    e["cambio"]["aprobacion"]["fecha"] = "mal"
    e["cambio"]["implantacion"]["resultado"] = "mal"
    assert len(carga_de(e).errores) == 2
