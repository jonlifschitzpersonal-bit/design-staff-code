---
name: <proyecto>-components
description: >-
  Catálogo de los componentes del Design System de <Proyecto> (librería <librería y versión>) y cuándo usar cada uno y
  con qué props. Usar SIEMPRE antes de elegir, usar o construir un componente en una pantalla de <Proyecto>, y cuando
  se pregunte «qué componente uso para X» o «qué variante va acá».
---

# Componentes de <Proyecto>

Fuente: la librería **<librería y versión>**. Documentación: `<llms-components.txt, llms-patterns.txt, servidor MCP u
otra fuente, con su dirección>`, leída el <fecha>. Si la librería cambió de versión, manda su documentación: volvé a
leerla y actualizá esta tabla. El color va por `<proyecto>-tokens` y el texto por `<proyecto>-typography`.

**Antes de usar un componente**, consultá su documentación en la fuente de arriba. Esta skill dice *cuándo* usarlo en
<Proyecto>; la documentación dice *cómo*.

## Catálogo

| Componente | Import | Props / variantes que usamos | Cuándo usarlo | Cuándo NO |
| --- | --- | --- | --- | --- |
| <nombre> | `<paquete>` | <prop: valores> | <uso en este producto> | <qué usar en su lugar> |

## Valores por defecto que NO cumplen los pisos del proyecto

Medidos con `tools/medir.mjs` sobre el componente sin personalizar. Cada fila dice dónde se corrige (una sola vez):

| Componente | Qué incumple | Medido | Piso | Dónde se corrige |
| --- | --- | --- | --- | --- |
| <nombre> | <tamaño de texto / target / contraste> | <valor> | <piso> | <variable del tema, prop de tamaño o clase> |

## Recetas

<Composiciones repetidas que no son un componente: encabezados, pies con acciones, listas de opciones. Una por bloque,
con los componentes que las forman.>

## Reglas

- Si un componente de la librería da exactamente el diseño, se usa tal cual, sin envolverlo ni reescribir sus estilos.
- Si ninguno lo da, se sobrescribe en la capa de tema (una vez) o se arma uno propio, y se marca para <dueño del DS>.
  No se fuerza un componente que empeore el diseño.
- Un cambio en la capa de tema afecta todas las pantallas que usan ese componente: volvé a medir todas las pantallas
  afectadas, y coordiná antes según `CLAUDE.md`.
- <Reglas de rol propias del producto: por ejemplo, un filtro no se dibuja como una acción; un solo botón principal por
  pantalla.>
