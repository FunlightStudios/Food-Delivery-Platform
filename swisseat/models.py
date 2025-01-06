from datetime import datetime
from swisseat import db, login_manager
from flask_login import UserMixin, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), default='user')
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    orders = db.relationship('Order', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    carts = db.relationship('Cart', back_populates='user', lazy=True)
    owned_restaurant = db.relationship('Restaurant', backref='owner', lazy=True, uselist=False)

    def is_restaurant_owner(self):
        return self.role == 'restaurant_owner'

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(200), nullable=False)
    cuisine_type = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    delivery_time = db.Column(db.Integer, nullable=False)  # in minutes
    minimum_order = db.Column(db.Float, nullable=False)  # in CHF
    delivery_fee = db.Column(db.Float, nullable=False, default=0)  # in CHF
    accepts_cash = db.Column(db.Boolean, nullable=False, default=True)
    accepts_twint = db.Column(db.Boolean, nullable=False, default=True)
    accepts_paypal = db.Column(db.Boolean, nullable=False, default=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True)
    orders = db.relationship('Order', backref='restaurant', lazy=True)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)
    carts = db.relationship('Cart', back_populates='restaurant', lazy=True)

    def __repr__(self):
        return f"Restaurant('{self.name}', '{self.cuisine_type}')"

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    cart_items = db.relationship('CartItem', back_populates='menu_item', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='orders')
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    delivered_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    delivery_address = db.Column(db.String(200), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)  # Total amount including delivery fee
    payment_method = db.Column(db.String(20), nullable=False)  # cash, twint, paypal
    date_ordered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order_ref', lazy=True)
    
    def get_total(self):
        return sum(item.get_total() for item in self.items)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Float, nullable=False)
    menu_item = db.relationship('MenuItem', backref='order_items')
    
    def get_total(self):
        return self.price_at_time * self.quantity

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    user = db.relationship('User', back_populates='carts')
    restaurant = db.relationship('Restaurant', back_populates='carts')
    items = db.relationship('CartItem', back_populates='cart', lazy=True, cascade='all, delete-orphan')

    def get_total(self):
        return sum(item.get_total() for item in self.items)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    cart = db.relationship('Cart', back_populates='items')
    menu_item = db.relationship('MenuItem', back_populates='cart_items')
    get_total = db.Column(db.Float, nullable=False)

    def get_total(self):
        return self.price * self.quantity

class CmsSiteInfos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variable = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(250), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class UserAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
