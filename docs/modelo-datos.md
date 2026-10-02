# Modelo de datos de entrada

Este documento define el JSON que describe **el registro de un cambio en un sistema de TIC en el que ha participado un agente de IA**. Solo describe la entrada. Qué se comprueba con ella se especificará aparte.

Siglas y fuentes (detalle y huellas en [`fuentes/FUENTES.md`](fuentes/FUENTES.md)):

- **DORA**: Reglamento (UE) 2022/2554, texto original (DO L 333 de 27.12.2022). No tiene versión consolidada con modificaciones.
- **RDel**: Reglamento Delegado (UE) 2024/1774, texto original (DO L, 2024/1774, de 25.6.2024). No tiene versión consolidada con modificaciones. Su corrección de errores de 15.5.2025 solo afecta al art. 22.d), que este modelo no usa.

Convenciones:

- Las citas van entre comillas «» y son literales.
- «Art. 17.1.d.ii» quiere decir: artículo 17, apartado 1, letra d), inciso ii). Sin sigla, el artículo es del RDel; los de DORA llevan «DORA».
- **[Decisión propia]** marca lo que no sale de los textos, sino del diseño de este proyecto.
- **[Decisión de alcance]** marca una decisión que tomó el responsable del proyecto el 2026-10-02, a la vista de las preguntas que se recogen en el §0.3.
- Las decisiones razonadas sobre lo que la norma no resuelve se citan como **D-n** (§12). Sus identificadores son estables: no se renumeran ni se reutilizan.

---

## 0. Principios

### 0.1. Los de la serie

1. **La entrada recoge hechos, no conclusiones.** **[Decisión propia]** El JSON dice quién solicitó, quién implantó y quién aprobó; qué pruebas y revisiones se hicieron, quién o qué las hizo, y con qué resultado. No dice si el cambio cumple, si las funciones son independientes ni si las pruebas fueron suficientes: eso depende del régimen y de la lectura.
2. **El régimen no forma parte de la entrada.** **[Decisión propia]** El régimen es un parámetro del cálculo, con dos valores:
   - `completo`: el art. 9.4.e) de DORA y el título II del RDel, en particular sus arts. 16 y 17;
   - `simplificado`: el art. 16 de DORA y el título III del RDel (arts. 28 a 41).

   Si una entidad está en uno u otro lo decide el art. 16.1 de DORA: «Los artículos 5 a 15 del presente Reglamento no se aplicarán a las empresas de servicios de inversión pequeñas y no interconectadas [...]». Es un hecho de la entidad, no del cambio. El mismo JSON se lee con los dos regímenes.
3. **La validación no depende del régimen.** **[Decisión propia]** Un hecho que un régimen no usa no es un error de entrada. Por ejemplo, el procedimiento de vuelta atrás de un cambio que se lee con el régimen simplificado.
4. **Los casos no resueltos se documentan, no se resuelven en silencio.** Cuando un texto admite dos lecturas, el modelo recoge los hechos que distinguen una de otra y el §12 dice qué lectura adopta y por qué.

### 0.1 bis. Qué puede concluir el validador

Estos dos principios son **[Decisión propia]** y rigen cualquier cálculo que se haga con esta entrada.

1. **Asimetría de los mecanismos (D-1).** Algunos requisitos dependen de un mecanismo de la entidad: la independencia del art. 17.1.b), las responsabilidades del art. 17.1.c), el procedimiento de emergencia del art. 17.1.f) y las medidas contra la manipulación de los arts. 16.1.c) y 37.c) (§0.3). Con ellos, el validador puede concluir «incumplimiento» o «sin indicio de incumplimiento», **nunca «cumple»**. El registro de un cambio puede probar que el mecanismo falló en ese cambio, pero no que existe (D-1).
2. **Solo es incumplimiento lo que sostiene el texto.** El validador da «incumplimiento» solo cuando la conclusión resulta del texto de la norma aplicado al registro. Cuando depende de una lectura propia, el resultado es un **aviso** que remite a ella y dice qué faltaría con esa lectura. Son lecturas propias las decisiones D-n del §12, las demás marcas **[Decisión propia]** de este documento y las dudas de implementación. Una lectura propia puede tener buenas razones, pero no tiene la autoridad del texto. Y un registro no debe darse por incumplidor por una razón que la norma no da.

Los dos principios se combinan. Si la falta de un requisito de mecanismo depende de una lectura propia, el resultado no es «incumplimiento», sino un aviso; y el requisito tampoco da «cumple», sino «sin indicio de incumplimiento». Por ejemplo, la independencia cuando solo coincide la función (D-1).

Este principio prevalece sobre lo que dicen las decisiones del §12 y los demás apartados escritos antes que él. Donde dicen que una lectura propia da «incumplimiento», que algo «no cumple» o que algo «falta», el resultado es un aviso que remite a esa lectura.

### 0.2. Las tres reglas propias de este proyecto

Estas reglas son **[Decisión propia]** y ningún cambio del modelo puede saltárselas.

1. **Cada campo se cita a su artículo y letra. Si un campo no sale de la norma, no entra, salvo que sea una decisión propia marcada como tal.** Un campo entra si un artículo exige que conste o si hace falta para aplicar un artículo a este cambio. Por ejemplo, saber si el cambio toca código fuente decide si se aplica la revisión del art. 16.3. Las tablas de cada sección dan la cita de cada campo. Lo que se ha dejado fuera, y por qué, está en el §14.
2. **Del agente de IA no se modela nada interno: ni prompts ni configuración.** No entran sus instrucciones, su contexto, sus parámetros, su razonamiento ni sus salidas intermedias. El agente es un actor más: su identidad (herramienta, modelo, versión) y sus acciones son datos del registro, como lo son las de una persona (§3, §11).
3. **Los ejemplos usan datos inventados y genéricos.** Ningún ejemplo describe un sistema, una entidad, una herramienta ni un modelo reales. Los nombres son del tipo `HERRAMIENTA-EJEMPLO`, `SISTEMA-EJEMPLO-1` u «Objeto de ejemplo (inventado)», y las evidencias son referencias opacas del tipo `EVIDENCIA-EJEMPLO-1`.

### 0.3. Alcance

**Qué es un cambio.** Es un cambio en el sentido del art. 9.4.e) de DORA y del art. 17.1: un cambio «en el software, el hardware, los componentes de firmware, los sistemas o los parámetros de seguridad». El agente de IA puede haber intervenido como solicitante, como implantador, como autor de pruebas o de revisiones, o en varias de esas tareas a la vez. El modelo admite también un cambio en el que no intervenga ningún agente, pero no está pensado para él.

**Régimen simplificado: solo lo que tiene base en el título III.** **[Decisión de alcance]** El título III no tiene un equivalente claro del art. 17:

- **Lo más parecido es el art. 38.2**, que repite, casi con las mismas palabras, el art. 9.4.e) de DORA: «todo cambio en los sistemas de TIC se registre, someta a prueba, evalúe, apruebe, aplique y verifique de manera controlada y con las salvaguardias adecuadas». No detalla ningún elemento del art. 17.1.
- **Sin equivalente.** Tampoco hay equivalente de la independencia del art. 17.1.b), del objeto, el alcance, el calendario y los resultados esperados (art. 17.1.d), de la vuelta atrás (art. 17.1.e), de los cambios de emergencia (art. 17.1.f y g) ni de la revisión de código del art. 16.3.

Con el régimen simplificado, el modelo **exige solo lo que tiene base en el título III**. Los campos que solo tienen base en los arts. 16 y 17 se aceptan, pero no se exigen, y en ese régimen no tienen base normativa. La tabla del §13 da la correspondencia completa.

**Fuera de alcance: obligaciones propias de las entidades de contrapartida central y de los depositarios centrales de valores.** **[Decisión de alcance]** El modelo no cubre dos grupos de obligaciones que dependen del tipo de entidad, no del cambio:

- el art. 17.2: «Tras la introducción de cambios significativos en sus sistemas de TIC, las entidades de contrapartida central y los depositarios centrales de valores someterán tales sistemas a pruebas estrictas mediante la simulación de condiciones de tensión», con las partes que deben asociar a esas pruebas;
- los párrafos segundo y tercero del art. 16.2, sobre las partes que esas mismas entidades deben asociar al diseño y la realización de las pruebas.

