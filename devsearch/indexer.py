from devsearch.models import *
import click
import datetime
from collections import Counter
import math
import re


class Indexer():
    def __init__(self):
        self.PAGE_LIMIT = app.config['INDEXER_PAGE_LIMIT']

    def index(self):
        pages = Page.objects.limit(self.PAGE_LIMIT).order_by('last_indexed')
        for page in pages:
            content = re.sub(r'[^a-zA-Z0-9_\-\' ]+', '', page.content)
            content_list = content.lower().split(' ')
            content_word_count = len(content_list)
            words = Counter(content_list)
            for word, count in words.items():
                tf = count / content_word_count
                if Index.objects(page=page, word=word).count() == 0:
                    word = Index(page=page, word=word, tf=tf).save()
                else:
                    word = Index.objects.get(page=page, word=word)
                    word.update(tf=tf)
            page.last_indexed = datetime.datetime.now()
            page.save()
            
            message = 'Page %s indexed, words: %d'
            click.echo(message % (click.style(page.url, fg='yellow'), len(words)))
    
        click.echo(click.style('Indexing complete', fg='green'))

    def idf(self):
        words = Index.objects.order_by('last_idfed').distinct(field='word')
        pages_count = Page.objects.count()
        for word in words:
            word_frequency = Index.objects(word=word).count()
            idf = math.log10(pages_count / word_frequency)
            Index.objects(word=word).update(idf=idf, last_idfed=datetime.datetime.now())

            message = 'word: %s, idf: %s'
            click.echo(message % (word, click.style(str(idf), fg='green')))

        click.echo(click.style('IDF computations complete', fg='green'))

    def tfidf(self):
        index = Index.objects.order_by('last_tfidfed')
        for index_record in index:
            tfidf = index_record.tf * index_record.idf
            index_record.update(tfidf=tfidf, last_tfidfed=datetime.datetime.now())

            message = 'word: %s, tfidf: %s'
            click.echo(message % (index_record.word, click.style(str(tfidf), fg='green')))
        
        click.echo(click.style('TFIDF computations complete', fg='green'))

    def score(self):
        index = Index.objects.order_by('last_scored')
        max_tfidf = Index.objects.order_by("-tfidf").limit(1).first().tfidf
        max_pagerank = Page.objects.order_by("-pagerank").limit(1).first().pagerank
        for index_record in index:
            # tfidf = 70%, pagerank = 30%
            tfidf_score = (index_record.tfidf / max_tfidf) * 0.7 if max_tfidf > 0 else 0.7
            pagerank_score = (index_record.page.pagerank / max_pagerank) * 0.3 if max_pagerank > 0 else 0.3
            score = tfidf_score + pagerank_score
            index_record.update(score=score, last_scored=datetime.datetime.now())

            message = 'word: %s, score: %s'
            click.echo(message % (index_record.word, click.style(str(score), fg='green')))
        
        click.echo(click.style('Score computations complete', fg='green'))