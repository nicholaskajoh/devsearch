from devsearch.models import *
import click


class PageRank():
    def __init__(self):
        self.MAX_ITERATIONS = app.config['PAGERANK_MAX_ITERATIONS']

    def rank(self):
        N = Page.objects.count()
        initial_pr = 1 / N
        Page.objects.update(pagerank=initial_pr)

        for iteration in range(1, self.MAX_ITERATIONS + 1):
            click.echo(click.style('ITERATION: %d' % iteration, fg='yellow'))
            pr_change_sum = 0

            for page in Page.objects:
                current_pagerank = page.pagerank
                new_pagerank = 0
                backlink_pages = Page.objects.filter(
                    links=PageLink.objects.filter(url=page.url).first()
                )
                for backlink_page in backlink_pages:
                    new_pagerank += (backlink_page.pagerank / len(backlink_page.links))
                damping_factor = 0.85
                new_pagerank = ((1 - damping_factor) / N) + (damping_factor * new_pagerank)
                page.update(pagerank=new_pagerank)

                pr_change = abs(new_pagerank - current_pagerank) / current_pagerank
                pr_change_sum += pr_change

                message = 'page: %s, backlinks: %s, current PR: %s, new PR: %s, PR change: %s'
                click.echo(message % (
                    page.url,
                    str(len(backlink_pages)),
                    str(current_pagerank),
                    str(new_pagerank),
                    str(pr_change),
                ))
            
            average_pr_change = pr_change_sum / N
            if average_pr_change < 0.0001:
                click.echo(click.style('Converged at iteration: %d' % iteration, fg='blue'))
                break
        
        click.echo(click.style('PageRank complete', fg='green'))