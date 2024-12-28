from swisseat import create_app, db, bcrypt
from swisseat.models import User, Restaurant

def create_restaurant_owner():
    app = create_app()
    
    with app.app_context():
        # Finde das erste Restaurant
        restaurant = Restaurant.query.first()
        
        if restaurant:
            # Erstelle einen Restaurant-Besitzer
            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
            owner = User(
                username='restaurant_owner',
                email='owner@example.com',
                password=hashed_password,
                role='restaurant_owner',
                owned_restaurant_id=restaurant.id
            )
            
            db.session.add(owner)
            db.session.commit()
            print(f"Restaurant-Besitzer erstellt für {restaurant.name}!")
            print("Login-Daten:")
            print("Email: owner@example.com")
            print("Passwort: password")
        else:
            print("Kein Restaurant in der Datenbank gefunden!")

if __name__ == '__main__':
    create_restaurant_owner()
