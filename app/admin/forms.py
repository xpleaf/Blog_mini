# coding:utf-8
from flask.ext.wtf import Form
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class SubmitArticlesForm(Form):
    title = StringField(u'标题', validators=[DataRequired(), Length(1, 64)])
    source = SelectField(u'博文来源', coerce=int, validators=[DataRequired()])
    content = TextAreaField(u'博文内容', validators=[DataRequired()])
    types = SelectField(u'博文分类', coerce=int, validators=[DataRequired()])
    summary = TextAreaField(u'博文摘要', validators=[DataRequired()])


class ManageArticlesForm(Form):
    pass
