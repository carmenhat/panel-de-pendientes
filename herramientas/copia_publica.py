"""Genera la copia pública y anonimizada de un panel a partir del que se usa de verdad.

Uso:
    python copia_publica.py <panel original> <archivo de salida> <datos privados .json>

El panel original no se toca. Las sustituciones y la lista de lo que no puede
quedar viven en el archivo de datos privados, que nunca se sube al repo (está en
.gitignore). Su formato está en datos_privados.ejemplo.json.

Es estricto a propósito:
  - Cada sustitución tiene que encontrar su texto exactamente las veces previstas.
    Si el panel ha cambiado y una no cuadra, se para y dice cuál.
  - Después revisa la salida: si queda alguno de los textos prohibidos, un correo
    que no esté permitido, algo con forma de id de usuario de Slack o algo con
    forma de id de Drive, se para y no escribe nada.

Solo usa la biblioteca estándar de Python.
"""

import json
import re
import sys
from pathlib import Path

PATRON_CORREO = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PATRON_SLACK = r"\b[UWCDG][0-9A-Z]{8,11}\b"
PATRON_ID = r"""["']([A-Za-z0-9_-]{25,})["']"""
MARCADOR_ID = "ID_DE_TU_"
MARCADOR_SLACK = "UXXXXXXXXXX"


def parar(mensaje):
    sys.exit("PARADO: " + mensaje)


def cargar_datos(ruta):
    try:
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    except FileNotFoundError:
        parar(f"no encuentro el archivo de datos privados: {ruta}")
    except json.JSONDecodeError as e:
        parar(f"el archivo de datos privados no es JSON válido: {e}")
    for clave in ("sustituciones", "prohibido"):
        if not isinstance(datos.get(clave), list) or not datos[clave]:
            parar(f"al archivo de datos privados le falta la lista «{clave}».")
    return datos


def sustituir(texto, sustituciones):
    for s in sustituciones:
        original, nuevo, veces = s["original"], s["nuevo"], s.get("veces", 1)
        n = texto.count(original)
        if n != veces:
            parar(f"se esperaba {veces} vez/veces y aparece {n}:\n  {original[:120]}\n"
                  "El panel ha cambiado: revisa esta sustitución antes de seguir.")
        texto = texto.replace(original, nuevo)
    return texto


def revisar(texto, datos):
    fallos = []
    lineas = texto.splitlines()
    for p in datos["prohibido"]:
        donde = [i + 1 for i, l in enumerate(lineas) if p.lower() in l.lower()]
        if donde:
            fallos.append(f"queda un texto prohibido (líneas {donde})")
    correos_ok = {c.lower() for c in datos.get("correos_permitidos", [])}
    for correo in sorted(set(re.findall(PATRON_CORREO, texto))):
        if correo.lower() not in correos_ok:
            fallos.append(f"correo no permitido: {correo}")
    for slack_id in sorted(set(re.findall(PATRON_SLACK, texto))):
        if slack_id != MARCADOR_SLACK:
            fallos.append(f"posible id de Slack: {slack_id}")
    ids_ok = set(datos.get("ids_permitidos", []))
    for cadena in sorted(set(re.findall(PATRON_ID, texto))):
        if cadena not in ids_ok and not cadena.startswith(MARCADOR_ID):
            fallos.append(f"posible id de Drive o de hoja: {cadena}")
    if fallos:
        # No se repite el texto prohibido en el mensaje: solo dónde está.
        parar("la copia no está limpia y no se ha escrito.\n  " + "\n  ".join(fallos))


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    origen, destino, ruta_datos = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    if origen.resolve() == destino.resolve():
        parar("la salida no puede ser el original.")
    datos = cargar_datos(ruta_datos)
    limpio = sustituir(origen.read_text(encoding="utf-8"), datos["sustituciones"])
    revisar(limpio, datos)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(limpio, encoding="utf-8", newline="\n")
    print(f"Copia escrita en {destino}: {len(datos['sustituciones'])} sustituciones, revisión limpia.")


if __name__ == "__main__":
    main()
