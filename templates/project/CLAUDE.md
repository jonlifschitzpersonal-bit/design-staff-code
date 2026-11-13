# <Proyecto> — instrucciones de proyecto

<!-- Plantilla del kit de arranque de design-staff-code. Cada `<…>` se completa; lo que no se sabe queda como
`<pendiente: qué falta y quién lo sabe>`. Si el proyecto ya tiene un CLAUDE.md, se suman solo las secciones que
faltan y se respeta lo que ya dice. -->

## Propósito de este repositorio

<Qué contiene este repo: producto, documentación de diseño, código, o una mezcla.> <Si el código de la app vive en
otro repo, decilo: «Si una tarea pide modificar código, primero localizá o pedí el repositorio correcto».>

## Inicio de cada sesión

1. Leé el encabezado de `docs/CURRENT_STATE.md` y de `docs/PENDING_TASKS.md`, y solo las secciones del actor, módulo o
   pantalla de la tarea. No cargues toda la documentación por rutina.
2. Leé solo el documento adicional relacionado con la tarea. Si hay una contradicción, abrí la fuente o la reunión
   necesaria para resolverla.

## Cómo trabajar

- **Modo Staff Design Lead.** El agente principal es `design-staff-code:staff-design-lead` (plugin `design-staff-code`). Para
  un producto o un área nueva grande, la fase previa al diseño la lleva `design-staff-code:discovery-lead`. El lead delega
  investigación al `evidence-scout` y crítica independiente al `design-critic`, en **una sola ronda**, y conserva la
  decisión.
- **Autonomía con límites.** El lead elige métodos, explora y descarta propuestas, corrige sus defectos y converge de
  forma provisional sin esperar que <responsable> elija entre opciones. Escala: <decisiones de dominio: clínicas,
  legales, financieras… o «ninguna»>, contradicciones con el flujo canónico, prioridades de negocio sin fuente y cambios
  compartidos del DS que requieren coordinación. Siempre con una propuesta. La revisión de IA no es validación de
  usuarios ni aprobación del cliente.
- **Un escritor en el código.** Los subagentes investigan y critican en solo lectura. Solo el lead edita el código de las
  pantallas.
- **El sistema multiagente vive en el plugin.** Lo genérico del sistema (agentes, skills de producto/UX/UI,
  conocimiento, plantillas, scripts y evaluaciones) se cambia en el repo del plugin `design-staff-code`, con versión y
  commit. En este repo queda solo lo propio del proyecto (y `tools/medir.mjs`, que es una copia de la plantilla).

## Quién decide qué

| Tema | Decide | Cómo se le lleva |
| --- | --- | --- |
| Diseño y UX dentro del alcance | <responsable de diseño> | Recomendación con descartes, evidencia y condición de cambio. |
| Producto y prioridades | <product owner o cliente> | <canal: reunión, comentario, mensaje> |
| <Dominio: clínico / legal / financiero / ninguno> | <experto o rol> | Pregunta concreta más una propuesta de UX. |
| DS compartido y componentes master | <dueño del DS> | Coordinación antes de editar, declarada en `WORKING_ON.md`. |

## Fuentes de verdad

### Flujo del producto

<Fuente canónica del orden y la existencia de pantallas: board, documento o «no hay; manda el expediente de discovery».>
- Ubicación: `<ruta o enlace>`

Antes de diseñar, auditar o proponer una pantalla, inspeccioná esta fuente. Ante un conflicto con docs o reuniones,
manda esta fuente.

### Diseño visual (en código)

- Superficie: **código** (sin Figma) · framework y librería de componentes: **<librería y versión>**
- Documentación de la librería: `<llms.txt, MCP u otra fuente>` · tema: `<ruta del CSS o la config de tema>`
- Levantar la app: `<comando>` · build: `<comando>` · medición: `node tools/medir.mjs` (Playwright)

Antes de modificar una pantalla, inspeccioná la app corriendo y seguí la skill `<proyecto>-design-pipeline`. Los
resúmenes no reemplazan la inspección ni la medición en el navegador.

## Trabajo en equipo

<Solo / N diseñadores.> <Si son varios: «Antes de tocar una pantalla o un master del DS, declaralo en `WORKING_ON.md`.
Editar un master propaga al instante a todas las pantallas que lo usan».> <Política de ramas del repo.>

## Idioma

- Conversación: <idioma>.
- Documentación interna: <idioma>.
- Todo lo que ve el cliente (pantallas, UI copy, decks, reportes, comentarios): <idioma>.
- Locale primario del producto: <locale>; otros: <locales o «ninguno por ahora»>.

## Reglas de producto y diseño

- Foco en el MVP y en el próximo deadline real: <deadline o `<pendiente>`>.
- <Reglas confirmadas del producto, una por línea, con quién la pidió y cuándo.>
- **Reglas absolutas que bloquean la construcción** (por ejemplo, algo que la ley o un experto prohíbe, o un asunto sin
  resolver donde «hasta que no haya respuesta, no se diseña nada que lo permita»). Una por línea, con quién la fijó, la
  frase textual si existe, y su **prueba adversarial**: el escenario concreto que hay que probar en cada pantalla y cada
  texto antes de cerrar. Una posible violación bloquea el cierre; no se acepta como riesgo residual.
  <Si no hay ninguna: «ninguna por ahora».>
- No resolver en silencio contradicciones de flujo o de dominio: registrarlas en `docs/PENDING_TASKS.md` y pedir
  validación.
- **Toda pregunta al cliente lleva una propuesta de UX.** Si la propuesta es no hacer nada, se dice con qué argumento.

## Cierre de sesión

1. Actualizá `docs/CURRENT_STATE.md` solo si cambió el estado vigente.
2. Actualizá `docs/PENDING_TASKS.md`: sacá lo resuelto y sumá los bloqueos nuevos concretos.
3. Creá `docs/sessions/YYYY-MM-DD-slug.md` (fecha, resultado, artefactos, decisiones y siguiente paso) y su fila en
   `docs/SESSION_LOG.md`. Un archivo por sesión.
4. El detalle de investigación, críticas, descartes y decisiones vive en `design/initiatives/<slug>/`, no en el log.
