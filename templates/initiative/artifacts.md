# Artefactos · {{TITLE}}

| ID | Tipo | Link o ruta | Versión / fecha | Qué representa | Estado |
| --- | --- | --- | --- | --- | --- |

Registrá, por cada pantalla y estado: la URL de la ruta, el archivo fuente (`src/...`), el viewport, el hash del commit (o «árbol de trabajo sin commit»), la captura y sus `.medidas.json` / `.contraste.json` (generados por `tools/medir.mjs` en `capturas/`), y los documentos utilizados en cada revisión. Una crítica debe apuntar a la versión que realmente vio; la decisión vigente debe apuntar al artefacto entregado. No confundas un borrador local con una pantalla publicada o aprobada.

Anotá la fecha y el resultado de la inspección de la app corriendo. Si solo hay capturas antiguas o la app no se pudo levantar, indicá qué estados y propiedades no se pudieron comprobar y pasá esa limitación al critic.

En la pasada final con las guías de Impeccable (`critique`, `clarify` y `distill`), agregá las capturas antes/después, URL y archivo fuente, modo, estados, viewport y versión exacta. La captura posterior debe haberse tomado después de la última corrección visible. Enlazá los hallazgos y decisiones registrados en `critiques.md`; no trates una captura vieja como evidencia de la versión entregada.

Si la iniciativa requiere caso de estudio, agregá acá su ruta (por defecto `docs/briefs/CASO_<NN>-<feature>.md`; el nombre del archivo empieza con `CASO_`), su fecha de actualización y el estado de la recomendación. El caso se redacta y actualiza durante la iniciativa; la bitácora no lo reemplaza.
