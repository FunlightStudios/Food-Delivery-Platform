from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from swisseat.config import Config
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    @app.template_filter('day_is')
    def day_is(date, compare_date):
        if date is None:
            return False
        return date.date() == compare_date

    from swisseat.users.routes import users
    from swisseat.restaurants.routes import restaurants
    from swisseat.main.routes import main
    from swisseat.orders.routes import orders
    from swisseat.reviews.routes import reviews
    from swisseat.admin.routes import admin
    from swisseat.cart.routes import cart

    app.register_blueprint(users)
    app.register_blueprint(restaurants)
    app.register_blueprint(main)
    app.register_blueprint(orders)
    app.register_blueprint(reviews)
    app.register_blueprint(admin)
    app.register_blueprint(cart)

    return app
