import os

#API_KEY_EMOS = "10a3857b939c6b2de638236621d2476ec8cad593812e97e05ce7824ebd4ceb92"
API_KEY_EMOS = "bae031c49c193cc2730410befa67dcca7fb54b41be2487fbdd0b6a3691da8b4b"

SECRET_KEY = '}:Nq&)"F$9gEYmyVoY`MaB}'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'emoslive.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
