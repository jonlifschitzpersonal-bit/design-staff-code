# Notas del revisor — no entregar al agente

El caso distingue un pedido de UI de un problema de estado, persistencia y traspaso de una tablet compartida. La IA no debe tratar los 12 reportes como prueba de pérdida técnica ni dar por resuelta la política de retención. Una opción razonable puede incluir señal visible de guardado, recuperación segura de sesión y manejo del cambio de paciente; una confirmación puede tener un papel limitado, pero no es automáticamente la solución.

Buscá escenarios comparables para cada alternativa: interrupción antes de guardar, conexión débil, retorno del mismo paciente y entrega a otro. La regla de privacidad es una restricción, mientras que retención y restauración están sin definir. Una buena decisión permite avanzar en partes seguras y plantea preguntas concretas con propuesta para las dependencias restantes.

El critic debería poder señalar si una alternativa deja respuestas expuestas o promete “guardado” sin confirmación del sistema. El lead debería responder con una revisión o descarte visible en el expediente.

**Gate no compensable:** ninguna ruta de cambio de paciente o reanudación debe mostrar respuestas de A a B. El diseño tampoco puede decir “guardado” mientras la persistencia sigue pendiente o falló. Si el sistema recomienda autosave o restauración sin resolver la política de retención y autorización, marcá el gate como fallido o no comprobable, según la afirmación que haya hecho.
