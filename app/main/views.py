#coding:utf-8
from flask import render_template, request, current_app, redirect,\
    url_for, flash, g
from flask.ext.login import login_required, current_user
from . import main
from ..models import Article, ArticleType, article_types, Comment, \
    Follow, User, Source, BlogView
from .forms import CommentForm, SearchForm
from .. import db

@main.before_request
def before_request():
    g.user = current_user
#    if g.user.is_authenticated():
#        g.user.last_seen = datetime.utcnow()
#        db.session.add(g.user)
#        db.session.commit()
#        g.search_form = SearchForm()
    g.search_form = SearchForm()
    #g.locale = get_locale()

@main.route('/search', methods = ['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('main.search_results', query = g.search_form.search.data))
    
@main.route('/search_results/<query>')
def search_results(query):
    BlogView.add_view(db)
    per_page = current_app.config['ARTICLES_PER_PAGE']
    max_search = current_app.config['MAX_SEARCH_RESULTS']
#    pagination = Article.query.whoosh_search(query, max_search).paginate(
#            page=1, per_page=current_app.config['ARTICLES_PER_PAGE'],
#            error_out=False)
#    print query, pagination
#    articles = pagination.items
#    return render_template('search_results.html', articles=articles,
#            query = query,pagination=pagination, endpoint='.search_results')

    articles = Article.query.whoosh_search(query, max_search).all()
    print query, articles
    #articles = pagination.items
    return render_template('search_results.html', articles=articles,
            query = query, endpoint='.search_results')


@main.route('/')
def index():
    BlogView.add_view(db)
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.create_time.desc()).paginate(
            page, per_page=current_app.config['ARTICLES_PER_PAGE'],
            error_out=False)
    articles = pagination.items
    return render_template('index.html', articles=articles,
                           pagination=pagination, endpoint='.index')


@main.route('/article-types/<int:id>/')
def articleTypes(id):
    BlogView.add_view(db)
    page = request.args.get('page', 1, type=int)
    pagination = ArticleType.query.get_or_404(id).articles.order_by(
            Article.create_time.desc()).paginate(
            page, per_page=current_app.config['ARTICLES_PER_PAGE'],
            error_out=False)
    articles = pagination.items
    return render_template('index.html', articles=articles,
                           pagination=pagination, endpoint='.articleTypes',
                           id=id)


@main.route('/article-sources/<int:id>/')
def article_sources(id):
    BlogView.add_view(db)
    page = request.args.get('page', 1, type=int)
    pagination = Source.query.get_or_404(id).articles.order_by(
            Article.create_time.desc()).paginate(
            page, per_page=current_app.config['ARTICLES_PER_PAGE'],
            error_out=False)
    articles = pagination.items
    return render_template('index.html', articles=articles,
                           pagination=pagination, endpoint='.article_sources',
                           id=id)


@main.route('/article-detials/<int:id>', methods=['GET', 'POST'])
def articleDetails(id):
    BlogView.add_view(db)
    form = CommentForm(request.form, follow=-1)
    article = Article.query.get_or_404(id)

    if form.validate_on_submit():
        comment = Comment(article=article,
                          content=form.content.data,
                          author_name=form.name.data,
                          author_email=form.email.data)
        db.session.add(comment)
        db.session.commit()
        followed_id = int(form.follow.data)
        if followed_id != -1:
            followed = Comment.query.get_or_404(followed_id)
            f = Follow(follower=comment, followed=followed)
            comment.comment_type = 'reply'
            comment.reply_to = followed.author_name
            db.session.add(f)
            db.session.add(comment)
            db.session.commit()
        flash(u'提交评论成功！', 'success')
        return redirect(url_for('.articleDetails', id=article.id, page=-1))
    if form.errors:
        flash(u'发表评论失败', 'danger')

    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (article.comments.count() - 1) // \
            current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = article.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    article.add_view(article, db)
    return render_template('article_detials.html', User=User, article=article,
                           comments=comments, pagination=pagination, page=page,
                           form=form, endpoint='main.articleDetails', id=article.id)
    # page=page, this is used to return the current page args to the
    # disable comment or enable comment endpoint to pass it to the articleDetails endpoint
