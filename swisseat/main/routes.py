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

@main.route("/impressum")
def impressum():
    return render_template('impressum.html')

@main.route("/privacy")
def privacy():
    return render_template('privacy.html')

@main.route("/partner")
def partner():
    return render_template('partner.html')
