"""Los tres ejemplos de docs/modelo-datos.md son entradas válidas y dan lo que dice el modelo.

Los ejemplos se leen del propio documento, así que un cambio en el modelo que
rompa un ejemplo se ve aquí.
"""

from ayudas import G, carga_de
from registro_cambio.salida import como_dict, informe

EJEMPLOS = G.ejemplos_del_modelo()


def _resumen(nombre):
    carga = carga_de(EJEMPLOS[nombre])
    assert carga.valida, carga.errores
    return G.resumen(como_dict(informe(carga)))


def test_hay_tres_ejemplos():
    assert set(EJEMPLOS) == {"1.1", "1.2", "D-1"}


def test_ejemplo_1_1_cambio_ordinario():
    # §1.1: sin incumplimientos; la revisión RC-1 la hace el agente que implanta:
    # aviso de autorrevisión en el completo (D-2, punto 4). En el simplificado, la
    # revisión de código es informativa (D-2, punto 5).
    assert _resumen("1.1") == {
        "completo": {"incumplimientos": [], "avisos": ["A-01"], "informativos": []},
        "simplificado": {"incumplimientos": [], "avisos": [], "informativos": ["I-02"]},
        "codigo_salida": 0,
    }


def test_ejemplo_1_2_parche_de_emergencia():
    # §1.2: sin incumplimientos en el completo; en el simplificado, R-23 por el art. 37.b)
    # literal, que es lo que el ejemplo muestra (D-5). El modelo corrigió el ejemplo:
    # ya no hereda una verificación anterior a la implantación (dudas, DI-7).
    assert _resumen("1.2") == {
        "completo": {"incumplimientos": [], "avisos": ["A-01"], "informativos": []},
        "simplificado": {"incumplimientos": ["R-23"], "avisos": [], "informativos": ["I-02"]},
        "codigo_salida": 1,
    }


def test_ejemplo_d_1_misma_persona_solicita_y_aprueba():
    # D-1: incumplimiento en el completo (lo sostiene el texto: es el mismo actor);
    # dato informativo en el simplificado.
    assert _resumen("D-1") == {
        "completo": {"incumplimientos": ["R-05"], "avisos": ["A-01"], "informativos": []},
        "simplificado": {"incumplimientos": [], "avisos": [], "informativos": ["I-01", "I-02"]},
        "codigo_salida": 1,
    }
    completo = como_dict(informe(carga_de(EJEMPLOS["D-1"])))["regimenes"]["completo"]
    r05 = next(r for r in completo["requisitos"] if r["id"] == "R-05")
    assert any("Ninguna lectura lo salva" in n for n in r05["notas"])
    assert any("P-2 aprueba" in m and "también solicita" in m for m in r05["motivos"])
