from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from swisseat import db
from swisseat.models import Restaurant, MenuItem, Order
from swisseat.restaurants.forms import RestaurantForm, MenuItemForm, RestaurantSearchForm
from datetime import datetime, date

restaurants = Blueprint('restaurants', __name__)

@restaurants.route("/restaurants")
def list():
    page = request.args.get('page', 1, type=int)
    restaurants_list = Restaurant.query.order_by(Restaurant.name).paginate(page=page, per_page=12)
    return render_template('restaurants/list.html', restaurants=restaurants_list)

@restaurants.route("/restaurants/search", methods=['GET'])
def search():
    query = request.args.get('q', '')
    cuisine = request.args.get('cuisine', '')
    
    restaurants_query = Restaurant.query
    
    if query:
        restaurants_query = restaurants_query.filter(
            Restaurant.name.ilike(f'%{query}%') | 
            Restaurant.description.ilike(f'%{query}%')
        )
    
    if cuisine:
        restaurants_query = restaurants_query.filter(Restaurant.cuisine_type == cuisine)
    
    restaurants_list = restaurants_query.order_by(Restaurant.rating.desc()).all()
    return render_template('restaurants/search.html', 
                         restaurants=restaurants_list, 
                         query=query,
                         cuisine=cuisine)

@restaurants.route("/restaurants/dashboard")
@login_required
def dashboard():
    if not current_user.is_restaurant_owner():
        flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
        return redirect(url_for('main.home'))
    
    restaurant = Restaurant.query.filter_by(owner=current_user).first()
    if not restaurant:
        flash('Sie haben kein Restaurant registriert.', 'danger')
        return redirect(url_for('restaurants.register'))
    
    today = datetime.utcnow().date()
    
    # Calculate today's orders and revenue
    today_orders = Order.query.filter(
        Order.restaurant_id == restaurant.id,
        db.func.date(Order.created_at) == today
    ).all()
    
    today_order_count = len(today_orders)
    today_revenue = sum(order.total_amount for order in today_orders)
    menu_item_count = len(restaurant.menu_items)
    
    # Get all orders for the restaurant
    orders = Order.query.filter_by(restaurant_id=restaurant.id).order_by(Order.created_at.desc()).all()
    
    return render_template('restaurants/dashboard.html', 
                         restaurant=restaurant,
                         today_order_count=today_order_count,
                         today_revenue=today_revenue,
                         menu_item_count=menu_item_count,
                         orders=orders)

@restaurants.route("/restaurant/<int:restaurant_id>")
def restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    return render_template('restaurants/restaurant.html', restaurant=restaurant)

@restaurants.route("/restaurant/<int:restaurant_id>/menu")
def menu(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id, is_available=True).all()
    return render_template('restaurants/menu.html', restaurant=restaurant, menu_items=menu_items)

@restaurants.route("/restaurant/orders")
@login_required
def orders():
    if not current_user.is_restaurant_owner():
        flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
        return redirect(url_for('main.home'))
    
    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not restaurant:
        flash('Sie haben noch kein Restaurant registriert.', 'warning')
        return redirect(url_for('restaurants.register'))
    
    # Get orders by status, ordered by creation date (oldest first)
    current_orders = Order.query.filter(
        Order.restaurant_id == restaurant.id,
        Order.status.in_(['pending', 'confirmed'])
    ).order_by(Order.created_at.asc()).all()
    
    completed_orders = Order.query.filter_by(
        restaurant_id=restaurant.id,
        status='delivered'
    ).order_by(Order.created_at.asc()).all()
    
    cancelled_orders = Order.query.filter_by(
        restaurant_id=restaurant.id,
        status='cancelled'
    ).order_by(Order.created_at.asc()).all()
    
    return render_template('restaurants/orders.html',
                         restaurant=restaurant,
                         current_orders=current_orders,
                         completed_orders=completed_orders,
                         cancelled_orders=cancelled_orders,
                         now=datetime.utcnow())

@restaurants.route("/restaurant/register", methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.role == 'restaurant_owner':
        flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
        return redirect(url_for('main.home'))
    
    if current_user.owned_restaurant:
        flash('Sie haben bereits ein Restaurant registriert.', 'info')
        return redirect(url_for('restaurants.dashboard'))
    
    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            cuisine_type=form.cuisine_type.data,
            delivery_time=form.delivery_time.data,
            minimum_order=form.minimum_order.data,
            delivery_fee=form.delivery_fee.data,
            accepts_cash=form.accepts_cash.data,
            accepts_twint=form.accepts_twint.data,
            accepts_paypal=form.accepts_paypal.data,
            owner=current_user,
            rating=0.0
        )
        db.session.add(restaurant)
        db.session.commit()
        flash('Ihr Restaurant wurde erfolgreich registriert!', 'success')
        return redirect(url_for('restaurants.dashboard'))
    return render_template('restaurants/register.html', title='Restaurant registrieren', form=form)

