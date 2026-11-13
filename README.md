# Design Staff Code

Variante de [`design-staff`](../design-staff) que diseña **directo en código** (React + una librería de componentes
como HeroUI), sin Figma. Es el mismo sistema multiagente de product design, con una superficie distinta: el artefacto
es la app corriendo, y el lead verifica con un navegador (Playwright) y **mide en el DOM real** los tamaños de texto,
los targets y el contraste. La guía de la superficie está en `knowledge/SUPERFICIE_CODIGO.md`. Viene **apagado por
defecto**: solo existe en los proyectos donde lo habilitás, y **no se habilita junto con `design-staff`** (comparten
los nombres de agentes y skills).

Estado: **0.2.0, experimental.** Nació para probar si una librería ya hecha mejora el resultado frente al diseño a mano
en Figma. Lo que cambió respecto de `design-staff`: `agents/staff-design-lead.md`, `agents/design-critic.md`,
`agents/evidence-scout.md`, `skills/design-accessibility/`, `skills/project-setup/`, las plantillas del expediente y
del proyecto, y lo nuevo: `knowledge/SUPERFICIE_CODIGO.md`, `knowledge/RECETAS_LIBRERIAS.md`, `templates/project/tools/medir.mjs` y
`templates/librerias/`. El discovery, las skills de producto, UX y UX writing, y los validadores son los mismos.

## Qué trae

