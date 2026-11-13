---
name: <proyecto>-tokens
description: >-
  Guía de decisión de los tokens de color del Design System de <Proyecto> (librería <librería y versión>, tema en
  <ruta del tema>): cuándo cada token DEBE y cuándo NO debe usarse, y qué modo va en cada superficie. Usar SIEMPRE al
  elegir un color en el código de <Proyecto> y al auditar el uso de color.
---

# Tokens de color de <Proyecto>

Fuente: las variables del tema en `<ruta del tema>` y las que la librería expone (`<fuente: documentación o
herramienta del MCP que lista las variables del tema>`), leídas el <fecha>. Si el tema cambió, manda el código.

## Modos

| Modo | Dónde va | Dónde no |
| --- | --- | --- |
| <modo> | <superficie o tipo de pantalla> | <…> |

## Tokens

| Token (variable CSS) | Valor (por modo) | Usalo para | No lo uses para |
| --- | --- | --- | --- |
| <--variable> | <valor light / valor dark> | <rol> | <error típico> |

Los valores se leen resueltos en el navegador (`tools/medir.mjs`): la librería puede declararlos en `oklch()` u otros
espacios, y lo que cuenta es el color que el navegador calcula.

**Cuidado con los valores compuestos.** Si un token usa `color-mix()` o transparencia, el valor «claro» que declara la
librería puede engañar en otro modo o sobre otro fondo: anotá el fondo contra el que se midió. Si leés los tokens con el
servidor MCP de la librería (`get_theme_variables` u otro), contrastalos con la medición: puede devolver el modo claro
incompleto.

## Contraste ya medido

Medido con `tools/medir.mjs` y el script de `design-staff-code:design-accessibility` sobre el DOM real:

| Texto / elemento | Fondo | Modo | Ratio | Cumple |
| --- | --- | --- | --- | --- |
| <token> | <token> | <modo> | <x.xx:1> | <AA texto / AA grande / no> |

Todo color crudo, todo par nuevo y todo modo sin fila en esta tabla se mide antes de entregar. Un valor por defecto de la
librería no se da por válido sin medirlo.
