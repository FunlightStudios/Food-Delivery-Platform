from flask import Flask, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from swisseat.config import Config
import requests
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

    # Freigegebene Länder (ISO Alpha-2 Ländercode)
    ALLOWED_COUNTRIES = {"CH"}
    REDIRECT_URL = "https://example.com/access-denied"

    # Funktion, um die IP des Clients zu ermitteln
    def get_client_ip():
        forwarded_for = request.headers.get('X-Forwarded-For', '')
        if forwarded_for:
            return forwarded_for.split(',')[0]
        return request.remote_addr

    # Funktion, um den Standort basierend auf der IP zu bestimmen
    def get_country_from_ip(ip):
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/")
            response.raise_for_status()
            data = response.json()
            return data.get("country")
        except Exception as e:
            app.logger.error(f"Fehler bei der Standortermittlung: {e}")
            return None

    # Middleware zur Länderüberprüfung
    @app.before_request
    def check_country():
        client_ip = get_client_ip()
        app.logger.info(f"Client IP: {client_ip}")

        # Lokale Entwicklung - Behandle localhost als Schweiz
        if client_ip in ["127.0.0.1", "::1"]:
            country_code = "CH"
        else:
            country_code = get_country_from_ip(client_ip)
        
        app.logger.info(f"Erkanntes Land: {country_code}")

        if country_code not in ALLOWED_COUNTRIES:
            app.logger.info("Weiterleitung wegen nicht erlaubtem Land")
            return redirect(REDIRECT_URL)

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
    from swisseat.backend.routes import backend

    app.register_blueprint(users)
    app.register_blueprint(restaurants)
    app.register_blueprint(main)
    app.register_blueprint(orders)
    app.register_blueprint(reviews)
    app.register_blueprint(admin)
    app.register_blueprint(cart)
    app.register_blueprint(backend)

    return app


