# Dudas de implementación

Ambigüedades o contradicciones de [`modelo-datos.md`](modelo-datos.md) que han aparecido al implementar la v0.1 del validador. El modelo no se ha cambiado. En cada duda se dice qué sección afecta, por qué no está resuelta y qué lectura implementa el código. Cuando hay varias, es la más conservadora: la que no da por cumplido lo que el registro no muestra. En el código, cada una se señala con un comentario «Dudas, DI-n».

Los identificadores DI-n son estables: no se renumeran ni se reutilizan.

### DI-1. Cadenas vacías

**Sección:** §4 a §10 (todos los campos de tipo cadena).

**Duda:** el modelo dice que un campo de cadena es obligatorio, pero no si la cadena vacía (`""`) o hecha solo de espacios cuenta como dato.

**Lectura implementada:** la carga la acepta, porque es una cadena. El cálculo la trata como dato ausente en los requisitos que piden ese texto: `objeto`, `alcance.descripcion`, `resultados_esperados`, `evaluacion.repercusion_seguridad`, `evaluacion.riesgos`, `vuelta_atras.procedimiento`, `emergencia.procedimiento` y `emergencia.salvaguardias`.

### DI-2. Qué actores «actúan en los sistemas de TIC»

**Sección:** §3.1, campo `cuenta`.

**Duda:** `cuenta` puede ser `null` «si el actor no actuó en ningún sistema; por ejemplo, quien solo solicita». El modelo no enumera qué pasos suponen actuar en un sistema.

**Lectura implementada (R-03):** actúan en los sistemas los actores de:
- `implantacion`;
- `pruebas[].realizada_por`;
- `revisiones_codigo[].realizada_por`;
- `vuelta_atras.ejecucion`;
- `acciones[].actor`.

A todos ellos se les exige `cuenta`. No se exige a quien solo solicita, aprueba, evalúa, verifica, revisa a posteriori o hace el seguimiento. Además, una prueba o revisión con `realizada_por` vacía no identifica a quien la hizo, y también es incumplimiento de R-03.

### DI-3. Verificación de seguridad negativa y cambio aplicado

**Sección:** §6.1, `verificacion_seguridad.resultado`.

**Duda:** el art. 17.1.a) pide verificar que el cambio cumple los requisitos de seguridad. El modelo recoge el resultado (`cumple` o `no_cumple`), pero no dice qué pasa si la verificación da `no_cumple` y el cambio se aplica igual.

**Lectura implementada (R-11):** con `no_cumple` y `implantacion.resultado` `aplicado`, es incumplimiento. Una verificación que se hace y se desoye no sirve para lo que pide el art. 17.1.a). Con `abortado` o `revertido` no lo es.

### DI-4. Pruebas previas en los cambios de emergencia (régimen completo)

**Sección:** §7.1, §9 y §13 («Probar antes de producción»).

**Duda:** el §13 dice que, en el régimen completo, la aprobación antes de producción «queda exceptuada por los cambios de emergencia del art. 17.1.f) y g)». No dice lo mismo de las pruebas. El art. 16.2 pide probar «antes de su uso» sin excepción, pero un procedimiento de emergencia (art. 17.1.f) podría prever pruebas reducidas o posteriores.

**Lectura implementada (R-14):** también en un cambio de emergencia se exige al menos una prueba anterior a `implantacion.inicio`. El resultado lleva una nota que lo dice.

### DI-5. ¿Toda prueba de un tipo es obligatoria en cada cambio?

**Sección:** §7.1, `pruebas[].tipo`.

**Duda:** la columna «Completo» de `tipo` dice «exige»: el tipo es un dato exigible. Pero el modelo no dice si cada cambio debe tener una prueba de cada tipo. Por ejemplo, una prueba de seguridad de paquetes (art. 16.4) en todo cambio de software. Tampoco recoge si un sistema está expuesto a internet (art. 16.3), que haría falta para exigir esa prueba.

**Lectura implementada (R-15):** se comprueba solo el momento de las pruebas de seguridad de paquetes que haya: «a más tardar en la fase de integración». Si no hay ninguna, el resultado es `no_aplica`, con el motivo. No se da por cumplido. La exigencia de pruebas de seguridad para sistemas expuestos a internet no se implementa (ver «Lo que no se ha implementado» en el informe de la v0.1).

