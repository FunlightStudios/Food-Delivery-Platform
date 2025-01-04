import os
from swisseat import create_app, db

def reset_database():
    app = create_app()
    
    with app.app_context():
        # Lösche die alte Datenbank
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swisseat', 'site.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Alte Datenbank gelöscht: {db_path}")
        
        # Erstelle die Tabellen neu
        db.create_all()
        print("Neue Datenbank-Tabellen erstellt!")

if __name__ == '__main__':
    reset_database()
