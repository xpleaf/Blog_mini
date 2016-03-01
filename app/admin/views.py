# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
import json
from flask import render_template, redirect, flash, \
    url_for, request, current_app, jsonify
from flask.ext.login import login_required
from . import admin
from ..models import ArticleType, Source, Article, article_types, \
    Comment, User, Follow, Menu, ArticleTypeSetting
from .forms import SubmitArticlesForm, ManageArticlesForm, DeleteArticleForm, \
    DeleteArticlesForm, AdminCommentForm, DeleteCommentsForm, AddArticleTypeForm, \
    EditArticleTypeForm, AddArticleTypeNavForm, EditArticleNavTypeForm
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
            flash(u'发表博文成功！', 'success')
            article_id = Article.query.filter_by(title=title).first().id
            return redirect(url_for('main.articleDetails', id=article_id))
    if form.errors:
        flash(u'发表博文失败', 'danger')

    return render_template('admin/submit_articles.html', form=form)


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
        articleType = ArticleType.query.get_or_404(int(form.types.data))
        article.articleType = articleType
        source = Source.query.get_or_404(int(form.source.data))
        article.source = source

        article.title = form.title.data
        article.content = form.content.data
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
    if form.errors:
        flash(u'提交评论失败！请查看填写有无错误。', 'danger')
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


@admin.route('/manage-articleTypes', methods=['GET', 'POST'])
@login_required
def manage_articleTypes():
    form = AddArticleTypeForm(menus=-1)
    form2= EditArticleTypeForm()

    menus = Menu.return_menus()
    return_setting_hide = ArticleTypeSetting.return_setting_hide()
    form.menus.choices = menus
    form.setting_hide.choices = return_setting_hide
    form2.menus.choices = menus
    form2.setting_hide.choices = return_setting_hide

    page = request.args.get('page', 1, type=int)
    # sub_type = request.args.get('type')

    if form.validate_on_submit():
        name = form.name.data
        articleType = ArticleType.query.filter_by(name=name).first()
        if articleType:
            flash(u'添加分类失败！该分类名称已经存在。', 'danger')
        else:
            introduction = form.introduction.data
            setting_hide = form.setting_hide.data
            menu = Menu.query.get(form.menus.data)
            if not menu:
               menu = None
            articleType = ArticleType(name=name, introduction=introduction, menu=menu,
                                      setting=ArticleTypeSetting(name=name))
            if setting_hide == 1:
                articleType.setting.hide = True
            if setting_hide == 2:
                articleType.setting.hide = False
            # Note: to check whether introduction or menu is existing or not,
            # just use if `articleType.introduction` or `if articleType.menu`.
            db.session.add(articleType)
            db.session.commit()
            flash(u'添加分类成功！', 'success')
        return redirect(url_for('.manage_articleTypes'))
    if form.errors:
        flash(u'添加分类失败！请查看填写有无错误。', 'danger')
        return redirect(url_for('.manage_articleTypes'))

    pagination = ArticleType.query.order_by(ArticleType.id.desc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    articleTypes = pagination.items
    return render_template('admin/manage_articleTypes.html', articleTypes=articleTypes,
                           pagination=pagination, endpoint='.manage_articleTypes',
                           form=form, form2=form2, page=page)
# 提示，添加分类的验证表单也写在了上面，建议可以分开来写，这里只是提供一种方法，前面的也是如此
# 虽然分开来写会多写一点代码，但这样的逻辑就更清晰了
# 另外需要注意的是，两个验证表单写在同一个view当中会出现问题，所以建议还是分开来写


@admin.route('/manage-articletypes/edit-articleType', methods=['POST'])
def edit_articleType():
    form2= EditArticleTypeForm()

    menus = Menu.return_menus()
    setting_hide = ArticleTypeSetting.return_setting_hide()
    form2.menus.choices = menus
    form2.setting_hide.choices = setting_hide

    page = request.args.get('page', 1, type=int)

    if form2.validate_on_submit():
        name = form2.name.data
        articleType_id = int(form2.articleType_id.data)
        articleType = ArticleType.query.get_or_404(articleType_id)
        setting_hide = form2.setting_hide.data

        if articleType.is_protected:
            if form2.name.data != articleType.name or \
                            form2.introduction.data != articleType.introduction:
                flash(u'您只能修改系统默认分类的属性和所属导航！', 'danger')
            else:
                menu = Menu.query.get(form2.menus.data)
                if not menu:
                    menu = None
                articleType.menu = menu
                if setting_hide == 1:
                    articleType.setting.hide = True
                if setting_hide == 2:
                    articleType.setting.hide = False
                db.session.add(articleType)
                db.session.commit()
                flash(u'修改系统默认分类成功！', 'success')
        elif ArticleType.query.filter_by(name=form2.name.data).first():
            if ArticleType.query.filter_by(name=form2.name.data).first().id != articleType_id:
                flash(u'修改分类失败！该分类名称已经存在。', 'danger')
        else:
            introduction = form2.introduction.data
            menu = Menu.query.get(form2.menus.data)
            if not menu:
               menu = None
            articleType = ArticleType.query.get_or_404(articleType_id)
            articleType.name = name
            articleType.introduction = introduction
            articleType.menu = menu
            if not articleType.setting:
                articleType.setting = ArticleTypeSetting(name=articleType.name)
            if setting_hide == 1:
                    articleType.setting.hide = True
            if setting_hide == 2:
                articleType.setting.hide = False

            db.session.add(articleType)
            db.session.commit()
            flash(u'修改分类成功！', 'success')
        return redirect(url_for('.manage_articleTypes', page=page))
    if form2.errors:
        flash(u'修改分类失败！请查看填写有无错误。', 'danger')
        return redirect(url_for('.manage_articleTypes', page=page))


@admin.route('/manage-articleTypes/delete-articleType/<int:id>')
@login_required
def delete_articleType(id):
    page = request.args.get('page', 1, type=int)

    articleType = ArticleType.query.get_or_404(id)
    if articleType.is_protected:
        flash(u'警告：您没有删除系统默认分类的权限！', 'danger')
        return redirect(url_for('admin.manage_articleTypes', page=page))
    count = 0
    systemType = ArticleTypeSetting.query.filter_by(protected=True).first().types.first()
    articleTypeSetting = ArticleTypeSetting.query.get(articleType.setting_id)
    for article in articleType.articles.all():
        count += 1
        article.articleType_id = systemType.id
        db.session.add(article)
        db.session.commit()
    if articleTypeSetting:
        db.session.delete(articleTypeSetting)
    db.session.delete(articleType)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'删除分类失败！', 'danger')
    else:
        flash(u'删除分类成功！同时将原来该分类的%s篇博文添加到<未分类>。' % count, 'success')
    return redirect(url_for('admin.manage_articleTypes', page=page))


