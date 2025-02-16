import os
import json
import sqlite3

# Ruta del directorio donde se encuentran los archivos seed y la base de datos.
SEEDS_DIR = os.path.join(os.path.dirname(__file__), 'seeds')
DB_PATH = os.path.join(os.path.dirname(__file__), 'words.db')

def run_seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Limpiar tablas existentes
    cursor.execute("DELETE FROM word_review_items")
    cursor.execute("DELETE FROM study_sessions")
    cursor.execute("DELETE FROM study_activities")
    cursor.execute("DELETE FROM word_groups")
    cursor.execute("DELETE FROM words")
    cursor.execute("DELETE FROM groups")
    
    # Reiniciar secuencias
    cursor.execute("DELETE FROM sqlite_sequence")
    
    conn.commit()
    print("Existing data cleaned successfully.")

    # Seed words
    seed_file = os.path.join(SEEDS_DIR, 'words.json')
    if os.path.exists(seed_file):
        with open(seed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for word in data:
            spanish = word.get("spanish")
            english = word.get("english")
            parts = json.dumps(word.get("parts", {}))
            cursor.execute(
                "INSERT INTO words (spanish, english, parts) VALUES (?, ?, ?)",
                (spanish, english, parts)
            )
        print("Words seed data inserted successfully.")
    
    # Seed groups
    groups_file = os.path.join(SEEDS_DIR, 'groups.json')
    if os.path.exists(groups_file):
        with open(groups_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for group in data:
            cursor.execute(
                "INSERT INTO groups (id, name, words_count) VALUES (?, ?, ?)",
                (group["id"], group["name"], group["word_count"])
            )
        print("Groups seed data inserted successfully.")
    
    # Seed word_groups
    word_groups_file = os.path.join(SEEDS_DIR, 'word_groups.json')
    if os.path.exists(word_groups_file):
        with open(word_groups_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for word_group in data:
            cursor.execute(
                "INSERT INTO word_groups (word_id, group_id) VALUES (?, ?)",
                (word_group["word_id"], word_group["group_id"])
            )
        print("Word-groups relationships seed data inserted successfully.")

    # Seed study_activities
    study_activities_file = os.path.join(SEEDS_DIR, 'study_activities.json')
    if os.path.exists(study_activities_file):
        with open(study_activities_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for activity in data:
            cursor.execute(
                """INSERT INTO study_activities 
                   (id, name, thumbnail_url, description, launch_url) 
                   VALUES (?, ?, ?, ?, ?)""",
                (activity["id"], activity["name"], activity.get("thumbnail_url"),
                 activity["description"], activity["launch_url"])
            )
        print("Study activities seed data inserted successfully.")

    # Seed study_sessions
    study_sessions_file = os.path.join(SEEDS_DIR, 'study_sessions.json')
    if os.path.exists(study_sessions_file):
        with open(study_sessions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for session in data:
            cursor.execute(
                """INSERT INTO study_sessions 
                   (id, group_id, study_activity_id, created_at, end_time) 
                   VALUES (?, ?, ?, ?, ?)""",
                (session["id"], session["group_id"], session["study_activity_id"],
                 session["created_at"], session["end_time"])
            )
        print("Study sessions seed data inserted successfully.")

    # Seed word_review_items
    word_review_items_file = os.path.join(SEEDS_DIR, 'word_review_items.json')
    if os.path.exists(word_review_items_file):
        with open(word_review_items_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for review in data:
            cursor.execute(
                """INSERT INTO word_review_items 
                   (word_id, study_session_id, correct, created_at) 
                   VALUES (?, ?, ?, ?)""",
                (review["word_id"], review["study_session_id"],
                 review["correct"], review["created_at"])
            )
        print("Word review items seed data inserted successfully.")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    run_seed()
