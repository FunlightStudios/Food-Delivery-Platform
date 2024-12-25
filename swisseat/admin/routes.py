from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from swisseat import db
from swisseat.models import Restaurant, MenuItem, Order, OrderItem, User
from swisseat.admin.forms import RestaurantUpdateForm, MenuItemForm

admin = Blueprint('admin', __name__)

def restaurant_owner_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_restaurant_owner():
            flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route("/restaurant/dashboard")
@login_required
@restaurant_owner_required
def restaurant_dashboard():
    restaurant = current_user.owned_restaurant
    
    # Bestellstatistiken für die letzten 30 Tage
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

@admin.route("/restaurant/update", methods=['GET', 'POST'])
@login_required
def update_restaurant():
    if not current_user.is_restaurant_owner():
        flash('Zugriff verweigert.', 'danger')
        return redirect(url_for('main.home'))
    
    restaurant = Restaurant.query.filter_by(owner=current_user).first()
    if not restaurant:
        flash('Kein Restaurant gefunden.', 'danger')
        return redirect(url_for('main.home'))
    
    form = RestaurantUpdateForm()
    if form.validate_on_submit():
        restaurant.name = form.name.data
        restaurant.description = form.description.data
        restaurant.address = form.address.data
        restaurant.cuisine_type = form.cuisine_type.data
        restaurant.delivery_time = form.delivery_time.data
        restaurant.minimum_order = form.minimum_order.data
        restaurant.delivery_fee = form.delivery_fee.data
        restaurant.accepts_cash = form.accepts_cash.data
        restaurant.accepts_twint = form.accepts_twint.data
        restaurant.accepts_paypal = form.accepts_paypal.data
        
        db.session.commit()
        flash('Restaurant wurde erfolgreich aktualisiert!', 'success')
        return redirect(url_for('admin.restaurant_dashboard'))
    
    elif request.method == 'GET':
        form.name.data = restaurant.name
        form.description.data = restaurant.description
        form.address.data = restaurant.address
        form.cuisine_type.data = restaurant.cuisine_type
        form.delivery_time.data = restaurant.delivery_time
        form.minimum_order.data = restaurant.minimum_order
        form.delivery_fee.data = restaurant.delivery_fee
        form.accepts_cash.data = restaurant.accepts_cash
        form.accepts_twint.data = restaurant.accepts_twint
        form.accepts_paypal.data = restaurant.accepts_paypal
    
    return render_template('admin/update_restaurant.html', 
                         title='Restaurant Aktualisieren',
                         form=form)

@admin.route("/restaurant/menu")
@login_required
@restaurant_owner_required
def menu_management():
    restaurant = current_user.owned_restaurant
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('admin/menu_management.html',
                         menu_items=menu_items)

@admin.route("/restaurant/menu/new", methods=['GET', 'POST'])
@login_required
@restaurant_owner_required
def new_menu_item():
    form = MenuItemForm()
    if form.validate_on_submit():
        menu_item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            is_available=form.is_available.data,
            restaurant_id=current_user.owned_restaurant.id
        )
        db.session.add(menu_item)
        db.session.commit()
        flash('Neues Menü-Item wurde hinzugefügt!', 'success')
        return redirect(url_for('admin.menu_management'))
    
    return render_template('admin/menu_item.html',
                         title='Neues Menü-Item',
                         form=form,
                         legend='Neues Menü-Item erstellen')

@admin.route("/restaurant/menu/<int:item_id>/update", methods=['GET', 'POST'])
@login_required
@restaurant_owner_required
def update_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    if menu_item.restaurant_id != current_user.owned_restaurant.id:
        flash('Sie haben keine Berechtigung, dieses Menü-Item zu bearbeiten.', 'danger')
        return redirect(url_for('admin.menu_management'))
    
    form = MenuItemForm()
    if form.validate_on_submit():
        menu_item.name = form.name.data
        menu_item.description = form.description.data
        menu_item.price = form.price.data
        menu_item.category = form.category.data
        menu_item.is_available = form.is_available.data
        db.session.commit()
        flash('Das Menü-Item wurde aktualisiert!', 'success')
        return redirect(url_for('admin.menu_management'))
    
    elif request.method == 'GET':
        form.name.data = menu_item.name
        form.description.data = menu_item.description
        form.price.data = menu_item.price
        form.category.data = menu_item.category
        form.is_available.data = menu_item.is_available
    
    return render_template('admin/menu_item.html',
                         title='Menü-Item Aktualisieren',
                         form=form,
                         legend='Menü-Item aktualisieren')

@admin.route("/restaurant/menu/<int:item_id>/delete", methods=['POST'])
@login_required
@restaurant_owner_required
def delete_menu_item(item_id):
    menu_item = MenuItem.query.get_or_404(item_id)
    if menu_item.restaurant_id != current_user.owned_restaurant.id:
        flash('Sie haben keine Berechtigung, dieses Menü-Item zu löschen.', 'danger')
        return redirect(url_for('admin.menu_management'))
    
    db.session.delete(menu_item)
    db.session.commit()
    flash('Das Menü-Item wurde gelöscht!', 'success')
    return redirect(url_for('admin.menu_management'))

@admin.route("/restaurant/orders")
@login_required
@restaurant_owner_required
def order_management():
    restaurant = current_user.owned_restaurant
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(restaurant_id=restaurant.id)\
        .order_by(Order.created_at.desc())\
        .paginate(page=page, per_page=10)
    return render_template('admin/order_management.html',
                         orders=orders)
