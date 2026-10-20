# Panel de pendientes

Un panel que junta en una pantalla lo que espera algo de mí en Gmail y en Slack, aparta lo que es solo informativo, deja aparte lo que tengo que leer, me enseña la agenda de hoy y guarda notas. Está hecho como artifact de Claude: lee mis conectores y usa la IA solo para lo que una regla no puede decidir.

> **Antes de clonar:** esto no es una aplicación que se instale. Es un único archivo HTML que funciona **publicado como artifact de Claude**, con los conectores de tu cuenta. Abierto en un navegador normal no hace nada. Cómo montarlo: [`docs/GUIA_DESPLIEGUE.md`](docs/GUIA_DESPLIEGUE.md).
>
> Es la copia anonimizada de un panel que uso a diario en el trabajo, y sigue en construcción.

## De dónde viene

La idea es de [David Hurtado Torán](https://www.linkedin.com/pulse/he-vivido-el-saaspocalypse-en-mis-propias-carnes-david-hurtado-tor%C3%A1n-x63ye/), que a su vez adaptó el panel de su compañero Fran García. Hice lo mismo que él: coger el suyo y adaptarlo a cómo trabajo yo. Me gustó mucho más que el que tenía, sobre todo la parte de guardar notas.

Cómo lo he adaptado:
- la memoria del panel vive en una hoja de cálculo que otros flujos pueden leer;
- lo informativo se aparta pero nunca desaparece;
- un mensaje se da por contestado aunque haya contestado por el otro canal;
- lo que no pide respuesta pero hay que leer tiene su propio apartado, «Para leer»;
- las notas son archivos markdown en Drive.

## Cómo está montado

| Pieza | Dónde vive | Qué hace |
| --- | --- | --- |
| El panel | `index.html`, publicado como artifact de Claude | Lee Gmail, Slack y Calendar, decide el estado de cada cosa y lo pinta |
| La hoja de estado | Una hoja de Google | Reglas, excepciones, accesos rápidos y límites, que edito yo; y lo resuelto, corregido y clasificado, que escribe el panel añadiendo filas |
| Las notas | Una carpeta de Drive y una hoja índice | Una nota markdown por tema; nunca se sobrescribe ninguna |
| La IA | Dentro del artifact | Solo decide si lo que queda pendiente es informativo. Sin herramientas: no puede escribir, enviar ni borrar |
| El botón de salud | Cabecera del panel | Lee el resumen de otra hoja, la de mi panel de salud de automatizaciones, y se pone en rojo o ámbar si alguna falla. Es opcional |

## Qué hay aquí

| Carpeta o archivo | Qué es | Estado |
| --- | --- | --- |
| [`index.html`](index.html) | El panel entero: HTML, estilos y JavaScript en un solo archivo | 🧪 pruebas |
| [`plantilla_hoja_estado/`](plantilla_hoja_estado/) | Una plantilla CSV por pestaña de la hoja de estado, y la del índice de notas | ✅ |
| [`herramientas/copia_publica.py`](herramientas/copia_publica.py) | Genera esta copia a partir del panel real, quitando los datos personales | ✅ |
| [`docs/`](docs/) | Cómo funciona y cómo montarlo | ✅ |

> ✅ producción · 🧪 pruebas · ⏸️ pausado · 🗄️ one-off · 💀 muerto

## Stack

- Un archivo HTML con JavaScript, sin dependencias ni compilación.
- Artifact de Claude con conectores de Gmail, Slack, Google Calendar, Google Sheets y Google Drive, y la capacidad de llamar a la IA.
- Google Sheets como memoria y Google Drive para las notas.
- La herramienta de anonimizar: Python 3, solo biblioteca estándar.

## Documentación

| Archivo | Qué contiene |
| --- | --- |
| [`docs/COMO_FUNCIONA.md`](docs/COMO_FUNCIONA.md) | El principio de diseño, qué hace en cada carga, cómo decide cada estado, la IA, las notas, la seguridad y las decisiones cerradas |
| [`docs/GUIA_DESPLIEGUE.md`](docs/GUIA_DESPLIEGUE.md) | Montarlo en tu cuenta: hoja, notas, configuración, publicación y comprobaciones |

## Pendiente

| Qué | Por qué está pendiente |
| --- | --- |
| Quién espera algo de mí, agrupado por persona | Siguiente entrega; necesita cruzar con mi registro de casos abiertos |
| Mensaje abierto, etiquetas, agenda navegable, «cargar más», lo que espero yo, posponer, antigüedad | Mejoras de uso, después de lo anterior |
| v2: buscar contexto, proponer respuestas como borrador, esquematizar notas con IA | Va después de cerrar la v1 |
| v3: que otros flujos (el resumen de la mañana, el semanal) lean las notas | Después de la v2 |

## Regenerar esta copia

El panel real lleva mis datos (correo, ids, remitentes, nombres). Esta copia se saca de él con [`herramientas/copia_publica.py`](herramientas/copia_publica.py), que lee las sustituciones de un archivo privado que nunca se sube (`datos_privados.json`, en `.gitignore`). Su formato está en [`herramientas/datos_privados.ejemplo.json`](herramientas/datos_privados.ejemplo.json).

```
python herramientas/copia_publica.py <panel real>/index.html index.html <ruta>/datos_privados.json
```

El script se para sin escribir nada si una sustitución no aparece las veces previstas (el panel ha cambiado) o si en la salida queda cualquier dato prohibido, un correo, un id de Slack o algo con forma de id de Drive.

### Cómo lo hago yo

El panel real vive en un repo privado del trabajo y `datos_privados.json` en mi copia local de este repo, en mi ordenador personal. No tengo los dos en la misma máquina, así que regenero desde una sesión de Claude en la nube con mi ordenador enlazado:

1. La sesión clona el repo privado del panel y este.
2. Pide acceso a mi copia local de este repo y lee de ahí `datos_privados.json`, sin copiarlo a ningún repo.
3. Ejecuta el script. Si para, ajusta la sustitución que nombra en `datos_privados.json` (y me devuelve el archivo actualizado) antes de volver a lanzarlo.
4. Revisa la salida: que el JavaScript sigue siendo válido y que el cambio es el que esperaba.
5. Actualiza en este README lo que haya cambiado (estado, pendiente, fecha) y lo sube.

---

Última actualización: 20/10/2026
