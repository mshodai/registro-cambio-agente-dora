# registro-cambio-agente-dora

Una entidad financiera cambia sus sistemas de TIC todos los días, y cada vez más el cambio lo escribe, lo prueba o lo implanta un agente de IA. El Reglamento (UE) 2022/2554 (DORA) exige que todos esos cambios se registren, prueben, evalúen, aprueben, apliquen y verifiquen de forma controlada, y el Reglamento Delegado (UE) 2024/1774 dice qué debe incluir ese procedimiento. Esta herramienta comprueba si el registro de un cambio en el que ha participado un agente de IA contiene lo que exige la norma, y distingue lo que exige el texto de lo que solo exige una lectura propia.

Sitio: https://mshodai.github.io/registro-cambio-agente-dora/, qué puede demostrar el registro de un cambio hecho por un agente de IA y qué no.

El escenario. Una persona encarga un cambio, un agente de IA lo implementa y alguien lo aprueba. A menudo, quien encarga y quien aprueba son la misma persona, que además responde del agente:
- **DORA pide que los cambios se aprueben de forma controlada.** Art. 9.4.e): políticas, procedimientos y controles «a fin de garantizar que todos los cambios en los sistemas de TIC se registren, sometan a prueba, evalúen, aprueben, apliquen y verifiquen de forma controlada».
- **El Reglamento Delegado pide independencia entre quien aprueba y quien solicita o aplica.** Art. 17.1.b): «mecanismos para garantizar la independencia de las funciones que aprueban los cambios y las funciones responsables de solicitar y aplicar dichos cambios».
- **Que implante un agente no separa nada.** La independencia que pide el art. 17.1.b) tiene dos lados: quien aprueba frente a quien solicita y quien aprueba frente a quien aplica. El agente solo cambia quién aplica.
- **El régimen simplificado no pide esa independencia.** Las entidades del art. 16.1 de DORA no aplican los arts. 5 a 15, y el título III del Reglamento Delegado no tiene un equivalente del art. 17.1.b).

La herramienta no evalúa el agente. Trata al agente como un actor cuya identidad (herramienta, modelo, versión y persona responsable) y cuyas acciones son datos del registro, y comprueba el registro con los dos regímenes. Solo da «incumplimiento» cuando lo sostiene el texto de la norma aplicado al registro. Cuando la conclusión depende de una lectura propia, da un aviso que remite a ella.

## El caso, calculado

El repositorio incluye un corpus de 46 registros sintéticos en `corpus/`, cada uno con su resultado esperado. En el caso 04, la misma persona solicita y aprueba un cambio que implanta un agente:

