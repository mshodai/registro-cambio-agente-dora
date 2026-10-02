# registro-cambio-agente-dora

Comprueba el registro de un cambio en un sistema de TIC en el que ha participado un agente de IA. Lo contrasta con dos regímenes:

- **completo:** el art. 9.4.e) de DORA y el art. 17 (con el 16) del Reglamento Delegado (UE) 2024/1774;
- **simplificado:** el título III del mismo Reglamento Delegado.

Cada resultado cita su artículo y letra. Es un cálculo bajo las lecturas que declara [`docs/modelo-datos.md`](docs/modelo-datos.md), no una determinación jurídica.

Versión 0.1.

## Instalación y uso

Hace falta Python 3.11 o posterior. No tiene dependencias externas. Desde la raíz del repositorio:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install .
registro-cambio-agente corpus/01-base-limpia.json
```

**Uso:** `registro-cambio-agente FICHERO [--regimen completo|simplificado] [--json]`

- **Régimen.** Es un parámetro del cálculo, no un dato de la entrada. Sin `--regimen` se calculan los dos.
- **Formato.** Con `--json`, el informe sale en JSON.

**Códigos de salida:**

- **1:** algún régimen calculado tiene algún incumplimiento: algo exige actuar.
- **0:** ningún incumplimiento. Puede haber avisos o datos informativos, que no cambian el código.
- **2:** el fichero no se puede leer, o la entrada no es válida (`ERR-01` a `ERR-05`, modelo §15).

## Qué da

Para cada requisito (R-01 a R-28), uno de estos resultados, con su cita:

- `cumple`: el registro tiene lo que el requisito pide.
- `incumplimiento`: falta algo o el registro lo contradice. Va con el motivo.
- `sin_indicio_de_incumplimiento`: solo en los requisitos que dependen de un mecanismo de la entidad (R-05 independencia, R-06 responsabilidades, R-22 controles contra la manipulación, R-26 procedimiento de emergencia). Un registro puede probar que el mecanismo falló en un cambio, pero no que existe. Por eso estos requisitos nunca dan `cumple` (D-1).
- `no_aplica`: el régimen no lo exige, o no se da la condición de la que depende. El motivo se dice siempre, y la cita remite al artículo del régimen que sí lo exige.

Aparte de los requisitos, el informe da dos cosas que no son incumplimientos:

- **Avisos:** A-01, autorrevisión de un agente (D-2), y A-02, falta de evidencias (modelo §7.3).
- **Datos informativos del régimen simplificado:** I-01, coincidencias de funciones sin requisito de independencia (D-1), e I-02, revisiones de código que el título III no exige (D-2).

## Documentación

- [`docs/modelo-datos.md`](docs/modelo-datos.md): la entrada, con la cita de cada campo y las decisiones D-1 a D-5.
- [`docs/dudas-implementacion.md`](docs/dudas-implementacion.md): las dudas encontradas al implementar (DI-1 a DI-11) y la lectura que aplica el código.
- [`corpus/README.md`](corpus/README.md): un caso por cada incumplimiento o aviso posible, con su resultado esperado. Se regeneran con `python corpus/generar.py`.
- [`docs/fuentes/FUENTES.md`](docs/fuentes/FUENTES.md): los textos oficiales y sus huellas.

## Tests

```sh
pip install pytest
pytest
```
