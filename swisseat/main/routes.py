from flask import Blueprint, render_template
from swisseat.models import Restaurant, CmsSiteInfos

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    restaurants = Restaurant.query.all()

    # Get features title
    features_title = CmsSiteInfos.query.filter_by(variable='features_title').first()
    features_title = features_title.content if features_title else "Unbekannt"

    # Get Features Icons
    features_icon_1 = CmsSiteInfos.query.filter_by(variable='features_icon_1').first()
    features_icon_1 = features_icon_1.content if features_icon_1 else "Unbekannt"
    features_icon_2 = CmsSiteInfos.query.filter_by(variable='features_icon_2').first()
    features_icon_2 = features_icon_2.content if features_icon_2 else "Unbekannt"
    features_icon_3 = CmsSiteInfos.query.filter_by(variable='features_icon_3').first()
    features_icon_3 = features_icon_3.content if features_icon_3 else "Unbekannt"

    # Get Features Titles
    features_title_1 = CmsSiteInfos.query.filter_by(variable='features_title_1').first()
    features_title_1 = features_title_1.content if features_title_1 else "Unbekannt"
    features_title_2 = CmsSiteInfos.query.filter_by(variable='features_title_2').first()
    features_title_2 = features_title_2.content if features_title_2 else "Unbekannt"
    features_title_3 = CmsSiteInfos.query.filter_by(variable='features_title_3').first()
    features_title_3 = features_title_3.content if features_title_3 else "Unbekannt"

    # Get Features Content
    features_content_1 = CmsSiteInfos.query.filter_by(variable='features_content_1').first()
    features_content_1 = features_content_1.content if features_content_1 else "Unbekannt"
    features_content_2 = CmsSiteInfos.query.filter_by(variable='features_content_2').first()
    features_content_2 = features_content_2.content if features_content_2 else "Unbekannt"
    features_content_3 = CmsSiteInfos.query.filter_by(variable='features_content_3').first()
    features_content_3 = features_content_3.content if features_content_3 else "Unbekannt"

    return render_template('home.html', restaurants=restaurants,
                                features_title=features_title,
                                features_icon_1=features_icon_1,
                                features_icon_2=features_icon_2,
                                features_icon_3=features_icon_3,
                                features_title_1=features_title_1,
                                features_title_2=features_title_2,
                                features_title_3=features_title_3,
                                features_content_1=features_content_1,
                                features_content_2=features_content_2,
                                features_content_3=features_content_3
                                )

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