| Pieza | Qué hace |
| --- | --- |
| `agents/discovery-lead.md` | Agente principal de la **fase previa al diseño** en un producto nuevo: encuadre, plan de research, síntesis, JTBD, journey, service blueprint, oportunidades, MVP, flujos, user stories y **design brief**. |
| `agents/staff-design-lead.md` | Agente principal de **diseño en código**. Parte del design brief si existe. Encuadra, investiga, explora mecanismos, decide de forma provisional, documenta y aplica las críticas. |
| `agents/design-critic.md` | Revisor independiente, de solo lectura. **Una sola pasada**, con todos los hallazgos y su corrección. |
| `agents/evidence-scout.md` | Investiga fuentes o audita los hechos contra las fuentes. **Una sola pasada.** |
| `skills/product-designer/` | Estrategia de producto senior: encuadre, segmento, priorización, métricas, experimentos, modelo operativo y entrega. |
| `skills/ux-designer/` | UX e interacción senior: flujos, IA, formularios, estados, recuperación, psicología de decisión y usabilidad. |
| `skills/ui-designer/` | UI y craft visual senior: jerarquía, tipografía, color, tokens, componentes, densidad y fidelidad. |
| `skills/ux-writing/` | UX writing y content design: voz y tono, microcopy por tipo de mensaje, lenguaje claro, glosario y localización. La usan el lead al escribir, el discovery-lead en flujos y wireframes, y el critic como lente de copy. |
| `skills/project-setup/` | **Kit de arranque**: diagnostica el proyecto, pregunta lo que falta, inspecciona el código y la librería de componentes, instala la medición y genera su capa propia con `templates/project/`. |
| `skills/design-discovery/` | Etapas de discovery, etiquetas de evidencia (observado / dicho / inferido / hipótesis), guías por método, **design sprint** (cuándo, variantes, agenda y rol del agente), **técnicas de taller** con cuándo usar cada una, y design brief. |
| `skills/design-accessibility/` | WCAG 2.2 AA verificable en la pantalla que corre, con tamaños y targets medidos en el DOM y contraste medido por `scripts/contrast.py`. |
| `knowledge/SUPERFICIE_CODIGO.md` | Cómo se dibuja, se mide, se registra y se cierra una iniciativa en código. Reemplaza lo que `design-staff` hace con Figma. |
| `templates/project/tools/medir.mjs` | Script de Playwright que captura una pantalla y mide el DOM: texto, controles reales (no el `<input>` oculto), contraste de texto y no textual, y foco con teclado. `project-setup` lo copia a `tools/medir.mjs` del proyecto. |
| `knowledge/RECETAS_LIBRERIAS.md` | Cómo adoptar una librería sin que sus valores por defecto rompan los pisos: banco de medición, capa de pisos en el tema, costo en jerarquía y trampas conocidas. |
| `templates/librerias/heroui/` | Banco de medición y capa de pisos para HeroUI v3 (Tailwind v4). `project-setup` los copia a `tools/banco/`. |
| `vendor/impeccable/` | 5 guías de Impeccable (`critique`, `clarify`, `distill`, `harden` y `onboard`), copiadas sin modificar bajo Apache-2.0. El lead las lee como lentes de la pasada visual. |
| `knowledge/STAFF_STANDARD.md` | Criterio compartido de una decisión staff. |
| `knowledge/LAWS_OF_UX.md` | Las 30 leyes de [lawsofux.com](https://lawsofux.com/) aplicadas: cómo se usa cada una, cuándo falla, la señal en una crítica, su fuente y su nivel de evidencia (High / Medium / Folk). La usan el lead y el critic como lente. |
| `knowledge/REFERENCIAS_MOBBIN.md` | Cómo buscar referencias de pantallas y flujos en el MCP de Mobbin antes de armar pantallas, cómo registrarlas y qué hacer si el MCP no está disponible. Lo usan los dos leads. Requiere agregar el MCP de Mobbin (cuenta Pro, Team o Enterprise): `claude mcp add mobbin --scope user --transport http https://api.mobbin.com/mcp`. |
| `templates/initiative/` | Plantillas del expediente de diseño: brief, evidencia, exploración, críticas, decisión y artefactos. |
| `templates/project/` | Plantillas de la capa propia de un proyecto: `CLAUDE.md`, fuentes, skill de reglas de diseño, skills del DS, settings, estado, pendientes y coordinación. |
| `templates/opportunities.md` | Plantilla de la cartera de oportunidades del proyecto (`design/opportunities.md`). |
| `templates/routines/opportunity-review.md` | Disparador reutilizable para que el lead revise la cartera y avance una oportunidad. |
| `templates/copy-deck.md` | Tabla de textos para desarrollo y traducción: clave, contexto, texto, límite, variables y plurales. |
| `templates/sprint/sprint.md` | Expediente de un design sprint, día por día, con preguntas del sprint, votos, storyboard, test y resultado. |
| `templates/discovery/` | Plantillas del expediente de discovery: una por etapa, de `00-encuadre.md` a `10-design-brief.md`. |
| `scripts/case.py` | Crea expedientes y registra eventos en `<proyecto>/design/initiatives/<slug>/`. |
| `scripts/validate_dossier.py` | Gate de cierre del expediente de diseño. `test_validate_dossier.py` contiene sus tests. |
| `evals/` | Banco de evaluación del sistema: rúbrica, scorecard, `prepare_fixture.py` y 3 casos ficticios. Un proyecto puede sumar casos propios con `--cases-dir`. |
| `scripts/validate_discovery.py` | Gate «listo para diseñar» del discovery. `test_validate_discovery.py` contiene sus tests. |

**Dos fases, dos agentes principales:**
1. **Discovery** (`claude --agent design-staff-code:discovery-lead`): producto nuevo o área nueva grande. Termina en un
   design brief. La IA prepara, sintetiza y estructura; las entrevistas y los tests los hacen personas. Lo que no se
   probó con usuarios queda marcado como hipótesis.
2. **Diseño** (`design-staff-code:staff-design-lead`, el agente por defecto): parte del brief y diseña en código.

**Al terminar cada tarea, un informe de cierre en el chat:** qué se hizo, por qué cada elemento (estructura,
componentes, color, tipografía, copy, estados) con la fuente de cada razón, qué se descartó, qué cambió por la crítica
y qué falta decidir. Lo que es criterio propio del agente se marca como tal.

**Regla central: una sola ronda de crítica.**
1. El critic, y el scout si hace falta, auditan una vez y en paralelo.
2. El lead implementa y verifica él mismo.
3. Solo hay una pasada focal si una corrección cambió el mecanismo o la recomendación.
4. El tope es de dos rondas.

## Instalar (una vez por máquina)

Repositorio: <https://github.com/jonlifschitzpersonal-bit/design-staff-code>. **No es un marketplace**: es el plugin solo.

En esta máquina vive en `D:\Escritorio\claude-plugins\design-staff-code` y está declarado en el `marketplace.json` del
marketplace local `jony-plugins` (el mismo que usa `design-staff`, que es una carpeta, no GitHub). Desde el proyecto
donde lo quieras:

```
claude plugin marketplace update jony-plugins
claude plugin install design-staff-code@jony-plugins --scope local
```

- Para actualizar después de editar el plugin: subí la versión en `.claude-plugin/plugin.json` y corré
  `claude plugin update design-staff-code@jony-plugins`.
- En otra máquina: cloná el repo y usá `claude --plugin-dir <ruta-del-clon>` (el plugin queda como
  `design-staff-code@inline`), o declaralo en el marketplace que uses apuntando a este repo.
- Para una corrida suelta sin instalar, lo mismo: `claude --plugin-dir D:\Escritorio\claude-plugins\design-staff-code`.

## Habilitar en un proyecto

En `.claude/settings.local.json` del proyecto (solo para vos) o en `.claude/settings.json` (para todo el equipo, si
todos tienen el marketplace):

```json
{
  "agent": "design-staff-code:staff-design-lead",
  "enabledPlugins": { "design-staff-code@jony-plugins": true }
}
```

- Sin `"agent"`, los agentes están disponibles pero el lead no toma la conversación principal.
- En los proyectos donde no lo habilitás, nada de esto existe.

## Arrancar un proyecto nuevo

1. Instalá el plugin en el proyecto (`claude plugin install design-staff-code@jony-plugins --scope local`) y habilitalo
   (`claude plugin enable design-staff-code@jony-plugins --scope local`). Viene apagado por defecto: instalado sin habilitar,
   no hace nada.
2. Abrí Claude Code en el proyecto y corré **`/design-staff-code:project-setup`**. Revisa qué hay, te pregunta lo que falta,
   inspecciona el código y la librería de componentes, instala `tools/medir.mjs` y genera la capa propia del proyecto
   sin pisar lo existente. También fija al
   `staff-design-lead` como agente principal.
3. Reiniciá Claude Code y probá con una iniciativa chica.

## Qué tiene que aportar cada proyecto

El sistema es genérico; rinde según la capa propia del proyecto, que arma `project-setup`:
- **`CLAUDE.md`**: fuentes de verdad (código, librería de componentes, flujo, documentos), quién decide qué, qué se
  escala, idioma, equipo y reglas de producto.
- **`<proyecto>-design-pipeline`**: reglas propias de producto, de código, DS y accesibilidad de su audiencia.
- **Skills del DS** (`<proyecto>-components`, `-tokens`, `-typography`), completadas desde la documentación de la
  librería y el tema real del proyecto.
- **`tools/medir.mjs`** y Playwright como dependencia de desarrollo, para medir en el navegador.
- **`design/knowledge/FUENTES_DEL_PROYECTO.md`**: dónde está cada tipo de conocimiento.
- Estado, pendientes, cartera de oportunidades y, si son varios, `WORKING_ON.md`.

Sin esa capa el sistema funciona, pero el lead marca como pendiente todo lo que el proyecto no define.

## Qué trae el plugin y qué queda afuera

Todo el sistema vive en el plugin: los agentes, las skills de producto, UX, UI, discovery y accesibilidad, el
conocimiento (`knowledge/`), las plantillas, los scripts y las guías de Impeccable (`vendor/impeccable/`, con su
licencia Apache-2.0). No hace falta instalar el plugin `impeccable`.

Queda afuera:
- **Playwright y su navegador**: lo instala el proyecto (`npm i -D playwright` y `npx playwright install chromium`).
  Es lo que le permite al lead capturar y medir.
- **La documentación de la librería de componentes** (por ejemplo `llms.txt` o su servidor MCP): la configura el
  proyecto.
- **Lo propio de cada proyecto**: `CLAUDE.md`, la skill de reglas de diseño y las skills del DS. Viven en el repo de
  ese proyecto (ver «Qué tiene que aportar cada proyecto»).

## Scripts

Corrélos desde la raíz del proyecto, con `python` (o `python3`):

```sh
python "<plugin>/scripts/case.py" init mi-iniciativa --title "Título"
python "<plugin>/scripts/case.py" event mi-iniciativa --actor staff-design-lead --type research --summary "..." --ref brief.md
python "<plugin>/scripts/validate_dossier.py" design/initiatives/mi-iniciativa --ready --case-study

# Discovery
python "<plugin>/scripts/case.py" init app-nueva --kind discovery --title "App nueva"
python "<plugin>/scripts/validate_discovery.py" design/initiatives/app-nueva --ready
```

Dentro de los agentes, `<plugin>` es `${CLAUDE_PLUGIN_ROOT}`. Funcionan en Windows, macOS y Linux.

Tests: `cd scripts && python -m unittest test_validate_dossier test_validate_discovery`.

## Mantener el sistema

Todo lo genérico del sistema se cambia **acá**, nunca en un proyecto: así cada proyecto que instale el plugin tiene la
misma versión. Por cada cambio: editar sin nada propio de un proyecto, subir la versión en `.claude-plugin/plugin.json`,
correr los tests (`python -m unittest discover -s scripts -p "test_*.py"`) y `claude plugin validate .`, hacer commit, y
correr `claude plugin update design-staff-code@jony-plugins`. Los cambios genéricos que valgan también para
`design-staff` (discovery, skills de producto y UX, validadores) hay que llevarlos a mano al otro plugin: son copias.
