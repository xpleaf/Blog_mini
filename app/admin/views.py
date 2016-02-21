# coding:utf-8
from flask import render_template, redirect, flash, \
    url_for
from . import admin
from ..models import ArticleType, Source, Article, article_types
from .forms import SubmitArticlesForm
from .. import db


@admin.route('/submit-articles', methods=['GET', 'POST'])
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
            return redirect(url_for('main.articleDetails', ArticleType=ArticleType,
                           article_types=article_types, id=article_id))
    if form.errors:
        flash(u'发表文章失败', 'danger')

    return render_template('admin/submit_articles.html', ArticleType=ArticleType,
                           article_types=article_types, form=form)
