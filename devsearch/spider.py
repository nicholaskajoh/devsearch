import scrapy
from scrapy.selector import Selector
from devsearch.models import *
import lxml
from lxml.html.clean import Cleaner
import re
from urllib.parse import urlparse


class DSSpider(scrapy.Spider):
    name = "ds_spider"

    def __init__(self):
        if app.config['SPIDER_ALLOWED_DOMAINS'] != None:
            self.allowed_domains = app.config['SPIDER_ALLOWED_DOMAINS']

        self.start_urls = []
        for link in CrawlList.objects(is_crawled=False):
            self.start_urls.append(link.url)

    def parse(self, response):
        selector = Selector(response)
        # get page title
        page_title = selector.xpath('//title/text()').extract()[0]
        # get page content
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        page_html = selector.xpath('//html').extract()[0]
        # remove js and css code
        page_html = cleaner.clean_html(page_html)
        # extract text
        html_doc = lxml.html.document_fromstring(page_html)
        page_content = " ".join(lxml.etree.XPath("//text()")(html_doc))
        # remove line breaks, tabs and extra spaces
        page_content = re.sub('\n', ' ', page_content)
        page_content = re.sub('\r', ' ', page_content)
        page_content = re.sub('\t', ' ', page_content)
        page_content = re.sub(' +', ' ', page_content)
        page_content = page_content.strip()
        # get page links
        page_hrefs = response.xpath('//a/@href').extract()
        page_urls = []
        # filter out links with unallowed domains
        for link in page_hrefs:
            # convert relative links to absolute urls
            url = response.urljoin(link)
            # extract domain from url
            parsed_url = urlparse(url)
            url_domain = parsed_url.netloc
            if url_domain in self.allowed_domains:
                page_urls.append(url)
        # log out some info
        self.log('Page: %s (%s)' % (response.url, page_title))

        # save the page
        if Page.objects(url=response.url).count() == 0:
            page = Page(url=response.url, title=page_title, content=page_content).save()
            for url in page_urls:
                page.update(add_to_set__links=PageLink(url=url).save())
                # add url to crawl list
                if CrawlList.objects(url=url).count() == 0:
                    CrawlList(url=url).save()
            # update crawl list for current page
            CrawlList.objects(url=response.url).update(is_crawled=True)

        # crawl page urls
        for url in page_urls:
            yield scrapy.Request(url, callback=self.parse)