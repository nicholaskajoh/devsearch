# devsearch
Google for devs.

## Stack
- Flask (Python 3)
- Scrapy
- LXML
- MongoEngine (MongoDB)
- Bootstrap 4

## Setup
- Clone or download this repo
- Create and/or activate a virtual environment
- Run `pip install -e .`
- Create MongoDB database
- Create a *.env* file from *.env.example*
- Crawl the web with `flask crawl`
- Index pages using `flask index`
- Run `flask run`