Esas entidades no pueden validar con este modelo el art. 17.2.

**Candidato para una versión posterior.** El art. 17.2 y los párrafos segundo y tercero del art. 16.2 podrían entrar en una versión posterior del modelo, con un segundo parámetro de cálculo: el tipo de entidad. Ese parámetro iría junto al régimen y, como él, fuera de la entrada, porque es un hecho de la entidad y no del cambio (§0.1, principio 2). Con él, el cambio tendría que decir si es «significativo» (art. 17.2) y recoger las pruebas de tensión y las partes asociadas a ellas.

**Requisitos de procedimiento y requisitos del registro.** Varias letras del art. 17.1 regulan el procedimiento de gestión de cambios, no cada cambio:

- la b): «mecanismos para garantizar la independencia»;
- la c): «una descripción clara de las funciones y responsabilidades»;
- la f): «procedimientos, protocolos y herramientas para gestionar los cambios de emergencia».

**[Decisión propia]** El registro no puede probar que esos procedimientos existen. Recoge los hechos de cada cambio que muestran si se aplicaron: quién hizo qué, con qué función, y si el cambio siguió el procedimiento de emergencia. Lo mismo vale para los arts. 16.1 y 37.c), que piden especificar medidas contra la alteración o la manipulación: el registro recoge las medidas aplicadas a este cambio (§6.3).

---

## 1. Ejemplos

### 1.1. Cambio ordinario implantado por un agente

Un cambio en el software de un sistema. Lo solicita una persona de una función de negocio. Lo implanta un agente de IA del que responde una persona de la función de desarrollo. El mismo agente hace una revisión de código, y una persona de la función de desarrollo hace otra. Lo aprueba una persona de otra función. Todo es inventado. Con el régimen completo, la revisión `RC-1` cuenta para el art. 16.3, pero da un aviso de autorrevisión, porque la hace el agente que implanta (D-2, punto 4).

```json
{
  "version_modelo": 1,
  "actores": [
    { "id": "P-1", "tipo": "persona", "funcion": "FUNCION-NEGOCIO-EJEMPLO", "cuenta": "CUENTA-EJEMPLO-1" },
    { "id": "P-2", "tipo": "persona", "funcion": "FUNCION-APROBACION-EJEMPLO", "cuenta": "CUENTA-EJEMPLO-2" },
    { "id": "P-3", "tipo": "persona", "funcion": "FUNCION-DESARROLLO-EJEMPLO", "cuenta": "CUENTA-EJEMPLO-3" },
    {
      "id": "AG-1",
      "tipo": "agente_ia",
      "funcion": "FUNCION-DESARROLLO-EJEMPLO",
      "cuenta": "CUENTA-EJEMPLO-4",
      "herramienta": "HERRAMIENTA-EJEMPLO",
      "modelo": "MODELO-EJEMPLO",
      "version": "0.0-ejemplo",
      "persona_responsable": "P-3"
    }
  ],
  "cambio": {
    "id": "CAMBIO-EJEMPLO-1",
    "elementos": ["software"],
    "objeto": "Objeto de ejemplo 1 (inventado)",
    "alcance": {
      "descripcion": "Alcance de ejemplo 1 (inventado)",
      "sistemas": ["SISTEMA-EJEMPLO-1"]
    },
    "calendario": {
      "inicio_previsto": "2026-11-09T09:00:00+01:00",
      "fin_previsto": "2026-11-09T12:00:00+01:00"
    },
    "resultados_esperados": "Resultado esperado de ejemplo 1 (inventado)",
    "comunicaciones": [
      { "fecha": "2026-11-04T10:00:00+01:00", "destinatarios": "Destinatarios de ejemplo (inventados)" }
    ],
    "incluye_codigo_fuente": true,
    "origen_codigo": ["desarrollo_interno"],
    "cambio_importante": false,
    "solicitud": { "actores": ["P-1"], "fecha": "2026-11-02T09:30:00+01:00" },
    "responsabilidades": {
      "especificacion_planificacion": ["P-1", "P-3"],
      "diseno_transicion": ["P-3"],
      "pruebas_ultimacion": ["P-3"],
      "aseguramiento_calidad": ["P-3"]
    },
    "verificacion_seguridad": {
      "actores": ["P-3"],
      "fecha": "2026-11-05T16:00:00+01:00",
      "resultado": "cumple",
      "evidencias": [{ "referencia": "EVIDENCIA-EJEMPLO-1", "descripcion": "Evidencia de ejemplo (inventada)" }]
    },
    "evaluacion": {
      "actores": ["P-3"],
      "fecha": "2026-11-05T16:30:00+01:00",
      "repercusion_seguridad": "Repercusión de ejemplo (inventada)",
      "requiere_medidas_adicionales": false,
      "medidas_adicionales": [],
      "riesgos": null
    },
    "controles_integridad": [
      { "descripcion": "Control de ejemplo 1 (inventado)", "evidencias": [{ "referencia": "EVIDENCIA-EJEMPLO-2", "descripcion": null }] }
    ],
    "pruebas": [
      {
        "id": "PR-1",
        "tipo": "idoneidad",
        "descripcion": "Prueba de ejemplo 1 (inventada)",
        "realizada_por": ["AG-1"],
        "fecha": "2026-11-05T11:00:00+01:00",
        "fase": "integracion",
        "entorno": "no_produccion",
        "datos": "sin_datos_produccion",
        "excepcion_datos_produccion": null,
        "resultado": "superada",
        "evidencias": [{ "referencia": "EVIDENCIA-EJEMPLO-3", "descripcion": null }]
      },
      {
        "id": "PR-2",
        "tipo": "seguridad_paquetes",
        "descripcion": "Prueba de ejemplo 2 (inventada)",
        "realizada_por": ["P-3"],
        "fecha": "2026-11-05T12:00:00+01:00",
        "fase": "integracion",
        "entorno": "no_produccion",
        "datos": "sin_datos_produccion",
        "excepcion_datos_produccion": null,
        "resultado": "superada",
        "evidencias": [{ "referencia": "EVIDENCIA-EJEMPLO-4", "descripcion": null }]
      }
    ],
    "revisiones_codigo": [
      {
        "id": "RC-1",
        "realizada_por": ["AG-1"],
        "fecha": "2026-11-05T13:00:00+01:00",
        "tecnicas": ["estatica"],
        "hallazgos": [{ "id": "H-1", "descripcion": "Hallazgo de ejemplo 1 (inventado)" }],
        "plan_accion": {
          "adoptado_por": ["P-3"],
          "fecha": "2026-11-05T14:00:00+01:00",
          "medidas": [{ "hallazgos": ["H-1"], "descripcion": "Medida de ejemplo 1 (inventada)" }]
        },
        "seguimiento": [
          { "actores": ["P-3"], "fecha": "2026-11-05T15:30:00+01:00", "estado": "completado", "descripcion": null }
        ],
        "evidencias": [{ "referencia": "EVIDENCIA-EJEMPLO-5", "descripcion": null }]
      },
      {
        "id": "RC-2",
        "realizada_por": ["P-3"],
        "fecha": "2026-11-05T15:00:00+01:00",
        "tecnicas": ["dinamica"],
        "hallazgos": [],
        "plan_accion": null,
        "seguimiento": [],
        "evidencias": [{ "referencia": "EVIDENCIA-EJEMPLO-6", "descripcion": null }]
      }
    ],
    "vuelta_atras": {
      "responsables": ["P-3"],
      "procedimiento": "Procedimiento de ejemplo (inventado)",
      "ejecucion": null
    },
    "aprobacion": { "actores": ["P-2"], "fecha": "2026-11-06T10:00:00+01:00" },
    "emergencia": null,
    "implantacion": {
      "actores": ["AG-1"],
      "inicio": "2026-11-09T09:05:00+01:00",
      "fin": "2026-11-09T09:40:00+01:00",
      "resultado": "aplicado"
    },
    "verificacion_posterior": {
      "actores": ["P-3"],
      "fecha": "2026-11-09T11:00:00+01:00",
      "resultado": "conforme",
      "descripcion": null
    },
    "acciones": [
      { "actor": "AG-1", "fecha": "2026-11-09T09:05:00+01:00", "etapa": "implantacion", "descripcion": "Acción de ejemplo 1 (inventada)" },
      { "actor": "AG-1", "fecha": "2026-11-09T09:40:00+01:00", "etapa": "implantacion", "descripcion": "Acción de ejemplo 2 (inventada)" }
    ]
  }
}
```