@restaurants.route("/restaurant/menu/new", methods=['GET', 'POST'])
@login_required
def add_menu_item():
    if not current_user.is_restaurant_owner():
        flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
        return redirect(url_for('main.home'))
    
    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not restaurant:
        flash('Sie haben noch kein Restaurant registriert.', 'warning')
        return redirect(url_for('restaurants.register'))
    
    form = MenuItemForm()
    if form.validate_on_submit():
        menu_item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            restaurant_id=restaurant.id
        )
        db.session.add(menu_item)
        db.session.commit()
        flash('Menüeintrag wurde erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('restaurants.menu', restaurant_id=restaurant.id))
    return render_template('restaurants/add_menu_item.html', form=form)

@restaurants.route("/restaurant/edit", methods=['GET', 'POST'])
@login_required
def edit_restaurant():
    if not current_user.is_restaurant_owner():
        flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
        return redirect(url_for('main.home'))
    
    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not restaurant:
        flash('Sie haben noch kein Restaurant registriert.', 'warning')
        return redirect(url_for('restaurants.register'))
    
    form = RestaurantForm()
    if request.method == 'GET':
        form.name.data = restaurant.name
        form.description.data = restaurant.description
        form.address.data = restaurant.address
        form.cuisine_type.data = restaurant.cuisine_type
        form.delivery_time.data = restaurant.delivery_time
        form.minimum_order.data = restaurant.minimum_order
        form.delivery_fee.data = restaurant.delivery_fee
    
    if form.validate_on_submit():
        restaurant.name = form.name.data
        restaurant.description = form.description.data
        restaurant.address = form.address.data
        restaurant.cuisine_type = form.cuisine_type.data
        restaurant.delivery_time = form.delivery_time.data
        restaurant.minimum_order = form.minimum_order.data
        restaurant.delivery_fee = form.delivery_fee.data
        db.session.commit()
        flash('Restaurant wurde erfolgreich aktualisiert!', 'success')
        return redirect(url_for('restaurants.dashboard'))
    
    return render_template('restaurants/edit_restaurant.html', form=form, restaurant=restaurant)

@restaurants.route("/restaurant/settings")
@login_required
def settings():
    if not current_user.is_restaurant_owner():
        flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
        return redirect(url_for('main.home'))
    
    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not restaurant:
        flash('Sie haben noch kein Restaurant registriert.', 'warning')
        return redirect(url_for('restaurants.register'))
    
    return render_template('restaurants/settings.html', restaurant=restaurant)

@restaurants.route("/restaurant/orders/<int:order_id>/status", methods=['POST'])
@login_required
def update_order_status(order_id):
    if not current_user.is_restaurant_owner():
        return jsonify({'success': False, 'message': 'Keine Berechtigung'}), 403
    
    restaurant = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not restaurant:
        return jsonify({'success': False, 'message': 'Restaurant nicht gefunden'}), 404
    
    order = Order.query.filter_by(id=order_id, restaurant_id=restaurant.id).first()
    if not order:
        return jsonify({'success': False, 'message': 'Bestellung nicht gefunden'}), 404
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['confirmed', 'delivered', 'cancelled']:
        return jsonify({'success': False, 'message': 'Ungültiger Status'}), 400
    
    # Update status and timestamps
    order.status = new_status
    if new_status == 'delivered':
        order.delivered_at = datetime.utcnow()
    elif new_status == 'cancelled':
        order.cancelled_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Status erfolgreich aktualisiert'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@restaurants.route("/toggle-status", methods=['POST'])
@login_required
def toggle_status():
    if not current_user.is_restaurant_owner():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    restaurant = Restaurant.query.filter_by(owner=current_user).first()
    if not restaurant:
        return jsonify({'success': False, 'message': 'Restaurant not found'}), 404

    restaurant.is_active = not restaurant.is_active
    db.session.commit()

    return jsonify({
        'success': True,
        'is_active': restaurant.is_active,
        'message': 'Restaurant status updated successfully'
    })

@restaurants.route("/menu/edit/<int:item_id>", methods=['GET', 'POST'])
@login_required
def edit_menu_item(item_id):
    if not current_user.is_restaurant_owner():
        flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
        return redirect(url_for('main.home'))
    
    restaurant = Restaurant.query.filter_by(owner=current_user).first()
    if not restaurant:
        flash('Sie haben kein Restaurant registriert.', 'danger')
        return redirect(url_for('restaurants.register'))
    
    menu_item = MenuItem.query.get_or_404(item_id)
    if menu_item.restaurant_id != restaurant.id:
        flash('Sie haben keine Berechtigung dieses Gericht zu bearbeiten.', 'danger')
        return redirect(url_for('restaurants.dashboard'))
    
    form = MenuItemForm()
    if form.validate_on_submit():
        menu_item.name = form.name.data
        menu_item.description = form.description.data
        menu_item.price = form.price.data
        menu_item.category = form.category.data
        menu_item.is_available = form.is_available.data
        db.session.commit()
        flash('Gericht wurde erfolgreich aktualisiert!', 'success')
        return redirect(url_for('restaurants.dashboard'))
    
    elif request.method == 'GET':
        form.name.data = menu_item.name
        form.description.data = menu_item.description
        form.price.data = menu_item.price
        form.category.data = menu_item.category
        form.is_available.data = menu_item.is_available
    
    return render_template('restaurants/edit_menu_item.html', form=form, menu_item=menu_item)

@restaurants.route("/menu/delete/<int:item_id>", methods=['POST'])
@login_required
def delete_menu_item(item_id):
    if not current_user.is_restaurant_owner():
        flash('Sie haben keine Berechtigung für diese Seite.', 'danger')
        return redirect(url_for('main.home'))
    
    restaurant = Restaurant.query.filter_by(owner=current_user).first()
    if not restaurant:
        flash('Sie haben kein Restaurant registriert.', 'danger')
        return redirect(url_for('restaurants.register'))
    
    menu_item = MenuItem.query.get_or_404(item_id)
    if menu_item.restaurant_id != restaurant.id:
        flash('Sie haben keine Berechtigung dieses Gericht zu löschen.', 'danger')
        return redirect(url_for('restaurants.dashboard'))
    
    db.session.delete(menu_item)
    db.session.commit()
    flash('Gericht wurde erfolgreich gelöscht!', 'success')
    return redirect(url_for('restaurants.dashboard'))
