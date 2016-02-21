from flask import render_template
from . import admin
from ..models import ArticleType, Source, article_types
from .forms import SubmitArticlesForm


@admin.route('/submit-articles', methods=['GET', 'POST'])
def submitArticles():
    form = SubmitArticlesForm()

    sources = [(s.id, s.name) for s in Source.query.all()]
    form.source.choices = sources
    types = [(t.id, t.name) for t in ArticleType.query.all()]
    form.types.choices = types

    articleTypes=ArticleType.query.all()
    sources = Source.query.all()
    return render_template('admin/submit_articles.html', ArticleType=ArticleType,
                           article_types=article_types,articleTypes=articleTypes,
                           sources=sources, form=form)