### 1.2. Parche de emergencia aplicado por un agente

Un parche aplicado fuera de horario por el procedimiento de emergencia, sin aprobación previa y con revisión y aprobación posteriores (art. 17.1.g). Solo se muestra `cambio.emergencia` y los campos que cambian respecto del §1.1. Los demás serían como allí.

```json
{
  "aprobacion": null,
  "emergencia": {
    "tipo": "parche",
    "motivo": "Motivo de ejemplo (inventado)",
    "procedimiento": "Procedimiento de emergencia de ejemplo (inventado)",
    "salvaguardias": "Salvaguardias de ejemplo (inventadas)",
    "revision_posterior": {
      "documentacion": { "actores": ["P-3"], "fecha": "2026-11-10T09:00:00+01:00" },
      "reexamen": { "actores": ["P-3"], "fecha": "2026-11-10T10:00:00+01:00" },
      "evaluacion": { "actores": ["P-2"], "fecha": "2026-11-10T11:00:00+01:00" },
      "aprobacion": { "actores": ["P-2"], "fecha": "2026-11-10T12:00:00+01:00" }
    }
  },
  "implantacion": {
    "actores": ["AG-1"],
    "inicio": "2026-11-09T23:10:00+01:00",
    "fin": "2026-11-09T23:25:00+01:00",
    "resultado": "aplicado"
  },
  "verificacion_posterior": {
    "actores": ["P-3"],
    "fecha": "2026-11-09T23:40:00+01:00",
    "resultado": "conforme",
    "descripcion": null
  },
  "acciones": [
    { "actor": "AG-1", "fecha": "2026-11-09T23:10:00+01:00", "etapa": "implantacion", "descripcion": "Acción de ejemplo 1 (inventada)" },
    { "actor": "AG-1", "fecha": "2026-11-09T23:25:00+01:00", "etapa": "implantacion", "descripcion": "Acción de ejemplo 2 (inventada)" }
  ]
}
```

`verificacion_posterior` se repite porque debe ser posterior a la implantación (§10), y la del §1.1 es anterior a la de emergencia. `acciones` se repite porque las del §1.1 describen una implantación hecha por la mañana, no esta.

---

## 2. Campos de primer nivel

| Campo | Tipo | Obligatorio | Descripción y cita |
|---|---|---|---|
| `version_modelo` | entero | sí | Versión de este esquema. Es `1`. **[Decisión propia]** |
| `actores` | lista | sí | Todas las personas y agentes de IA que aparecen en el cambio. Ver §3. |
| `cambio` | objeto | sí | El cambio. Ver §4 a §11. |

No hay campo de régimen (§0.1, principio 2). Un JSON con `regimen`, o con cualquier otro campo que el modelo no define, es un error de validación (§15).

**Fechas.** Todas son fecha y hora en ISO 8601 con desfase horario (`2026-11-09T09:05:00+01:00`). **[Decisión propia]** Varias reglas dependen del orden de dos hechos que pueden ocurrir el mismo día:

- la aprobación y la prueba deben ser anteriores a la introducción en producción (art. 37.b);
- la revisión de un cambio de emergencia es posterior a su aplicación (art. 17.1.g);
- la revisión de código de software de terceros es anterior a la implantación en producción (art. 16.8).

El art. 12.2.f) pide sincronizar los relojes «con una fuente de tiempo de referencia fiable y documentada», así que la hora es un dato que la entidad tiene.

**Columnas «Completo» y «Simplificado» de las tablas siguientes.** Dicen si el régimen **exige** el dato:

- «exige»: el régimen lo exige;
- «si …»: lo exige con una condición;
- «—»: no lo exige. El campo se acepta igualmente (§0.1, principio 3).

Que un campo sea «obligatorio» en el JSON es otra cosa: quiere decir que debe estar presente, aunque sea con `null` o una lista vacía. Así, un registro incompleto se distingue de uno mal formado.

**Pasos con actores y fecha.** Muchos campos describen un paso del cambio con la forma `{ "actores": [ids], "fecha": … }`. `actores` es una lista no vacía de `id` de `actores`. La misma forma se usa en todos los pasos para que la independencia y la autoría se comparen igual en todos (D-1). **[Decisión propia]**

---

## 3. Actores: `actores[]`

Un actor es una persona o un agente de IA. El agente es un **tipo de actor propio**, no un atributo de una persona ni una herramienta usada por ella. Cualquier paso del cambio (solicitar, implantar, aprobar, probar, revisar) puede tener como actor una persona o un agente. Si eso cumple o no lo dice el régimen con la lectura del §12.

### 3.1. Campos comunes

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `id` | cadena | sí | — | — | Identificador dentro del registro. **[Decisión propia]** Técnico: no añade hechos. |
| `tipo` | `persona` \| `agente_ia` | sí | exige | exige | Art. 20.1: la gestión de la identidad debe garantizar «la identificación y autenticación únicas de las personas físicas y los sistemas». El modelo distingue a las personas de los agentes porque el §12 los trata distinto (D-1, D-2, D-4). |
| `funcion` | cadena | sí | exige | — | La función de la entidad a la que pertenece el actor o en cuyo nombre actúa. Art. 17.1.b): independencia de «las funciones que aprueban los cambios y las funciones responsables de solicitar y aplicar dichos cambios». Considerando 17: «las funciones responsables de aprobar dichos cambios estén separadas de las funciones que los soliciten e implementen». En el simplificado no hay requisito de independencia (§13). Valor libre declarado por la entidad. |
| `cuenta` | cadena \| `null` | sí | exige | exige | La cuenta con la que el actor actuó en los sistemas de TIC. Art. 21.c): que «en todo momento, los usuarios sean identificables cuando realicen acciones en los sistemas de TIC». Art. 20.2.a): «una identidad única correspondiente a una cuenta de usuario única». Simplificado, art. 33.b): «la identificación de los usuarios en las acciones realizadas en los sistemas de TIC». Puede ser `null` si el actor no actuó en ningún sistema; por ejemplo, quien solo solicita. |

### 3.2. Campos propios del agente de IA (`tipo` `agente_ia`)

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `herramienta` | cadena | sí | exige | exige | Nombre de la herramienta o el producto con el que actúa el agente. |
| `modelo` | cadena | sí | exige | exige | Identificador del modelo de IA que usa el agente. |
| `version` | cadena | sí | exige | exige | Versión de la herramienta o del modelo con que se hizo el cambio. |
| `persona_responsable` | `id` de una persona | sí | exige | exige | La persona que responde de lo que hace el agente en este cambio. |

**Cita de los cuatro campos.** **[Decisión propia]**, apoyada en el art. 20.1 («identificación [...] únicas de las personas físicas y los sistemas») y, en el simplificado, en el art. 33.b). La norma pide que el actor sea identificable, pero no dice cómo se identifica un agente de IA:

- **Herramienta, modelo y versión.** El modelo usa estos tres datos porque juntos distinguen un agente de otro, y uno de sí mismo en otra versión. Son datos de identidad, no de funcionamiento (§0.2, regla 2).
- **`persona_responsable`.** **[Decisión propia]**, apoyada en el art. 17.1.c) («una descripción clara de las funciones y responsabilidades»), en el art. 19.a) («la determinación y asignación de toda responsabilidad específica en materia de seguridad de las TIC») y, en el simplificado, en el art. 28.2.b) («defina claramente las funciones y responsabilidades para todas las tareas relacionadas con las TIC»). Un agente no puede ser titular de una responsabilidad. El modelo la atribuye a una persona y usa ese dato en D-1, D-2 y D-4.

`persona_responsable` debe ser el `id` de un actor de `tipo` `persona`. Un actor `persona` no lleva ninguno de estos cuatro campos.

---

