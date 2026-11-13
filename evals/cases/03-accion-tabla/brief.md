# Caso simulado 03: acción poco utilizada en una tabla

**Simulación para evaluar el sistema.** Los datos y personas de este caso son ficticios; no son hechos de ningún producto real.

## Pedido inicial

“Los médicos no ven el botón ‘Resolver’ en la tabla. Hacelo más grande y con un color más fuerte.”

## Objetivo declarado

Reducir el tiempo que las tareas pendientes permanecen abiertas. No existe una meta numérica definida.

## Material disponible

- En seis sesiones observadas, cuatro médicos localizaron el botón sin ayuda. Dos no intentaron usarlo porque entendieron que la tarea aún no estaba lista para resolver.
- En un registro de uso, el 70 % de las tareas pendientes se abre desde una notificación y no desde la tabla. El registro no permite saber si el botón se vio o no.
- Un PM afirma que el color es el problema. No hay medición de contraste ni prueba de variantes.
- Las tareas pueden estar `pendiente`, `en revisión` o `resuelta`. Se desconoce si el médico puede resolver una tarea `en revisión` o si requiere otra aprobación.
- Restricción confirmada para este ejercicio: no se debe ofrecer una acción ejecutable cuando el sistema sabe que la tarea no puede resolverse.
- Se dispone de un diseño actual de la tabla, pero no se adjunta en esta prueba. Si su evaluación visual es decisiva, registrá esa dependencia; no inventes propiedades del diseño.

## Entrega esperada

Elegí el siguiente paso de diseño más útil. Podés recomendar una revisión visual condicionada, cambiar la forma de comunicar el estado, investigar una regla del flujo o intervenir en la notificación. Compará al menos dos hipótesis de causa, explicá qué evidencia faltaría y documentá por qué aceptás o descartás el pedido de agrandar el botón.
