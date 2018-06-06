from devsearch import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2000), unique=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    links = db.relationship('PageLink', backref='page', lazy=True)
    pagerank = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), \
                           server_onupdate=db.func.now())

    def __repr__(self):
        return '<Page %s>' % self.url


class PageLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), \
                    nullable=False)
    link = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), \
                    server_onupdate=db.func.now())

    def __repr__(self):
        return '<PageLink %s>' % self.link


class CrawlLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    is_crawled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), \
                    server_onupdate=db.func.now())

    def __repr__(self):
        return '<CrawlLink %s>' % self.url


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.Text)
    search_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), \
                    server_onupdate=db.func.now())

    def __repr__(self):
        return '<Query %s>' % self.string