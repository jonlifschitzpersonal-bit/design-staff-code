# Tabla de textos · <pantalla o flujo>

**Versión del diseño:** <ruta y archivo fuente · commit · fecha> · **Idioma fuente:** <locale> · **Locales destino:** <locales>

Cada texto que va a desarrollo o a traducción. Las claves las define desarrollo si ya tiene una convención; si no,
`<pantalla>.<elemento>.<estado>`. Los términos salen del glosario del proyecto.

| Clave | Dónde aparece (componente · estado) | Texto | Máx. caracteres | Variables y plurales | Notas para traducción / desarrollo |
| --- | --- | --- | --- | --- | --- |
| <checkout.submit.default> | <botón primario · por defecto> | <Enviar pedido> | <20> | <—> | <verbo: es la acción final> |
| <checkout.items.count> | <subtítulo> | <{count, plural, one {# producto} other {# productos}}> | <30> | <count: entero ≥ 0> | <—> |

## Estados cubiertos

- [ ] por defecto
- [ ] vacío
- [ ] carga
- [ ] error (de validación, de conexión, de permisos)
- [ ] éxito
- [ ] texto más largo probado en el frame
