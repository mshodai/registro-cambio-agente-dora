# Fuentes

Documentos que usa el proyecto. Los PDF no se redistribuyen (están en `.gitignore`), así que cada uno debe descargarse de su URL y guardarse en `docs/fuentes/` con el nombre indicado.

Son tres textos publicados en el Diario Oficial de la Unión Europea, que son los auténticos:

- **Reglamento (UE) 2022/2554** («DORA»), sobre la resiliencia operativa digital del sector financiero. Su art. 15 encarga a las autoridades europeas de supervisión las normas técnicas que desarrollan la gestión del riesgo de TIC del régimen completo. Su art. 16 regula el marco simplificado y, en su apartado 3, las normas técnicas de ese régimen.
- **Reglamento Delegado (UE) 2024/1774**, que contiene esas normas técnicas. El registro del cambio que valida este proyecto se contrasta con:
  - el **art. 17**, «Gestión de cambios en las TIC», del título II (régimen completo);
  - el **título III**, «Marco simplificado de gestión del riesgo relacionado con las TIC a que se refiere el artículo 16, apartado 1, del Reglamento (UE) 2022/2554» (arts. 28 a 41).
- **Corrección de errores del Reglamento Delegado (UE) 2024/1774** en su versión española (DO L 2025/90420, de 15.5.2025).

**Versiones consolidadas.** Ninguno de los dos reglamentos tiene una versión consolidada que incorpore modificaciones. Se comprobó el 2026-10-02 con la misma consulta SPARQL al [Cellar](https://publications.europa.eu/webapi/rdf/sparql) de la Oficina de Publicaciones que usa `vigilancia-fuentes` (`consulta_cellar` en `vigilancia_fuentes.py`):

- **Una sola versión consolidada por reglamento.** El Cellar solo da una para cada uno: `02022R2554-20221227` para DORA y `02024R1774-20240625` para el Reglamento Delegado. Las dos llevan la fecha de publicación del original en el Diario Oficial. Es la versión consolidada inicial, que coincide con el propio texto original. Por eso no se ha descargado: se cita el original, y `vigilancia-fuentes` sigue vigilando el acto a través de él. Si aparece una versión consolidada posterior, la tratará como un cambio.
- **Sin actos modificativos.** El Cellar no registra ningún acto que modifique a ninguno de los dos (`cdm:resource_legal_amends_resource_legal`).
- **Rectificaciones no incorporadas.** Sí registra rectificaciones (`cdm:resource_legal_corrects_resource_legal`), que no están incorporadas a ninguna versión consolidada:
  - DORA: nueve, de `32022R2554R(01)` a `32022R2554R(09)`. Según el Cellar, **ninguna tiene versión en español**. Afectan a otras versiones lingüísticas y no se han descargado.
  - Reglamento Delegado: dos, `32024R1774R(01)` y `32024R1774R(02)`. Solo la segunda tiene versión en español, y se recoge más abajo como fuente propia.
- **Las versiones consolidadas no tienen efecto jurídico por sí solas.** EUR-Lex las publica como instrumento de documentación. El texto vinculante es el publicado en el Diario Oficial, junto con sus correcciones de errores. Si en el futuro se cita una versión consolidada, cada cita que importe deberá contrastarse con el original y con los actos que la modifiquen.

**Qué significa cada columna:**

- **Autor.** Órgano emisor, tal como figura en la cabecera del documento. Entre paréntesis, el autor del PDF según sus metadatos (`pdfinfo`).
- **Versión o fecha declarada.** Copiada literalmente del documento.
- **Fecha de descarga.** Los tres PDF se descargaron con el navegador el 2026-10-02 (`kMDItemDateAdded`). Los metadatos de origen de macOS (`kMDItemWhereFroms`) solo guardan el dominio, `https://eur-lex.europa.eu/`, no la URL completa.
- **URL.** Enlace de descarga del PDF en EUR-Lex. El 2026-10-02, las descargas automáticas con `curl` de esas mismas URL fallaron dos veces seguidas: EUR-Lex respondió `202` con un cuerpo vacío. Por eso las URL no se han comprobado por descarga automática. Cada PDF descargado con el navegador declara en su texto el acto que es (título, número y DO), y eso sí se ha comprobado.

## Documentos

| Fichero | Título | Autor | Versión o fecha declarada | Descarga | URL |
|---|---|---|---|---|---|
| `CELEX_32022R2554_ES_TXT.pdf` | Reglamento (UE) 2022/2554 del Parlamento Europeo y del Consejo, de 14 de diciembre de 2022, sobre la resiliencia operativa digital del sector financiero y por el que se modifican los Reglamentos (CE) n.º 1060/2009, (UE) n.º 648/2012, (UE) n.º 600/2014, (UE) n.º 909/2014 y (UE) 2016/1011 (DORA) | Parlamento Europeo y Consejo (metadatos: «Publications Office») | **Texto original, auténtico.** «DO L 333/1», «27.12.2022». Art. 64: «Será aplicable a partir del 17 de enero de 2025». Última versión consolidada según el Cellar: `02022R2554-20221227`, que coincide con este texto | 2026-10-02 | https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32022R2554 · ELI: http://data.europa.eu/eli/reg/2022/2554/oj |
| `CELEX_32024R1774_ES_TXT.pdf` | Reglamento Delegado (UE) 2024/1774 de la Comisión, de 13 de marzo de 2024, por el que se completa el Reglamento (UE) 2022/2554 del Parlamento Europeo y del Consejo en lo que respecta a las normas técnicas de regulación que especifican las herramientas, métodos, procesos y políticas de gestión del riesgo relacionado con las TIC y el marco simplificado de gestión del riesgo relacionado con las TIC | Comisión Europea (metadatos: «Oficina de Publicaciones de la Unión Europea, 2985 Luxemburgo») | **Texto original, auténtico.** «Serie L», «2024/1774», «25.6.2024». Art. 42: entra en vigor «a los veinte días de su publicación». No incorpora la corrección de errores de la fila siguiente. Última versión consolidada según el Cellar: `02024R1774-20240625`, que coincide con este texto | 2026-10-02 | https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32024R1774 · ELI: http://data.europa.eu/eli/reg_del/2024/1774/oj |
| `CELEX_32024R1774R(02)_ES_TXT.pdf` | Corrección de errores del Reglamento Delegado (UE) 2024/1774 de la Comisión, de 13 de marzo de 2024, [...] (Diario Oficial de la Unión Europea L, 2024/1774, 25 de junio de 2024) | Comisión Europea (metadatos: «Oficina de Publicaciones de la Unión Europea, 2985 Luxemburgo») | **Texto auténtico.** «Serie L», «2025/90420», «15.5.2025». Una página | 2026-10-02 | https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32024R1774R(02) · ELI: http://data.europa.eu/eli/reg_del/2024/1774/corrigendum/2025-05-15/oj |

**Qué corrige la corrección de errores de 15.5.2025.** Corrige una sola disposición: el **art. 22**, «Política de gestión de incidentes relacionados con las TIC», letra d), párrafo primero (página 23 del DO). Cambia la remisión al Reglamento Delegado (UE) 2024/1772, que en el original estaba incompleta:

