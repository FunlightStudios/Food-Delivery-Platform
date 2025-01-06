from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from swisseat import db, bcrypt
from swisseat.models import User, UserAddress
from swisseat.users.forms import RegistrationForm, LoginForm, RestaurantRegistrationForm, UpdateAccountForm
from sqlalchemy import select

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role='customer'
        )
        db.session.add(user)
        db.session.commit()
        flash('Ihr Account wurde erfolgreich erstellt! Sie können sich jetzt anmelden.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Registrierung', form=form)

@users.route("/register/restaurant", methods=['GET', 'POST'])
def register_restaurant():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RestaurantRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            phone=form.phone.data,
            role='restaurant_owner'
        )
        db.session.add(user)
        db.session.commit()
        flash('Ihr Restaurant-Account wurde erstellt! Bitte melden Sie sich an und registrieren Sie Ihr Restaurant.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register_restaurant.html', title='Restaurant Registrierung', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login fehlgeschlagen. Bitte überprüfen Sie E-Mail und Passwort.', 'danger')
    return render_template('users/login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_authenticated:
        current_user_address = db.session.execute(
            select(UserAddress.street, UserAddress.city, UserAddress.zipcode, UserAddress.country)
            .where(UserAddress.user_id == current_user.id)
        ).first()
    else:
        current_user_address = None  # oder eine andere geeignete Handhabung
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user_address.street = form.street.data
        current_user_address.city = form.city.data
        current_user_address.zipcode = form.zipcode.data
        current_user_address.country = form.country.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Ihr Account wurde aktualisiert!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.street.data = current_user_address.street
        form.city.data = current_user_address.city
        form.zipcode.data = current_user_address.zipcode
        form.country.data = current_user_address.country
        form.phone.data = current_user.phone
    return render_template('users/profile.html', title='Account', form=form)
