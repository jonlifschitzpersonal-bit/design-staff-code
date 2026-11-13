---
name: project-setup
description: >-
  Kit de arranque de design-staff-code en un proyecto: revisa qué tiene el proyecto, pregunta lo que falta, inspecciona el código
  y la librería de componentes, instala la medición con Playwright y genera la capa propia del proyecto (CLAUDE.md de diseño, fuentes, skill de reglas de diseño, skills
  del DS, settings, estado, pendientes, cartera y rutina) sin pisar lo que ya existe. Usar cuando se instala el plugin
  en un proyecto nuevo, cuando se pide «configurá el proyecto», «armá el kit», «onboarding del plugin», o cuando el lead
  detecta que el proyecto no tiene esa capa antes de una decisión material.
---

# Arranque de un proyecto con design-staff-code

El plugin trae el sistema genérico. Lo que hace rendir al sistema en un proyecto es su **capa propia**: dónde están las
fuentes de verdad, quién decide qué, las reglas de producto, el DS y la accesibilidad de su audiencia. Esta skill la
arma en una sesión. Las plantillas están en `${CLAUDE_PLUGIN_ROOT}/templates/project/` y
`${CLAUDE_PLUGIN_ROOT}/templates/`.

## Reglas

- **Nunca pises lo que existe.** Si un archivo ya está, leelo entero y sumá solo las secciones o filas que falten. Si
  algo existente contradice una plantilla, manda lo existente; anotá la diferencia en el resumen.
- **No inventes.** Lo que el usuario no sabe o no contestó queda como `<pendiente: qué falta y quién lo sabe>`. Nunca
  completes una regla de dominio, una prioridad o un responsable por intuición.
- **Superficie: código.** Este plugin diseña en código, sin Figma. No pidas ni inspecciones un archivo de Figma: las
  «fuentes de verdad» visuales son el repositorio de código, la librería de componentes y su documentación. Si el
  proyecto igual tiene Figma, anotalo como referencia y preguntá si manda sobre el código (si manda, este plugin no es
  el adecuado: usá `design-staff`).
- **No instales nada que ejecute código externo sin preguntar** (servidores MCP, skills por `curl`, paquetes `@latest`).
  Proponé la opción y dejá que el usuario decida; si ya se instaló, solo documentala.
- **Lo propio queda en el proyecto, lo genérico en el plugin.** Si al armar el kit encontrás algo genérico que le falta
  al sistema, proponé agregarlo al plugin (ver «Mantener el sistema» en el lead); no lo copies al proyecto.
- No hagas commit salvo que el usuario lo pida.

## 1. Diagnóstico

Revisá, sin modificar nada:
- `CLAUDE.md`: ¿existe? ¿tiene fuentes de verdad, idioma, reglas de producto, quién decide y qué se escala?
- `.claude/skills/`: ¿hay una skill de reglas de diseño y skills del DS?
- `.claude/settings.local.json` y `.claude/settings.json`: ¿está habilitado `design-staff-code` y fijado el lead como agente?
- `design/knowledge/FUENTES_DEL_PROYECTO.md`, `design/opportunities.md`, `design/routines/`.
- `docs/`: ¿hay estado vigente, pendientes y registro de sesiones? Si el proyecto usa otros nombres, adoptalos en vez de
  crear archivos nuevos.
- Fuentes de evidencia del repo: research, minutas, transcripciones, tickets, analytics.

**Referencias viejas.** Buscá en lo que ya existe (`CLAUDE.md`, `design/knowledge/`, `.claude/skills/`, `docs/`) lo que
quedó desactualizado respecto de esta superficie: menciones a `design-staff` (sin `-code`), a Figma o a node IDs, a
«no hay sistema de diseño» cuando el proyecto ya adoptó una librería, y rutas que no existen. No las reescribas en
silencio: listalas en una tabla «lugar → qué dice → qué debería decir», corregí las que sean puro nombre del plugin o
del sistema de diseño, y dejá las demás como `<pendiente>` con la diferencia anotada.

Mostrá una tabla corta: pieza → existe / parcial / falta.

## 2. Preguntas

Preguntá solo lo que el diagnóstico no resolvió, en rondas de hasta 4 preguntas con la herramienta de preguntas,
proponiendo siempre una opción por defecto. Si la sesión no es interactiva o el pedido ya trae las respuestas, usalas y
dejá el resto como `<pendiente>`.

1. **Producto:** qué es, para quién, superficies y plataformas (con los viewports a medir, por ejemplo 390×844 en
   móvil), y el próximo deadline real.
2. **Fuentes de verdad:** repositorio de código y comando que levanta la app, **librería de componentes** y dónde está
   su documentación (por ejemplo `llms.txt` o un servidor MCP), fuente canónica del flujo, documentos de estado y dónde
   están las reuniones y la evidencia de usuarios.
3. **Autoridad:** quién decide diseño, producto y DS, qué dominio exige escalar (clínico, legal, financiero o ninguno) y
   por qué canal se le lleva una pregunta.
4. **Idioma y voz:** de la conversación, de la documentación interna, de lo que ve el cliente y locale del producto;
   si hay una voz o una guía de estilo, y los términos que el producto ya usa (o que no puede usar).
5. **Equipo:** cuántas personas editan el mismo código y la política de ramas del repo.
6. **Audiencia y accesibilidad:** edad, contexto y condiciones de uso, y si hay pisos propios de texto o targets.
7. **Reglas confirmadas:** las reglas de producto o visuales que ya se decidieron, con quién y cuándo.

## 3. Inspección

- **Código del proyecto:** leé `package.json` (framework, versión de la librería, comando de desarrollo y de build) y
  la capa de tema (CSS con los tokens, configuración de la librería). Anotá qué valores por defecto de la librería
  quedan bajo los pisos del proyecto.
