---
title: "Borrador: qué puede demostrar el registro de un cambio hecho por un agente de IA"
description: "Borrador. DORA y su Reglamento Delegado exigen que los cambios en los sistemas de TIC se aprueben con independencia de quien los solicita y los aplica. Un registro de cambios puede demostrar que ese control falló en un cambio concreto, pero nunca que existe. Qué dice el texto, qué no exige a cada cambio y qué pasa cuando la misma persona encarga, supervisa y aprueba el trabajo de un agente."
---

> **Borrador.** Este artículo está en revisión y puede cambiar antes de publicarse. Las citas y los resultados de la herramienta son reales; el texto no es definitivo.

# Lo que un registro de cambios no puede demostrar: agentes de IA, independencia y DORA

Una entidad financiera cambia el software de uno de sus sistemas. Una persona del equipo encarga el cambio a un agente de IA, el agente lo escribe, lo prueba y lo implanta, y esa misma persona, que es la responsable del agente, revisa el resultado y lo aprueba. El cambio funciona y queda registrado con todo detalle: quién lo pidió, qué hizo el agente, qué pruebas pasó y quién lo aprobó.

**¿Qué puede demostrar ese registro sobre los controles que DORA exige, y qué no?**

## Lo que exige el texto

El Reglamento (UE) 2022/2554 (DORA) pide un proceso controlado para todos los cambios. Art. 9.4.e): las entidades deberán «aplicar políticas, procedimientos y controles documentados para la gestión de los cambios en las TIC, incluidos los cambios en el software, el hardware, los componentes de firmware, los sistemas o los parámetros de seguridad, [...] a fin de garantizar que todos los cambios en los sistemas de TIC se registren, sometan a prueba, evalúen, aprueben, apliquen y verifiquen de forma controlada».

El Reglamento Delegado (UE) 2024/1774 dice qué deben incluir esos procedimientos. Art. 17.1: las entidades «incluirán en los procedimientos de gestión de cambios en las TIC a que se refiere el artículo 9, apartado 4, letra e), del Reglamento (UE) 2022/2554, en relación con todos los cambios en el software, el hardware, los componentes de firmware, los sistemas o los parámetros de seguridad, todos los elementos siguientes». La letra b) es la que importa aquí: «mecanismos para garantizar la independencia de las funciones que aprueban los cambios y las funciones responsables de solicitar y aplicar dichos cambios».

El considerando 17 explica para qué: «A fin de asegurar la objetividad y la eficacia del proceso de gestión de cambios en las TIC, evitar conflictos de intereses y garantizar que los cambios en las TIC se evalúen de forma objetiva, es necesario que las funciones responsables de aprobar dichos cambios estén separadas de las funciones que los soliciten e implementen».

Ningún artículo menciona los agentes de IA. El texto habla de funciones que solicitan, aplican y aprueban, sin decir si quien aplica es una persona o una herramienta.

## Un registro demuestra fallos, no controles

El art. 17.1 regula el procedimiento: dice qué incluirán «los procedimientos de gestión de cambios». Un registro de cambios, en cambio, describe cambios. Eso limita lo que puede probar, y el límite es asimétrico.

**Un registro puede demostrar que un control falló.** La letra b) no pide solo que existan mecanismos de independencia, sino mecanismos «para garantizar la independencia». Un mecanismo que garantiza algo debe producirlo en cada cambio al que se aplica, y el art. 17.1 los extiende a «todos los cambios». Si en un cambio la misma persona solicita y aprueba, ese cambio demuestra que el mecanismo no garantizó la independencia en él. No hace falta saber si no existía, si no cubría el caso o si alguien lo eludió: las tres cosas incumplen la letra b).

**Un registro no puede demostrar que el control existe.** Un cambio en el que solicita una persona y aprueba otra de otra función es compatible con un buen mecanismo y también con la casualidad. Cien cambios así tampoco lo demuestran: el control puede no existir en el cambio ciento uno, o en los que no se registraron.

