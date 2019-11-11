import os
SECRET_KEY = '}:Nq&)"F$9gEYmyVoY`MaB}'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'emoslive.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
