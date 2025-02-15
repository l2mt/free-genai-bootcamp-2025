import os
import sqlite3

MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), 'migrations')
DB_PATH = os.path.join(os.path.dirname(__file__), 'words.db')

def run_migrations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    migration_files = sorted(f for f in os.listdir(MIGRATIONS_DIR) if f.endswith('.sql'))
    
    for migration in migration_files:
        migration_path = os.path.join(MIGRATIONS_DIR, migration)
        print(f"Ejecutando migración: {migration}")
        with open(migration_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()
    
    conn.close()

if __name__ == '__main__':
    # Para forzar la reinicialización, descomenta la siguiente línea:
    if os.path.exists(DB_PATH): os.remove(DB_PATH)
    
    if not os.path.exists(DB_PATH):
        print("La base de datos no existe. Creando y ejecutando migraciones.")
        run_migrations()
        print("Migraciones ejecutadas correctamente.")
    else:
        print("La base de datos ya existe.")