```
$ registro-cambio-agente corpus/04-art-17-1-b-d-1-misma-persona-solicita-y-aprueba.json --regimen completo
Cambio CAMBIO-EJEMPLO-1

Resultado de un cálculo bajo las lecturas que declara docs/modelo-datos.md, no una determinación jurídica. Las decisiones propias se citan como D-n y las dudas de implementación como DI-n.

Régimen completo:
  1 incumplimiento; 0 avisos de lectura propia.
  R-01 Registro del cambio: cumple: garantizado por la validación de entrada — DORA, art. 9.4.e) («se registren»); art. 12.2.c.iii)
  R-02 Elementos que se cambian: cumple — Art. 17.1.d.i); art. 17.1, encabezado
  R-03 Identificación de los actores en sus acciones: cumple — Arts. 20.2.a) y 21.c)
  R-04 Quién solicita: cumple: garantizado por la validación de entrada — Art. 17.1.b)
  R-05 Independencia entre quien aprueba y quien solicita o aplica: INCUMPLIMIENTO — Art. 17.1.b); considerando 17; D-1
      P-2 aprueba (cambio.aprobacion) y también solicita.
      Nota: El mismo actor aprueba y solicita o aplica: el registro de este cambio muestra que el mecanismo del art. 17.1.b) no funcionó en él. Ninguna lectura lo salva (D-1).
  R-06 Funciones y responsabilidades del cambio: sin indicio de incumplimiento — Art. 17.1.c), incisos i) a iv)
  R-07 Objeto y alcance: cumple — Art. 17.1.d.i)
  R-08 Calendario: cumple: garantizado por la validación de entrada — Art. 17.1.d.ii)
  R-09 Resultados esperados: cumple — Art. 17.1.d.iii)
  R-10 Comunicación de los detalles del cambio: cumple — Art. 17.1.d), encabezado
  R-11 Verificación de los requisitos de seguridad: cumple — Art. 17.1.a)
  R-12 Evaluación del cambio: cumple — DORA, art. 9.4.e) («evalúen»); art. 17.1.h)
  R-13 Riesgos de un cambio importante: no aplica — Art. 31.1.e) (solo régimen simplificado)
      Solo lo exige el régimen simplificado.
  R-14 Pruebas antes de la implantación: cumple — DORA, art. 9.4.e); art. 16.2 («antes de su uso»)
      Pruebas anteriores a la implantación: PR-1, PR-2.
  R-15 Seguridad de los paquetes a más tardar en integración: cumple — Art. 16.4
  R-16 Datos de producción en entornos de prueba: cumple — Art. 16.5.a) y 16.6; D-4
  R-17 Revisión del código fuente, estática y dinámica: cumple — Art. 16.3; D-2
  R-18 Plan de acción ante los hallazgos: cumple — Art. 16.3.b); D-2
  R-19 Seguimiento del plan de acción: cumple — Art. 16.3.c); D-2
  R-20 Origen del código: cumple — Art. 16.7 y 16.8; D-3
  R-21 Revisión previa del código de terceros, propietario o abierto: no aplica — Art. 16.8; D-3
      La entidad no declara código de terceros, propietario ni abierto (D-3).
  R-22 Medidas contra la alteración o la manipulación: sin indicio de incumplimiento — Art. 16.1.c); art. 16.7
  R-23 Aprobación: cumple — DORA, art. 9.4.e) («aprueben»); art. 16.2; art. 17.1.b); D-4
  R-24 Aplicación: cumple: garantizado por la validación de entrada — DORA, art. 9.4.e) («apliquen»)
  R-25 Vuelta atrás: cumple — Art. 17.1.e)
  R-26 Procedimiento de emergencia con salvaguardias: no aplica — Art. 17.1.f)
      El cambio no siguió el procedimiento de emergencia (`emergencia` es null).
  R-27 Revisión posterior del cambio de emergencia: no aplica — Art. 17.1.g); D-4
      El cambio no es de emergencia.
  R-28 Verificación posterior: cumple — DORA, art. 9.4.e) («verifiquen»)
      Resultado: conforme.

Exige actuar: sí.
  completo: R-05 (texto: Art. 17.1.b); considerando 17; D-1)
```

Cómo leerlo:

- **R-05 da incumplimiento, y lo sostiene el texto.** El art. 17.1.b) no pide solo mecanismos de independencia, sino mecanismos «para garantizar» la independencia. Si en un cambio la misma persona solicita y aprueba, ese cambio demuestra que el mecanismo no la garantizó en él. Da igual si no existía, si no cubría el caso o si alguien lo eludió.
- **R-06 y R-22 dan «sin indicio de incumplimiento», no «cumple».** Dependen de un mecanismo de la entidad: las responsabilidades del procedimiento (art. 17.1.c) y las medidas contra la manipulación (arts. 16.1.c y 16.7). El registro de un cambio puede probar que un mecanismo falló, pero nunca que existe.
- **R-13 no aplica.** Es un requisito del régimen simplificado (art. 31.1.e), y la cita lo dice.
- **Exige actuar.** Dice qué lo activa: aquí, el texto del art. 17.1.b). Si lo activara una lectura propia, lo diría también, con su D-n o DI-n.

El código de salida es 1, porque algo exige actuar. Con el régimen simplificado, el mismo registro no tiene ningún incumplimiento: la coincidencia entre quien solicita y quien aprueba es un dato informativo (I-01).

## Instalación

Hace falta Python 3.11 o posterior. No tiene dependencias externas: `pip install` solo descarga setuptools para construir el paquete. Desde la raíz del repositorio:

```sh
python3 -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install .
registro-cambio-agente corpus/04-art-17-1-b-d-1-misma-persona-solicita-y-aprueba.json
```

**Uso:** `registro-cambio-agente FICHERO [--regimen completo|simplificado] [--json]`.
- **Régimen:** es un parámetro del cálculo, no un dato del registro. Sin `--regimen` se calculan los dos.
- **`--json`:** el mismo informe en JSON, con el estado, la cita, los motivos y las notas de cada requisito, los avisos y qué activa el código de salida.

