from devsearch import app
from flask import render_template, request
from devsearch.models import *
import re


@app.route('/')
def index():
    return render_template('index.html', title='Google for devs')


@app.route('/search')
def search():
    q = request.args.get('q', default=None)
    results = None
    if q != None and q.strip() != '':
        q = re.sub(' +', ' ', q)
        words = q.lower().split()
        pipeline = [
            {'$match': {'word': {'$in': words}}},
            {'$lookup': {
                'from': 'page',
                'localField': 'page',
                'foreignField': '_id',
                'as': 'page',
            }},
            {'$unwind': '$page'},
            {'$project': {
                'page': 1,
                'score': {
                    '$sum': [
                        {'$multiply': ['$page.pagerank', 0.3]},
                        {'$multiply': ['$tf', '$idf', 0.7]},
                    ],
                },
            }},
            {'$sort': {'score': -1}},
            {'$group': {'_id': None, 'pages': {'$addToSet': '$page'}}},
        ]
        result = list(Index.objects.aggregate(*pipeline))[0]
    
    return render_template(
        'search.html',
        title='Search pages...',
        q=q,
        pages=result['pages'],
    )