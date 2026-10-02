"""Propiedades del cálculo que valen para todo el corpus.

- Cada resultado cita su artículo, también los que no aplican.
- Los requisitos que dependen de un mecanismo de la entidad nunca dan «cumple» (D-1).
- Lo que no aplica en un régimen lo dice, con su motivo.
- El régimen es un parámetro: el mismo registro se calcula con los dos.
"""

import re

import pytest

from ayudas import CORPUS, G, carga_de
from registro_cambio.calculo import CATALOGO, COMPLETO, ESTADOS, NO_APLICA, SIMPLIFICADO, calcular
from registro_cambio.carga import cargar_fichero

CITA = re.compile(r"\b(art|arts)\. \d+|considerando \d+|DORA, art\.", re.I)
MECANISMO = {r.id for r in CATALOGO if r.mecanismo}


def _resultados():
    for caso in G.CASOS:
        entrada = cargar_fichero(CORPUS / f"{caso.nombre}.json").entrada
        for regimen in (COMPLETO, SIMPLIFICADO):
            res = calcular(entrada, regimen)
            yield caso.nombre, regimen, res


def test_el_catalogo_tiene_28_requisitos_con_cita_en_algun_regimen():
    assert [r.id for r in CATALOGO] == [f"R-{n:02}" for n in range(1, 29)]
    for r in CATALOGO:
        assert r.cita[COMPLETO] or r.cita[SIMPLIFICADO]


def test_los_requisitos_de_mecanismo_son_los_del_modelo():
    # Modelo, §0.3: letras b), c) y f) del art. 17.1, y los arts. 16.1.c) y 37.c).
    assert MECANISMO == {"R-05", "R-06", "R-22", "R-26"}


def test_cada_resultado_cita_su_articulo():
    for nombre, regimen, res in _resultados():
        for r in res.resultados:
            assert r.estado in ESTADOS
            assert CITA.search(r.cita), (nombre, regimen, r.id, r.cita)
        for a in res.avisos + res.informativos:
            assert re.search(r"art\.|D-\d|§", a.cita), (nombre, a)


def test_un_requisito_de_mecanismo_nunca_da_cumple():
    vistos = set()
    for nombre, regimen, res in _resultados():
        for r in res.resultados:
            if r.id in MECANISMO:
                assert r.estado != "cumple", (nombre, regimen, r.id)
                vistos.add(r.estado)
    assert {"incumplimiento", "sin_indicio_de_incumplimiento"} <= vistos


def test_lo_que_no_aplica_dice_por_que():
    for nombre, regimen, res in _resultados():
        for r in res.resultados:
            if r.estado == NO_APLICA:
                assert r.motivos and all(m.strip() for m in r.motivos), (nombre, regimen, r.id)


def test_lo_que_el_titulo_iii_no_tiene_no_aplica_en_el_simplificado():
    entrada = carga_de(G.base_limpia()).entrada
    res = {r.id: r for r in calcular(entrada, SIMPLIFICADO).resultados}
    sin_base = {r.id for r in CATALOGO if r.cita[SIMPLIFICADO] is None}
    assert sin_base == {
        "R-02", "R-04", "R-05", "R-06", "R-07", "R-08", "R-09", "R-10", "R-11",
        "R-15", "R-16", "R-17", "R-18", "R-19", "R-20", "R-21", "R-25", "R-26", "R-27",
    }
    for id_ in sin_base:
        assert res[id_].estado == NO_APLICA
        assert "título III" in res[id_].motivos[0]
        assert "solo régimen completo" in res[id_].cita


def test_el_cambio_importante_solo_se_exige_en_el_simplificado():
    entrada = carga_de(G.base_limpia()).entrada
    r13 = next(r for r in calcular(entrada, COMPLETO).resultados if r.id == "R-13")
    assert r13.estado == NO_APLICA and "Art. 31.1.e)" in r13.cita


def test_sin_indicio_dice_que_el_registro_no_prueba_el_mecanismo():
    entrada = carga_de(G.base_limpia()).entrada
    r05 = next(r for r in calcular(entrada, COMPLETO).resultados if r.id == "R-05")
    assert r05.estado == "sin_indicio_de_incumplimiento"
    assert any("no puede probar" in n for n in r05.notas)


def test_misma_funcion_depende_de_la_lectura_del_considerando():
    caso = next(c for c in G.CASOS if c.nombre.startswith("05-"))
    r05 = next(r for r in calcular(carga_de(caso.entrada()).entrada, COMPLETO).resultados if r.id == "R-05")
    assert r05.estado == "incumplimiento"
    assert any("considerando 17" in n for n in r05.notas)
    assert not any("Ninguna lectura lo salva" in n for n in r05.notas)


def test_d_5_la_nota_de_emergencia_va_en_la_aprobacion_del_simplificado():
    entrada = carga_de(G.base_emergencia()).entrada
    r23 = next(r for r in calcular(entrada, SIMPLIFICADO).resultados if r.id == "R-23")
    assert r23.estado == "incumplimiento" and any("D-5" in n for n in r23.notas)
    r23c = next(r for r in calcular(entrada, COMPLETO).resultados if r.id == "R-23")
    assert r23c.estado == NO_APLICA


def test_regimen_desconocido():
    with pytest.raises(ValueError):
        calcular(carga_de(G.base_limpia()).entrada, "otro")
