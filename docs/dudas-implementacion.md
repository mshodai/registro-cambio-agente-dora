# Dudas de implementación

Ambigüedades o contradicciones de [`modelo-datos.md`](modelo-datos.md) que han aparecido al implementar el validador. En cada duda se dice qué sección afecta, por qué no está resuelta y qué hace el código. En el código, cada una se señala con un comentario «Dudas, DI-n».

Los identificadores DI-n son estables: no se renumeran ni se reutilizan.

**Cómo se aplican desde el principio del §0.1 bis del modelo.** Una duda es una lectura propia. Por eso, cuando una duda es lo único que hace fallar un requisito, el resultado no es «incumplimiento», sino un **aviso de lectura propia (A-03)** que remite a la duda. El requisito da `aviso` o, si es de mecanismo, `sin_indicio_de_incumplimiento`. Un A-03 activa el código de salida 1, como en la serie: alguna lectura exige actuar.

Hay una excepción: la DI-1, que no es una lectura jurídica. Ver abajo.

### DI-1. Cadenas vacías

**Sección:** §4 a §10 (todos los campos de tipo cadena).

**Duda:** el modelo dice que un campo de cadena es obligatorio, pero no si la cadena vacía (`""`) o hecha solo de espacios cuenta como dato.

**Qué hace el código:** la carga la acepta, porque es una cadena. El cálculo la trata como dato ausente en los requisitos que piden ese texto: `objeto`, `alcance.descripcion`, `resultados_esperados`, `evaluacion.repercusion_seguridad`, `evaluacion.riesgos`, `vuelta_atras.procedimiento`, `emergencia.procedimiento` y `emergencia.salvaguardias`.

**Con el principio nuevo:** no es una lectura jurídica, sino una regla sobre qué cuenta como dato. Un texto vacío sigue la base del requisito al que pertenece. En R-07, R-09, R-12 y R-25, que tienen base en el texto, da incumplimiento. En R-26, que solo tiene base en el modelo (§9), da aviso.

### DI-2. Qué actores «actúan en los sistemas de TIC»

**Sección:** §3.1, campo `cuenta`.

**Duda:** `cuenta` puede ser `null` «si el actor no actuó en ningún sistema; por ejemplo, quien solo solicita». El modelo no enumera qué pasos suponen actuar en un sistema.

**Qué hace el código (R-03):** actúan en los sistemas los actores de:
- `implantacion`;
- `pruebas[].realizada_por`;
- `revisiones_codigo[].realizada_por`;
- `vuelta_atras.ejecucion`;
- `acciones[].actor`.

**Con el principio nuevo:** los arts. 21.c) y 33.b) regulan la política de acceso; que cada registro lleve la cuenta lo pide el modelo (§3.1). Un actor de esa lista sin `cuenta` da un aviso A-03, no un incumplimiento. R-03 ya no puede dar incumplimiento.

### DI-3. Verificación de seguridad negativa y cambio aplicado

**Sección:** §6.1, `verificacion_seguridad.resultado`.

**Duda:** el art. 17.1.a) pide verificar que el cambio cumple los requisitos de seguridad. El modelo recoge el resultado (`cumple` o `no_cumple`), pero no dice qué pasa si la verificación da `no_cumple` y el cambio se aplica igual.

**Qué hace el código (R-11):** con `no_cumple` y `implantacion.resultado` `aplicado`, aviso A-03 que remite a esta duda. La verificación se hizo, que es lo que pide el texto. Que no se deba aplicar un cambio que no la supera es una lectura propia.

### DI-4. Pruebas previas en los cambios de emergencia del régimen completo

**Sección:** §7.1, §9 y §13 («Probar antes de producción»).

**Duda:** el §13 dice que, en el régimen completo, la aprobación antes de producción «queda exceptuada por los cambios de emergencia del art. 17.1.f) y g)». No dice lo mismo de las pruebas. El art. 16.2 pide probar «antes de su uso», pero un procedimiento de emergencia (art. 17.1.f) podría prever pruebas reducidas o posteriores.

**Qué hace el código (R-14):** en el completo, un cambio de emergencia sin ninguna prueba anterior a `implantacion.inicio` da un aviso A-03 que remite a esta duda.

En el simplificado, la misma situación sí es incumplimiento, porque el art. 37.b) literal no prevé excepción. La D-5 documenta la lectura alternativa.

### DI-5. ¿Toda prueba de un tipo es obligatoria en cada cambio?

**Sección:** §7.1, `pruebas[].tipo`.

