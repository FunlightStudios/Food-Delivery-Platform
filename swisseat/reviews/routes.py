from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from swisseat import db
from swisseat.models import Review, Restaurant, Order
from swisseat.reviews.forms import ReviewForm

reviews = Blueprint('reviews', __name__)

@reviews.route("/restaurant/<int:restaurant_id>/reviews")
def restaurant_reviews(restaurant_id):
    page = request.args.get('page', 1, type=int)
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    reviews = Review.query.filter_by(restaurant_id=restaurant_id)\
        .order_by(Review.date_posted.desc())\
        .paginate(page=page, per_page=10)
    return render_template('reviews/restaurant_reviews.html', 
                         restaurant=restaurant, 
                         reviews=reviews)

@reviews.route("/order/<int:order_id>/review", methods=['GET', 'POST'])
@login_required
def add_review(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        flash('Sie haben keine Berechtigung, diese Bestellung zu bewerten.', 'danger')
        return redirect(url_for('main.home'))
    
    if order.review:
        flash('Sie haben diese Bestellung bereits bewertet.', 'info')
        return redirect(url_for('orders.order_detail', order_id=order_id))
    
    if order.status != 'delivered':
        flash('Sie können nur gelieferte Bestellungen bewerten.', 'warning')
        return redirect(url_for('orders.order_detail', order_id=order_id))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            rating=form.rating.data,
            comment=form.comment.data,
            user_id=current_user.id,
            restaurant_id=order.restaurant_id,
            order_id=order.id
        )
        db.session.add(review)
        
        # Aktualisiere die durchschnittliche Restaurantbewertung
        restaurant = order.restaurant
        avg_rating = db.session.query(db.func.avg(Review.rating))\
            .filter_by(restaurant_id=restaurant.id).scalar()
        restaurant.rating = float(avg_rating)
        
        db.session.commit()
        flash('Ihre Bewertung wurde erfolgreich hinzugefügt!', 'success')
        return redirect(url_for('orders.order_detail', order_id=order_id))
        
    return render_template('reviews/add_review.html', 
                         form=form, 
                         order=order)