Por eso, en los requisitos que dependen de un mecanismo de la entidad, la herramienta nunca dice «cumple». Dice «incumplimiento» cuando el registro demuestra el fallo, y «sin indicio de incumplimiento» cuando no lo demuestra. Son cuatro requisitos:
- la independencia (art. 17.1.b);
- las funciones y responsabilidades (art. 17.1.c: «una descripción clara de las funciones y responsabilidades»);
- el procedimiento de emergencia (art. 17.1.f: «procedimientos, protocolos y herramientas para gestionar los cambios de emergencia que ofrezcan las salvaguardias adecuadas»);
- las medidas contra la manipulación (art. 16.1.c: «medidas para mitigar el riesgo de alteración no intencionada o de manipulación intencionada de los sistemas de TIC»).

La existencia del mecanismo es otra prueba, sobre el procedimiento y no sobre el registro.

## El texto no exige que cada cambio tenga revisión de código

La revisión de código es el ejemplo más claro de un requisito que se suele atribuir a cada cambio y que el texto pone en el procedimiento. Art. 16.3 del Reglamento Delegado: «El procedimiento a que se refiere el apartado 2 incluirá la realización de revisiones de códigos fuente que abarquen pruebas tanto estáticas como dinámicas». Y el apartado 2 define ese procedimiento: uno «de adquisición, desarrollo y mantenimiento de sistemas de TIC a efectos de la prueba y aprobación de todos los sistemas de TIC antes de su uso y después del mantenimiento».

El texto exige que el procedimiento incluya revisiones de código. No dice que cada cambio deba pasar una, ni con las dos técnicas. Cabe sostener que, leídos juntos, los apartados 2 y 3 lo implican para cada mantenimiento. Pero eso es una lectura, no lo que dice el texto. Lo que DORA sí exige de cada cambio es que se someta «a prueba» (art. 9.4.e), y una prueba no es una revisión de código.

La herramienta lo trata así. Un cambio con código fuente y sin ninguna revisión, como el caso base del corpus ([caso 01](https://github.com/mshodai/registro-cambio-agente-dora/blob/main/corpus/01-base-limpia.json)) con `revisiones_codigo` vacía, no da incumplimiento, sino un aviso que remite a la lectura del modelo de datos:

```
$ registro-cambio-agente sin-revision.json
[...]
Régimen completo:
  0 incumplimientos; 1 aviso de lectura propia.
[...]
  R-17 Revisión del código fuente, estática y dinámica: aviso (lectura propia) — Art. 16.3; D-2
      Con la lectura modelo §7.2: el cambio incluye código fuente y no tiene revisiones de código.
[...]
Régimen simplificado:
  0 incumplimientos; 0 avisos de lectura propia.
[...]
  R-17 Revisión del código fuente, estática y dinámica: no aplica — Art. 16.3; D-2 (solo régimen completo)
```

El aviso sigue exigiendo actuar, y el código de salida es 1: con esa lectura falta algo. Pero quien lea el resultado sabe que lo exige una lectura, no el texto. Es el mismo criterio para todo el validador: **solo es incumplimiento lo que sostiene el texto de la norma aplicado al registro**. Lo que depende de una lectura propia es un aviso que la nombra.

La misma razón vale para quién revisa. Ni el art. 16 ni ningún otro artículo del Reglamento Delegado dicen que la revisión tenga que hacerla una persona. Si la hace un agente, la herramienta la cuenta como revisión del art. 16.3. Solo avisa si el agente que revisa es el mismo que implantó el cambio, y como aviso, no como incumplimiento.

## El régimen simplificado no exige independencia

DORA, art. 16.1: «Los artículos 5 a 15 del presente Reglamento no se aplicarán a las empresas de servicios de inversión pequeñas y no interconectadas ni a las entidades de pago exentas en virtud de la Directiva (UE) 2015/2366; ni a las entidades exentas en virtud de la Directiva 2013/36/UE [...], ni a las entidades de dinero electrónico exentas en virtud de la Directiva 2009/110/CE; ni a los fondos de pensiones de empleo pequeños». Para ellas no rige el art. 9.4.e), y el art. 17 del Reglamento Delegado está en su título II, que tampoco les corresponde.

Su marco simplificado es el título III. Para los cambios, su art. 38.2 pide un procedimiento «para garantizar que todo cambio en los sistemas de TIC se registre, someta a prueba, evalúe, apruebe, aplique y verifique de manera controlada y con las salvaguardias adecuadas». El art. 37.b) añade que los sistemas se sometan a prueba y sean aprobados «antes de introducir cambios en el entorno de producción».