### DI-6. Revisión posterior «pendiente»

**Sección:** §9, `revision_posterior`.

**Duda:** el modelo dice que los pasos de la revisión posterior son `null` «mientras no se hayan hecho», y que entonces «el registro queda pendiente». No dice si «pendiente» es un incumplimiento o un estado propio.

**Lectura implementada (R-27):** es incumplimiento, y el motivo dice que la revisión está pendiente. Mientras falte, el registro no muestra lo que pide el art. 17.1.g), y algo exige actuar (código de salida 1).

### DI-7. El ejemplo del §1.2, compuesto literalmente, verifica antes de implantar

**Sección:** §1.2.

**Contradicción:** el §1.2 muestra solo los campos que cambian respecto del §1.1 y dice que «los demás serían como allí». Compuesto así, el ejemplo conserva dos cosas del §1.1:
- `verificacion_posterior.fecha` (`2026-11-09T11:00`), que es anterior a la implantación de emergencia (`2026-11-09T23:10`);
- las `acciones` del §1.1, también anteriores.

Una verificación «posterior» anterior a lo que verifica contradice el §10 («Debe ser posterior a `implantacion.inicio`»). Parece una omisión del ejemplo, no una regla.

**Lectura implementada:** el ejemplo se compone literalmente, sin corregirlo, y se trata como entrada válida, porque la carga no comprueba ese orden (§15). Da R-28 en los dos regímenes. En el simplificado da además R-23, por el D-5, que es lo que el ejemplo pretende mostrar. Los tests lo esperan así. El corpus incluye además una versión con la verificación tras la implantación (`20-emergencia-bien-registrada`), que en el completo no tiene incumplimientos.

### DI-8. «Lista no vacía»: ¿error de entrada o requisito?

**Sección:** §2, §4, §6.3, §7.1 y §7.2.

**Duda:** el modelo dice «lista no vacía» en sitios de distinta naturaleza:
- en los pasos (§2: «`actores` es una lista no vacía»);
- en `elementos`, `alcance.sistemas`, `controles_integridad` y `pruebas`;
- en `comunicaciones`, solo «en el completo».

No dice si una lista vacía es un error de entrada (§15) o un incumplimiento.

**Lectura implementada:**
- **Error de entrada (ERR-01):** solo las listas de actores de los pasos del §2, que el modelo declara no vacías como forma. Por coherencia, también `verificacion_seguridad.actores`, `evaluacion.actores` y `verificacion_posterior.actores`, que el modelo tipa como «paso», y `revisiones_codigo[].tecnicas`, porque una revisión usa «una técnica o las dos» (§7.2).
- **Incumplimiento de su requisito:** las demás listas vacías. Así se dice qué artículo falta, y una lista que un régimen no exige no rompe la entrada (§0.1, principio 3). Esto incluye `realizada_por`, `plan_accion.adoptado_por`, `plan_accion.medidas[].hallazgos`, `responsabilidades` y `vuelta_atras.responsables`.

### DI-9. Independencia sin ninguna aprobación

**Sección:** §5.2 y D-1.

**Duda:** si no hay ninguna aprobación (ni previa ni posterior de emergencia), no hay con qué comparar. El modelo no dice qué resultado da el art. 17.1.b).

**Lectura implementada (R-05):** `sin_indicio_de_incumplimiento`, nunca `cumple`, con un motivo que remite a R-23 y R-27. Son esos requisitos los que dan la falta de aprobación como incumplimiento.

### DI-10. Verificación posterior de un cambio abortado o revertido

**Sección:** §10.

**Duda:** el §10 pide la verificación posterior sin distinguir el resultado de la implantación. No está claro qué se verifica en un cambio abortado.

**Lectura implementada (R-28):** se exige igual. Verificar que el sistema quedó como estaba es parte de abortar o revertir de forma controlada (DORA, art. 9.4.e).

### DI-11. De qué objetos se avisa si faltan evidencias

**Sección:** §7.3.

**Duda:** el §7.3 dice que la evidencia no es exigible y que «el validador puede avisar de que falta», pero no dice de qué objetos.

**Lectura implementada (aviso A-02):**
- en los dos regímenes, de las pruebas y de los controles de integridad;
- en el completo, además, de `verificacion_seguridad` y de las revisiones de código, que el simplificado no usa.
