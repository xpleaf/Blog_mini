# coding:utf-8
from datetime import datetime
from flask import render_template, redirect, flash, \
    url_for, request, current_app
from flask.ext.login import login_required
from . import admin
from ..models import ArticleType, Source, Article, article_types
from .forms import SubmitArticlesForm, ManageArticlesForm
from .. import db


@admin.route('/', methods=['GET', 'POST'])
@login_required
def manager():
    return render_template('admin/admin_base.html', ArticleType=ArticleType, article_types=article_types)


@admin.route('/submit-articles', methods=['GET', 'POST'])
@login_required
def submitArticles():
    form = SubmitArticlesForm()

    sources = [(s.id, s.name) for s in Source.query.all()]
    form.source.choices = sources
    types = [(t.id, t.name) for t in ArticleType.query.all()]
    form.types.choices = types

    if form.validate_on_submit():
        title = form.title.data
        source_id = form.source.data
        content = form.content.data
        type_id = form.types.data
        summary = form.summary.data

        source = Source.query.get(source_id)
        articleType = ArticleType.query.get(type_id)

        if source and articleType:
            article = Article(title=title, content=content, summary=summary,
                              source=source, articleType=articleType)
            db.session.add(article)
            db.session.commit()
            flash(u'发表文章成功！', 'success')
            article_id = Article.query.filter_by(title=title).first().id
            return redirect(url_for('main.articleDetails', id=article_id))
    if form.errors:
        flash(u'发表文章失败', 'danger')

    return render_template('admin/submit_articles.html', ArticleType=ArticleType,
                           article_types=article_types, form=form)


@admin.route('/edit-articles/<int:id>', methods=['GET', 'POST'])
@login_required
def editArticles(id):
    article = Article.query.get_or_404(id)
    form = SubmitArticlesForm()

    sources = [(s.id, s.name) for s in Source.query.all()]
    form.source.choices = sources
    types = [(t.id, t.name) for t in ArticleType.query.all()]
    form.types.choices = types

    if form.validate_on_submit():
        article.title = form.title.data
        article.source_id = form.source.data
        article.content = form.content.data
        article.type_id = form.types.data
        article.summary = form.summary.data
        article.update_time = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        flash(u'博文更新成功！', 'success')
        return redirect(url_for('main.articleDetails', id=article.id))
    form.source.data = article.source_id
    form.title.data = article.title
    form.content.data = article.content
    form.types.data = article.articleType_id
    form.summary.data = article.summary
    return render_template('admin/submit_articles.html', ArticleType=ArticleType, article_types=article_types,
                           form=form)


@admin.route('/manage-articles', methods=['GET', 'POST'])
@login_required
def manageArticles():
    form = ManageArticlesForm()

    sources = [(s.id, s.name) for s in Source.query.all()]
    sources.append((-1, u'全部分类'))
    form.source.choices = sources
    types = [(t.id, t.name) for t in ArticleType.query.all()]
    types.append((-1, u'全部来源'))
    form.types.choices = types

    if form.validate_on_submit():
        types_id = form.types.data
        source_id = form.source.data
        page = request.args.get('page', 1, type=int)

        if types_id == -1 and source_id != -1:
            source = Source.query.get_or_404(source_id)
            pagination = Article.query.order_by(Article.create_time.desc()).filter_by(source=source).paginate(
                    page, per_page=current_app.config['ARTICLES_PER_PAGE'],error_out=False)
        elif source_id == -1 and types_id != -1:
            articleType = ArticleType.query.get_or_404(types_id)
            pagination = Article.query.order_by(Article.create_time.desc()).filter_by(
                    articleType=articleType).paginate(
                    page, per_page=current_app.config['ARTICLES_PER_PAGE'],error_out=False)
        elif source_id == -1 and types_id == -1:
            pagination = Article.query.order_by(Article.create_time.desc()).paginate(
                    page, per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)
        else:
            source = Source.query.get_or_404(source_id)
            articleType = ArticleType.query.get_or_404(types_id)
            pagination = Article.query.order_by(Article.create_time.desc()).filter_by(
                    source=source).filter_by(articleType=articleType).paginate(
                    page, per_page=current_app.config['ARTICLES_PER_PAGE'],error_out=False)

        articles = pagination.items
        return render_template('admin/manage_articles.html', ArticleType=ArticleType, article_types=article_types,
                               Article=Article, articles=articles, pagination=pagination,
                               endpoint='admin.manageArticles', form=form)

    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
            page, per_page=current_app.config['ARTICLES_PER_PAGE'],
            error_out=False)
    articles = pagination.items
    return render_template('admin/manage_articles.html', ArticleType=ArticleType, article_types=article_types,
                           Article=Article, articles=articles, pagination=pagination, endpoint='admin.manageArticles',
                           form=form)