No hay un equivalente del art. 17.1.b). La única independencia que pide el título III es otra. Art. 28.4: las entidades «garantizarán una separación adecuada, así como la independencia, de las funciones de control y las funciones de auditoría interna». Eso separa el control de la auditoría, no a quien solicita un cambio de quien lo aprueba.

En el régimen simplificado, que la misma persona solicite y apruebe no es un incumplimiento. La herramienta lo da como dato informativo, para que la entidad lo vea, sin convertirlo en un requisito que el texto no pone.

## El flujo con agentes que incumple el art. 17.1.b)

Vuelta al caso del principio. Una persona encarga el cambio, responde del agente que lo implanta y lo aprueba. En el corpus, es el [caso 06](https://github.com/mshodai/registro-cambio-agente-dora/blob/main/corpus/06-art-17-1-b-aviso-d-1-aprueba-el-responsable-del-agente.json) ([resultado esperado](https://github.com/mshodai/registro-cambio-agente-dora/blob/main/corpus/06-art-17-1-b-aviso-d-1-aprueba-el-responsable-del-agente.esperado.json)), en el que aprueba la responsable del agente, con un cambio: la solicitud también es suya (`"solicitud": {"actores": ["P-3"], ...}`).

```
$ registro-cambio-agente flujo.json
[...]
Régimen completo:
  1 incumplimiento; 1 aviso de lectura propia.
[...]
  R-05 Independencia entre quien aprueba y quien solicita o aplica: INCUMPLIMIENTO — Art. 17.1.b); considerando 17; D-1
      P-3 aprueba (cambio.aprobacion) y también solicita.
      Nota: El mismo actor aprueba y solicita o aplica: el registro de este cambio muestra que el mecanismo del art. 17.1.b) no funcionó en él. Ninguna lectura lo salva (D-1).
[...]
  Avisos (no son incumplimientos; A-03 viene de una lectura propia y exige actuar):
    A-03 R-05: con la lectura D-1 (persona responsable del agente, modelo §3.2), P-3 aprueba (cambio.aprobacion) y AG-1 aplica: responde de los dos la persona P-3. [...]

Régimen simplificado:
  0 incumplimientos; 0 avisos de lectura propia.
[...]
  Datos informativos:
    I-01 P-3 aprueba (cambio.aprobacion) y también solicita. El título III no exige independencia: es un dato informativo. [...]
```

El resultado separa dos cosas que en la práctica van juntas:
- **Solicitar y aprobar la misma persona es incumplimiento del art. 17.1.b) en el régimen completo.** Lo sostiene el texto: la independencia entre la función que aprueba y la que solicita no depende de quién implante.
- **Aprobar el trabajo del agente del que se responde es un aviso, no un incumplimiento.** Atribuir los actos del agente a la persona que responde de él es razonable, pero es una lectura: el texto habla de funciones que aplican cambios y no dice a quién se imputan los actos de una herramienta.

Que implante un agente no aporta ninguna separación. La independencia del art. 17.1.b) tiene dos lados, quien aprueba frente a quien solicita y quien aprueba frente a quien aplica, y el agente solo cambia quién aplica. Si el flujo de trabajo pone a la misma persona a encargar y a aprobar, el registro de cada cambio lo mostrará como un fallo del mecanismo.

