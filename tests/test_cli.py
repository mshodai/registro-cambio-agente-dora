"""La línea de órdenes registro-cambio-agente y sus códigos de salida."""

import json

import pytest

from ayudas import CORPUS, G
from registro_cambio.cli import main

LIMPIA = str(CORPUS / "01-base-limpia.json")
D5 = str(CORPUS / "20-emergencia-bien-registrada-art-37-b-simplificado-d-5.json")
LECTURA = str(CORPUS / "31-art-37-b-aviso-d-4-aprobacion-solo-por-un-agente.json")
AVISO = str(CORPUS / "41-modelo-7-3-aviso-sin-evidencias.json")


def test_codigo_0_sin_incumplimientos(capsys):
    assert main([LIMPIA]) == 0
    salida = capsys.readouterr().out
    assert "Régimen completo:" in salida and "Régimen simplificado:" in salida
    assert "Exige actuar: no." in salida


def test_los_avisos_no_cambian_el_codigo(capsys):
    assert main([AVISO]) == 0
    assert "Avisos (no son incumplimientos" in capsys.readouterr().out


def test_codigo_1_con_algun_incumplimiento(capsys):
    assert main([D5]) == 1
    assert "Exige actuar: sí." in capsys.readouterr().out


def test_codigo_1_con_un_aviso_de_lectura_propia(capsys):
    # Sin incumplimientos: el 1 lo activa el aviso A-03 de la D-4, y el informe lo dice.
    assert main([LECTURA]) == 1
    salida = capsys.readouterr().out
    assert "0 incumplimientos; 1 aviso de lectura propia." in salida
    assert "R-23 (lectura propia: D-4)" in salida
    assert "R-23 Aprobación: aviso (lectura propia)" in salida


def test_garantizado_por_la_validacion_de_entrada(capsys):
    main([LIMPIA])
    assert "R-01 Registro del cambio: cumple: garantizado por la validación de entrada" in capsys.readouterr().out


def test_el_regimen_es_un_parametro(capsys):
    # El mismo registro: sin incumplimientos en el completo, R-23 en el simplificado (D-5).
    assert main([D5, "--regimen", "completo"]) == 0
    assert "Régimen simplificado:" not in capsys.readouterr().out
    assert main([D5, "--regimen", "simplificado"]) == 1


def test_salida_json(capsys):
    assert main([D5, "--json"]) == 1
    datos = json.loads(capsys.readouterr().out)
    assert datos["regimenes"]["simplificado"]["incumplimientos"] == ["R-23"]
    assert all(r["cita"] for r in datos["regimenes"]["completo"]["requisitos"])
    assert datos["exige_actuar"] == {"valor": True, "activado_por": {"simplificado": [
        "R-23 (texto: Art. 37.b); art. 38.2; D-4; D-5)"
    ]}}


def test_codigo_2_entrada_no_valida(tmp_path, capsys):
    f = tmp_path / "e.json"
    f.write_text(json.dumps(G.base_limpia() | {"regimen": "completo"}), encoding="utf-8")
    assert main([str(f)]) == 2
    assert "ERR-01" in capsys.readouterr().out


def test_codigo_2_fichero_inexistente(tmp_path, capsys):
    assert main([str(tmp_path / "no.json")]) == 2
    assert "no existe" in capsys.readouterr().err


def test_codigo_2_regimen_desconocido():
    with pytest.raises(SystemExit) as e:
        main([LIMPIA, "--regimen", "otro"])
    assert e.value.code == 2
