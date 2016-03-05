# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
    email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
