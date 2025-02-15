import os
import json
import sqlite3

# Ruta del directorio donde se encuentran los archivos seed y la base de datos.
SEEDS_DIR = os.path.join(os.path.dirname(__file__), 'seeds')
DB_PATH = os.path.join(os.path.dirname(__file__), 'words.db')

def run_seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Archivo JSON de seed (por ejemplo, "words.json")
    seed_file = os.path.join(SEEDS_DIR, 'words.json')
    if not os.path.exists(seed_file):
        print("No se encontró el archivo de seed: words.json")
        return
    
    with open(seed_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Insertar cada registro en la tabla "words"
    for word in data:
        spanish = word.get("spanish")
        english = word.get("english")
        # Convertir el campo "parts" a JSON string, o asignar un objeto vacío si no existe.
        parts = json.dumps(word.get("parts", {}))
        cursor.execute(
            "INSERT INTO words (spanish, english, parts) VALUES (?, ?, ?)",
            (spanish, english, parts)
        )
    
    conn.commit()
    conn.close()
    print("Datos seed insertados correctamente.")

if __name__ == '__main__':
    run_seed()
