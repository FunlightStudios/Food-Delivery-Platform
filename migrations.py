from swisseat import create_app, db
from swisseat.models import User, Restaurant, MenuItem, Order, OrderItem, Review, Cart, CartItem
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt()

def reset_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create test users
        owner = User(
            username='Restaurant Owner',
            email='owner@example.com',
            password=bcrypt.generate_password_hash('password').decode('utf-8'),
            role='restaurant_owner',
            address='Musterstrasse 1, 8000 Zürich',
            phone='+41 44 123 45 67'
        )
        db.session.add(owner)
        db.session.commit()

        # Create test restaurant
        restaurant = Restaurant(
            name='Beispiel Restaurant',
            description='Ein gemütliches Restaurant mit ausgezeichneter Küche',
            address='Musterstrasse 123, 8000 Zürich',
            cuisine_type='schweizerisch',
            rating=4.5,
            delivery_time=30,
            minimum_order=20.0,
            delivery_fee=5.0,
            accepts_cash=True,
            accepts_twint=True,
            accepts_paypal=True,
            owner=owner
        )
        db.session.add(restaurant)
        
        # Create test menu items
        menu_items = [
            MenuItem(
                name='Zürcher Geschnetzeltes',
                description='Kalbfleisch in Rahmsauce mit Rösti',
                price=28.50,
                category='hauptgerichte',
                restaurant=restaurant
            ),
            MenuItem(
                name='Rösti',
                description='Traditionelle Schweizer Rösti',
                price=12.00,
                category='beilagen',
                restaurant=restaurant
            ),
            MenuItem(
                name='Apfelstrudel',
                description='Hausgemachter Apfelstrudel mit Vanillesauce',
                price=8.50,
                category='desserts',
                restaurant=restaurant
            )
        ]
        for item in menu_items:
            db.session.add(item)

        # Create test user
        user = User(
            username='Test User',
            email='user@example.com',
            password=bcrypt.generate_password_hash('password').decode('utf-8'),
            address='Beispielstrasse 42, 8001 Zürich',
            phone='+41 44 987 65 43'
        )
        db.session.add(user)
        
        db.session.commit()
        print("Database has been reset and populated with test data!")

if __name__ == '__main__':
    reset_db()
