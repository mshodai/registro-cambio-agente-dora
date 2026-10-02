# Corpus

Registros sintéticos de cambios con su resultado esperado. Lo genera `corpus/generar.py`, que comprueba cada caso con el código de `src/` antes de escribirlo. No se edita a mano.

```
python corpus/generar.py
```

Cada caso rompe un solo requisito o provoca un solo aviso, y su nombre lleva el artículo que rompe. Si el resultado es un aviso de lectura propia (A-03, modelo §0.1 bis), el nombre lleva además «aviso» y la lectura de la que sale. Parte de una base limpia (el ejemplo del §1.1 de `docs/modelo-datos.md`, con la revisión estática hecha por una persona) o de una base de emergencia (el ejemplo del §1.2). El código de salida es 1 si hay un incumplimiento o un A-03 en algún régimen. `I-02` aparece en el simplificado de todos los casos porque todos tienen revisiones de código, que el título III no exige.

| Caso | Artículo | Completo | Simplificado | Código |
|---|---|---|---|---|
| 01-base-limpia | — | — | info I-02 | 0 |
| 02-art-17-1-d-i-sin-elementos | Art. 17.1.d.i); art. 17.1, encabezado | R-02 | info I-02 | 1 |
| 03-art-21-c-art-33-b-aviso-di-2-implantador-sin-cuenta | Arts. 21.c) y 33.b); modelo §3.1; DI-2 | aviso A-03 R-03 | aviso A-03 R-03, info I-02 | 1 |
| 04-art-17-1-b-d-1-misma-persona-solicita-y-aprueba | Art. 17.1.b); D-1 | R-05 | info I-01, info I-02 | 1 |
| 05-art-17-1-b-aviso-d-1-considerando-17-misma-funcion | Art. 17.1.b); considerando 17; D-1 | aviso A-03 R-05 | info I-01, info I-02 | 1 |
| 06-art-17-1-b-aviso-d-1-aprueba-el-responsable-del-agente | Art. 17.1.b); D-1; modelo §3.2 | aviso A-03 R-05 | info I-01, info I-02 | 1 |
| 07-art-17-1-c-iv-aviso-modelo-5-1-aseguramiento-de-calidad-sin-asignar | Art. 17.1.c.iv); modelo §5.1 | aviso A-03 R-06 | info I-02 | 1 |
| 08-art-17-1-d-i-sin-objeto | Art. 17.1.d.i); dudas, DI-1 | R-07 | info I-02 | 1 |
| 09-art-17-1-d-iii-sin-resultados-esperados | Art. 17.1.d.iii) | R-09 | info I-02 | 1 |
| 10-art-17-1-d-sin-comunicaciones | Art. 17.1.d), encabezado | R-10 | info I-02 | 1 |
| 11-art-17-1-a-sin-verificacion-de-seguridad | Art. 17.1.a) | R-11 | info I-02 | 1 |
| 12-art-17-1-a-aviso-di-3-verificacion-negativa-y-aplicado | Art. 17.1.a); dudas, DI-3 | aviso A-03 R-11 | info I-02 | 1 |
| 13-dora-art-9-4-e-art-38-2-sin-evaluacion | DORA, art. 9.4.e); art. 38.2 | R-12 | R-12, info I-02 | 1 |
| 14-art-17-1-h-aviso-modelo-6-2-medidas-adicionales-sin-detallar | Art. 17.1.h); modelo §6.2 | aviso A-03 R-12 | info I-02 | 1 |
| 15-art-31-1-e-cambio-importante-sin-riesgos | Art. 31.1.e) | — | R-13, info I-02 | 1 |
| 16-art-31-1-e-aviso-modelo-4-sin-declarar-si-es-importante | Art. 31.1.e); modelo §4 | — | aviso A-03 R-13, info I-02 | 1 |
| 17-art-16-2-art-37-b-pruebas-posteriores-a-la-implantacion | Art. 16.2; art. 37.b) | R-14 | R-14, info I-02 | 1 |
| 18-art-16-2-art-37-b-sin-pruebas | Art. 16.2; art. 37.b); dudas, DI-8 | R-14 | R-14, info I-02 | 1 |
| 19-art-16-4-seguridad-de-paquetes-en-produccion | Art. 16.4 | R-15 | info I-02 | 1 |
| 20-emergencia-bien-registrada-art-37-b-simplificado-d-5 | Art. 37.b); D-5 | — | R-23, info I-02 | 1 |
| 21-art-16-5-a-datos-de-produccion-sin-excepcion | Art. 16.5.a) | R-16 | info I-02 | 1 |
| 22-art-16-6-aviso-d-4-excepcion-aprobada-solo-por-un-agente | Art. 16.6; D-4 | aviso A-03 R-16 | info I-02 | 1 |
| 23-art-16-3-aviso-modelo-7-2-sin-revision-dinamica | Art. 16.3; modelo §7.2 | aviso A-03 R-17 | info I-02 | 1 |
| 24-art-16-3-b-aviso-d-2-plan-adoptado-solo-por-un-agente | Art. 16.3.b); D-2, punto 2 | aviso A-03 R-18 | info I-02 | 1 |
| 25-art-16-3-b-hallazgo-sin-medida | Art. 16.3.b) | R-18 | info I-02 | 1 |
| 26-art-16-3-c-aviso-d-2-seguimiento-solo-por-un-agente | Art. 16.3.c); D-2, punto 3 | aviso A-03 R-19 | info I-02 | 1 |
| 27-art-16-7-aviso-d-3-codigo-sin-origen | Arts. 16.7 y 16.8; D-3 | aviso A-03 R-20 | info I-02 | 1 |
| 28-art-16-8-d-3-codigo-abierto-revisado-despues | Art. 16.8; D-3 | R-21 | info I-02 | 1 |
| 29-art-16-1-c-art-37-c-aviso-modelo-6-3-sin-controles-de-integridad | Art. 16.1.c); art. 37.c); modelo §6.3 | aviso A-03 R-22 | aviso A-03 R-22, info I-02 | 1 |
| 30-dora-art-9-4-e-art-37-b-aprobacion-posterior-a-la-implantacion | DORA, art. 9.4.e); art. 16.2; art. 37.b) | R-23 | R-23, info I-02 | 1 |
| 31-art-37-b-aviso-d-4-aprobacion-solo-por-un-agente | Art. 37.b); D-4 | aviso A-03 R-23 | aviso A-03 R-23, info I-02 | 1 |
| 32-dora-art-9-4-e-art-37-b-sin-aprobacion | DORA, art. 9.4.e); art. 37.b); dudas, DI-9 | R-23 | R-23, info I-02 | 1 |
| 33-art-17-1-e-sin-vuelta-atras | Art. 17.1.e) | R-25 | info I-02 | 1 |
| 34-art-17-1-e-aviso-modelo-8-revertido-sin-ejecucion | Art. 17.1.e); modelo §8 | aviso A-03 R-25 | info I-02 | 1 |
| 35-art-17-1-f-aviso-modelo-9-emergencia-sin-salvaguardias | Art. 17.1.f); modelo §9 | aviso A-03 R-26 | R-23, info I-02 | 1 |
| 36-art-17-1-g-aviso-di-6-revision-posterior-pendiente | Art. 17.1.g); dudas, DI-6 | aviso A-03 R-27 | R-23, info I-02 | 1 |
| 37-art-17-1-g-reexamen-anterior-a-la-aplicacion | Art. 17.1.g) | R-27 | R-23, info I-02 | 1 |
| 38-art-17-1-g-aviso-d-4-aprobacion-posterior-solo-por-un-agente | Art. 17.1.g); D-4 | aviso A-03 R-27 | R-23, info I-02 | 1 |
| 39-dora-art-9-4-e-art-38-2-sin-verificacion-posterior | DORA, art. 9.4.e); art. 38.2 | R-28 | R-28, info I-02 | 1 |
| 40-art-17-1-c-iv-d-2-aviso-autorrevision | Art. 17.1.c.iv); D-2, punto 4 | aviso A-01 | info I-02 | 0 |
| 41-modelo-7-3-aviso-sin-evidencias | DORA, art. 9.4.e); art. 38.2; modelo, §7.3 | aviso A-02 | aviso A-02, info I-02 | 0 |
| 42-art-16-2-aviso-di-4-emergencia-sin-pruebas-previas | Art. 16.2; art. 37.b); dudas, DI-4; D-5 | aviso A-03 R-14 | R-14, R-23, info I-02 | 1 |
| 43-dora-art-9-4-e-aviso-di-10-revertido-sin-verificacion | DORA, art. 9.4.e); art. 38.2; dudas, DI-10 | aviso A-03 R-28 | aviso A-03 R-28, info I-02 | 1 |
| 44-dora-art-9-4-e-aviso-modelo-10-verificacion-anterior-a-la-implantacion | DORA, art. 9.4.e); art. 38.2; modelo §10 | aviso A-03 R-28 | aviso A-03 R-28, info I-02 | 1 |
| 45-art-21-c-art-33-b-aviso-di-8-prueba-sin-autor | Arts. 21.c) y 33.b); modelo §7.1; DI-8 | aviso A-03 R-03 | aviso A-03 R-03, info I-02 | 1 |
| 46-art-16-3-c-sin-seguimiento | Art. 16.3.c) | R-19 | info I-02 | 1 |