- **Librería de componentes:** leé su documentación (`llms-components.txt`, `llms-patterns.txt` o las herramientas de
  su MCP: lista de componentes, docs de cada uno, variables del tema) y generá las skills del DS a partir de ahí.
  Cada componente lleva «cuándo usarlo / cuándo NO» según las reglas del producto, y las reglas de rol (por ejemplo,
  un filtro no se dibuja como una acción).
- **Medición:** copiá `${CLAUDE_PLUGIN_ROOT}/templates/project/tools/medir.mjs` a `tools/medir.mjs` del proyecto, y
  comprobá que corra (`node tools/medir.mjs --url <url de la app> --name prueba`). Requiere `playwright` como
  dependencia de desarrollo y Chromium instalado (`npx playwright install chromium`): si falta, proponelo, no lo
  instales sin preguntar.
- **Banco de la librería:** leé `${CLAUDE_PLUGIN_ROOT}/knowledge/RECETAS_LIBRERIAS.md`. Si hay un banco para la librería
  del proyecto en `${CLAUDE_PLUGIN_ROOT}/templates/librerias/<librería>/` (hoy: `heroui`), copialo a `tools/banco/` y
  revisá que los imports coincidan con la versión instalada; si no, armá uno con un `data-bloque` por componente.
  Medí el banco sin personalizar y con `?pisos`, y volcá el resultado en la tabla «Valores por defecto que NO cumplen
  los pisos» de `<proyecto>-components`. La capa de pisos es una **propuesta**: no la apliques a `src/` sin que el
  usuario la apruebe, y decí qué jerarquía de tamaños pierde (ver la receta).
- Si hay un board de flujo, registrá su dirección.
- Anotá la fecha de inspección en cada skill del DS.

## 4. Generación

`<proyecto>` es un slug corto en minúsculas. Generá o completá, en este orden:

| Plantilla | Destino en el proyecto |
| --- | --- |
| `project/CLAUDE.md` | `CLAUDE.md` (sumar secciones si ya existe) |
| `project/design/knowledge/FUENTES_DEL_PROYECTO.md` | `design/knowledge/FUENTES_DEL_PROYECTO.md` |
| `project/design/knowledge/VOZ_Y_GLOSARIO.md` | `design/knowledge/VOZ_Y_GLOSARIO.md` (si no hay voz confirmada, queda como propuesta) |
| `project/skills/design-pipeline/SKILL.md` | `.claude/skills/<proyecto>-design-pipeline/SKILL.md` |
| `project/skills/components/SKILL.md` | `.claude/skills/<proyecto>-components/SKILL.md` (solo si hay DS) |
| `project/skills/tokens/SKILL.md` | `.claude/skills/<proyecto>-tokens/SKILL.md` (solo si hay DS) |
| `project/skills/typography/SKILL.md` | `.claude/skills/<proyecto>-typography/SKILL.md` (solo si hay DS) |
| `project/dotclaude/settings.local.json` | `.claude/settings.local.json` (fusionar el JSON; no borrar claves existentes) |
| `project/tools/medir.mjs` | `tools/medir.mjs` (medición con Playwright; ver «Inspección») |
| `librerias/<librería>/banco/` | `tools/banco/` (solo si hay plantilla para la librería; ver «Inspección») |
| `project/docs/CURRENT_STATE.md` y `PENDING_TASKS.md` | `docs/` (solo si el proyecto no tiene equivalentes) |
| `project/WORKING_ON.md` | `WORKING_ON.md` (solo si editan dos o más personas) |
| `opportunities.md` | `design/opportunities.md` |
| `routines/opportunity-review.md` | `design/routines/opportunity-review.md` |

Si el proyecto **adoptó una librería de componentes**, la librería es su DS: generá las tres skills del DS a partir de su
documentación (ver «Inspección»), y dejá escrito en la skill `-components` qué librería y qué versión, y cómo se
consulta su documentación. Si el proyecto no tiene DS ni librería, no generes las tres skills: anotá en la skill de
reglas de diseño que el DS es un pendiente y que el lead diseña con `design-staff-code:ui-designer` hasta que exista. Si el marketplace instalado no se llama
`jony-plugins`, ajustá la clave de `enabledPlugins` al nombre real (`claude plugin list` lo muestra). La clave
`design-staff-code@inline` aparece solo cuando el plugin se carga con `--plugin-dir` (evaluaciones): no la cambies.

Escribir en `.claude/` pide aprobación del usuario. Si no se puede escribir un archivo, mostrá su contenido completo en
la entrega para que se pegue a mano, y marcalo como no escrito.

En las skills generadas, reemplazá todos los `<…>`. En la descripción del frontmatter no dejes marcadores: si falta un
dato, describí la skill sin él.

## 5. Verificación

- Buscá los marcadores que quedaron (`<` seguido de texto y `>` en los archivos generados): cada uno tiene que ser un
  `<pendiente: …>` explícito. `<slug>` dentro de una ruta de expediente (`design/initiatives/<slug>/`) es literal.
- Comprobá que cada `SKILL.md` generado tenga frontmatter válido con `name` y `description`.
- Corré `claude plugin list` desde la raíz del proyecto: `design-staff-code` tiene que figurar habilitado.
- Si el proyecto no estaba habilitado antes, avisá que hay que **reiniciar Claude Code** para que el lead tome la
  conversación.

## 6. Entrega

Un resumen corto:
- qué se creó y qué se completó, con sus rutas;
- la lista de `<pendiente>` con quién puede resolver cada uno, ordenada por lo que más limita al lead;
- lo existente que se respetó y difería de la plantilla;
- una primera iniciativa sugerida, chica, para probar el sistema en el proyecto.
