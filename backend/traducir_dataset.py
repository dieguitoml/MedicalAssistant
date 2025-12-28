import os
from deep_translator import GoogleTranslator
import chardet

# Directorios de entrada y salida
input_dir = "dataset_respiratorio"
output_dir = "dataset_respiratorio_es"
os.makedirs(output_dir, exist_ok=True)

# Tamaño máximo por bloque (Google Translate permite hasta ~5000)
MAX_CHARS = 4000

def detectar_encoding(filepath):
    with open(filepath, "rb") as f:
        raw = f.read()
    result = chardet.detect(raw)
    return result["encoding"] or "utf-8"

def dividir_en_bloques(texto, max_chars=MAX_CHARS):
    lineas = texto.splitlines()
    bloques = []
    bloque_actual = ""
    for linea in lineas:
        if len(bloque_actual) + len(linea) + 1 <= max_chars:
            bloque_actual += linea + "\n"
        else:
            bloques.append(bloque_actual.strip())
            bloque_actual = linea + "\n"
    if bloque_actual:
        bloques.append(bloque_actual.strip())
    return bloques

def traducir_bloque(bloque):
    try:
        return GoogleTranslator(source='auto', target='es').translate(bloque)
    except Exception as e:
        print(f"[X] Error al traducir bloque: {e}")
        return "[Error de traducción]"

# Procesar cada archivo
for filename in os.listdir(input_dir):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(input_dir, filename)
    encoding = detectar_encoding(filepath)
    with open(filepath, "r", encoding=encoding, errors="replace") as f:
        contenido = f.read()

    bloques = dividir_en_bloques(contenido)
    contenido_traducido = ""

    for i, bloque in enumerate(bloques):
        print(f"    Traduciendo bloque {i+1}/{len(bloques)} de {filename}...")
        contenido_traducido += traducir_bloque(bloque) + "\n\n"

    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(contenido_traducido.strip())

    print(f"[✓] Traducido y guardado: {output_path}")
