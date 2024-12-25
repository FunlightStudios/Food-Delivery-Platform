from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from swisseat import db
from swisseat.models import Order, OrderItem, Restaurant, MenuItem, Cart
from datetime import datetime

orders = Blueprint('orders', __name__)

@orders.route("/orders/checkout/<int:restaurant_id>", methods=['GET', 'POST'])
@login_required
def checkout(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    cart = Cart.query.filter_by(user_id=current_user.id, restaurant_id=restaurant_id).first()
    
    if not cart or not cart.items:
        flash('Ihr Warenkorb ist leer.', 'warning')
        return redirect(url_for('restaurants.menu', restaurant_id=restaurant_id))
    
    if request.method == 'POST':
        if not current_user.address:
            flash('Bitte fügen Sie eine Lieferadresse in Ihrem Profil hinzu.', 'warning')
            return redirect(url_for('users.register'))

        payment_method = request.form.get('payment_method')
        if not payment_method:
            flash('Bitte wählen Sie eine Zahlungsmethode.', 'warning')
            return redirect(url_for('orders.checkout', restaurant_id=restaurant_id))

        # Verify payment method is accepted by restaurant
        if (payment_method == 'cash' and not restaurant.accepts_cash) or \
           (payment_method == 'twint' and not restaurant.accepts_twint) or \
           (payment_method == 'paypal' and not restaurant.accepts_paypal):
            flash('Diese Zahlungsmethode wird vom Restaurant nicht akzeptiert.', 'warning')
            return redirect(url_for('orders.checkout', restaurant_id=restaurant_id))

        # Berechne den Gesamtbetrag aus dem Cart
        total_amount = cart.get_total()
        
        if total_amount < restaurant.minimum_order:
            flash(f'Mindestbestellwert von CHF {restaurant.minimum_order:.2f} nicht erreicht', 'warning')
            return redirect(url_for('cart.view_cart'))

        try:
            # Erstelle die Bestellung
            order = Order(
                user_id=current_user.id,
                restaurant_id=restaurant_id,
                total_amount=total_amount + restaurant.delivery_fee,
                delivery_address=current_user.address,
                payment_method=payment_method,
                status='pending'
            )
            db.session.add(order)
            db.session.commit()  # Commit to get the order ID
            
            # Füge die Bestellpositionen hinzu
            for cart_item in cart.items:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=cart_item.menu_item_id,
                    quantity=cart_item.quantity,
                    price_at_time=cart_item.price
                )
                db.session.add(order_item)
            
            # Lösche den Warenkorb
            db.session.delete(cart)
            db.session.commit()
            
            flash('Ihre Bestellung wurde erfolgreich aufgegeben!', 'success')
            return redirect(url_for('orders.order_detail', order_id=order.id))
            
        except Exception as e:
            db.session.rollback()
            flash('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.', 'danger')
            return redirect(url_for('cart.view_cart'))
    
    # Make sure the restaurant has at least one payment method enabled
    if not (restaurant.accepts_cash or restaurant.accepts_twint or restaurant.accepts_paypal):
        restaurant.accepts_cash = True
        restaurant.accepts_twint = True
        restaurant.accepts_paypal = True
        db.session.commit()
    
    return render_template('orders/checkout.html', cart=cart, restaurant=restaurant)

@orders.route("/orders/my-orders")
@login_required
def my_orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(user_id=current_user.id)\
        .order_by(Order.date_ordered.desc())\
        .paginate(page=page, per_page=10)
    return render_template('orders/my_orders.html', orders=orders)

@orders.route("/orders/<int:order_id>")
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Sie haben keine Berechtigung, diese Bestellung einzusehen.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('orders/order_detail.html', order=order)

@orders.route("/orders/<int:order_id>/cancel", methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return jsonify({
            'success': False,
            'message': 'Keine Berechtigung'
        }), 403
        
    if order.status != 'pending':
        return jsonify({
            'success': False,
            'message': 'Bestellung kann nicht mehr storniert werden'
        }), 400
        
    order.status = 'cancelled'
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Bestellung wurde storniert'
    })
