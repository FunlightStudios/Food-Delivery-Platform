from swisseat import create_app, db, bcrypt
from swisseat.models import User, Restaurant, MenuItem

def setup_database():
    app = create_app()
    
    with app.app_context():
        # Lösche und erstelle alle Tabellen neu
        db.drop_all()
        db.create_all()
        print("Datenbank-Tabellen erstellt!")

        # Füge Beispiel-Restaurants hinzu
        restaurants_data = [
            {
                'name': 'Pizza Express',
                'description': 'Authentische italienische Pizza aus dem Steinofen.',
                'address': 'Bahnhofstrasse 1, 8001 Zürich',
                'cuisine_type': 'italienisch',
                'rating': 4.5,
                'delivery_time': 30,
                'minimum_order': 25.00,
                'delivery_fee': 5.00,
                'menu_items': [
                    {
                        'name': 'Margherita',
                        'description': 'Tomaten, Mozzarella, Basilikum',
                        'price': 18.50,
                        'category': 'Pizza',
                        'is_available': True
                    }
                ]
            }
        ]

        # Füge die Restaurants und ihre Menüs in die Datenbank ein
        for restaurant_data in restaurants_data:
            menu_items = restaurant_data.pop('menu_items')
            restaurant = Restaurant(**restaurant_data)
            db.session.add(restaurant)
            db.session.flush()  # Um die restaurant.id zu erhalten
            
            for item_data in menu_items:
                item_data['restaurant_id'] = restaurant.id
                menu_item = MenuItem(**item_data)
                db.session.add(menu_item)

        # Erstelle einen Restaurant-Besitzer
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        owner = User(
            username='restaurant_owner',
            email='owner@example.com',
            password=hashed_password,
            role='restaurant_owner',
            owned_restaurant_id=1  # ID des ersten Restaurants
        )
        db.session.add(owner)

        # Erstelle einen normalen Benutzer
        user = User(
            username='test_user',
            email='user@example.com',
            password=hashed_password,
            role='user'
        )
        db.session.add(user)
        
        db.session.commit()
        print("Beispieldaten eingefügt!")
        print("\nRestaurant-Besitzer Login:")
        print("Email: owner@example.com")
        print("Passwort: password")
        print("\nBenutzer Login:")
        print("Email: user@example.com")
        print("Passwort: password")

if __name__ == '__main__':
    setup_database()
