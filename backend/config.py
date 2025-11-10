import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'vishaal' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'parking_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