## 4. Descripción del cambio

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `id` | cadena | sí | — | — | Identificador del cambio en la entidad. **[Decisión propia]** |
| `elementos` | lista de `software` \| `hardware` \| `firmware` \| `sistema` \| `parametros_seguridad` | sí | exige | — | Qué se cambia. Art. 17.1, encabezado, y DORA, art. 9.4.e): «los cambios en el software, el hardware, los componentes de firmware, los sistemas o los parámetros de seguridad». El art. 38.2 habla de «todo cambio en los sistemas de TIC», sin distinguir. Lista no vacía. |
| `objeto` | cadena | sí | exige | — | Para qué se hace el cambio. Art. 17.1.d.i): «el objeto y alcance de los cambios». Es lo que el encargo llama «propósito»: el campo usa la palabra de la norma. |
| `alcance.descripcion` | cadena | sí | exige | — | Art. 17.1.d.i). |
| `alcance.sistemas` | lista de cadenas | sí | exige | — | Los sistemas de TIC afectados. Art. 17.1.d.i), «alcance». Lista no vacía. |
| `calendario.inicio_previsto`, `calendario.fin_previsto` | fecha y hora | sí | exige | — | Art. 17.1.d.ii): «el calendario para la aplicación de los cambios». Las fechas reales están en `implantacion` (§5.2). |
| `resultados_esperados` | cadena | sí | exige | — | Art. 17.1.d.iii): «los resultados esperados». |
| `comunicaciones` | lista | sí | exige | — | Cada comunicación de los detalles del cambio, con `fecha` y `destinatarios` (cadena). Art. 17.1.d), encabezado: «la documentación y comunicación de los detalles de los cambios». Lista no vacía en el completo. |
| `incluye_codigo_fuente` | booleano | sí | exige | — | Si el cambio modifica código fuente. Hace falta para aplicar el art. 16.3 («revisiones de códigos fuente») y el art. 16.7 («controles para proteger la integridad del código fuente»). Un cambio de parámetros puede no tenerlo. |
| `origen_codigo` | lista de `desarrollo_interno` \| `proveedor_tercero` \| `software_propietario` \| `codigo_abierto` | sí | si `incluye_codigo_fuente` | — | De dónde procede el código del cambio. Art. 16.7: código «desarrollado internamente o desarrollado y entregado a la entidad financiera por un proveedor tercero». Art. 16.8: «el software propietario y, cuando sea factible, el código fuente proporcionado por proveedores terceros [...] o procedente de proyectos de código abierto». Lo declara la entidad. Para el código que escribe un agente, ver D-3. |
| `cambio_importante` | booleano \| `null` | sí | — | exige | Si la entidad considera el cambio «importante». Simplificado, art. 31.1.e): la evaluación de «todo riesgo [...] que sea consecuencia de un cambio importante en los sistemas de TIC». Lo declara la entidad, porque la norma no define «importante». En el completo no se usa y puede ser `null`. |

---

## 5. Solicitud, responsabilidades, implantación y aprobación

### 5.1. Quién solicita y las responsabilidades

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `solicitud` | paso | sí | exige | — | Quién solicitó el cambio y cuándo. Art. 17.1.b): «las funciones responsables de solicitar». En el simplificado no se exige un solicitante identificado. El art. 38.2 empieza en «se registre». |
| `responsabilidades.especificacion_planificacion` | lista de `id` | sí | exige | — | Art. 17.1.c.i): «la especificación y planificación de los cambios». |
| `responsabilidades.diseno_transicion` | lista de `id` | sí | exige | — | Art. 17.1.c.ii): «el diseño de una transición adecuada». |
| `responsabilidades.pruebas_ultimacion` | lista de `id` | sí | exige | — | Art. 17.1.c.iii): «el sometimiento a prueba y la ultimación de los cambios de manera controlada». |
| `responsabilidades.aseguramiento_calidad` | lista de `id` | sí | exige | — | Art. 17.1.c.iv): «la existencia de un aseguramiento eficaz de la calidad». |

Las cuatro listas de `responsabilidades` dicen quién tenía asignada cada responsabilidad en este cambio. **[Decisión propia]**: el art. 17.1.c) pide describir las funciones y responsabilidades en el procedimiento, y el registro recoge a quién se asignaron (§0.3). Si un agente figura en una de ellas, la responsabilidad se atribuye a su `persona_responsable` (§3.2).

En el simplificado, el art. 38.1 pide especificar «las funciones y responsabilidades» del procedimiento de gestión de proyectos, no del de cambios, y el art. 28.2.b) las pide «para todas las tareas relacionadas con las TIC», sin desglosarlas. Ninguno de los dos pide las cuatro del art. 17.1.c).

### 5.2. Quién implanta y quién aprueba

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `implantacion.actores` | lista de `id` | sí | exige | exige | Quién aplicó el cambio. Art. 17.1.b): «las funciones responsables de [...] aplicar dichos cambios». DORA, art. 9.4.e): que los cambios se «apliquen». Simplificado, art. 38.2: que se «aplique». |
| `implantacion.inicio`, `implantacion.fin` | fecha y hora | sí | exige | exige | Cuándo se introdujo el cambio en producción. Hace falta para comprobar el orden que piden el art. 37.b) («antes de introducir cambios en el entorno de producción») y el art. 17.1.g) («tras su aplicación»). `fin` puede ser `null` si el cambio se abortó antes de terminar. |
| `implantacion.resultado` | `aplicado` \| `abortado` \| `revertido` | sí | exige | exige | Art. 17.1.e): «abortar un cambio o recuperarse de un cambio que no se ha ejecutado correctamente». DORA, art. 9.4.e), y art. 38.2: que el cambio se «aplique» y «verifique». |
| `aprobacion` | paso \| `null` | sí | exige | exige | Quién aprobó el cambio antes de aplicarlo. Art. 17.1.b): «las funciones que aprueban los cambios». DORA, art. 9.4.e): que se «aprueben». Simplificado, art. 37.b): que los sistemas «sean aprobados [...] antes de introducir cambios en el entorno de producción», y art. 38.2. Es `null` solo en un cambio de emergencia sin aprobación previa (§9). |

Quién solicita, quién implanta y quién aprueba son **tres campos distintos**: `solicitud.actores`, `implantacion.actores` y `aprobacion.actores`. Pueden repetir el mismo `id`. El modelo no lo impide, porque es un hecho (§0.1, principio 1). Qué significa que se repita se trata en D-1.

---

## 6. Seguridad del cambio

### 6.1. Verificación de los requisitos de seguridad: `verificacion_seguridad`

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `verificacion_seguridad` | objeto \| `null` | sí | exige | — | Art. 17.1.a): «la verificación del cumplimiento de los requisitos de seguridad de las TIC». Considerando 17: «un riguroso proceso de verificación que permita confirmar que todos los cambios cumplen los requisitos necesarios en materia de seguridad de las TIC». |
| `.actores`, `.fecha` | paso | sí | exige | — | Art. 17.1.a). |
| `.resultado` | `cumple` \| `no_cumple` | sí | exige | — | Art. 17.1.a). |
| `.evidencias` | lista de evidencias | sí | — | — | **[Decisión propia]** (§7.3). |

En el simplificado, el art. 37.a) pide especificar y aprobar los requisitos de seguridad de la información «antes de la adquisición o el desarrollo de un sistema de TIC», no verificar que cada cambio los cumple.

### 6.2. Evaluación del cambio: `evaluacion`

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `evaluacion` | objeto \| `null` | sí | exige | exige | DORA, art. 9.4.e), y simplificado, art. 38.2: que el cambio se «evalúe». |
| `.actores`, `.fecha` | paso | sí | exige | exige | Las mismas citas. |
| `.repercusion_seguridad` | cadena \| `null` | sí | exige | — | Art. 17.1.h): «la determinación de las posibles repercusiones de un cambio sobre las medidas de seguridad de las TIC vigentes». |
| `.requiere_medidas_adicionales` | booleano \| `null` | sí | exige | — | Art. 17.1.h): «la evaluación de si dicho cambio requiere la adopción de medidas de seguridad de las TIC adicionales». |
| `.medidas_adicionales` | lista de cadenas | sí | si `requiere_medidas_adicionales` | — | Art. 17.1.h). |
| `.riesgos` | cadena \| `null` | sí | — | si `cambio_importante` | Simplificado, art. 31.1.e): «la determinación y evaluación de todo riesgo relacionado con las TIC y la seguridad de la información que sea consecuencia de un cambio importante». |

