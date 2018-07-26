# devsearch
A web search engine built with Python which uses TF-IDF and PageRank to sort search results.

## Stack
- Flask (Python 3)
- Scrapy
- LXML
- MongoEngine (MongoDB)
- Bootstrap 4

# Requirements
- Docker
- Docker Compose

## Setup
- Install Docker and Docker Compose.
- Clone or download this repo.
- Create a *.env* file from *.env.example*.
- Run `docker-compose up`.

## Crawling
- Update the `SPIDER_ALLOWED_DOMAINS` variable in *.env* with domains you want the spider to crawl.
- Add at least one url to the **crawl_list** collection (in MongoDB) for the spider to start with.
- Run `docker-compose run web flask crawl` to crawl new web pages.
- You can add the `--recrawl` option to update pages already crawled: `docker-compose run web flask crawl --recrawl True`.

## Indexing
- To index crawled pages, run `docker-compose run web flask index`.
- To compute TFIDF, run the following one after the other:
    - `docker-compose run web flask idf`
    - `docker-compose run web flask tfidf`
- To compute PageRank, run `docker-compose run web flask rank`.
- To compute page-word score, run `docker-compose run web flask score`.

## Deploy
- Create a *.env.secret* file from *.env.secret.example*.
- Run `docker-compose -f docker-compose.prod.yml up --build -d`.