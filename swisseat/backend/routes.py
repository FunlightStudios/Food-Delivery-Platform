from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from swisseat import db
from swisseat.models import Restaurant, MenuItem, Order, OrderItem, User, CmsSiteInfos
from swisseat.backend.forms import  LoginForm

backend = Blueprint('backend', __name__)

def staff_required(s):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_staff():
            flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
            return redirect(url_for('main.home'))
        return s(*args, **kwargs)
    decorated_function.__name__ = s.__name__
    return decorated_function

@backend.route("/backend")
@backend.route("/backend/login", methods=['GET', 'POST'])
def backend_login():
    if current_user.is_authenticated:
        return redirect(url_for('backend.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('backend.dashboard'))
        else:
            flash('Login fehlgeschlagen. Bitte überprüfen Sie E-Mail und Passwort.', 'danger')
    return render_template(
        'backend/login.html',
        title='Backend Login',
        form=form,
    )



@backend.route("/backend/dashboard")
@login_required
@staff_required
def backend_dashboard():
    backend = current_user.is_staff

    
    # Umsatz für die letzten 30 Tage
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Hole die Bestellstatistiken der letzten 30 Tage
    order_stats = db.session.query(
        MenuItem.name,
        func.sum(OrderItem.quantity).label('total_ordered'),
        func.sum(OrderItem.price_at_time * OrderItem.quantity).label('total_revenue')
    ).join(OrderItem).join(Order).filter(
        Order.restaurant_id == restaurant.id,
        Order.created_at >= thirty_days_ago
    ).group_by(MenuItem.name).all()

    # Hole die aktuellen Bestellungen
    current_orders = Order.query.filter_by(
        restaurant_id=restaurant.id,
        status='pending'
    ).order_by(Order.created_at.desc()).all()

    # Berechne Statistiken
    total_orders = len(current_orders)
    total_revenue = db.session.query(
        func.sum(OrderItem.price_at_time * OrderItem.quantity).label('total_revenue')
    ).join(Order).filter(Order.restaurant_id == restaurant.id).scalar() or 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Beliebteste Gerichte
    popular_items = db.session.query(
        MenuItem,
        func.sum(OrderItem.quantity).label('total_ordered')
    ).join(
        OrderItem, MenuItem.id == OrderItem.menu_item_id
    ).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        MenuItem.restaurant_id == restaurant.id
    ).group_by(
        MenuItem
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         restaurant=restaurant,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         avg_order_value=avg_order_value,
                         popular_items=popular_items)



# PHPMyAdmin Redirect
@backend.route("/phpmyadmin")
def phpmyadmin_redirect():
    return redirect("http://localhost:8080/phpmyadmin")