**La separación tiene que configurarse aparte.** No sale del agente ni de la herramienta que lo ejecuta, sino de cómo la entidad reparte las funciones y los permisos. El propio Reglamento Delegado lo pide en el control de acceso. Art. 21.b): «la separación de funciones con el fin de impedir el acceso injustificado a datos esenciales o la asignación de combinaciones de derechos de acceso que puedan utilizarse para eludir los controles». Una cuenta que puede encargar un cambio a un agente y aprobar su resultado es una de esas combinaciones.

## Qué hace la herramienta

[registro-cambio-agente-dora](https://github.com/mshodai/registro-cambio-agente-dora) no evalúa el agente. Valida el registro de un cambio en los dos regímenes, completo y simplificado, que son un parámetro del cálculo y no un dato del registro. Para cada uno de sus veintiocho requisitos da un resultado con el artículo y la letra de los que sale:
- `cumple`;
- `incumplimiento`, solo cuando lo sostiene el texto;
- `aviso`, cuando solo lo sostiene una lectura propia, que nombra;
- `sin_indicio_de_incumplimiento`, en lugar de `cumple`, en los requisitos de mecanismo;
- `no_aplica`, con su motivo.

El agente es un actor más. Se recogen su identidad (herramienta, modelo, versión y la persona que responde de él) y sus acciones, y nada interno: ni instrucciones, ni configuración, ni razonamiento.

El [modelo de datos](https://github.com/mshodai/registro-cambio-agente-dora/blob/main/docs/modelo-datos.md) cita cada campo a su artículo y documenta las decisiones que la norma no toma. Entre ellas:
- qué pasa cuando la misma persona solicita y aprueba ([D-1](https://github.com/mshodai/registro-cambio-agente-dora/blob/main/docs/modelo-datos.md#d-1-quien-solicita-y-quien-aprueba-son-la-misma-persona));
- si cuenta la revisión de código de un agente (D-2);
- si puede aprobar un agente (D-4);
- qué pasa con los cambios urgentes en el régimen simplificado (D-5).

El [corpus](https://github.com/mshodai/registro-cambio-agente-dora/blob/main/corpus/README.md) tiene un caso sintético por cada incumplimiento o aviso posible, con su resultado esperado escrito a mano.

## La consecuencia general

Un registro de cambios es una prueba de lo que pasó en cada cambio, no de cómo está organizada la entidad. Puede mostrar que un control falló; no puede mostrar que existe. **Una herramienta que dijera «cumple» sobre un requisito de procedimiento estaría certificando algo que el registro no contiene.**

Los agentes de IA no cambian esa limitación, pero la hacen más frecuente. Cuando el trabajo lo hace una herramienta, es fácil que una sola persona encargue, supervise y apruebe, y que el flujo se sienta controlado porque cada paso queda registrado. El registro solo demuestra que alguien registró el cambio. La independencia que exige el art. 17.1.b) en el régimen completo no la da el agente: hay que configurarla en las funciones y los permisos de la entidad, y el registro de cada cambio dirá si se respetó.

---

El código, el modelo de datos, el corpus y las fuentes con su versión y su huella están en [github.com/mshodai/registro-cambio-agente-dora](https://github.com/mshodai/registro-cambio-agente-dora). Las citas de DORA son del texto publicado en el DO L 333 de 27.12.2022, y las del Reglamento Delegado (UE) 2024/1774, del texto publicado en el DO L de 25.6.2024. Ninguno de los dos tiene versión consolidada con modificaciones, y la única corrección de errores en español del Reglamento Delegado, de 15.5.2025, solo afecta a su art. 22.d) ([docs/fuentes/FUENTES.md](https://github.com/mshodai/registro-cambio-agente-dora/blob/main/docs/fuentes/FUENTES.md)).

Este artículo es un análisis de la arquitectura de una herramienta de validación, no asesoramiento jurídico.