- donde dice: «de conformidad con el [artículo [15] del Reglamento Delegado (UE) 2024/1772 de la Comisión (12)»;
- debe decir: «de conformidad con el artículo 8, apartado 2, del Reglamento Delegado (UE) 2024/1772 de la Comisión (12)».

El art. 22 pertenece al título II (régimen completo), capítulo III, «Detección de incidentes relacionados con las TIC y respuesta a tales incidentes». **La corrección no toca el art. 16, el art. 17 ni ningún artículo del título III (régimen simplificado, arts. 28 a 41).** Para lo que valida este proyecto, el texto original publicado el 25.6.2024 es el vigente sin cambios.

**Casos que este documento no resuelve:**

- **Corrección de errores sin vigilancia automática.** `vigilancia-fuentes` no la puede comprobar como acto de EUR-Lex. Con la URL citada (`uri=CELEX:32024R1774R(02)`), su función `acto_eurlex` no la reconoce como acto, porque el sufijo `R(02)` no encaja en el patrón de CELEX. Con la otra URL de EUR-Lex (`uri=OJ:L_202590420`), el Cellar sí la encuentra, pero no le da fecha de entrada en vigor. En los dos casos el script la dará como «no comprobable». Se cita la URL por CELEX porque es la que corresponde al nombre del fichero. Este repositorio no modifica `vigilancia-fuentes`.
- **Repositorio no vigilado aún.** `vigilancia-fuentes` vigila por defecto cinco repositorios, y este no está entre ellos. Hasta que se añada, sus fuentes solo se vigilan si se ejecuta el script pasando este repositorio de forma explícita.
- **Dos fechas de entrada en vigor de DORA.** El Cellar da dos: 2023-01-16 y 2025-01-17. La primera es la entrada en vigor del art. 64 («a los veinte días de su publicación»). La segunda coincide con la fecha de aplicación. No se ha investigado por qué el Cellar registra las dos. `vigilancia-fuentes` toma la menor.
- **Rectificaciones de DORA en otras lenguas.** Las nueve rectificaciones de DORA no tienen versión en español según el Cellar. No se ha comprobado su contenido.

## Huellas SHA-256

Sirven para comprobar que una copia local es la misma versión con la que se hizo el análisis. Los tres son textos publicados en el Diario Oficial, que no cambian. Una huella distinta indica una copia distinta, no una versión nueva del acto. Las versiones nuevas se detectan por el Cellar, como se explica arriba.

```
e6e60fe523d57e78b3db174fe0c9a8b478a4b6bd93a92dccfce5cc742f2c0da8  CELEX_32022R2554_ES_TXT.pdf
6e3125c73200422b4fb5b2bb7c9c47c5611de3fbd07fd1d7b1822b4442d76576  CELEX_32024R1774_ES_TXT.pdf
78e89e78d7a92d2a1ffd9c68457e69afc6f75a7d24a4e0ee654f7f30910f80d2  CELEX_32024R1774R(02)_ES_TXT.pdf
```

Para comprobarlas: `cd docs/fuentes && shasum -a 256 -c` pegando el bloque anterior en la entrada estándar.

## Datos para la vigilancia automática

Repite en formato legible por máquina el fichero, la URL de descarga y la huella SHA-256 de cada documento de las secciones anteriores. Lo lee el script de `vigilancia-fuentes`, que comprueba que coincida con el texto. Si difieren, prevalece el texto.

```json
{
  "documentos": [
    {
      "fichero": "CELEX_32022R2554_ES_TXT.pdf",
      "url": "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32022R2554",
      "sha256": "e6e60fe523d57e78b3db174fe0c9a8b478a4b6bd93a92dccfce5cc742f2c0da8"
    },
    {
      "fichero": "CELEX_32024R1774_ES_TXT.pdf",
      "url": "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32024R1774",
      "sha256": "6e3125c73200422b4fb5b2bb7c9c47c5611de3fbd07fd1d7b1822b4442d76576"
    },
    {
      "fichero": "CELEX_32024R1774R(02)_ES_TXT.pdf",
      "url": "https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32024R1774R(02)",
      "sha256": "78e89e78d7a92d2a1ffd9c68457e69afc6f75a7d24a4e0ee654f7f30910f80d2"
    }
  ]
}
```
