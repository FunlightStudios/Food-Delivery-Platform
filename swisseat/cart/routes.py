from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from swisseat import db
from swisseat.models import MenuItem, Cart, CartItem, Restaurant

cart = Blueprint('cart', __name__)

@cart.route('/cart')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    return render_template('cart/cart.html', cart=cart)

@cart.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    
    if not data or 'item_id' not in data:
        return jsonify({'success': False, 'message': 'Ungültige Anfrage'}), 400
    
    item_id = data['item_id']
    quantity = data.get('quantity', 1)
    
    menu_item = MenuItem.query.get_or_404(item_id)
    
    # Prüfen ob der Benutzer bereits einen Warenkorb hat
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    # Wenn kein Warenkorb existiert oder der Warenkorb von einem anderen Restaurant ist
    if not cart or cart.restaurant_id != menu_item.restaurant_id:
        # Wenn ein alter Warenkorb existiert, lösche ihn
        if cart:
            db.session.delete(cart)
            db.session.commit()
        # Erstelle einen neuen Warenkorb
        cart = Cart(user_id=current_user.id, restaurant_id=menu_item.restaurant_id)
        db.session.add(cart)
        db.session.commit()
    
    # Prüfen ob das Item bereits im Warenkorb ist
    cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_item_id=item_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            menu_item_id=item_id,
            quantity=quantity,
            price=menu_item.price
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    # Gesamtanzahl der Items im Warenkorb
    cart_count = sum(item.quantity for item in cart.items)
    
    return jsonify({
        'success': True,
        'message': 'Item wurde zum Warenkorb hinzugefügt',
        'cart_count': cart_count
    })

@cart.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    data = request.get_json()
    if not data or 'delta' not in data:
        return jsonify({'success': False, 'message': 'Ungültige Anfrage'}), 400
    
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Zugriff verweigert'}), 403
    
    new_quantity = cart_item.quantity + data['delta']
    if new_quantity < 1:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = new_quantity
    
    db.session.commit()
    return jsonify({'success': True})

@cart.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Zugriff verweigert'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'success': True})

@cart.route('/cart/clear', methods=['POST'])
@login_required
def clear_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        db.session.delete(cart)
        db.session.commit()
    return jsonify({'success': True})

@cart.route('/cart/count')
@login_required
def get_cart_count():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    count = 0
    if cart:
        count = sum(item.quantity for item in cart.items)
    return jsonify({'count': count})