# coding:utf-8
from datetime import datetime
import json
from flask import render_template, redirect, flash, \
    url_for, request, current_app
from flask.ext.login import login_required
from . import admin
from ..models import ArticleType, Source, Article, article_types, \
    Comment, User, Follow
from .forms import SubmitArticlesForm, ManageArticlesForm, DeleteArticleForm, \
    DeleteArticlesForm, AdminCommentForm, DeleteCommentsForm
from .. import db


@admin.route('/', methods=['GET', 'POST'])
@login_required
def manager():
    return render_template('admin/admin_base.html')


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

    return render_template('admin/submit_articles.html', form=form)


@admin.route('/edit-articles/<int:id>')
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
    return render_template('admin/submit_articles.html', form=form)


@admin.route('/manage-articles', methods=['GET', 'POST'])
@login_required
def manage_articles():
    types_id = request.args.get('types_id', -1, type=int)
    source_id = request.args.get('source_id', -1, type=int)
    form = ManageArticlesForm(request.form, types=types_id, source=source_id)
    form2 = DeleteArticleForm()  # for delete an article
    from3 = DeleteArticlesForm()  # for delete articles

    types = [(t.id, t.name) for t in ArticleType.query.all()]
    types.append((-1, u'全部分类'))
    form.types.choices = types
    sources = [(s.id, s.name) for s in Source.query.all()]
    sources.append((-1, u'全部来源'))
    form.source.choices = sources

    pagination_search = 0

    if form.validate_on_submit() or \
            (request.args.get('types_id') is not None and request.args.get('source_id') is not None):
        if form.validate_on_submit():
            types_id = form.types.data
            source_id = form.source.data
            page = 1
        else:
            types_id = request.args.get('types_id', type=int)
            source_id = request.args.get('source_id', type=int)
            form.types.data = types_id
            form.source.data = source_id
            page = request.args.get('page', 1, type=int)

        result = Article.query.order_by(Article.create_time.desc())
        if types_id != -1:
            articleType = ArticleType.query.get_or_404(types_id)
            result = result.filter_by(articleType=articleType)
        if source_id != -1:
            source = Source.query.get_or_404(source_id)
            result = result.filter_by(source=source)
        pagination_search = result.paginate(
                page, per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)

    if pagination_search != 0:
        pagination = pagination_search
        articles = pagination_search.items
    else:
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(Article.create_time.desc()).paginate(
                page, per_page=current_app.config['ARTICLES_PER_PAGE'],
                error_out=False)
        articles = pagination.items

    return render_template('admin/manage_articles.html', Article=Article,
                           articles=articles, pagination=pagination,
                           endpoint='admin.manage_articles',
                           form=form, form2=form2, form3=from3,
                           types_id=types_id, source_id=source_id, page=page)


@admin.route('/manage-articles/delete-article', methods=['GET', 'POST'])
@login_required
def delete_article():
    types_id = request.args.get('types_id', -1, type=int)
    source_id = request.args.get('source_id', -1, type=int)
    form = DeleteArticleForm()

    if form.validate_on_submit():
        articleId = int(form.articleId.data)
        article = Article.query.get_or_404(articleId)
        count = article.comments.count()
        for comment in article.comments:
            db.session.delete(comment)
        db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败！', 'danger')
        else:
            flash(u'成功删除博文和%s条评论！' % count, 'success')
    if form.errors:
        flash(u'删除失败！', 'danger')

    return redirect(url_for('admin.manage_articles', types_id=types_id, source_id=source_id,
                            page=request.args.get('page', 1, type=int)))


