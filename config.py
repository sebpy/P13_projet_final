import os
SECRET_KEY = '}:Nq&)"F$9gEYmyVoY`MaB}'

#  Use sqlite because Emos-Live is Standalone app
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'emoslive.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
