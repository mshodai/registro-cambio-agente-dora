# registro-cambio-agente-dora

Comprueba el registro de un cambio en un sistema de TIC en el que ha participado un agente de IA. Lo contrasta con dos regímenes:

- **completo:** el art. 9.4.e) de DORA y el art. 17 (con el 16) del Reglamento Delegado (UE) 2024/1774;
- **simplificado:** el título III del mismo Reglamento Delegado.

Cada resultado cita su artículo y letra. Es un cálculo bajo las lecturas que declara [`docs/modelo-datos.md`](docs/modelo-datos.md), no una determinación jurídica.

Versión 0.1. Solo da «incumplimiento» cuando lo sostiene el texto. Lo que solo sostiene una lectura propia del modelo es un aviso que remite a ella.

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

- **1:** algo exige actuar en algún régimen calculado. Puede ser un incumplimiento, que sostiene el texto de la norma, o un aviso de lectura propia (A-03), que dice que con esa lectura falta algo. Es el criterio de la serie: alguna lectura exige actuar. El informe dice qué activó el 1.
- **0:** nada exige actuar. Puede haber avisos A-01 o A-02 o datos informativos, que no cambian el código.
- **2:** el fichero no se puede leer, o la entrada no es válida (`ERR-01` a `ERR-05`, modelo §15).

## Qué da

Para cada requisito (R-01 a R-28), uno de estos resultados, con su cita:

- `cumple`: el registro tiene lo que el requisito pide. En R-01, R-04, R-08 y R-24 sale como «cumple: garantizado por la validación de entrada», porque la carga ya exige sus datos.
- `incumplimiento`: falta algo o el registro lo contradice, **y lo sostiene el texto de la norma** aplicado al registro (modelo §0.1 bis). Va con el motivo.
- `aviso`: el texto no sostiene un incumplimiento, pero una lectura propia (una decisión D-n del modelo, otra decisión propia o una duda DI-n) dice que falta algo. Va con un aviso A-03 que remite a esa lectura.
- `sin_indicio_de_incumplimiento`: solo en los requisitos que dependen de un mecanismo de la entidad (R-05 independencia, R-06 responsabilidades, R-22 controles contra la manipulación, R-26 procedimiento de emergencia). Un registro puede probar que el mecanismo falló en un cambio, pero no que existe. Por eso estos requisitos nunca dan `cumple` (D-1). Si solo fallan por una lectura propia, dan este resultado con su aviso A-03.
- `no_aplica`: el régimen no lo exige, o no se da la condición de la que depende. El motivo se dice siempre, y la cita remite al artículo del régimen que sí lo exige.

Aparte de los requisitos, el informe da dos cosas que no son incumplimientos:

- **Avisos:**
  - A-01: autorrevisión de un agente (D-2);
  - A-02: faltan evidencias (modelo §7.3);
  - A-03: con una lectura propia falta algo. Lleva el requisito y la lectura, y activa el código 1.
- **Datos informativos del régimen simplificado:** I-01, coincidencias de funciones sin requisito de independencia (D-1), e I-02, revisiones de código que el título III no exige (D-2).

## Documentación

- [`docs/modelo-datos.md`](docs/modelo-datos.md): la entrada, con la cita de cada campo y las decisiones D-1 a D-5.
- [`docs/dudas-implementacion.md`](docs/dudas-implementacion.md): las dudas encontradas al implementar (DI-1 a DI-11), qué hace el código con cada una y cómo se aplica el principio del §0.1 bis.
- [`corpus/README.md`](corpus/README.md): un caso por cada incumplimiento o aviso posible, con su resultado esperado. Se regeneran con `python corpus/generar.py`.
- [`docs/fuentes/FUENTES.md`](docs/fuentes/FUENTES.md): los textos oficiales y sus huellas.

## Tests

```sh
pip install pytest
pytest
```
