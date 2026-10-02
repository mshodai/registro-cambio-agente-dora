"""Línea de órdenes: registro-cambio-agente FICHERO [--regimen R] [--json]."""

import argparse
import sys

from registro_cambio.calculo import REGIMENES
from registro_cambio.carga import cargar_fichero
from registro_cambio.salida import codigo_de_salida, como_json, informe, texto

EPILOG = (
    "códigos de salida: 1 si algo exige actuar en algún régimen calculado: un incumplimiento que sostiene el "
    "texto, o un aviso de lectura propia (A-03) que dice que con esa lectura falta algo; 0 si nada lo exige, "
    "aunque haya avisos A-01 o A-02 o datos informativos; 2 si el fichero no se puede leer o la entrada no es "
    "válida."
)


class _Formato(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        return super().add_usage(usage, actions, groups, prefix or "uso: ")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="registro-cambio-agente",
        description=(
            "Comprueba el registro de un cambio en un sistema de TIC en el que ha participado un agente de IA "
            "frente al art. 17 del Reglamento Delegado (UE) 2024/1774 (régimen completo) y su título III "
            "(régimen simplificado). Cada resultado cita su artículo. Es un cálculo bajo las lecturas que declara "
            "docs/modelo-datos.md, no una determinación jurídica."
        ),
        epilog=EPILOG,
        formatter_class=_Formato,
        add_help=False,
    )
    argumentos = parser.add_argument_group("argumentos")
    argumentos.add_argument("fichero", help="fichero JSON con el registro (docs/modelo-datos.md)")
    opciones = parser.add_argument_group("opciones")
    opciones.add_argument("-h", "--help", action="help", help="muestra esta ayuda y termina")
    opciones.add_argument(
        "--regimen",
        choices=REGIMENES,
        help="calcula solo ese régimen; sin esta opción se calculan los dos",
    )
    opciones.add_argument("--json", action="store_true", help="emite el informe en JSON en lugar de texto")
    args = parser.parse_args(argv)  # un uso incorrecto termina con código 2 (argparse)

    try:
        carga = cargar_fichero(args.fichero)
    except FileNotFoundError:
        return _error(parser, f"no existe el fichero {args.fichero}")
    except IsADirectoryError:
        return _error(parser, f"{args.fichero} es un directorio")
    except UnicodeDecodeError:
        return _error(parser, f"el fichero {args.fichero} no está codificado en UTF-8")
    except OSError as e:
        return _error(parser, f"no se puede leer el fichero {args.fichero}: {e.strerror}")

    inf = informe(carga, (args.regimen,) if args.regimen else REGIMENES)
    print(como_json(inf) if args.json else texto(inf), end="\n" if args.json else "")
    return codigo_de_salida(inf)


def _error(parser, mensaje):
    print(f"{parser.prog}: error: {mensaje}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
