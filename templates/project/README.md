# Kit de arranque de proyecto

Plantillas de la **capa propia** de un proyecto: lo que el plugin a propósito no trae y que hace que el sistema rinda
en ese proyecto. No se copian a mano: las usa la skill `design-staff-code:project-setup`, que pregunta lo que falta,
inspecciona el código y la librería de componentes y genera los archivos sin pisar lo existente.

| Plantilla | Para qué |
| --- | --- |
| `CLAUDE.md` | Fuentes de verdad, quién decide qué, qué se escala, idioma, equipo, reglas de producto y cierre de sesión. |
| `design/knowledge/FUENTES_DEL_PROYECTO.md` | Dónde buscar cada tipo de conocimiento del proyecto. |
| `design/knowledge/VOZ_Y_GLOSARIO.md` | Voz, tono, glosario y lo que el copy no puede afirmar; lo usa `design-staff-code:ux-writing`. |
| `skills/design-pipeline/SKILL.md` | Reglas propias de producto, código, DS y accesibilidad (`<proyecto>-design-pipeline`). |
| `skills/components/`, `tokens/`, `typography/` | Las skills del DS, completadas desde la documentación de la librería y el tema real. |
| `dotclaude/settings.local.json` | Habilita el plugin y fija al lead como agente principal (va en `.claude/`). |
| `docs/CURRENT_STATE.md`, `docs/PENDING_TASKS.md` | Estado vigente y pendientes, si el proyecto no tiene equivalentes. |
| `WORKING_ON.md` | Coordinación cuando dos o más personas editan el mismo código. |

También usa `../opportunities.md` y `../routines/opportunity-review.md`.

Convención: `<…>` se completa; lo que no se sabe queda como `<pendiente: qué falta y quién lo sabe>`.
