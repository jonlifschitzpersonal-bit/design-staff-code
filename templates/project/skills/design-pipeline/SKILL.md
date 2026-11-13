---
name: <proyecto>-design-pipeline
description: >-
  Aplicar las reglas propias de producto, de código y de Design System de <Proyecto> al diseñar o modificar pantallas, flujos
  y componentes. Usar junto al protocolo del staff-design-lead (plugin design-staff-code); cargar solo las skills de
  ejecución pertinentes.
---

# Diseño de <Proyecto>

El ciclo de decisión, la crítica y el expediente los dirige `design-staff-code:staff-design-lead`. Esta skill aporta solo
las restricciones propias de <Proyecto>. Lo genérico (método, accesibilidad WCAG, guías de Impeccable, leyes de UX)
está en el plugin y no se repite acá.

## Fuentes antes de diseñar

1. Leé `CLAUDE.md` y las secciones de `docs/CURRENT_STATE.md` y `docs/PENDING_TASKS.md` que toquen la tarea.
2. Para el orden y la existencia de pantallas, inspeccioná <fuente canónica del flujo> (`<ubicación>`). Ante un
   conflicto con un documento, registrá la contradicción y seguí la fuente canónica.
3. Inspeccioná la pantalla real (la app corriendo) antes de cambiarla: rutas en `<carpeta de pantallas>`, capa de tema
   en `<ruta del tema>`.
4. Superficies y actores: <por ejemplo «web móvil 390×844 para el cliente; web de escritorio 1440×900 para el operador»>.
   Verificá si cambió el modelo operativo antes de mejorar una pantalla existente.

## Construir en código

- Antes de dibujar, leé `knowledge/SUPERFICIE_CODIGO.md` del plugin (el lead conoce su ruta). Para la UI, consultá
  `design-staff-code:ui-designer` y las skills del DS: `<proyecto>-components`, `<proyecto>-tokens` y
  `<proyecto>-typography`, y la documentación de la librería (`<fuente>`) para cada componente que uses.
- **El diseño manda, la librería lo sostiene.** Primero jerarquía, composición e interacción; después el mapeo a la
  librería. Si un componente de la librería da exactamente ese diseño, se usa tal cual. Si no, se sobrescribe en la capa
  de tema (una vez, no pantalla por pantalla) o se arma uno propio, y se registra el motivo para <dueño del DS>.
- <Reglas visuales confirmadas del proyecto: modos de color, densidad, plataformas, una por línea, con quién y cuándo.>
- Idioma de lo que ve el cliente en la app: <idioma>.
- Después de editar: levantá la app, corré `node tools/medir.mjs` sobre cada estado y viewport, y mirá la captura.

## Accesibilidad en <Proyecto> (reglas del proyecto)

`design-staff-code:design-accessibility` aporta WCAG 2.2 AA, la medición de contraste con su script y el formato de salida.
Estas reglas **se suman** y mandan cuando son más exigentes:
- **Audiencia:** <edad, contexto de uso, condiciones: baja visión, temblor, uso al sol, estrés, conectividad…>.
- **Texto mínimo:** <tamaño mínimo por superficie, o `<pendiente>`>.
- **Targets:** <piso medido en el DS por superficie>.
- **Pares de color ya validados:** <par → ratio, o «ninguno todavía: medir todo»>.
- **Errores del DS que ya ocurrieron:** <lista, o «ninguno registrado»>.

## Revisión antes de entregar

- Objetivo y acción primaria, estados vacío/carga/error, casos fuera del camino, recuperación y consistencia entre
  superficies. Cada número o claim tiene fuente.
- Control de `design-staff-code:ui-designer`, accesibilidad y la pasada visual con las guías de Impeccable que describe el
  lead. Lo de forma y copy propio se arregla antes de entregar, sin pasarle el QA a <responsable>.
- La recomendación queda provisional hasta la validación humana que corresponda según `CLAUDE.md`.
