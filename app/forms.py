from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    login = StringField('', ['', DataRequired(
        message='Forgot your email address?')], default="my@fra.com",
                      )
    password = PasswordField('', [DataRequired(
        message='Must provide a password. ;-)')], default="fra", render_kw={"placeholder": "Password"}
                             )
