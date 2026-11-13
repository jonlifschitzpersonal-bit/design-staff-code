# Fuentes del proyecto <Proyecto>

Mapa de dónde está el conocimiento de <Proyecto> para los agentes del plugin `design-staff-code`. El criterio genérico vive
en `knowledge/STAFF_STANDARD.md` del plugin; acá va solo lo propio del proyecto.

## Dónde está el conocimiento

| Pregunta | Fuente que se consulta |
| --- | --- |
| ¿Qué flujo y pantallas existen hoy? | <board de flujo o documento, indicado en `CLAUDE.md`>. Inspeccioná la versión vigente. |
| ¿Cuál es el estado y qué espera respuesta? | `docs/CURRENT_STATE.md` y `docs/PENDING_TASKS.md`: solo las secciones de la tarea. |
| ¿Qué se decidió y con qué alcance? | <`docs/DECISIONS.md`, documento del módulo> y el expediente de la iniciativa. Una propuesta anterior no es una aprobación. |
| ¿Qué se dijo en las reuniones? | <carpeta de minutas o transcripciones, o `<pendiente>`>. Buscá por actor, pantalla, concepto y fecha; verificá si una reunión posterior cambió la propuesta. |
| ¿Qué dicen los usuarios? | <research, entrevistas, tickets, analytics, o «no hay evidencia de usuarios todavía»>. |
| ¿Cómo habla el producto? | `design/knowledge/VOZ_Y_GLOSARIO.md` (voz, tono, glosario y lo que el copy no puede afirmar). |
| ¿Cómo se representa en la UI? | La app corriendo (rutas y tema en `CLAUDE.md`), `<proyecto>-design-pipeline` y las skills del DS. No infieras del resumen textual. |
| ¿Qué método de product design corresponde? | `design-staff-code:product-designer`, `design-staff-code:ux-designer` y `design-staff-code:ui-designer`, solo las referencias pertinentes. |

Los documentos históricos, los ejemplos, los benchmarks y la opinión del agente sirven para generar hipótesis o
contrastar patrones. No reemplazan una fuente vigente ni validan el comportamiento de los usuarios. Para afirmaciones
de dominio, permisos o prioridades comerciales sin fuente, registrá la pregunta y la propuesta; no cierres el vacío por
intuición.

En cada iniciativa material, `evidence.md` deja la **cobertura de fuentes**: área y términos buscados, documentos y
reuniones consultados con su fecha, contradicciones y quién puede resolverlas. `artifacts.md` registra la URL, el archivo fuente, el commit
y la fecha de inspección de la app corriendo.