**Códigos de salida:**
- **1:** algo exige actuar en algún régimen calculado. Puede ser un incumplimiento, que sostiene el texto de la norma, o un aviso de lectura propia (A-03), que dice que con esa lectura falta algo. El 1 señala que alguna lectura exige actuar, como en los demás repositorios del proyecto.
- **0:** nada exige actuar. Puede haber avisos que no dicen que falte nada (A-01, autorrevisión de un agente; A-02, faltan evidencias) o datos informativos.
- **2:** el fichero no se puede leer o la entrada no es válida. Los errores de validación salen con su código (`ERR-01` a `ERR-05`) y la ruta del dato.

**Con tu propio registro.** La entrada es un JSON con:
- los actores, personas o agentes de IA, con su función y su cuenta. Del agente, su herramienta, su modelo, su versión y la persona que responde de él;
- el cambio: qué elementos cambia, su objeto, alcance, calendario y resultados esperados, a quién se comunicó, el origen del código, la solicitud, las responsabilidades, la verificación de seguridad, la evaluación, los controles contra la manipulación, las pruebas, las revisiones de código, la vuelta atrás, la aprobación, la emergencia si la hubo, la implantación, la verificación posterior y las acciones de cada actor.

Cada campo cita el artículo y la letra de los que sale, o se marca como decisión propia. El formato, con tres ejemplos, está en [docs/modelo-datos.md](docs/modelo-datos.md). Del agente no se recoge nada interno: ni instrucciones, ni configuración, ni razonamiento.

**El corpus.** Los 46 casos, con su tabla de resultados, están en [corpus/README.md](corpus/README.md). Cada caso rompe un solo requisito o provoca un solo aviso, y su nombre lleva el artículo que rompe. Se regeneran con `python corpus/generar.py`, que comprueba cada caso contra su resultado esperado antes de escribirlo. Los resultados esperados están escritos a mano.

**Tests:** `pip install pytest` y `pytest` desde la raíz.

## Qué comprueba

Veintiocho requisitos, R-01 a R-28, en dos regímenes:
- **`completo`:** DORA, art. 9.4.e), y el título II del Reglamento Delegado, en particular su art. 17 (gestión de cambios) y su art. 16 (adquisición, desarrollo y mantenimiento): solicitud, independencia, responsabilidades, objeto, alcance, calendario, resultados esperados, comunicación, verificación de los requisitos de seguridad, evaluación, pruebas, revisión de código, datos de producción en pruebas, origen del código, controles contra la manipulación, aprobación, vuelta atrás, emergencia y su revisión posterior, y verificación.
- **`simplificado`:** las entidades del art. 16.1 de DORA y el título III del Reglamento Delegado (arts. 28 a 41). Su equivalente del art. 17 es el art. 38.2, que repite el art. 9.4.e) de DORA: que todo cambio «se registre, someta a prueba, evalúe, apruebe, aplique y verifique de manera controlada». Además, el art. 37.b) exige prueba y aprobación «antes de introducir cambios en el entorno de producción», el art. 37.c) medidas contra la manipulación y el art. 31.1.e) la evaluación de los riesgos de un «cambio importante». Lo que el título III no tiene sale como «no aplica», con la cita del régimen completo.

Para cada requisito, uno de cinco resultados, siempre con su cita:
- `cumple`. En R-01, R-04, R-08 y R-24 dice «cumple: garantizado por la validación de entrada».
- `incumplimiento`, **solo cuando lo sostiene el texto de la norma aplicado al registro.**
- `aviso`, cuando el texto no lo sostiene pero una lectura propia dice que falta algo. Lleva un aviso A-03 que remite a la decisión (D-n), la duda (DI-n) o la sección del modelo de la que sale.
- `sin_indicio_de_incumplimiento`, **en los requisitos que dependen de un mecanismo de la entidad**: R-05 (independencia), R-06 (responsabilidades), R-22 (controles contra la manipulación) y R-26 (procedimiento de emergencia). Nunca dan `cumple`, porque el registro de un cambio puede probar que el mecanismo falló, pero no que existe (D-1).
- `no_aplica`, con el motivo.

Las reglas completas están en el [modelo de datos](docs/modelo-datos.md): el principio (§0.1 bis), las decisiones D-1 a D-5 (§12) y la tabla de qué exige cada régimen (§13). Las dudas que aparecieron al implementar están en [docs/dudas-implementacion.md](docs/dudas-implementacion.md).

## Qué no hace

