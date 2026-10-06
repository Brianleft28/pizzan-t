## Plan: Documentación de Dependencia del Tema (Plantilla)

### [Goal Description] (目的 - Mokuteki)
Confirmar y documentar formalmente que el bot "vive en el tema" (es decir, depende fuertuate y estrictamente de la plantilla/tema visual de PokéMMO actual). Dado que el OCR y los píxeles (HP, Status) están calibrados para esa interfaz específica, es crucial documentarlo en el `README.md` apuntando a un archivo detallado en `docs/`.

### Proposed Changes

#### [NEW] `docs/theme_dependency.md`
Crear un archivo explicando la simbiosis entre el bot y el tema:
```markdown
# 🎨 Dependencia de Plantilla (Theme Dependency)

Este bot "vive en el tema". Esto significa que toda su lógica de visión (OCR y detección de píxeles) está anclada a la plantilla estética que se usó durante la calibración.

## ¿Qué pasa si cambio el tema de PokéMMO?
Si cambias el tema (Theme) en el juego o alteras los archivos XML de la interfaz original, el bot dejará de funcionar correctamente porque:
1. La barra de HP cambiará de posición o tamaño.
2. Los textos de combate (Battle Message) se desplazarán.
3. Los iconos de estado (Status) no coincidirán con las coordenadas en `config.json`.

**Mandato de Diseño:** Respeta la UI original. Si actualizas tu tema, tendrás que volver a calibrar todas las coordenadas usando la pestaña **Calib** en la interfaz del bot.
```

#### [MODIFY] `README.md`
Añadir una nota de advertencia en la sección de instalación/calibración y usar el enlace hacia la carpeta `docs/`.
```markdown
## ⚠️ Dependencia del Tema Visual (Muy Importante)
El bot "vive en el tema". Las coordenadas de calibración dependen estrictamente de la plantilla visual que tengas instalada en el juego. Si cambias de tema, el bot se romperá. 
👉 Lee más sobre esto en la [Documentación de Plantillas (Theme Dependency)](docs/theme_dependency.md).
```

## Verification Plan
1. Crear el archivo en `docs/theme_dependency.md`.
2. Actualizar el `README.md` con el link.
3. Confirmar que el renderizado de *Markdown* apunte correctamente al archivo.