**Un solo objeto para «evalúe» en los dos regímenes.** **[Decisión propia]** DORA y el art. 38.2 dicen que el cambio se «evalúe», pero no dicen qué se evalúa. Cada régimen lo concreta con un artículo distinto:

- en el completo, el art. 17.1.h): la repercusión en la seguridad;
- en el simplificado, el art. 31.1.e): los riesgos, si el cambio es importante.

Un solo objeto, con un campo para cada concreción, evita que la misma evaluación figure dos veces.

### 6.3. Protección frente a la alteración o la manipulación: `controles_integridad`

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `controles_integridad` | lista | sí | exige | exige | Las medidas aplicadas en este cambio contra la alteración o la manipulación, cada una con `descripcion` y `evidencias`. Art. 16.1.c): «medidas para mitigar el riesgo de alteración no intencionada o de manipulación intencionada de los sistemas de TIC durante su desarrollo, mantenimiento e implementación en el entorno de producción». Si `incluye_codigo_fuente`, también art. 16.7: «controles para proteger la integridad del código fuente». Simplificado, art. 37.c): «medidas para mitigar el riesgo de alteración no intencionada o de manipulación intencionada de los sistemas de TIC durante el desarrollo y la implementación en el entorno de producción». Lista no vacía. |

El art. 16.1.c) y el art. 37.c) piden que la política o el procedimiento **determinen** las medidas. El registro recoge las que se aplicaron a este cambio (§0.3). Un control puede afectar al propio agente, por ejemplo la limitación de los permisos de su cuenta. Se describe como cualquier otro control, sin modelar la configuración del agente (§0.2, regla 2).

---

## 7. Pruebas y revisiones de código

### 7.1. Pruebas: `pruebas[]`

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `pruebas` | lista | sí | exige | exige | DORA, art. 9.4.e): que los cambios se «sometan a prueba». Art. 16.2: «la prueba y aprobación de todos los sistemas de TIC antes de su uso y después del mantenimiento». Simplificado, art. 37.b): que «se sometan a prueba [...] antes de introducir cambios en el entorno de producción», y art. 38.2. Lista no vacía. |
| `.id` | cadena | sí | — | — | **[Decisión propia]** Técnico. |
| `.tipo` | `idoneidad` \| `calidad_software` \| `seguridad_expuesto_internet` \| `seguridad_paquetes` \| `otra` | sí | exige | — | Art. 16.2: pruebas para «verificar la idoneidad de los nuevos sistemas de TIC para funcionar según lo previsto, así como la calidad del software desarrollado internamente». Art. 16.3: «pruebas de seguridad de los sistemas y aplicaciones expuestos a internet». Art. 16.4: «pruebas de seguridad de los paquetes de software a más tardar en la fase de integración». `otra`: cualquier otra prueba. |
| `.descripcion` | cadena | sí | — | — | **[Decisión propia]** Texto libre. |
| `.realizada_por` | lista de `id` | sí | exige | exige | Quién o qué hizo la prueba. Art. 21.c) y, en el simplificado, art. 33.b): los usuarios identificables en sus acciones. Art. 17.1.c.iii): la responsabilidad de las pruebas. |
| `.fecha` | fecha y hora | sí | exige | exige | Art. 37.b): «antes de introducir cambios en el entorno de producción». Art. 16.2: «antes de su uso». |
| `.fase` | `desarrollo` \| `integracion` \| `preproduccion` \| `produccion` | sí | si `tipo` es `seguridad_paquetes` | — | Art. 16.4: «a más tardar en la fase de integración». |
| `.entorno` | `produccion` \| `no_produccion` | sí | exige | — | Art. 16.5: el procedimiento rige los datos de «los entornos distintos del de producción». |
| `.datos` | `sin_datos_produccion` \| `produccion_anonimizados` \| `produccion` | sí | si `entorno` es `no_produccion` | — | Art. 16.5.a): «los entornos distintos del de producción únicamente almacenarán datos de producción anonimizados, seudonimizados o aleatorizados». `produccion_anonimizados` abarca las tres técnicas. |
| `.excepcion_datos_produccion` | objeto \| `null` | sí | si `datos` es `produccion` en `no_produccion` | — | Art. 16.6: los datos de producción pueden usarse «únicamente para la realización de pruebas específicas, durante un tiempo limitado y previa aprobación de la función pertinente», y las pruebas se notifican «a la función de gestión del riesgo relacionado con las TIC». Campos: `aprobacion` (paso), `hasta` (fecha y hora) y `notificacion_funcion_riesgo_tic` (fecha y hora). |
| `.resultado` | `superada` \| `no_superada` | sí | exige | exige | DORA, art. 9.4.e), y art. 38.2: que el cambio se «verifique» de forma controlada. Art. 16.2: las pruebas verifican la idoneidad. |
| `.evidencias` | lista de evidencias | sí | — | — | **[Decisión propia]** (§7.3). |

### 7.2. Revisiones de código: `revisiones_codigo[]`

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `revisiones_codigo` | lista | sí | si `incluye_codigo_fuente` | — | Art. 16.3: el procedimiento «incluirá la realización de revisiones de códigos fuente que abarquen pruebas tanto estáticas como dinámicas». Art. 16.8: el código de terceros y el de código abierto se analizan y prueban «de conformidad con el apartado 3 antes de su implementación en el entorno de producción». El título III no tiene revisión de código (§13). |
| `.id` | cadena | sí | — | — | **[Decisión propia]** Técnico. |
| `.realizada_por` | lista de `id` | sí | exige | — | Quién o qué hizo la revisión: una persona, un agente o los dos. Si un agente cuenta como revisor se trata en D-2. |
| `.fecha` | fecha y hora | sí | exige | — | Art. 16.8: «antes de su implementación en el entorno de producción». |
| `.tecnicas` | lista de `estatica` \| `dinamica` | sí | exige | — | Art. 16.3: «pruebas tanto estáticas como dinámicas». Una revisión puede usar una técnica o las dos. Entre todas las del cambio deben estar las dos. |
| `.hallazgos` | lista | sí | exige | — | Cada vulnerabilidad o anomalía, con `id` y `descripcion`. Art. 16.3.a): «identificar y analizar las vulnerabilidades y anomalías en el código fuente». Puede estar vacía. |
| `.plan_accion` | objeto \| `null` | sí | si hay `hallazgos` | — | Art. 16.3.b): «adoptar un plan de acción para hacer frente a esas vulnerabilidades y anomalías». Campos: `adoptado_por` (lista de `id`), `fecha` y `medidas` (lista de `{ hallazgos: [ids], descripcion }`). Quién puede adoptarlo se trata en D-2. |
| `.seguimiento` | lista | sí | si hay `plan_accion` | — | Art. 16.3.c): «hacer un seguimiento de la aplicación de dicho plan de acción». Cada entrada tiene `actores`, `fecha`, `estado` (`pendiente` \| `completado`) y `descripcion`. |
| `.evidencias` | lista de evidencias | sí | — | — | **[Decisión propia]** (§7.3). |

### 7.3. Evidencias

Una evidencia es `{ "referencia": cadena, "descripcion": cadena | null }`. La `referencia` apunta a donde la entidad guarda la evidencia y el modelo no la interpreta.

**[Decisión propia]** Ningún artículo pide adjuntar la evidencia de cada prueba o revisión. El modelo la recoge porque el art. 9.4.e) de DORA y el art. 38.2 piden que el cambio se registre, pruebe y verifique «de forma controlada», y sin evidencia no se puede comprobar que lo que se registra ocurrió. Por eso no es exigible en ningún régimen: el validador puede avisar de que falta, pero no tratarlo como incumplimiento.

---

## 8. Vuelta atrás: `vuelta_atras`

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `vuelta_atras` | objeto \| `null` | sí | exige | — | Art. 17.1.e): «la determinación de responsabilidades y procedimientos alternativos, en particular responsabilidades y procedimientos para abortar un cambio o recuperarse de un cambio que no se ha ejecutado correctamente». |
| `.responsables` | lista de `id` | sí | exige | — | Art. 17.1.e), «responsabilidades». Considerando 17: «asignar responsabilidades con el fin de garantizar una respuesta rápida y eficaz». |
| `.procedimiento` | cadena | sí | exige | — | Art. 17.1.e), «procedimientos». Descripción o referencia al procedimiento previsto para este cambio. |
| `.ejecucion` | objeto \| `null` | sí | si `implantacion.resultado` es `abortado` o `revertido` | — | Si se ejecutó: `actores`, `fecha` y `motivo`. Art. 17.1.e). |

