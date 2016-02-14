#coding:utf-8
from flask import render_template, request, current_app, redirect,\
    url_for, flash
from . import main
from ..models import Article, ArticleType, article_types, Comment
from .forms import CommentForm
from .. import db


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
            page, per_page=current_app.config['ARTICLES_PER_PAGE'],
            error_out=False)
    articles = pagination.items
    return render_template('index.html', ArticleType=ArticleType, article_types=article_types,
                           articles=articles, pagination=pagination, endpoint='.index')


@main.route('/article-types/<int:id>/')
def articleTypes(id):
    page = request.args.get('page', 1, type=int)
    pagination = ArticleType.query.get_or_404(id).articles.order_by(
            Article.create_time.desc()).paginate(
            page, per_page=current_app.config['ARTICLES_PER_PAGE'],
            error_out=False)
    articles = pagination.items
    return render_template('index.html', ArticleType=ArticleType, article_types=article_types,
                           articles=articles, pagination=pagination, endpoint='.articleTypes', id=id)


@main.route('/article-detials/<int:id>', methods=['GET', 'POST'])
def articleDetails(id):
    form = CommentForm()
    article = Article.query.get_or_404(id)
    if form.validate_on_submit():
        comment = Comment(article=article,
                          content=form.content.data,
                          author_name=form.name.data,
                          author_email=form.email.data)
        db.session.add(comment)
        db.session.commit()
        flash(u'提交评论成功！')
        return redirect(url_for('.articleDetails', id=article.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (article.comments.count() - 1) // \
            current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = article.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('article_detials.html', ArticleType=ArticleType,
                           article_types=article_types, article=article,
                           comments=comments, pagination=pagination, form=form,
                           endpoint='.articleDetails', id=article.id)
