# coding:utf-8
from flask.ext.wtf import Form
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from ..main.forms import CommentForm


class CommonForm(Form):
    types = SelectField(u'博文分类', coerce=int, validators=[DataRequired()])
    source = SelectField(u'博文来源', coerce=int, validators=[DataRequired()])


class SubmitArticlesForm(CommonForm):
    title = StringField(u'标题', validators=[DataRequired(), Length(1, 64)])
    content = TextAreaField(u'博文内容', validators=[DataRequired()])
    summary = TextAreaField(u'博文摘要', validators=[DataRequired()])


class ManageArticlesForm(CommonForm):
    pass


class DeleteArticleForm(Form):
    articleId = StringField(validators=[DataRequired()])


class DeleteArticlesForm(Form):
    articleIds = StringField(validators=[DataRequired()])


class DeleteCommentsForm(Form):
    commentIds = StringField(validators=[DataRequired()])


class AdminCommentForm(CommentForm):
    article = StringField(validators=[DataRequired()])


class AddArticleTypeForm(Form):
    name = StringField(u'分类名称', validators=[DataRequired(), Length(1, 64)])
    introduction = TextAreaField(u'分类介绍')
    setting_hide = SelectField(u'属性', coerce=int, validators=[DataRequired()])
    menus = SelectField(u'所属导航', coerce=int, validators=[DataRequired()])
# You must add coerce=int, or the SelectFile validate function only validate the int data


class EditArticleTypeForm(AddArticleTypeForm):
    articleType_id = StringField(validators=[DataRequired()])


class AddArticleTypeNavForm(Form):
    name = StringField(u'导航名称', validators=[DataRequired(), Length(1, 64)])


class EditArticleNavTypeForm(AddArticleTypeNavForm):
    nav_id = StringField(validators=[DataRequired()])
