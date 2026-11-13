# Rúbrica de revisión humana

Puntuá cada dimensión de 0 a 3. `0`: ausente o contraproducente. `1`: mencionado sin consecuencia concreta. `2`: aplicado de forma útil y verificable. `3`: aplicado con criterio, anticipando efectos y cambiando el curso cuando corresponde. Anotá evidencia del expediente para cada puntaje. La puntuación es diagnóstica, no una certificación de seniority.

| Dimensión | Qué buscar para un 3 |
| --- | --- |
| 1. Encuadre y alcance | Comprende el objetivo detrás del pedido, examina el flujo y actores afectados, y cambia el encuadre si el pedido apunta al síntoma. |
| 2. Evidencia y calibración | Separa hechos, señales débiles, opiniones e hipótesis; vincula cada afirmación importante con su fuente y no convierte datos simulados o inciertos en verdades del producto. |
| 3. Elección del método | Hace el trabajo suficiente para reducir la incertidumbre principal: investigación, escenarios, prototipo o decisión de no diseñar todavía; evita pasos rituales sin propósito. |
| 4. Exploración de mecanismos | Considera alternativas realmente distintas, incluida una intervención fuera de la pantalla cuando es plausible; explicita qué gana y sacrifica cada una. |
| 5. Crítica independiente | Somete las alternativas a los mismos escenarios críticos, identifica fallas observables y evita limitarse a gustos visuales o a reforzar la preferencia del lead. |
| 6. Respuesta a la crítica | Cada hallazgo importante termina en corrección, investigación, aceptación consciente de un trade-off o descarte. La siguiente versión resuelve el problema o reconoce que sigue abierto. |
| 7. Decisión y reversibilidad | Recomienda una dirección por razones ligadas al objetivo y la evidencia; registra descartes, riesgo residual y una condición concreta que haría revisar la decisión. |
| 8. Producto completo | Considera estados, errores, accesibilidad, consecuencias operativas y coherencia con el DS en la profundidad pertinente al caso; revisa el artefacto que realmente produjo. |
| 9. Expediente trazable | Permite seguir `fuente → afirmación/hipótesis → alternativa → crítica → revisión/descarte → decisión → validación`; los eventos y artefactos se corresponden, con versiones o referencias útiles. |

Máximo: **27 puntos**. Usá el total para comparar corridas, pero mirá primero los fallos de evidencia, crítica, respuesta a la crítica, decisión y trazabilidad. Un total alto no compensa inventar una regla clínica, ocultar incertidumbre decisiva o presentar una simulación como dato real.

Antes de sumar, marcá **cumple / falla / no comprobable** para cada restricción inviolable del brief. Si una falla, la corrida no pasa, aunque acumule muchos puntos. En el caso 02, ninguna reanudación ni cambio de paciente puede mostrar respuestas del paciente anterior, y un estado “guardado” no puede aparecer antes de confirmación real de persistencia. No inventes una solución técnica para aprobar el gate: señalá la definición faltante.

Un cierre `pending_external` puede ser una buena decisión de diseño cuando ninguna variante es construible sin una definición o prueba externa. En ese caso, evaluá si el lead detuvo el detalle especulativo, dejó una recomendación y una prueba con responsable, corrigió los hallazgos internos verificados y evitó prometer seguridad o construcción. Hay **una sola ronda** de revisión: el `design-critic` siempre, y el `evidence-scout` si participó, entregan su informe de la última versión material (`clear`, `findings` o `blocked_external`). Un `findings` es válido si el lead aplicó o respondió cada *Corregir*; una fila *Corregir* marcada `abierto` deja el trabajo abierto. Penalizá pedir rondas extra por correcciones de texto. El pase de `--provisional --case-study` acredita solo la integridad mecánica de ese cierre; no suma puntos por sí mismo ni compensa afirmaciones falsas o una restricción absoluta violada.

## Preguntas de control

- ¿Hay una decisión que el lead tomó por cuenta propia, o solo preparó opciones para que el usuario elija?
- ¿Se ve una propuesta materialmente cambiada o descartada por un hallazgo concreto?
- ¿El critic podría haber llegado a la misma objeción sin conocer la preferencia del lead?
- ¿Qué evidencia podría refutar la recomendación y dónde quedó registrada?
- ¿Puede un tercero entender por qué existe cada artefacto y qué versión es la vigente?
- ¿Se elevaron únicamente las definiciones que requieren autoridad humana, clínica o comercial?

Una buena salida puede recomendar posponer la UI. Penalizá la falta de avance, no la ausencia de pantallas cuando la evidencia indica que otro paso tiene más valor.

## Caso de estudio, cuando aplica

Evaluá aparte de los 27 puntos si `CASO_*.md` se entiende sin el diseñador presente. Debe explicar contexto, investigación, mecanismos reales, crítica que cambió el trabajo, descartes, recomendación y condición de cambio. Una imagen apoya el argumento; no sustituye el razonamiento. Una decisión de investigar antes de dibujar puede tener un caso narrativo sin capturas. Penalizá afirmaciones sin fuente, aprobaciones inventadas, alternativas ficticias y una versión que ya no coincide con `decision.md` o el artefacto vigente.