@admin.route('/manage-articles/delete-articles', methods=['GET', 'POST'])
@login_required
def delete_articles():
    types_id = request.args.get('types_id', -1, type=int)
    source_id = request.args.get('source_id', -1, type=int)
    # form2 = DeleteArticleForm()
    form = DeleteArticlesForm()

    # if form2.validate_on_submit():
    #     articleId = form2.articleId.data
    #     print articleId

    if form.validate_on_submit():
        articleIds = json.loads(form.articleIds.data)
        count = 0
        for articleId in articleIds:
            article = Article.query.get_or_404(int(articleId))
            count += article.comments.count()
            for comment in article.comments:
                db.session.delete(comment)
            db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败！', 'danger')
        else:
            flash(u'成功删除%s篇博文和%s条评论！' % (len(articleIds), count), 'success')
    if form.errors:
        flash(u'删除失败！', 'danger')

    return redirect(url_for('admin.manage_articles', types_id=types_id, source_id=source_id,
                            page=request.args.get('page', 1, type=int)))


@admin.route('/manage-comments/disable/<int:id>')
@login_required
def disable_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    flash(u'屏蔽评论成功！', 'success')
    if request.args.get('disable_type') == 'admin':
        page = request.args.get('page', 1, type=int)
        return redirect(url_for('admin.manage_comments',
                                page=page))

    return redirect(url_for('main.articleDetails',
                            id=comment.article_id,
                            page=request.args.get('page', 1, type=int)))


@admin.route('/manage-comments/enable/<int:id>')
@login_required
def enable_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    flash(u'恢复显示评论成功！', 'success')
    if request.args.get('enable_type') == 'admin':
        page = request.args.get('page', 1, type=int)
        return redirect(url_for('admin.manage_comments',
                                page=page))

    return redirect(url_for('main.articleDetails',
                            id=comment.article_id,
                            page=request.args.get('page', 1, type=int)))


# 单条评论的删除，这里就不使用表单或者Ajax了，这与博文的管理不同，但后面多条评论的删除会使用Ajax
# 前面在admin页面删除单篇博文时使用表单而不是Ajax，其实使用Ajax效果会更好，当然这里只是尽可能
# 使用不同的技术，因为以后在做自动化运维开发时总有用得上的地方
@admin.route('/manage-comments/delete-comment/<int:id>')
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    article_id = comment.article_id
    db.session.delete(comment)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'删除评论失败！', 'danger')
    else:
        flash(u'删除评论成功！', 'success')
    if request.args.get('delete_type') == 'admin':
        page = request.args.get('page', 1, type=int)
        return redirect(url_for('admin.manage_comments',
                                page=page))

    return redirect(url_for('main.articleDetails',
                            id=article_id,
                            page=request.args.get('page', 1, type=int)))


@admin.route('/manage-comments', methods=['GET', 'POST'])
@login_required
def manage_comments():
    form = AdminCommentForm(follow=-1, article=-1)
    form2 = DeleteCommentsForm(commentIds=-1)

    if form.validate_on_submit():
        article = Article.query.get_or_404(int(form.article.data))
        comment = Comment(article=article,
                          content=form.content.data,
                          author_name=form.name.data,
                          author_email=form.email.data)
        db.session.add(comment)
        db.session.commit()

        followed = Comment.query.get_or_404(int(form.follow.data))
        f = Follow(follower=comment, followed=followed)
        comment.comment_type = 'reply'
        comment.reply_to = followed.author_name
        db.session.add(f)
        db.session.add(comment)
        db.session.commit()
        flash(u'提交评论成功！', 'success')
        return redirect(url_for('.manage_comments'))

    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('admin/manage_comments.html', User=User,
                           Comment=Comment, comments=comments,
                           pagination=pagination, page=page,
                           endpoint='.manage_comments', form=form, form2=form2)


@admin.route('/manage-comments/delete-comments', methods=['GET', 'POST'])
@login_required
def delete_comments():
    form2 = DeleteCommentsForm(commentIds=-1)

    if form2.validate_on_submit():
        commentIds = json.loads(form2.commentIds.data)
        count = 0
        for commentId in commentIds:
            comment = Comment.query.get_or_404(int(commentId))
            count += 1
            db.session.delete(comment)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败！', 'danger')
        else:
            flash(u'成功删除%s条评论！' % count , 'success')
    if form2.errors:
        flash(u'删除失败！', 'danger')

    page = request.args.get('page', 1, type=int)
    return redirect(url_for('.manage_comments', page=page))
