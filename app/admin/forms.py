# coding:utf-8
from flask.ext.wtf import Form
from wtforms import SelectField, StringField, TextAreaField, SubmitField, \
    PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
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


class SortArticleNavTypeForm(AddArticleTypeNavForm):
    order = StringField(u'序号', validators=[DataRequired()])


class CustomBlogInfoForm(Form):
    title = StringField(u'博客标题', validators=[DataRequired()])
    signature = TextAreaField(u'个性签名', validators=[DataRequired()])
    navbar = SelectField(u'导航样式', coerce=int, validators=[DataRequired()])


class AddBlogPluginForm(Form):
    title = StringField(u'插件名称', validators=[DataRequired()])
    note = TextAreaField(u'备注')
    content = TextAreaField(u'内容', validators=[DataRequired()])


class ChangePasswordForm(Form):
    old_password = PasswordField(u'原来密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次输入密码不一致！')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])


class EditUserInfoForm(Form):
    username = StringField(u'昵称', validators=[DataRequired()])
    email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u'密码确认', validators=[DataRequired()])
