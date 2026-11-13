---
name: <proyecto>-typography
description: >-
  Referencia de la escala tipográfica del Design System de <Proyecto> (librería <librería y versión>, tema en <ruta del tema>) y cuál usar al diseñar. Usar
  SIEMPRE al escribir o estilar texto en una pantalla de <Proyecto>, al elegir un nivel de la escala o al auditar tipografía.
---

# Tipografía de <Proyecto>

Fuente: la escala tipográfica del tema (`<ruta del tema>`) y las clases o variables de la librería, leídas el <fecha>. Si el tema cambió, manda el código. El
color va por `<proyecto>-tokens`.

Familias: <familia de display / títulos> y <familia de texto / UI>.

| Nivel (clase o variable) | Familia · peso | Tamaño / interlineado | Usalo para | No lo uses para |
| --- | --- | --- | --- | --- |
| <clase o variable> | <familia · peso> | <px / px> | <rol> | <…> |

## Reglas

- Todo texto va con un nivel de la escala del tema. Un tamaño suelto (`text-[17px]`, `font-size: 17px`) se marca como propio y se justifica.
- Piso de tamaño por superficie: <superficie → nivel mínimo, o `<pendiente>`>.
- Cada superficie usa su propia escala si el DS la tiene (por ejemplo, web y móvil); no se mezclan.
