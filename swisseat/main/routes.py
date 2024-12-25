from flask import Blueprint, render_template
from swisseat.models import Restaurant

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    restaurants = Restaurant.query.all()
    return render_template('home.html', restaurants=restaurants)

@main.route('/about')
def about():
    return render_template('about.html', title='Über uns')
