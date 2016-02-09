#coding: utf-8
from datetime import datetime
from . import db


class ArticleType(db.Model):
    __tablename__ = 'articleTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    introduction = db.Column(db.String(128))
    articles = db.relationship('Article', backref='articleType', lazy='dynamic')

    @staticmethod
    def insert_articleTypes():
        article_types = {'Python': '记录Python的点点滴滴'.decode('utf8'),
                 'Linux': '我的Linux成长之路'.decode('utf8'),
                 '开源技术'.decode('utf8'): '感兴趣的开源技术，当然也有我自己的开源软件'.decode('utf8'),
                 '网络技术'.decode('utf8'): '大而全的网络技术，没有具体的方向'.decode('utf8'),
                 '思科网络技术'.decode('utf8'): '主要是思科的路由交换技术'.decode('utf8'),
                 'CCIE': '因为曾经CCIE这个名词对我有特殊的意义，所以特留一个板块'.decode('utf8'),
                 '学校那些事'.decode('utf8'): '小学 初中 高中 大学，总有一些刻骨铭心的事'.decode('utf8'),
                 '感情那些事'.decode('utf8'): '各种情感的交织'.decode('utf8'),
                 '不一样的自己'.decode('utf8'): '奋斗中的自己'.decode('utf8')}
        for t in article_types:
            article_type = ArticleType.query.filter_by(name=t).first()
            if article_type is None:
                article_type = ArticleType(name=t, introduction=article_types[t])
            db.session.add(article_type)
        db.session.commit()

    def __repr__(self):
        return '<Type %r>' % self.name


class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    articles = db.relationship('Article', backref='source', lazy='dynamic')

    @staticmethod
    def insert_sources():
        sources = ('原创'.decode('utf8'),
                   '转载'.decode('utf8'),
                   '翻译'.decode('utf8'))
        for s in sources:
            source = Source.query.filter_by(name=s).first()
            if source is None:
                source = Source(name=s)
            db.session.add(source)
        db.session.commit()

    def __repr__(self):
        return '<Source %r>' % self.name


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    creat_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    num_of_view = db.Column(db.Integer, default=0)
    comment_of_view = db.Column(db.Integer, default=0)
    articleType_id = db.Column(db.Integer, db.ForeignKey('articleTypes.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    def __repr__(self):
        return '<Article %r>' % self.title