En el simplificado no hay equivalente. El art. 39 regula los planes de continuidad de la actividad, no la vuelta atrás de un cambio.

---

## 9. Cambio de emergencia: `emergencia`

`emergencia` es `null` si el cambio no siguió el procedimiento de emergencia. Si es un objeto, el cambio es de emergencia.

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `emergencia` | objeto \| `null` | sí | exige | — | Art. 17.1.f): «procedimientos, protocolos y herramientas para gestionar los cambios de emergencia que ofrezcan las salvaguardias adecuadas». |
| `.tipo` | `cambio` \| `solucion_alternativa` \| `parche` | sí | exige | — | Art. 17.1.g): «los cambios de emergencia tras su aplicación, incluidas las soluciones alternativas y los parches». |
| `.motivo` | cadena | sí | — | — | **[Decisión propia]** Por qué se usó el procedimiento de emergencia. La norma no lo pide, pero sin el motivo no se puede reexaminar el cambio (art. 17.1.g). |
| `.procedimiento` | cadena | sí | exige | — | Art. 17.1.f), «procedimientos, protocolos y herramientas». |
| `.salvaguardias` | cadena | sí | exige | — | Art. 17.1.f): «que ofrezcan las salvaguardias adecuadas». |
| `.revision_posterior.documentacion` | paso \| `null` | sí | exige | — | Art. 17.1.g): «procedimientos para documentar [...] los cambios de emergencia tras su aplicación». |
| `.revision_posterior.reexamen` | paso \| `null` | sí | exige | — | Art. 17.1.g), «reexaminar». |
| `.revision_posterior.evaluacion` | paso \| `null` | sí | exige | — | Art. 17.1.g), «evaluar». |
| `.revision_posterior.aprobacion` | paso \| `null` | sí | exige | — | Art. 17.1.g), «aprobar». |

Los cuatro pasos de `revision_posterior` deben ser posteriores a `implantacion.inicio` («tras su aplicación»). Mientras no se hayan hecho, son `null`, y el registro queda pendiente.

**En el simplificado no hay cambios de emergencia.** El título III no prevé un procedimiento de emergencia. El art. 37.b) exige la prueba y la aprobación «antes de introducir cambios en el entorno de producción», sin excepción. Ver D-5.

---

## 10. Verificación posterior: `verificacion_posterior`

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `verificacion_posterior` | objeto \| `null` | sí | exige | exige | DORA, art. 9.4.e): que los cambios se «verifiquen». Art. 38.2: que el cambio se «verifique». |
| `.actores`, `.fecha` | paso | sí | exige | exige | Las mismas citas. Debe ser posterior a `implantacion.inicio`. |
| `.resultado` | `conforme` \| `no_conforme` | sí | exige | exige | Las mismas citas. En el completo se compara con `resultados_esperados` (art. 17.1.d.iii). |
| `.descripcion` | cadena \| `null` | sí | — | — | **[Decisión propia]** Texto libre. |

---

## 11. Acciones de los actores: `acciones[]`

| Campo | Tipo | Obligatorio | Completo | Simplificado | Descripción y cita |
|---|---|---|---|---|---|
| `acciones` | lista | sí | — | — | Las acciones concretas que hizo cada actor, con `actor` (`id`), `fecha`, `etapa` (`solicitud` \| `especificacion` \| `pruebas` \| `revision_codigo` \| `implantacion` \| `vuelta_atras` \| `verificacion` \| `otra`) y `descripcion`. Puede estar vacía. |

**[Decisión propia]**, apoyada en el art. 12.2.c.iii), que pide registrar «los hechos relacionados con [...] la gestión de cambios», y, en el simplificado, en el art. 34.f), que pide registrar «los acontecimientos relacionados con [...] la gestión de cambios en las TIC». Esos artículos piden registros (logs) de los sistemas, no un campo del registro del cambio. Por eso `acciones` no es exigible en ningún régimen.

Es el lugar donde las acciones del agente quedan como datos del registro (§0.2, regla 2), con el grado de detalle que la entidad quiera dar. La `descripcion` dice qué hizo el actor, por ejemplo qué fichero modificó o qué orden ejecutó. **No dice qué se le pidió ni cómo lo decidió.**

---

## 12. Decisiones propias razonadas

### D-1. Quien solicita y quien aprueba son la misma persona

**Qué dice la norma.**
- Art. 17.1.b): «mecanismos para garantizar la independencia de las funciones que aprueban los cambios y las funciones responsables de solicitar y aplicar dichos cambios».
- Considerando 17: «A fin de asegurar la objetividad y la eficacia del proceso de gestión de cambios en las TIC, evitar conflictos de intereses y garantizar que los cambios en las TIC se evalúen de forma objetiva, es necesario que las funciones responsables de aprobar dichos cambios estén separadas de las funciones que los soliciten e implementen».
- Título III: ningún requisito de independencia en la gestión de cambios. El art. 28.4 pide la independencia «de las funciones de control y las funciones de auditoría interna», que es otra cosa.

**Qué representa el modelo.** Lo que pasó, sin más. La misma persona figura en `solicitud.actores` y en `aprobacion.actores` con el mismo `id`. No hay un campo que diga «hay conflicto»: eso es una conclusión (§0.1, principio 1), y se deduce de los datos.

**Por qué el agente no resuelve la separación.** La independencia que pide el art. 17.1.b) tiene dos lados: quien aprueba frente a quien solicita y quien aprueba frente a quien aplica. Que implante un agente solo afecta al segundo lado. Si la misma persona solicita y aprueba, el primer lado falla igual, implante quien implante.

Además, el agente puede crear un conflicto nuevo en el segundo lado. Un agente no tiene función propia: actúa en nombre de una función y responde de él una persona (§3.2). Si esa persona, o su función, es la que aprueba, el aprobador controla en la práctica la implantación.

**Por qué un requisito del procedimiento se valida en un cambio concreto.** El §0.3 dice que la letra b) del art. 17.1 regula el procedimiento, no cada cambio, y que el registro no puede probar que el procedimiento existe. Aun así, un cambio en el que la misma persona solicita y aprueba se valida como incumplimiento, por esta razón:

- **El mecanismo debe garantizar un resultado.** La letra b) no pide solo que haya mecanismos de independencia. Pide «mecanismos para garantizar la independencia». Un mecanismo que garantiza la independencia debe producirla en cada cambio al que se aplica, y la norma no prevé excepciones: el art. 17.1, encabezado, lo extiende a «todos los cambios».
- **Un solo caso basta para refutarlo.** Si en un cambio la misma persona solicitó y aprobó, ese cambio demuestra que el mecanismo no garantizó la independencia en él. Puede ser que no existiera, que no cubriera ese caso o que alguien lo eludiera. El registro no dice cuál de las tres, pero no hace falta: las tres incumplen la letra b).
- **El incumplimiento es de la entidad, no del cambio.** Lo que se incumple es el procedimiento de la entidad, y el registro de este cambio es la prueba. La salida lo dirá así: el registro muestra que el mecanismo del art. 17.1.b) no funcionó en este cambio.
- **La prueba solo funciona en un sentido.** Un cambio sin coincidencias no demuestra que el mecanismo exista ni que funcione: puede ser casualidad. Por eso, sin coincidencias, la salida no dirá que el cambio «cumple» el art. 17.1.b). Dirá que no hay indicio de incumplimiento en este cambio, y que la existencia del mecanismo queda fuera de lo que el registro puede probar (§14).

Este razonamiento vale sin matices cuando coincide la persona. Cuando son personas distintas de la misma `funcion`, solo vale si se acepta que una misma función no puede ser independiente de sí misma. Esa es la lectura del considerando 17, que el modelo adopta abajo y que la salida señala.

