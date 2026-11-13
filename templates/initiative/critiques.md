# Críticas y respuestas · {{TITLE}}

Cada crítica identifica la versión exacta inspeccionada. El lead completa la respuesta y la nueva comprobación antes de cerrar el hallazgo.

| ID | Agente | Opción / artefacto y versión | Escenario y hallazgo | Tipo e impacto | Evidencia | Respuesta del lead | Nueva comprobación / estado |
| --- | --- | --- | --- | --- | --- | --- | --- |

Tipos: `problema corregible`, `dependencia`, `trade-off`, `falla de mecanismo`, `violación de restricción`. Estados: `abierta`, `corregida`, `investigar`, `aceptada`, `bloqueante`, `descartó opción`. Una posible violación de una regla absoluta no se acepta como trade-off. Una hipótesis empírica no queda refutada por una opinión del critic.

## Pasada visual final

Si hay artefacto visual, registrá por separado los hallazgos de las guías de Impeccable (`critique`, `clarify` y `distill`) sobre la captura y las medidas del DOM reales. Incluí incluso las sugerencias descartadas que podrían cambiar la pantalla; explicá la razón según objetivo, DS, estados necesarios o accesibilidad. Una corrección propia no se deja como pregunta para el usuario. Verificá una vez la versión posterior al cambio con una captura nueva; no pidas re-revisión al especialista.

| ID | Skill | Pantalla (ruta), captura y versión inspeccionada | Hallazgo y efecto para el usuario | Decisión y fundamento | Cambio aplicado o motivo de descarte | Captura/versión posterior y nueva comprobación | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- |

Si falta una captura actual o la medición necesaria, anotá `no comprobable` con la causa; no marques la UI como aprobada.
