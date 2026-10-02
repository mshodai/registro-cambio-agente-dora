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
            assert re.search(r"art\.|D-\d|DI-\d|§", a.cita, re.I), (nombre, a)


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


def test_misma_funcion_da_sin_indicio_con_aviso_de_la_d_1():
    caso = next(c for c in G.CASOS if c.nombre.startswith("05-"))
    res = calcular(carga_de(caso.entrada()).entrada, COMPLETO)
    r05 = next(r for r in res.resultados if r.id == "R-05")
    assert r05.estado == "sin_indicio_de_incumplimiento"
    assert not any("Ninguna lectura lo salva" in n for n in r05.notas)
    (aviso,) = res.avisos_de_lectura
    assert aviso.requisito == "R-05" and "considerando 17" in aviso.lectura


def test_un_requisito_que_no_es_de_mecanismo_da_aviso():
    caso = next(c for c in G.CASOS if c.nombre.startswith("31-"))
    for regimen in (COMPLETO, SIMPLIFICADO):
        res = calcular(carga_de(caso.entrada()).entrada, regimen)
        r23 = next(r for r in res.resultados if r.id == "R-23")
        assert r23.estado == "aviso" and r23.motivos[0].startswith("Con la lectura D-4")
        assert [a.lectura for a in res.avisos_de_lectura] == ["D-4"]
        assert res.activadores == ("R-23 (lectura propia: D-4)",)


def test_los_garantizados_dicen_que_los_garantiza_la_carga():
    res = calcular(carga_de(G.base_limpia()).entrada, COMPLETO)
    garantizados = {r.id for r in res.resultados if r.garantizado}
    assert garantizados == {"R-01", "R-04", "R-08", "R-24"}
    for r in res.resultados:
        if r.garantizado:
            assert r.estado == "cumple" and r.motivos == ("Garantizado por la validación de entrada.",)


def test_d_5_la_nota_de_emergencia_va_en_la_aprobacion_del_simplificado():
    entrada = carga_de(G.base_emergencia()).entrada
    r23 = next(r for r in calcular(entrada, SIMPLIFICADO).resultados if r.id == "R-23")
    # Art. 37.b) literal: incumplimiento; la D-5 documenta la lectura alternativa en una nota.
    assert r23.estado == "incumplimiento" and any("D-5" in n for n in r23.notas)
    r23c = next(r for r in calcular(entrada, COMPLETO).resultados if r.id == "R-23")
    assert r23c.estado == NO_APLICA


def test_regimen_desconocido():
    with pytest.raises(ValueError):
        calcular(carga_de(G.base_limpia()).entrada, "otro")
