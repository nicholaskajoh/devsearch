from devsearch.models import *
from devsearch.stopwords import STOP_WORDS
import click
import datetime


class Indexer():
    def __init__(self):
        self.INDEXER_PAGE_LIMIT = app.config['INDEXER_PAGE_LIMIT']

    def index(self):
        pages = Page.objects.limit(self.INDEXER_PAGE_LIMIT).order_by('last_indexed')
        for page in pages:
            content = page.content
            words = list(set(content.lower().split(' ')))
            for word in words:
                if word not in STOP_WORDS:
                    if Index.objects(word=word).count() == 0:
                        word = Index(word=word, pages=[page]).save()
                    else:
                        word = Index.objects.get(word=word)
                        word.update(add_to_set__pages=page)
            page.last_indexed = datetime.datetime.now()
            page.save()
            
            message = 'Page %s indexed, words: %d'
            click.echo(message % (click.style(page.url, fg='yellow'), len(words)))
    
        click.echo(click.style('Indexing complete', fg='green'))
