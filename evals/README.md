# Evaluación del sistema

Este directorio prueba si el sistema toma decisiones de diseño defendibles y deja un expediente auditable. Sirve para
comparar versiones del plugin, de un agente, de una skill o del modelo con la misma entrada.

Los casos de `cases/` son **fixtures ficticios**: no son hechos de ningún producto real y no se incorporan al
conocimiento de un proyecto. `reviewer.md` es la guía del revisor humano y nunca se entrega a los agentes. Un proyecto
puede sumar casos propios, por ejemplo un replay histórico recortado con la solución final oculta, en su propia carpeta
(`design/evals/cases/`) y usarlos con `--cases-dir`.

## Qué se evalúa

Si el lead entiende el problema, busca y calibra evidencia, explora mecanismos distintos, usa la crítica para cambiar el
trabajo, descarta propuestas cuando corresponde, toma una decisión provisional y explica qué la haría cambiar. También
si el expediente permite reconstruir el recorrido. No exige coincidir con una solución de referencia, y un buen puntaje
no equivale a validación de usuarios.

## Cómo correr un caso

`<plugin>` es la carpeta del plugin (en una instalación desde el marketplace, la que muestra `claude plugin list` en
«Read from»). En Windows el intérprete es `python`; en macOS y Linux, `python3`.

1. Prepará una carpeta separada. El preparador copia **solo** el `brief.md` del caso y un `settings.json` que habilita el
   plugin (`design-staff-code@inline`, porque viene apagado por defecto) y fija al `staff-design-lead` como agente principal. Deja fuera `reviewer.md`, la rúbrica y cualquier proyecto real:

   ```sh
   python "<plugin>/evals/prepare_fixture.py" 02-tablet-interrumpida <carpeta-nueva>
   # Caso propio de un proyecto, corrido desde la raíz de ese proyecto:
   python "<plugin>/evals/prepare_fixture.py" <caso> <carpeta-nueva> --cases-dir design/evals/cases
   ```

2. Abrí Claude Code en esa carpeta, con el plugin cargado, sin MCP externo y con un límite de turnos:

   ```sh
   cd <carpeta-nueva>
   claude --plugin-dir "<plugin>" -p "Procesá brief_input.md como una iniciativa completa. Investigá, criticá, revisá o descartá, decidí provisionalmente y dejá un expediente trazable. No uses datos fuera de este brief." \
     --setting-sources project --strict-mcp-config \
     --permission-mode auto --max-turns 30 --no-session-persistence
   ```

   Antes de la corrida larga, comprobá que cargó: la sesión tiene que responder que es `design-staff-code:staff-design-lead`.
   La carpeta separa los materiales del caso, pero **no es una barrera de acceso al filesystem**. Comprobá que la
   corrida cite solo el brief y el método del plugin. Si necesitás aislamiento estricto, usá un contenedor que no monte
   tus proyectos. Si leyó una fuente externa, la corrida es **no ciega**.
3. Dejá que el lead trabaje solo: que convoque **una** ronda de crítica, implemente y tome postura. No elijas por él ni
   respondas preguntas salvo que el caso lo indique. Si le falta un dato, debe registrarlo como incertidumbre y decidir
   algo que lo tolere, o explicar por qué no puede decidir.
4. Corré el gate:

   ```sh
   python "<plugin>/scripts/validate_dossier.py" design/initiatives/<slug> --ready --case-study
   # Si la construcción queda bloqueada por una definición o prueba externa:
   python "<plugin>/scripts/validate_dossier.py" design/initiatives/<slug> --provisional --case-study
   ```

5. Leé el expediente y el artefacto. Puntuá con `scorecard-template.md`, la rúbrica de `RUBRIC.md` y las notas de
   `reviewer.md`. Cada puntaje cita una sección o un evento concreto. El gate no reemplaza esta revisión.
6. Repetí con la misma entrada al cambiar prompts, agentes, skills o modelo. Registrá modelo, tokens, duración,
   llamadas a especialistas e intervenciones humanas cuando el CLI los reporte. Compará decisiones y errores, no solo el
   total.

## Qué acredita el gate

- **`--ready --case-study`**: la estructura completa, los eventos de investigación, propuesta, crítica y decisión, el
  caso de estudio enlazado y el informe del `design-critic` (y del `evidence-scout` si participó) posterior a la última
  revisión **material**, con informe en `reviews/` y outcome `clear` o `findings`. Una revisión `text_only` no invalida
  el informe recibido. Una fila *Corregir* marcada `abierto` en `critiques.md` bloquea el cierre.
- **`--provisional --case-study`**: además acepta `blocked_external`, y exige en `decision.md` la sección
  `## Cierre provisional` (`pending_external`, construcción bloqueada, dependencia con responsable y prueba de
  desbloqueo) y un evento `decision` con `outcome=pending_external` posterior al informe. Documenta una investigación
  bloqueada; **no autoriza construir**.

Ningún gate juzga si la decisión es buena, si los auditores tienen razón ni si el diseño resuelve el problema. Eso se
evalúa con la rúbrica.

## Uso para mejorar el sistema

Guardá los scorecards fuera de `cases/` para no contaminar la prueba ciega. Empezá con los casos sintéticos y después
repetí el procedimiento con iniciativas históricas propias: ocultá la solución final, conservá las fuentes disponibles
en ese momento y compará la decisión y el recorrido. Si el sistema falla, corregí la fuente de conocimiento, la
autoridad del lead o el punto de control que causó el fallo, **en el plugin**. No agregues una regla general a partir de
un único caso.
