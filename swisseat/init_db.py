from swisseat import db, bcrypt, create_app
from swisseat.models import User, Restaurant

def init_test_data():
    app = create_app()
    with app.app_context():
        # Create test restaurant owner if not exists
        if not User.query.filter_by(email='owner@example.com').first():
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
            db.session.commit()

        # Create test user if not exists
        if not User.query.filter_by(email='user@example.com').first():
            user = User(
                username='Test User',
                email='user@example.com',
                password=bcrypt.generate_password_hash('password').decode('utf-8'),
                address='Beispielstrasse 42, 8001 Zürich',
                phone='+41 44 987 65 43'
            )
            db.session.add(user)
            db.session.commit()

if __name__ == '__main__':
    init_test_data()