## Qué demuestra cada caso

- **01-base-limpia.** Base limpia, sin incumplimientos ni avisos.
- **02-art-17-1-d-i-sin-elementos.** No dice qué se cambia: incumplimiento en el completo.
- **03-art-21-c-art-33-b-aviso-di-2-implantador-sin-cuenta.** El agente que implanta no tiene cuenta. Registrar la cuenta lo pide el modelo: aviso en los dos regímenes.
- **04-art-17-1-b-d-1-misma-persona-solicita-y-aprueba.** El mismo actor solicita y aprueba: incumplimiento que sostiene el texto. En el simplificado es solo informativo.
- **05-art-17-1-b-aviso-d-1-considerando-17-misma-funcion.** Solicita otra persona de la misma función que aprueba: sin indicio, con aviso de la D-1.
- **06-art-17-1-b-aviso-d-1-aprueba-el-responsable-del-agente.** Aprueba la persona responsable del agente que implanta: sin indicio, con aviso de la D-1.
- **07-art-17-1-c-iv-aviso-modelo-5-1-aseguramiento-de-calidad-sin-asignar.** Nadie tiene asignado el aseguramiento de la calidad en el registro: sin indicio, con aviso.
- **08-art-17-1-d-i-sin-objeto.** El objeto es una cadena vacía.
- **09-art-17-1-d-iii-sin-resultados-esperados.** Faltan los resultados esperados.
- **10-art-17-1-d-sin-comunicaciones.** No se comunicaron los detalles.
- **11-art-17-1-a-sin-verificacion-de-seguridad.** No se verificaron los requisitos de seguridad.
- **12-art-17-1-a-aviso-di-3-verificacion-negativa-y-aplicado.** La verificación da no_cumple y el cambio se aplica: aviso.
- **13-dora-art-9-4-e-art-38-2-sin-evaluacion.** No se evaluó el cambio.
- **14-art-17-1-h-aviso-modelo-6-2-medidas-adicionales-sin-detallar.** Hacen falta medidas adicionales y no se dice cuáles: aviso.
- **15-art-31-1-e-cambio-importante-sin-riesgos.** Cambio importante sin evaluación de riesgos: solo simplificado.
- **16-art-31-1-e-aviso-modelo-4-sin-declarar-si-es-importante.** La entidad no declara si el cambio es importante: aviso, solo simplificado.
- **17-art-16-2-art-37-b-pruebas-posteriores-a-la-implantacion.** Todas las pruebas son posteriores a la implantación.
- **18-art-16-2-art-37-b-sin-pruebas.** No hay pruebas.
- **19-art-16-4-seguridad-de-paquetes-en-produccion.** La prueba de seguridad de paquetes se hace en producción.
- **20-emergencia-bien-registrada-art-37-b-simplificado-d-5.** Parche de emergencia bien registrado: el completo no tiene incumplimientos; el simplificado incumple el art. 37.b) literal (la D-5 documenta la lectura alternativa).
- **21-art-16-5-a-datos-de-produccion-sin-excepcion.** Una prueba fuera de producción usa datos de producción sin excepción.
- **22-art-16-6-aviso-d-4-excepcion-aprobada-solo-por-un-agente.** La excepción de datos de producción la aprueba solo un agente: aviso.
- **23-art-16-3-aviso-modelo-7-2-sin-revision-dinamica.** Ninguna revisión usa la técnica dinámica: aviso.
- **24-art-16-3-b-aviso-d-2-plan-adoptado-solo-por-un-agente.** El plan de acción lo adopta solo un agente: aviso.
- **25-art-16-3-b-hallazgo-sin-medida.** Un hallazgo sin medida en el plan de acción.
- **26-art-16-3-c-aviso-d-2-seguimiento-solo-por-un-agente.** El seguimiento lo hace solo un agente: aviso.
- **27-art-16-7-aviso-d-3-codigo-sin-origen.** El cambio incluye código y no declara su origen: aviso.
- **28-art-16-8-d-3-codigo-abierto-revisado-despues.** Código abierto revisado después de la implantación.
- **29-art-16-1-c-art-37-c-aviso-modelo-6-3-sin-controles-de-integridad.** No hay medidas contra la manipulación en el registro: sin indicio, con aviso en los dos regímenes.
- **30-dora-art-9-4-e-art-37-b-aprobacion-posterior-a-la-implantacion.** La aprobación es posterior a la implantación.
- **31-art-37-b-aviso-d-4-aprobacion-solo-por-un-agente.** Aprueba solo un agente: aviso en los dos regímenes.
- **32-dora-art-9-4-e-art-37-b-sin-aprobacion.** Sin aprobación y sin emergencia.
- **33-art-17-1-e-sin-vuelta-atras.** No hay procedimiento de vuelta atrás.
- **34-art-17-1-e-aviso-modelo-8-revertido-sin-ejecucion.** El cambio se revirtió y no consta cómo: aviso.
- **35-art-17-1-f-aviso-modelo-9-emergencia-sin-salvaguardias.** Cambio de emergencia sin salvaguardias en el registro: sin indicio, con aviso.
- **36-art-17-1-g-aviso-di-6-revision-posterior-pendiente.** Falta la aprobación posterior del cambio de emergencia: pendiente, aviso.
- **37-art-17-1-g-reexamen-anterior-a-la-aplicacion.** El reexamen es anterior a la aplicación.
- **38-art-17-1-g-aviso-d-4-aprobacion-posterior-solo-por-un-agente.** La aprobación posterior la da solo un agente: aviso.
- **39-dora-art-9-4-e-art-38-2-sin-verificacion-posterior.** No se verificó un cambio aplicado.
- **40-art-17-1-c-iv-d-2-aviso-autorrevision.** Revisa otro agente con la misma herramienta, modelo y versión que el que implanta: aviso A-01, no exige actuar.
- **41-modelo-7-3-aviso-sin-evidencias.** Una prueba sin evidencias: aviso A-02 en los dos regímenes, no exige actuar.
- **42-art-16-2-aviso-di-4-emergencia-sin-pruebas-previas.** Cambio de emergencia sin pruebas previas: aviso en el completo (DI-4); incumplimiento del art. 37.b) literal en el simplificado.
- **43-dora-art-9-4-e-aviso-di-10-revertido-sin-verificacion.** Cambio revertido sin verificación posterior: aviso en los dos regímenes.
- **44-dora-art-9-4-e-aviso-modelo-10-verificacion-anterior-a-la-implantacion.** La verificación posterior es anterior a la implantación: aviso en los dos regímenes.
- **45-art-21-c-art-33-b-aviso-di-8-prueba-sin-autor.** Una prueba no dice quién la hizo: aviso en los dos regímenes.
- **46-art-16-3-c-sin-seguimiento.** El plan de acción no tiene seguimiento.
