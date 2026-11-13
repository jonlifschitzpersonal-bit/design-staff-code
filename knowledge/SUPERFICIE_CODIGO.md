# Superficie: código

Este plugin diseña **directo en código** (React u otro framework web con una librería de componentes), sin Figma. Esta
guía reemplaza todo lo que `design-staff` hace con Figma. Donde otra guía diga «frame», «node ID» o «archivo de Figma»,
leé: **pantalla en la app que corre**, **ruta + archivo fuente** y **repositorio del proyecto**.

## Principio

El artefacto es la aplicación corriendo. La verdad visual es lo que el navegador calcula, no lo que el agente declara ni
lo que dice el código fuente. Un tamaño, un color o un contraste solo cuenta como medido si salió de
`tools/medir.mjs` (Playwright) sobre la pantalla real.

## 1. Antes de escribir un componente

1. Leé las skills de diseño del plugin en el orden de siempre (`product-designer`, `ux-designer`, `ui-designer`), y las
   skills del sistema de diseño del proyecto (`<proyecto>-components`, `-tokens`, `-typography`).
2. Consultá la documentación de la librería de componentes del proyecto (su `llms.txt` o su MCP, según diga el
   `CLAUDE.md`) para **cada componente que vayas a usar**, antes de usarlo. Anotá en `exploration.md` qué consultaste.
3. **No reinventes lo que la librería ya trae.** Un componente propio solo se justifica si la librería no tiene el rol
   o si sus reglas de dominio lo impiden. Registrá cada componente propio con su motivo.

## 2. Dibujar

- Cada pantalla es una ruta o una vista que se puede abrir por URL. Cada **estado** que definiste (vacío, cargando,
  error, texto muy largo, muchos ítems, sin conexión, sin permiso) tiene que poder abrirse directo, por ejemplo con un
  parámetro `?estado=vacio` o con datos de muestra fijos. Si un estado no se puede abrir, no se puede medir ni revisar.
- **Datos de muestra realistas**, incluidos los casos difíciles: el nombre más largo, el recuento más alto, el texto en
  otro formato. Los pisos de accesibilidad se prueban con ellos, no con «Juan Pérez».
- **Los valores por defecto de la librería no cumplen los pisos del proyecto** (típicamente texto de 14 px y controles de
  40 px). Se sobrescriben **una sola vez, en la capa de tema** (variables CSS, props de tamaño, clases de la
  librería), no pantalla por pantalla. Esa capa es lo que documenta la skill `-tokens` del proyecto.
- Usá los tokens y la escala tipográfica del proyecto. Nada de valores sueltos (`#1a73e8`, `text-[17px]`) en una
  pantalla: si falta un token, agregalo a la capa de tema y a la skill, y registralo.

## 3. Medir y mirar (obligatorio al terminar de dibujar y antes de la revisión)

Con el servidor de desarrollo levantado, desde la raíz del proyecto, **por cada estado relevante y por cada viewport del
alcance**:

```
node tools/medir.mjs --url http://localhost:5173/<ruta> --name <pantalla>-<estado> \
  --out design/initiatives/<slug>/capturas --width 390 --height 844 \
  --min-text <piso de texto del proyecto> --min-target <piso de target del proyecto>
```

Genera junto a la captura:
- `<name>.png`: captura a 2x. De página completa; con `--selector "<css>" --crop`, recortada a ese elemento (útil para
  una sola pieza o un solo componente).
- `<name>.medidas.json`: el texto (tamaño, peso, interlineado, color resuelto), los **controles** (el que ve y toca la
  persona, no el `<input>` nativo oculto que ponen las librerías), el contraste **no textual** de campos, casillas,
  radios e interruptores, el **foco con teclado** y el resumen con los incumplimientos de los pisos. Los controles
  llevan un nombre estable (`rol "texto" @bloque`), comparable entre corridas.
- `<name>.contraste.json`: pares de color de texto y `non-text` en el formato de
  `skills/design-accessibility/scripts/contrast.py`. Los fondos translúcidos ya vienen compuestos. Corrélo:
  `python "${CLAUDE_PLUGIN_ROOT}/skills/design-accessibility/scripts/contrast.py" --json <name>.contraste.json`.
- `<name>.contraste-no-comprobable.json`, si existe: solo textos sobre fondo con imagen o degradado. Esos pares quedan
  **no comprobables**; no inventes un valor.

**Foco con teclado.** `medir.mjs` recorre la página con `Tab`, compara una captura recortada de cada control con y sin
foco, y mide el contraste del aro contra lo que tapa (≥ 3:1). Es una aproximación por píxeles: informa «sin indicador de
foco», «aro bajo 3:1» y los controles que `Tab` no alcanza (los radios de un grupo se recorren con flechas: informativo).
`--sin-foco` lo omite.

**`--strict`** sale con código 1 si hay texto o controles bajo los pisos, contraste no textual bajo 3:1, controles sin
indicador de foco, aro bajo 3:1 o desborde horizontal.

Después de **mirar la captura** (abrila con `Read`): la medición dice si cumple, no si se ve bien. La pasada visual
(`critique`, `clarify`, `distill`) se hace sobre esa captura.

Lo que esta medición **no** comprueba, y hay que marcar como no comprobable si el diseño depende de ello: hover, estado
seleccionado o con error si la página no se carga en ese estado (abrilo por URL o parámetro y medí de nuevo), modo
oscuro (medí con la captura tomada en ese modo), lector de pantalla, orden real de lectura, dispositivos reales, zoom
del sistema, animaciones y contraste sobre imágenes. Si podés probarlo con Playwright (otro viewport,
`page.emulateMedia`), probalo y anotá el resultado.

Si el proyecto adoptó una librería de componentes, antes de dibujar medí su **banco** sin personalizar y aplicá la
**capa de pisos** en el tema: ver `RECETAS_LIBRERIAS.md`.

## 4. Registrar

En `artifacts.md`, en lugar del file key y los node IDs, por cada pantalla y estado:
- la URL de la ruta y el **archivo fuente** (`src/...`);
- el viewport y la fecha de la inspección;
- la captura y los `.medidas.json` / `.contraste.json` correspondientes;
- si el proyecto usa git, el **hash del commit** (o «sin commit: árbol de trabajo» si no se hizo). Una crítica debe
  apuntar a la versión que realmente vio.

En la tabla de accesibilidad, la columna «Elemento (node ID)» pasa a ser «Elemento (selector o texto) + captura», y la
columna «Medido» cita el valor del JSON, no una estimación.

## 5. Revisión independiente

El critic y el scout **no tienen navegador**. Inspeccioná vos la app real y armá el paquete con:
- las capturas locales de cada estado y viewport;
- los `.medidas.json` y el resultado de `contrast.py`;
- las rutas de los archivos fuente de las pantallas (pueden leer el código, no ejecutarlo);
- la lista de estados y cómo abrir cada uno.

Una captura sola no alcanza para que juzguen tamaños: pasales las medidas.

## 6. Cierre

Para cerrar con `--ready`:
- `npm run build` (o el equivalente del proyecto) termina sin errores;
- `tools/medir.mjs --strict` termina en 0 sobre los estados finales (o cada incumplimiento está en `decision.md` como
  excepción con su motivo y su responsable). Un falso positivo se documenta, no se silencia: decí qué elemento es y por
  qué no cuenta;
- la tabla «Skills y guías leídas» está completa, e incluye la documentación de la librería que consultaste.

## 7. Qué no cambia

El discovery, las skills de producto, UX y UX writing, las reglas del proyecto, la revisión de **una sola ronda**, el
expediente, los validadores y el informe de cierre funcionan igual que en `design-staff`.