- **No mira dentro del agente.** No modela instrucciones, configuración, contexto, parámetros ni razonamiento. Del agente recoge su identidad y sus acciones.
- **No clasifica el agente.** No dice si es un sistema de IA de alto riesgo según el Reglamento (UE) 2024/1689.
- **No comprueba el procedimiento.** Que exista, que esté documentado o que lo haya aprobado la dirección (DORA, art. 9.4, párrafo tercero) es un hecho del procedimiento, no de cada cambio.
- **No valora.** No dice si el nivel de las pruebas es «acorde con el carácter esencial» de lo afectado (art. 16.2) ni si las salvaguardias de emergencia son «adecuadas» (art. 17.1.f).
- **No cubre las entidades de contrapartida central ni los depositarios centrales de valores** en lo que solo les afecta a ellos: las pruebas de tensión tras cambios significativos (art. 17.2) y las partes que deben asociar a las pruebas (art. 16.2, párrafos segundo y tercero). Es candidato para una versión posterior, con el tipo de entidad como parámetro.
- **No comprueba las pruebas de seguridad de los sistemas expuestos a internet** (art. 16.3): el modelo no recoge si un sistema lo está.
- **No dice qué lectura es la correcta.** Aplica una y la nombra, y cuando solo una lectura propia hace fallar un requisito, lo da como aviso.

## Decisiones y dudas

El modelo documenta cinco decisiones propias, cada una con qué dice la norma, por qué no la determina y qué lectura adopta:
- **D-1:** qué pasa cuando la misma persona solicita y aprueba, y por qué un requisito del procedimiento se valida en un cambio concreto;
- **D-2:** si la revisión de código hecha por un agente cuenta como la del art. 16.3;
- **D-3:** de dónde procede el código que escribe un agente;
- **D-4:** si puede aprobar un agente;
- **D-5:** los cambios urgentes en el régimen simplificado.

La implementación añadió once dudas, DI-1 a DI-11, en [docs/dudas-implementacion.md](docs/dudas-implementacion.md). El porqué de la arquitectura está en el [ADR 0001](docs/adr/0001-validar-el-registro-del-cambio-no-el-agente.md).

## Fuentes

| Documento | Versión |
|---|---|
| Reglamento (UE) 2022/2554 (DORA), de 14 de diciembre de 2022 | Texto original publicado en el DO L 333 de 27 de diciembre de 2022. No tiene versión consolidada con modificaciones |
| Reglamento Delegado (UE) 2024/1774 de la Comisión, de 13 de marzo de 2024 | Texto original publicado en el DO L de 25 de junio de 2024. No tiene versión consolidada con modificaciones |
| Corrección de errores del Reglamento Delegado (UE) 2024/1774 | DO L 2025/90420, de 15 de mayo de 2025. Solo corrige el art. 22.d), que este proyecto no usa |

Los tres se descargaron de EUR-Lex el 2 de octubre de 2026. Que no hay versiones consolidadas posteriores se comprobó en el Cellar de la Oficina de Publicaciones. Las URL y las huellas SHA-256 de cada documento están en [docs/fuentes/FUENTES.md](docs/fuentes/FUENTES.md). Los PDF no se redistribuyen.

Las versiones consolidadas de EUR-Lex no tienen efecto jurídico por sí solas. El texto vinculante es el publicado en el Diario Oficial.

## Otros repositorios del proyecto

- [validador-cadena-verifactu](https://github.com/mshodai/validador-cadena-verifactu): comprueba la integridad de una cadena de registros de facturación de Verifactu.
- [calculo-titularidad-real](https://github.com/mshodai/calculo-titularidad-real): calcula la titularidad real bajo la Ley 10/2010 y el AMLR.
- [plazos-conservacion-pbc](https://github.com/mshodai/plazos-conservacion-pbc): calcula el estado de conservación de la documentación bajo la Ley 10/2010 y el AMLR.
- [plazos-actualizacion-pbc](https://github.com/mshodai/plazos-actualizacion-pbc): calcula la próxima revisión obligatoria de la información de un cliente bajo el RD 304/2014 y el AMLR.
- [registro-examen-especial-pbc](https://github.com/mshodai/registro-examen-especial-pbc): comprueba si el registro de un examen especial de prevención del blanqueo, en el que puede intervenir un sistema de IA, contiene lo que exigen el RD 304/2014 y el AMLR.

## Licencia

MIT; el texto completo está en [LICENSE](LICENSE). Cubre el código y la documentación de este repositorio, no los documentos de `docs/fuentes/`, que no se incluyen.

---

Es una implementación de referencia, probada sobre datos sintéticos. No es software de cumplimiento normativo y no constituye asesoramiento jurídico.
