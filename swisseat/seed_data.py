from swisseat import create_app, db
from swisseat.models import Restaurant, MenuItem

def seed_data():
    # Restaurants
    restaurants_data = [
        {
            'name': 'Pizza Express',
            'description': 'Authentische italienische Pizza aus dem Steinofen. Frische Zutaten und traditionelle Rezepte.',
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
                },
                {
                    'name': 'Prosciutto e Funghi',
                    'description': 'Tomaten, Mozzarella, Schinken, Champignons',
                    'price': 21.00,
                    'category': 'Pizza',
                    'is_available': True
                },
                {
                    'name': 'Insalata Mista',
                    'description': 'Gemischter Salat mit Balsamico-Dressing',
                    'price': 9.50,
                    'category': 'Vorspeisen',
                    'is_available': True
                }
            ]
        },
        {
            'name': 'Sushi King',
            'description': 'Frisches Sushi und japanische Spezialitäten. Täglich frischer Fisch von höchster Qualität.',
            'address': 'Löwenstrasse 15, 8001 Zürich',
            'cuisine_type': 'asiatisch',
            'rating': 4.7,
            'delivery_time': 45,
            'minimum_order': 30.00,
            'delivery_fee': 6.00,
            'menu_items': [
                {
                    'name': 'California Roll (8 Stück)',
                    'description': 'Surimi, Avocado, Gurke, Sesam',
                    'price': 16.00,
                    'category': 'Sushi Rolls',
                    'is_available': True
                },
                {
                    'name': 'Salmon Nigiri (2 Stück)',
                    'description': 'Frischer Lachs auf Sushi-Reis',
                    'price': 8.50,
                    'category': 'Nigiri',
                    'is_available': True
                },
                {
                    'name': 'Miso Suppe',
                    'description': 'Traditionelle japanische Suppe mit Tofu und Wakame',
                    'price': 6.50,
                    'category': 'Suppen',
                    'is_available': True
                }
            ]
        },
        {
            'name': 'Burger House',
            'description': 'Premium Burger aus 100% Schweizer Rindfleisch. Hausgemachte Saucen und Beilagen.',
            'address': 'Langstrasse 50, 8004 Zürich',
            'cuisine_type': 'amerikanisch',
            'rating': 4.3,
            'delivery_time': 35,
            'minimum_order': 25.00,
            'delivery_fee': 5.50,
            'menu_items': [
                {
                    'name': 'Classic Cheese Burger',
                    'description': 'Rindfleisch, Cheddar, Salat, Tomaten, Zwiebeln, Burger-Sauce',
                    'price': 19.50,
                    'category': 'Burger',
                    'is_available': True
                },
                {
                    'name': 'Crispy Chicken Burger',
                    'description': 'Knuspriges Pouletbrustfilet, Coleslaw, Chipotle-Mayo',
                    'price': 18.50,
                    'category': 'Burger',
                    'is_available': True
                },
                {
                    'name': 'Sweet Potato Fries',
                    'description': 'Mit Meersalz und Rosmarin',
                    'price': 7.50,
                    'category': 'Beilagen',
                    'is_available': True
                }
            ]
        },
        {
            'name': 'Taj Mahal',
            'description': 'Authentische indische Küche mit traditionellen Gewürzen. Große Auswahl an vegetarischen Gerichten.',
            'address': 'Militärstrasse 84, 8004 Zürich',
            'cuisine_type': 'indisch',
            'rating': 4.6,
            'delivery_time': 40,
            'minimum_order': 35.00,
            'delivery_fee': 6.00,
            'menu_items': [
                {
                    'name': 'Butter Chicken',
                    'description': 'Poulet in cremiger Tomaten-Butter-Sauce',
                    'price': 24.50,
                    'category': 'Hauptgerichte',
                    'is_available': True
                },
                {
                    'name': 'Palak Paneer',
                    'description': 'Hausgemachter Käse in Spinatsauce',
                    'price': 22.00,
                    'category': 'Vegetarisch',
                    'is_available': True
                },
                {
                    'name': 'Garlic Naan',
                    'description': 'Indisches Fladenbrot mit Knoblauch',
                    'price': 4.50,
                    'category': 'Beilagen',
                    'is_available': True
                }
            ]
        },
        {
            'name': 'Helvetia',
            'description': 'Traditionelle Schweizer Küche mit modernem Touch. Regionale und saisonale Zutaten.',
            'address': 'Stauffacherstrasse 60, 8004 Zürich',
            'cuisine_type': 'schweizerisch',
            'rating': 4.4,
            'delivery_time': 45,
            'minimum_order': 30.00,
            'delivery_fee': 7.00,
            'menu_items': [
                {
                    'name': 'Zürcher Geschnetzeltes',
                    'description': 'Mit Rösti und Champignonsauce',
                    'price': 32.00,
                    'category': 'Hauptgerichte',
                    'is_available': True
                },
                {
                    'name': 'Käsefondue (2 Personen)',
                    'description': 'Klassische Mischung mit Greyerzer und Vacherin',
                    'price': 45.00,
                    'category': 'Spezialitäten',
                    'is_available': True
                },
                {
                    'name': 'Rösti',
                    'description': 'Klassisch mit Speck und Zwiebeln',
                    'price': 18.50,
                    'category': 'Hauptgerichte',
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
    
    db.session.commit()
    print("Beispieldaten wurden erfolgreich in die Datenbank eingefügt!")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Lösche bestehende Daten
        MenuItem.query.delete()
        Restaurant.query.delete()
        db.session.commit()
        
        # Füge neue Beispieldaten ein
        seed_data()
