# Criterio compartido de product design

Este documento orienta al Staff Design Lead, al Discovery Lead, al Evidence Scout y al Design Critic del plugin `design-staff-code`. Es un **mapa de decisiones**, no una fuente de hechos del dominio ni una checklist para ejecutar entera. Leé los apartados relevantes y seguí sus fuentes cuando el problema lo requiera.

**Dónde está el conocimiento de cada proyecto:**
- su `CLAUDE.md`, que define las fuentes de verdad;
- `design/knowledge/FUENTES_DEL_PROYECTO.md`, si existe;
- su skill de reglas de diseño.

Documentos históricos, ejemplos, capturas de Mobbin y la opinión del agente sirven para generar hipótesis o contrastar patrones. No reemplazan una fuente vigente ni validan el comportamiento de los usuarios del proyecto. Para afirmaciones de dominio (clínicas, legales, financieras), permisos o prioridades comerciales sin fuente, registrá la pregunta y la propuesta; no cierres el vacío por intuición.

Para cada iniciativa material, dejá en `evidence.md` una **cobertura de fuentes**: área y términos buscados, documentos vigentes y reuniones relevantes consultados, fecha de cada fuente, contradicciones y qué fuente o dueño puede resolverlas. En `artifacts.md`, registrá file key, node ID y fecha de inspección del Figma/FigJam vivo; si no se pudo abrir, registrá el intento y dejá la parte visual o de flujo como no comprobada. El lead pasa extractos y capturas con versión al scout y al critic. Acceso a una carpeta o plugin instalado no prueba que se leyó una fuente ni que el archivo vivo estaba disponible.

## Estándar de una decisión Staff

1. **Encuadre:** distinguí pedido, problema y oportunidad. Preguntá por qué ahora, quién gana, qué pasa si no se cambia nada y cuál es el resultado observable del usuario y del producto. Una pantalla solicitada puede ser el síntoma de un problema de flujo o de operación.
2. **Sistema:** ubicá la decisión en el mapa de actores, objetos, estados y traspasos. Buscá reglas o vocabulario duplicados entre superficies (apps, dashboards, equipos internos) y procesos fuera de pantalla. Mostrá consecuencias para otras superficies y responsables.
3. **Evidencia calibrada:** separá hecho confirmado, inferencia, supuesto y contradicción. Para cada afirmación decisiva guardá fuente, fecha y alcance. Si una fuente da recuentos parciales, no supongas que sus grupos no se superponen ni que agotan la muestra; si mide una demora, no la conviertas por sí sola en causa de una pérdida. Una heurística explica una preferencia de diseño; no demuestra que funcionará para estas personas. Priorizá la incertidumbre que podría cambiar la elección.
4. **Mecanismos:** en decisiones materiales, compará formas de resolver el problema que cambien la interacción o el modelo operativo. Incluí una intervención sin pantalla si podría resolver mejor el problema. Probá las opciones con el mismo escenario, estados de excepción y consecuencias repetidas en el tiempo.
5. **Crítica que cambia el trabajo:** distinguí defecto reparable, dependencia empírica, trade-off real y falla de mecanismo. Una crítica útil puede llevar a corregir, probar, descartar o reformular. El critic señala una objeción; el lead registra su respuesta y verifica la versión siguiente.
6. **Decisión responsable:** recomendá una dirección provisional con beneficio, sacrificio, evidencia, riesgo residual, señal de éxito y condición concreta que la haría cambiar. Una restricción absoluta no se negocia como sacrificio: probá la versión vigente en el escenario que puede romperla y bloqueá su implementación si falla o no puede comprobarse. Si su alcance es ambiguo, documentá ambas lecturas, proponé la más segura y pedí la definición a su dueño. Separá hipótesis de diseño, trabajo preparatorio y autorización para construir. La aprobación humana, una entrevista y una revisión de IA son evidencias diferentes.
7. **Entrega completa:** contrastá el artefacto real con la decisión, el flujo, los estados, la accesibilidad y el DS. Registrá qué cambió por feedback y cuándo revisar el resultado. Promové a conocimiento estable solo lo confirmado y vigente.

## Profundización a demanda

| Si la incertidumbre dominante es… | Consultá |
| --- | --- |
| Modelo operativo, varios actores o influencia entre equipos | `${CLAUDE_PLUGIN_ROOT}/skills/product-designer/references/product-systems-and-edge-cases.md` (permisos, concurrencia, estado entre dispositivos) y `collaboration-and-delivery.md` (influencia y entrega entre equipos). |
| Evidencia, descubrimiento o supuestos | `${CLAUDE_PLUGIN_ROOT}/skills/product-designer/references/discovery-and-evidence.md`. |
| Producto nuevo, discovery, o elegir entre JTBD, journey, blueprint, story map u otro método | Skill `design-staff-code:design-discovery` (etapas, etiquetas de evidencia, plantillas y design brief; para leerla sin invocarla: `skills/design-discovery/` dentro del plugin). Para producto nuevo, el agente `discovery-lead`. |
| KPI, experimento o señal posterior a entrega | `${CLAUDE_PLUGIN_ROOT}/skills/product-designer/references/metrics-and-experiments.md`. |
| Flujo, recuperación o estados | `${CLAUDE_PLUGIN_ROOT}/skills/ux-designer/references/patterns-and-flows.md`; `psychology-deep-dive.md` de esa skill solo si afecta el caso. |
| Craft visual y fidelidad en código | `design-staff-code:ui-designer`, la skill de reglas de diseño del proyecto y las skills de su DS, la documentación de la librería de componentes, y `${CLAUDE_PLUGIN_ROOT}/knowledge/SUPERFICIE_CODIGO.md`; inspección de la app corriendo. |
| Accesibilidad | Skill `design-staff-code:design-accessibility` (WCAG 2.2 AA verificable en la pantalla que corre; contraste, tamaños y targets medidos en el DOM con `tools/medir.mjs`) más las reglas de accesibilidad del proyecto. |

La calidad del sistema se puede revisar con una rúbrica y casos simulados del proyecto, si los tiene. Un resultado convincente en una simulación no certifica que los agentes trabajen como un staff designer en un caso real; compará también decisiones históricas ocultando la solución final y evaluá qué cambió gracias a la crítica.