**Lectura que adopta el modelo.** **[Decisión propia]**
- **Régimen completo.** Para comprobar la independencia, cada agente cuenta con su propia `funcion` y también con la de su `persona_responsable`. Hay falta de independencia (art. 17.1.b) si alguna `funcion` de `aprobacion.actores` coincide con alguna de `solicitud.actores` o de `implantacion.actores`.
  - **Misma persona.** Si la misma persona solicita y aprueba, la `funcion` coincide necesariamente, así que es siempre un incumplimiento, por la razón que se acaba de dar. Ninguna lectura lo salva.
  - **Personas distintas en la misma función.** El art. 17.1.b) habla de «mecanismos», y una entidad podría sostener que dos personas de la misma unidad son independientes. El considerando 17 pide funciones «separadas», y el modelo sigue al considerando: también es un incumplimiento. La salida dirá que esta parte depende de la lectura del considerando.
  - **Cambio de emergencia.** Se aplica lo mismo a `emergencia.revision_posterior.aprobacion`.
- **Régimen simplificado.** No hay requisito. La coincidencia se da como dato informativo, no como incumplimiento.

**Límite.** `funcion` es un valor que declara la entidad. El modelo no comprueba que dos nombres distintos sean, de verdad, funciones distintas.

**Fragmento de ejemplo** (el resto, como en el §1.1):

```json
{
  "solicitud": { "actores": ["P-2"], "fecha": "2026-11-02T09:30:00+01:00" },
  "implantacion": { "actores": ["AG-1"], "inicio": "2026-11-09T09:05:00+01:00", "fin": "2026-11-09T09:40:00+01:00", "resultado": "aplicado" },
  "aprobacion": { "actores": ["P-2"], "fecha": "2026-11-06T10:00:00+01:00" }
}
```

Con el régimen completo, falta de independencia en el lado de la solicitud. En el de la implantación no la hay, si la función de `AG-1` y la de su responsable `P-3` son distintas de la de `P-2`.

### D-2. ¿Cuenta como revisión del art. 16.3 la que hace un agente de IA?

**Qué dice la norma.**
- Art. 16.3: el procedimiento «incluirá la realización de revisiones de códigos fuente que abarquen pruebas tanto estáticas como dinámicas». Siguen las tres obligaciones de la entidad: «a) identificar y analizar las vulnerabilidades y anomalías en el código fuente; b) adoptar un plan de acción para hacer frente a esas vulnerabilidades y anomalías; c) hacer un seguimiento de la aplicación de dicho plan de acción».
- Ni el art. 16 ni ningún otro del RDel dicen quién debe hacer la revisión ni exigen que la haga una persona o alguien distinto del autor del código.
- El art. 17.1.c.iv) pide responsabilidades que garanticen «un aseguramiento eficaz de la calidad».

**La norma no lo determina.** El art. 16.3 no excluye que la revisión la haga una herramienta. De hecho, las «pruebas estáticas y dinámicas» suelen hacerse con herramientas automatizadas. Pero tampoco dice que baste con una herramienta. Y no distingue entre una herramienta de análisis clásica y un agente de IA.

**Lectura que adopta el modelo.** **[Decisión propia]**
1. **Identificación y análisis (art. 16.3.a).** Una revisión hecha por un agente cuenta como revisión del art. 16.3. La norma no pide que sea humana, y negarlo obligaría a negar también las herramientas automáticas de análisis estático y dinámico, que la propia norma da por supuestas. La técnica (`estatica` o `dinamica`) se declara igual que en cualquier otra revisión.
2. **Plan de acción (art. 16.3.b).** Adoptar el plan es una decisión de la entidad sobre cómo tratar las vulnerabilidades. El modelo exige que `plan_accion.adoptado_por` incluya al menos una persona: un agente no puede ser titular de esa responsabilidad (§3.2).
3. **Seguimiento (art. 16.3.c).** Puede hacerlo un agente, pero el seguimiento debe tener al menos una entrada con una persona entre sus `actores`, por la misma razón.
4. **Autorrevisión.** Si el agente que revisa es el mismo que implantó el cambio, la revisión cuenta igual para el art. 16.3, que no exige independencia del revisor. Es el mismo agente si es el mismo `id`, o si tiene la misma `herramienta`, el mismo `modelo` y la misma `version`. Con el régimen completo, el validador lo dará como aviso, citando el art. 17.1.c.iv), no como incumplimiento.
5. **Régimen simplificado.** El título III no exige revisión de código. La que se registre es informativa.

Si una autoridad o unas directrices dijeran que la revisión del art. 16.3 debe ser humana, esta lectura cambiaría. La entrada no: `realizada_por` ya dice quién o qué la hizo.

### D-3. ¿De dónde procede el código que escribe un agente?

**Qué dice la norma.** El art. 16.7 distingue el código «desarrollado internamente» del «desarrollado y entregado a la entidad financiera por un proveedor tercero de servicios de TIC». El art. 16.8 pide analizar y probar «antes de su implementación en el entorno de producción» el software propietario, el código de terceros y el de código abierto.

**Por qué no lo determina.** Un agente suele ser un servicio de un tercero, pero el código lo produce dentro del proceso de la entidad y bajo su dirección. Puede leerse como desarrollo interno con una herramienta, o como código que entrega un tercero.

**Lectura que adopta el modelo.** **[Decisión propia]** `origen_codigo` lo declara la entidad, y el modelo no lo deduce del tipo de actor. Si declara `proveedor_tercero`, `software_propietario` o `codigo_abierto`, se aplica el orden del art. 16.8: alguna revisión anterior a `implantacion.inicio`. Si declara `desarrollo_interno`, se aplica el art. 16.3 sin ese orden explícito. Pero el art. 16.2 ya pide probar «antes de su uso», así que la diferencia práctica es pequeña.

### D-4. ¿Puede aprobar un agente?

**Qué dice la norma.** El art. 17.1.b) habla de «las funciones que aprueban los cambios». DORA, art. 9.4.e), y el art. 37.b) dicen que los cambios se «aprueben» o «sean aprobados». Ninguno dice quién puede aprobar.

**Por qué no lo determina.** La norma no se plantea que apruebe algo que no sea una persona. Aprobar es asumir la responsabilidad del cambio (considerando 17: «las funciones responsables de aprobar»).

**Lectura que adopta el modelo.** **[Decisión propia]** Un paso de aprobación cuenta solo si entre sus `actores` hay al menos una persona. Se aplica a `aprobacion`, a `emergencia.revision_posterior.aprobacion` y a `excepcion_datos_produccion.aprobacion`, en los dos regímenes. Que figure también un agente no lo invalida. El agente se registra como hecho.

### D-5. Cambios urgentes en el régimen simplificado

**Qué dice la norma.** El art. 37.b) exige que los sistemas se sometan a prueba y sean aprobados «antes de introducir cambios en el entorno de producción». El título III no prevé cambios de emergencia.

**Por qué no lo determina.** Puede leerse que la entidad simplificada no tiene excepción y debe aprobar antes en todo caso. Pero el art. 37 dice que el procedimiento se aplica «en su caso» y «con arreglo a un enfoque basado en el riesgo», y eso podría dar cabida a un procedimiento de urgencia propio.

**Lectura que adopta el modelo.** **[Decisión propia]**, coherente con la decisión de alcance del §0.3: en el simplificado se exige solo lo que tiene base en el título III. Un cambio con `aprobacion` `null` o posterior a `implantacion.inicio` no cumple el art. 37.b), aunque `emergencia` esté relleno. La salida dirá que el título III no prevé excepción de emergencia y que una lectura basada en el «enfoque basado en el riesgo» del art. 37 podría admitirla.

---

## 13. Qué exige cada régimen y qué tiene uno que el otro no

«Completo» es DORA, art. 9.4.e), con el título II del RDel. «Simplificado» es DORA, art. 16, con el título III del RDel. «—» quiere decir que ese régimen no lo pide. Las filas del art. 17.2 y del art. 16.2, párrafos segundo y tercero, están fuera de alcance (§0.3).

