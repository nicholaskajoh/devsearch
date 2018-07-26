from devsearch import app
from devsearch.spider import DSSpider
from scrapy.crawler import CrawlerProcess
from devsearch.indexer import Indexer
from devsearch.pagerank import PageRank
import click


@app.cli.command()
@click.option('--recrawl', default=False)
def crawl(recrawl):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'CLOSESPIDER_PAGECOUNT': app.config['CLOSESPIDER_PAGECOUNT'],
    })
    process.crawl(DSSpider, recrawl=recrawl)
    process.start()

@app.cli.command()
def index():
    indexer = Indexer()
    indexer.index()

@app.cli.command()
def idf():
    indexer = Indexer()
    indexer.idf()

@app.cli.command()
def tfidf():
    indexer = Indexer()
    indexer.tfidf()

@app.cli.command()
def score():
    indexer = Indexer()
    indexer.score()

@app.cli.command()
def rank():
    ranker = PageRank()
    ranker.rank()