**Duda:** la columna «Completo» de `tipo` dice «exige»: el tipo es un dato exigible. Pero el modelo no dice si cada cambio debe tener una prueba de cada tipo. Por ejemplo, una prueba de seguridad de paquetes (art. 16.4) en todo cambio de software. Tampoco recoge si un sistema está expuesto a internet (art. 16.3).

**Qué hace el código (R-15):** se comprueba solo el momento de las pruebas de seguridad de paquetes que haya: «a más tardar en la fase de integración». Eso lo sostiene el texto. Si no hay ninguna, el resultado es `no_aplica`, con el motivo. No se da por cumplido. La exigencia de pruebas de seguridad de los sistemas expuestos a internet no se implementa.

### DI-6. Revisión posterior «pendiente»

**Sección:** §9, `revision_posterior`.

**Duda:** el modelo dice que los pasos de la revisión posterior son `null` «mientras no se hayan hecho», y que entonces «el registro queda pendiente». No dice si «pendiente» es un incumplimiento o un estado propio.

**Qué hace el código (R-27):** aviso A-03 que remite a esta duda. El art. 17.1.g) pide la revisión «tras su aplicación» sin fijar plazo, así que un paso aún no hecho no es un incumplimiento que sostenga el texto. Un paso hecho antes de la aplicación sí lo es.

### DI-7. El ejemplo del §1.2 verificaba antes de implantar (resuelta)

**Sección:** §1.2.

**Contradicción:** el §1.2 mostraba solo los campos que cambiaban respecto del §1.1. Compuesto así, conservaba una `verificacion_posterior` anterior a la implantación de emergencia, contra el §10.

**Resolución:** el modelo corrigió el ejemplo en `main` (commit «Modelo de datos: solo es incumplimiento lo que sostiene el texto; corregir el ejemplo del §1.2»). Ahora el fragmento incluye `verificacion_posterior` y `acciones` con fechas coherentes. El ejemplo da R-23 en el simplificado, por el art. 37.b), y nada más. Los tests lo comprueban leyendo el ejemplo del propio documento.

### DI-8. «Lista no vacía»: ¿error de entrada o requisito?

**Sección:** §2, §4, §6.3, §7.1 y §7.2.

**Duda:** el modelo dice «lista no vacía» en sitios de distinta naturaleza:
- en los pasos (§2: «`actores` es una lista no vacía»);
- en `elementos`, `alcance.sistemas`, `controles_integridad` y `pruebas`;
- en `comunicaciones`, solo «en el completo».

No dice si una lista vacía es un error de entrada (§15) o un incumplimiento.

**Qué hace el código:**
- **Error de entrada (ERR-01):** solo las listas de actores de los pasos del §2. Por coherencia, también `verificacion_seguridad.actores`, `evaluacion.actores` y `verificacion_posterior.actores`, que el modelo tipa como «paso», y `revisiones_codigo[].tecnicas`, porque una revisión usa «una técnica o las dos» (§7.2).
- **Las demás listas vacías:** las juzga su requisito, con la base de ese requisito. Una prueba o revisión con `realizada_por` vacía da un aviso A-03 en R-03 (modelo §7.1 y §7.2).

### DI-9. Independencia sin ninguna aprobación

**Sección:** §5.2 y D-1.

**Duda:** si no hay ninguna aprobación (ni previa ni posterior de emergencia), no hay con qué comparar. El modelo no dice qué resultado da el art. 17.1.b).

**Qué hace el código (R-05):** `sin_indicio_de_incumplimiento`, nunca `cumple`, con un motivo que remite a R-23 y R-27. Son esos requisitos los que dan la falta de aprobación.

### DI-10. Verificación posterior de un cambio abortado o revertido

**Sección:** §10.

**Duda:** el §10 pide la verificación posterior sin distinguir el resultado de la implantación. No está claro qué se verifica en un cambio abortado.

**Qué hace el código (R-28):** si el cambio se abortó o se revirtió y no hay verificación, aviso A-03 que remite a esta duda. Si el cambio se aplicó, la falta de verificación es incumplimiento: lo sostienen DORA, art. 9.4.e), y el art. 38.2 («verifiquen»).

### DI-11. De qué objetos se avisa si faltan evidencias

**Sección:** §7.3.

**Duda:** el §7.3 dice que la evidencia no es exigible y que «el validador puede avisar de que falta», pero no dice de qué objetos.

**Qué hace el código (aviso A-02):**
- en los dos regímenes, de las pruebas y de los controles de integridad;
- en el completo, además, de `verificacion_seguridad` y de las revisiones de código, que el simplificado no usa.

A-02 no dice que falte nada exigible, así que no activa el código 1.
