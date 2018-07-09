from devsearch.models import *
import click


class PageRank():
    def __init__(self):
        self.MAX_ITERATIONS = app.config['PAGERANK_MAX_ITERATIONS']

    def rank(self):
        for iteration in range(self.MAX_ITERATIONS):
            click.echo(click.style('ITERATION: %d' % iteration, fg='yellow'))

            change_sum = 0
            pages_count = Page.objects.count()

            for page in Page.objects:
                current_pagerank = page.pagerank
                new_pagerank = 1
                backlink_pages = Page.objects.filter(
                    links=PageLink.objects.filter(url=page.url).first()
                )
                for backlink_page in backlink_pages:
                    new_pagerank += (backlink_page.pagerank / len(backlink_page.links))
                page.update(pagerank=new_pagerank)

                change = abs(new_pagerank - current_pagerank) / current_pagerank
                change_sum += change

                message = 'page: %s, backlinks: %s, current PR: %s, new PR: %s, change: %s'
                click.echo(message % (
                    page.url,
                    str(len(backlink_pages)),
                    str(current_pagerank),
                    str(new_pagerank),
                    str(change),
                ))
            
            average_change = change_sum / pages_count
            if average_change < 0.0001:
                click.echo(click.style('Converged at iteration: %d' % iteration, fg='blue'))
                break
        
        click.echo(click.style('PageRank complete', fg='green'))