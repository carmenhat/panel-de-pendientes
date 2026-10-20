# Montarlo desde cero

Para adaptar el panel a tu propia cuenta. Lleva un rato, no un proyecto.

## Qué necesitas

- Una cuenta de Claude que permita publicar artifacts con conectores y con IA.
- Los conectores **Gmail**, **Slack**, **Google Calendar**, **Google Sheets** y **Google Drive**, conectados con la cuenta cuyos pendientes quieres ver.
- Una carpeta de Drive donde guardar la hoja de estado y las notas.

La clasificación con IA gasta uso de tu cuenta de Claude. Si no la quieres, pon `ia_lotes` a 0 en la hoja y el resto funciona igual.

## 1. La hoja de estado

1. Crea una hoja de cálculo de Google.
2. Crea una pestaña por cada archivo de [`plantilla_hoja_estado/`](../plantilla_hoja_estado/), salvo `notas_indice.csv`: `reglas`, `excepciones`, `botones`, `limites`, `resueltos`, `correcciones` y `clasificacion`. **Los nombres tienen que ser exactos**: el panel lee las pestañas por nombre, no por posición.
3. Importa en cada pestaña su CSV. Las de `reglas`, `excepciones`, `botones` y `limites` traen ejemplos: cámbialos por los tuyos. Las otras tres solo llevan la cabecera; las rellena el panel.
4. En `botones`, el enlace va como texto (`https://…`), no como chip de Google: la lectura de la hoja solo devuelve el texto visible.

Las reglas usan expresiones regulares sin distinguir mayúsculas. El campo puede ser `remitente`, `asunto`, `etiqueta` (de Gmail) o `slack` (el nombre de quien escribe, con « (bot)» detrás si es una aplicación). Con `campo2` y `patron2` se tienen que cumplir las dos condiciones. Una regla solo cuenta si en `activa` pone `sí`. Con `destino` vacío, lo que coge va a Informativos; con `leer`, a «Para leer».

## 2. Las notas

1. Crea una carpeta de Drive para las notas y, dentro, una subcarpeta `_anteriores`.
2. Crea otra hoja de cálculo con una pestaña llamada `notas` e importa en ella [`notas_indice.csv`](../plantilla_hoja_estado/notas_indice.csv).

## 3. Configurar el panel

Abre [`index.html`](../index.html) y rellena las líneas marcadas con `←`:

| Constante | Qué va |
| --- | --- |
| `ME_EMAIL` | Tu correo. También decide qué remitentes son de tu propia empresa |
| `ME_SLACK` | Tu id de usuario de Slack (empieza por `U`; está en tu perfil, en «Copiar id de miembro») |
| `STATE_SHEET` | El id de la hoja de estado: lo que va entre `/d/` y `/edit` en su dirección |
| `NOTES_FOLDER` | El id de la carpeta de notas |
| `NOTES_OLD_FOLDER` | El id de la subcarpeta `_anteriores` |
| `NOTES_SHEET` | El id de la hoja índice de notas |
| `HEALTH_SHEET` | Opcional. El id de la hoja de tu panel de salud, con una pestaña `Resumen` (proyecto, estado, detalle, timestamp en `dd/mm/aaaa hh:mm`). Si no tienes, el botón sale en gris |
| Enlace del botón de salud | En el HTML, `href="https://claude.ai/artifact/TU_PANEL_DE_SALUD"`: la dirección de tu panel de salud |

Si quieres, revisa también `DEFAULT_RULES`: son las reglas que se usan cuando no se puede leer la hoja.

## 4. Publicarlo

Pídele a Claude, en una conversación, que publique tu `index.html` como artifact con estas capacidades:

- **Conectores** (`mcp`):
  - Gmail: `search_threads`, `get_thread`
  - Slack: `slack_search_public_and_private`, `slack_read_channel`, `slack_read_thread`, `slack_read_user_profile`
  - Google Calendar: `list_events`
  - Google Sheets: `get_values`, `append_values`, `update_values`
  - Google Drive: `search_files`, `create_file`, `download_file_content`, `update_file`
- **IA** (`sample`).

La primera vez que lo abras te pedirá permiso para cada conector y para la IA.

## 5. Comprobarlo

- Que los contadores cuadran con tu bandeja revisada a mano.
- Que una corrección («Informativo» o «Necesita respuesta») aparece como fila nueva en `correcciones`.
- Que una nota crea su archivo en la carpeta y su fila en la hoja índice.

Si algo no se lee, el bloque correspondiente lo dice con su error y su botón de reintentar.
