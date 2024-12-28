import sqlite3
import os

def update_database():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swisseat', 'site.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Füge die role-Spalte zur user-Tabelle hinzu
        cursor.execute('ALTER TABLE user ADD COLUMN role TEXT NOT NULL DEFAULT "user"')
        print("role-Spalte hinzugefügt")

        # Füge die owned_restaurant_id-Spalte zur user-Tabelle hinzu
        cursor.execute('ALTER TABLE user ADD COLUMN owned_restaurant_id INTEGER REFERENCES restaurant(id)')
        print("owned_restaurant_id-Spalte hinzugefügt")

        conn.commit()
        print("Datenbank erfolgreich aktualisiert!")

    except sqlite3.OperationalError as e:
        print(f"Fehler: {e}")
        if "duplicate column name" in str(e):
            print("Die Spalten existieren bereits.")
        else:
            raise e

    finally:
        conn.close()

if __name__ == '__main__':
    update_database()