@admin.route('/manage-articleTypes/get-articleType-info/<int:id>')
@login_required
def get_articleType_info(id):
    if request.is_xhr:
        articletype = ArticleType.query.get_or_404(id)
        if articletype.is_hide:
            setting_hide = 1
        else:
            setting_hide = 2
        return jsonify({
            'name': articletype.name,
            'setting_hide': setting_hide,
            'introduction': articletype.introduction,
            'menu': articletype.menu_id or -1
        })


@admin.route('/manage-articleTypes/nav', methods=['GET', 'POST'])
@login_required
def manage_articleTypes_nav():
    form = AddArticleTypeNavForm()
    form2 = EditArticleNavTypeForm()

    page = request.args.get('page', 1, type=int)

    if form.validate_on_submit():
        name = form.name.data
        menu = Menu.query.filter_by(name=name).first()
        if menu:
            flash(u'添加导航失败！该导航名称已经存在。', 'danger')

        else:
            menu = Menu(name=name)
            db.session.add(menu)
            db.session.commit()
            flash(u'添加导航成功！', 'success')
        return redirect(url_for('admin.manage_articleTypes_nav', page=page))

    pagination = Menu.query.paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False)
    menus = pagination.items
    return render_template('admin/manage_articleTypes_nav.html', menus=menus,
                           pagination=pagination, endpoint='.manage_articleTypes_nav',
                           page=page, form=form, form2=form2)


@admin.route('/manage-articleTypes/nav/edit-nav', methods=['GET', 'POST'])
@login_required
def edit_nav():
    form2 = EditArticleNavTypeForm()

    page = request.args.get('page', 1, type=int)

    if form2.validate_on_submit():
        name = form2.name.data
        nav_id = int(form2.nav_id.data)
        if Menu.query.filter_by(name=name).first():
            if Menu.query.filter_by(name=name).first().id != nav_id:
                flash(u'修改导航失败！该导航名称已经存在。', 'danger')
        else:
            nav = Menu.query.get_or_404(nav_id)
            nav.name = name
            db.session.add(nav)
            db.session.commit()
            flash(u'修改导航成功！', 'success')
        return redirect(url_for('admin.manage_articleTypes_nav', page=page))
    if form2.errors:
        flash(u'修改导航失败！请查看填写有无错误。', 'danger')
        return redirect(url_for('admin.manage_articleTypes_nav', page=page))


@admin.route('/manage-articleTypes/get-articleTypeNav-info/<int:id>')
@login_required
def get_articleTypeNav_info(id):
    if request.is_xhr:
        menu = Menu.query.get_or_404(id)
        return jsonify({
            'name': menu.name,
            'nav_id': menu.id,
        })
