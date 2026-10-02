"""El informe: lo que se muestra en texto o en JSON.

`informe` junta la carga y el cálculo de los regímenes pedidos. El código de
salida es 1 si algún régimen calculado tiene algún incumplimiento: algo exige
actuar. Los avisos y los datos informativos no lo cambian.
"""

import json
from dataclasses import dataclass

from registro_cambio.calculo import (
    CUMPLE,
    INCUMPLIMIENTO,
    NO_APLICA,
    REGIMENES,
    SIN_INDICIO,
    ResultadoRegimen,
    calcular,
)
from registro_cambio.modelo import ResultadoCarga

AVISO_LEGAL = (
    "Resultado de un cálculo bajo las lecturas que declara docs/modelo-datos.md, no una determinación jurídica. "
    "Las decisiones propias se citan como D-n y las dudas de implementación como DI-n."
)

ETIQUETAS = {
    CUMPLE: "cumple",
    INCUMPLIMIENTO: "INCUMPLIMIENTO",
    SIN_INDICIO: "sin indicio de incumplimiento",
    NO_APLICA: "no aplica",
}


@dataclass(frozen=True)
class Informe:
    carga: ResultadoCarga
    regimenes: tuple[ResultadoRegimen, ...]

    @property
    def valida(self) -> bool:
        return self.carga.valida

    @property
    def exige_actuar(self) -> bool:
        return any(r.incumplimientos for r in self.regimenes)


def informe(carga: ResultadoCarga, regimenes=REGIMENES) -> Informe:
    if not carga.valida:
        return Informe(carga, ())
    return Informe(carga, tuple(calcular(carga.entrada, r) for r in regimenes))


def codigo_de_salida(inf: Informe) -> int:
    if not inf.valida:
        return 2
    return 1 if inf.exige_actuar else 0


def _aviso_dict(a):
    return {"codigo": a.codigo, "mensaje": a.mensaje, "cita": a.cita}


def como_dict(inf: Informe) -> dict:
    if not inf.valida:
        return {
            "valida": False,
            "errores": [{"codigo": e.codigo, "mensaje": e.mensaje, "ruta": e.ruta} for e in inf.carga.errores],
            "codigo_salida": codigo_de_salida(inf),
        }
    return {
        "valida": True,
        "cambio": inf.carga.entrada.cambio.id,
        "regimenes": {
            r.regimen: {
                "requisitos": [
                    {
                        "id": res.id,
                        "nombre": res.nombre,
                        "estado": res.estado,
                        "cita": res.cita,
                        "motivos": list(res.motivos),
                        "notas": list(res.notas),
                    }
                    for res in r.resultados
                ],
                "incumplimientos": [res.id for res in r.incumplimientos],
                "avisos": [_aviso_dict(a) for a in r.avisos],
                "informativos": [_aviso_dict(a) for a in r.informativos],
            }
            for r in inf.regimenes
        },
        "exige_actuar": inf.exige_actuar,
        "codigo_salida": codigo_de_salida(inf),
    }


def como_json(inf: Informe) -> str:
    return json.dumps(como_dict(inf), ensure_ascii=False, indent=2)


def texto(inf: Informe) -> str:
    if not inf.valida:
        lineas = ["La entrada no es válida (docs/modelo-datos.md, §15):"]
        for e in inf.carga.errores:
            lineas.append(f"  {e.codigo} {e.ruta + ': ' if e.ruta else ''}{e.mensaje}")
        return "\n".join(lineas) + "\n"
    lineas = [f"Cambio {inf.carga.entrada.cambio.id}", "", AVISO_LEGAL]
    for r in inf.regimenes:
        lineas += ["", f"Régimen {r.regimen}:"]
        n = len(r.incumplimientos)
        lineas.append(f"  {n} incumplimiento{'s' if n != 1 else ''}.")
        for res in r.resultados:
            lineas.append(f"  {res.id} {res.nombre}: {ETIQUETAS[res.estado]} — {res.cita}")
            for m in res.motivos:
                lineas.append(f"      {m}")
            for nota in res.notas:
                lineas.append(f"      Nota: {nota}")
        if r.avisos:
            lineas.append("  Avisos (no son incumplimientos):")
            lineas += [f"    {a.codigo} {a.mensaje} ({a.cita})" for a in r.avisos]
        if r.informativos:
            lineas.append("  Datos informativos:")
            lineas += [f"    {a.codigo} {a.mensaje} ({a.cita})" for a in r.informativos]
    lineas += ["", f"Exige actuar: {'sí' if inf.exige_actuar else 'no'}."]
    return "\n".join(lineas) + "\n"