| Dato | Completo | Simplificado | Campo |
|---|---|---|---|
| Registrar el cambio | DORA, art. 9.4.e): que los cambios «se registren». Art. 12.2.c.iii): registrar los hechos de «la gestión de cambios». | Art. 38.2: que todo cambio «se registre». Art. 34.f): registrar los acontecimientos de «la gestión de cambios en las TIC». | todo el registro; `acciones` |
| Qué elementos se cambian | Art. 17.1, encabezado: software, hardware, firmware, sistemas o parámetros de seguridad. | — (art. 38.2: «todo cambio en los sistemas de TIC», sin distinguir) | `elementos` |
| Identificar a los actores en sus acciones | Arts. 20.1, 20.2.a) y 21.c). | Art. 33.b). | `actores[].cuenta`, `tipo`; datos del agente |
| Quién solicita | Art. 17.1.b). | — | `solicitud` |
| Independencia entre quien aprueba y quien solicita o aplica | Art. 17.1.b); considerando 17 (D-1). | — (el art. 28.4 trata las funciones de control y de auditoría) | `funcion`, `solicitud`, `implantacion`, `aprobacion` |
| Funciones y responsabilidades del cambio | Art. 17.1.c), incisos i) a iv). | — (arts. 28.2.b y 38.1, genéricos) | `responsabilidades` |
| Objeto y alcance | Art. 17.1.d.i). | — | `objeto`, `alcance` |
| Calendario | Art. 17.1.d.ii). | — | `calendario` |
| Resultados esperados | Art. 17.1.d.iii). | — | `resultados_esperados` |
| Comunicar los detalles | Art. 17.1.d), encabezado. | — | `comunicaciones` |
| Verificar los requisitos de seguridad | Art. 17.1.a). | — (el art. 37.a pide especificarlos antes de adquirir o desarrollar, no verificarlos en cada cambio) | `verificacion_seguridad` |
| Evaluar el cambio | DORA, art. 9.4.e); art. 17.1.h): repercusión en las medidas de seguridad y medidas adicionales. | Art. 38.2; art. 31.1.e): riesgos, si el cambio es importante. | `evaluacion` |
| Cambio importante | — | Art. 31.1.e). | `cambio_importante` |
| Probar antes de producción | DORA, art. 9.4.e); art. 16.2: «antes de su uso y después del mantenimiento». | Art. 37.b): «antes de introducir cambios en el entorno de producción»; art. 38.2. | `pruebas` |
| Tipos de prueba | Art. 16.2 (idoneidad, calidad), 16.3 (sistemas expuestos a internet) y 16.4 (paquetes, a más tardar en integración). | — | `pruebas[].tipo`, `fase` |
| Datos de producción en entornos de prueba | Arts. 16.5 y 16.6. | — | `pruebas[].entorno`, `datos`, `excepcion_datos_produccion` |
| Revisión de código fuente, estática y dinámica | Art. 16.3 (D-2). | — | `revisiones_codigo` |
| Vulnerabilidades, plan de acción y seguimiento | Art. 16.3.a) a c). | — | `hallazgos`, `plan_accion`, `seguimiento` |
| Código de terceros, propietario o abierto | Art. 16.8 (D-3). | — | `origen_codigo` |
| Integridad del código fuente | Art. 16.7. | — | `controles_integridad` |
| Alteración o manipulación | Art. 16.1.c). | Art. 37.c). | `controles_integridad` |
| Aprobar | DORA, art. 9.4.e); art. 17.1.b) (D-4). | Art. 37.b): antes de producción; art. 38.2 (D-4, D-5). | `aprobacion` |
| Aplicar | DORA, art. 9.4.e). | Art. 38.2. | `implantacion` |
| Vuelta atrás | Art. 17.1.e); considerando 17. | — | `vuelta_atras` |
| Cambios de emergencia | Art. 17.1.f). | — (D-5) | `emergencia` |
| Revisión posterior de los cambios de emergencia | Art. 17.1.g). | — | `emergencia.revision_posterior` |
| Verificar | DORA, art. 9.4.e). | Art. 38.2. | `verificacion_posterior` |
| Proceso aprobado por la dirección | DORA, art. 9.4, párrafo tercero: el proceso «será aprobado por los niveles directivos adecuados». Es del procedimiento, no del cambio (§14). | Art. 28.2.f) y g), también del procedimiento. | — |
| Pruebas de tensión tras cambios significativos | Art. 17.2, solo entidades de contrapartida central y depositarios centrales de valores. **Fuera de alcance.** | — | — |

**Qué tiene el completo que el simplificado no.**
- Todo el art. 17.1 salvo lo que coincide con el art. 38.2: verificación de los requisitos de seguridad (a), independencia (b), responsabilidades del cambio (c), objeto, alcance, calendario, resultados esperados y comunicación (d), vuelta atrás (e), cambios de emergencia y su revisión posterior (f y g) y repercusión en las medidas de seguridad (h).
- Del art. 16: la revisión de código, los tipos de prueba, el control de los datos de producción en las pruebas, la integridad del código fuente y el tratamiento del código de terceros.

**Qué tiene el simplificado que el completo no.**
- **Dos cosas solo de este régimen:**
  - la evaluación de riesgos ligada a un **cambio importante** (art. 31.1.e);
  - la exigencia de aprobación previa sin excepción de emergencia (art. 37.b, D-5).
- **Una que el completo dice con otras palabras:** la aprobación antes de producción. En el completo resulta del art. 9.4.e) de DORA, «de forma controlada», y del art. 16.2, «antes de su uso», y queda exceptuada por los cambios de emergencia del art. 17.1.f) y g).

**Lo que resulta de la tabla.** El simplificado comparte con el completo el esqueleto del art. 9.4.e) de DORA: registrar, probar, evaluar, aprobar, aplicar y verificar. Del art. 38.2 y de los arts. 31, 33, 34 y 37 se sacan pocos datos más. Todo lo que el encargo pide además (objeto, alcance, calendario, resultado esperado, vuelta atrás, emergencia, revisión de código) tiene base en el completo, y en el simplificado se acepta sin exigirse.

---

## 14. Lo que no entra

Por la regla 1 del §0.2, cada omisión tiene su motivo.

| Dato | Por qué no entra |
|---|---|
| Prompts, instrucciones, contexto, configuración, parámetros, razonamiento y salidas intermedias del agente | Regla 2 del §0.2. |
| Si el agente es un sistema de IA de alto riesgo según el Reglamento (UE) 2024/1689 | No es un régimen de este registro, y clasificarlo exigiría conocer su funcionamiento (regla 2). |
| Si el procedimiento de gestión de cambios existe, está documentado y lo ha aprobado la dirección (DORA, art. 9.4, párrafo tercero; art. 17.1, encabezado; arts. 28.2 y 38.2) | Es un hecho del procedimiento, no de cada cambio (§0.3). |
| Política de adquisición, desarrollo y mantenimiento (art. 16.1.a y b) | Es un hecho de la política, no de cada cambio. |
| Si el nivel de las pruebas es «acorde con el carácter esencial de los procedimientos empresariales y los activos de TIC afectados» (art. 16.2) | Es una valoración de proporcionalidad, no un hecho del registro (§0.1, principio 1). |
| Pruebas de tensión y partes asociadas a las pruebas de las entidades de contrapartida central y de los depositarios centrales de valores (art. 17.2; art. 16.2, párrafos segundo y tercero) | **[Decisión de alcance]** (§0.3). |
| Si el sistema lo desarrollan o gestionan usuarios ajenos a la función de TIC (art. 16.9) | El art. 16.9 extiende los apartados 1 a 8 a esos sistemas «utilizando un enfoque basado en el riesgo». El modelo aplica el art. 16 a todo cambio, así que el dato no cambia ningún requisito. |
| Conservación del registro (art. 12.2.a) y protección de los registros (art. 12.2.d) | Son medidas sobre los sistemas de registro, no datos del cambio. |

---

## 15. Validación

Errores de entrada, que no dependen del régimen (§0.1, principio 3):

- un campo que el modelo no define, incluido `regimen`;
- falta un campo obligatorio, o su tipo o su valor no son los de las tablas;
- una fecha que no tiene la forma del §2;
- un `id` repetido en `actores`, en `pruebas`, en `revisiones_codigo` o en los `hallazgos` de una misma revisión;
- una referencia a un `id` que no existe: en un paso, en `responsabilidades`, en `persona_responsable`, en `acciones[].actor` o en `plan_accion.medidas[].hallazgos`;
- una `persona_responsable` que no es una persona, o los campos del §3.2 en un actor `persona`;
- `implantacion.fin` anterior a `implantacion.inicio`.

Que falte un dato **exigible** en un régimen (por ejemplo, `vuelta_atras` en `null` con el completo) no es un error de entrada: es un resultado del cálculo para ese régimen.
