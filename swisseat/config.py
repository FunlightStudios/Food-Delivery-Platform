import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/swisseat' or 'sqlite:///swisseat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Swisseat]'
    FLASKY_MAIL_SENDER = 'Swisseat Admin <6Oc1I@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    SiteName = 'Swisseat'
    SiteDescription = 'Lokale Essen in der Schweiz'
    SiteOwner = 'SwissEat'

    SiteCompany = 'SwissEat GmbH'
    SiteAddress = 'Orpundstrasse 12, 2504 Biel, Schweiz'
    SitePhone = '+41 123 456 789'
    SiteEmail = 'info@swisseat.ch'

