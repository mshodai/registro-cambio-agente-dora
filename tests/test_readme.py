"""La salida pegada en el README es la que da hoy la línea de órdenes."""

import re
from pathlib import Path

from registro_cambio.cli import main

RAIZ = Path(__file__).resolve().parent.parent


def test_la_salida_del_readme_es_la_real(capsys, monkeypatch):
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    bloque = re.search(r"```\n\$ registro-cambio-agente ([^\n]+)\n(.*?)\n```", readme, re.S)
    argumentos, pegada = bloque.group(1).split(), bloque.group(2)
    monkeypatch.chdir(RAIZ)
    codigo = main(argumentos)
    assert capsys.readouterr().out.rstrip("\n") == pegada
    assert codigo == 1
    assert "El código de salida es 1" in readme


def test_el_readme_enlaza_los_otros_cinco_repositorios():
    readme = (RAIZ / "README.md").read_text(encoding="utf-8")
    for repo in (
        "validador-cadena-verifactu",
        "calculo-titularidad-real",
        "plazos-conservacion-pbc",
        "plazos-actualizacion-pbc",
        "registro-examen-especial-pbc",
    ):
        assert f"https://github.com/mshodai/{repo}" in readme
