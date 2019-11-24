import os
SECRET_KEY = '}:Nq&)"F$9gEYmyVoY`MaB}'

if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'emoslive.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

else:
    # Postgresql Heroku
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']