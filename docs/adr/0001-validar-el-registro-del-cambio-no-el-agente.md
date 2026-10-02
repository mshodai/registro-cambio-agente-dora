# 0001. Validar el registro del cambio, no el agente de IA

- Estado: aceptada
- Fecha: 02/10/2026

## Contexto

Las entidades financieras cambian sus sistemas de TIC constantemente, y cada vez más el cambio lo escribe, lo prueba o lo implanta un agente de IA. DORA y su Reglamento Delegado regulan la gestión de esos cambios, pero no hablan de agentes.

**DORA pide un proceso controlado para todos los cambios.**
- Art. 9.4.e): políticas, procedimientos y controles documentados para la gestión de los cambios en las TIC, «a fin de garantizar que todos los cambios en los sistemas de TIC se registren, sometan a prueba, evalúen, aprueben, apliquen y verifiquen de forma controlada».
- Art. 9.4, párrafo tercero: ese proceso «será aprobado por los niveles directivos adecuados y dispondrá de protocolos específicos».

**El Reglamento Delegado (UE) 2024/1774 dice qué incluye ese procedimiento en el régimen completo.**
- Art. 17.1, letras a) a h): la verificación de los requisitos de seguridad, «mecanismos para garantizar la independencia de las funciones que aprueban los cambios y las funciones responsables de solicitar y aplicar dichos cambios», las funciones y responsabilidades, el objeto, el alcance, el calendario y los resultados esperados, la vuelta atrás, los cambios de emergencia y su revisión posterior, y la repercusión en la seguridad.
- Art. 16: las pruebas «antes de su uso y después del mantenimiento» (apartado 2), las revisiones de código fuente (apartado 3), las pruebas de seguridad de los paquetes (apartado 4), los datos de producción en las pruebas (apartados 5 y 6) y la integridad del código fuente (apartado 7).

**El régimen simplificado es mucho más corto.** Las entidades del art. 16.1 de DORA no aplican los arts. 5 a 15. El título III del Reglamento Delegado solo pide, para los cambios:
- que se registren, prueben, evalúen, aprueben, apliquen y verifiquen de manera controlada (art. 38.2);
- prueba y aprobación antes de producción (art. 37.b);
- medidas contra la manipulación (art. 37.c);
- la evaluación de los riesgos de un «cambio importante» (art. 31.1.e).

No pide independencia entre quien solicita y quien aprueba.

**Muchos requisitos regulan el procedimiento, no cada cambio.** El art. 17.1 dice qué incluirán «los procedimientos de gestión de cambios», y el art. 16.3, qué incluirá «el procedimiento». La pregunta práctica de una entidad no es si su agente es bueno, sino si el registro de cada cambio en el que ha participado contiene lo que exige la norma, y qué puede demostrar ese registro sobre el procedimiento.

## Decisión

**1. La herramienta valida el registro de un cambio en dos regímenes, que son un parámetro del cálculo.**

El régimen, `completo` o `simplificado`, no es un dato del registro: es un hecho de la entidad (DORA, art. 16.1), y el mismo registro se lee con los dos ([modelo](../modelo-datos.md), §0.1, principio 2). Lo que un régimen no exige sale como «no aplica», con la cita del régimen que sí lo exige.

**2. El agente es un actor, no un sistema que se evalúa.**

Del agente se recogen su identidad (herramienta, modelo, versión y la persona que responde de él) y sus acciones, como datos del registro (modelo, §0.2, regla 2, y §3). No se modelan instrucciones, configuración, contexto ni razonamiento. Solicitar, implantar, aprobar, probar y revisar son pasos con actores, y cualquiera de ellos puede ser una persona o un agente. Si eso cumple lo dice el régimen.

**3. Solo es incumplimiento lo que sostiene el texto.**

El validador da «incumplimiento» solo cuando la conclusión resulta del texto de la norma aplicado al registro (modelo, §0.1 bis, principio 2). El criterio para distinguirlo:
- es **texto** cuando el artículo, aplicado a un cambio concreto, exige ese dato o ese acto para ese cambio;
- es **lectura propia** cuando el artículo regula el procedimiento y la obligación de reflejarlo en cada registro la pone el modelo.

Lo que depende de una lectura propia da un aviso A-03 que remite a ella. Ese aviso también activa el código de salida 1, porque con esa lectura falta algo.

**4. Los requisitos de mecanismo nunca dan «cumple».**

La independencia (art. 17.1.b), las responsabilidades (art. 17.1.c), el procedimiento de emergencia (art. 17.1.f) y las medidas contra la manipulación (arts. 16.1.c y 37.c) dependen de un mecanismo de la entidad. Un registro puede probar que ese mecanismo falló en un cambio, pero no que existe. Estos requisitos dan «incumplimiento» o «sin indicio de incumplimiento» (modelo, §0.1 bis, principio 1, y D-1).

## Consecuencias

**Lo que la herramienta puede comprobar desde el registro:**
- que constan los datos que exige cada régimen, con el artículo y la letra de cada requisito;
- si el mismo actor aprueba y solicita o aplica un cambio, que es incumplimiento del art. 17.1.b) en el régimen completo;
- si la aprobación, las pruebas y la revisión posterior de emergencia van en el orden que exige el texto («antes de su uso», art. 16.2; «antes de introducir cambios en el entorno de producción», art. 37.b; «tras su aplicación», art. 17.1.g);
- qué hizo cada agente y quién responde de él.

**Lo que no puede comprobar:**
- **Que el procedimiento exista.** Ni su aprobación por la dirección (DORA, art. 9.4, párrafo tercero), ni que los mecanismos funcionen en los cambios que no se registran.
- **Si el agente es de alto riesgo**, o si es un sistema de IA según el Reglamento (UE) 2024/1689.
- **Valoraciones:** si el nivel de las pruebas es proporcionado (art. 16.2) o si las salvaguardias de emergencia son adecuadas (art. 17.1.f).
- **Las pruebas de tensión de las entidades de contrapartida central y de los depositarios centrales de valores** (art. 17.2), fuera de alcance en esta versión.

**Hay tres costes.**
- **Muchos avisos de lectura propia.** Seis requisitos (R-03, R-06, R-17, R-20, R-22 y R-26) solo pueden dar aviso, porque el texto, aplicado a un cambio, no exige su dato: lo pide el modelo. Un registro que los omita da código 1 sin ningún incumplimiento, y el informe dice que lo activa una lectura.
- **La independencia depende de lo que declara la entidad.** La función de cada actor es un dato declarado, y el modelo no comprueba que dos nombres distintos sean funciones distintas.
- **El régimen simplificado comprueba poco.** Es lo que pide el título III. La herramienta no lo completa con exigencias del régimen completo.

## Referencias

- Reglamento (UE) 2022/2554 (DORA), arts. 9.4 y 16 (DO L 333 de 27.12.2022): <http://data.europa.eu/eli/reg/2022/2554/oj>
- Reglamento Delegado (UE) 2024/1774, arts. 12, 16, 17, 20, 21, 28, 31, 33, 34, 37 y 38 y considerando 17 (DO L de 25.6.2024): <http://data.europa.eu/eli/reg_del/2024/1774/oj>
- Corrección de errores del Reglamento Delegado (UE) 2024/1774 (DO L 2025/90420, de 15.5.2025): <http://data.europa.eu/eli/reg_del/2024/1774/corrigendum/2025-05-15/oj>
- Versiones y huellas de los documentos usados: [fuentes/FUENTES.md](../fuentes/FUENTES.md)
