from devsearch import app
from mongoengine import *
import datetime


connect(host=app.config['MONGODB_URI'])

class PageLink(Document):
    url = URLField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(PageLink, self).save(*args, **kwargs)


class Page(Document):
    url = URLField(required=True, unique=True)
    title = StringField(required=True)
    content = StringField()
    links = ListField(ReferenceField(PageLink))
    pagerank = FloatField()
    last_indexed = DateTimeField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(Page, self).save(*args, **kwargs)


class Index(Document):
    word = StringField(unique=True)
    pages = ListField(ReferenceField(Page))


class CrawlList(Document):
    url = URLField()
    is_crawled = BooleanField(default=False)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(CrawlList, self).save(*args, **kwargs)


class Query(Document):
    q = StringField()
    frequency = IntField(default=1)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(Query, self).save(*args, **kwargs)