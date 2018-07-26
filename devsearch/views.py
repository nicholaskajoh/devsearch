from devsearch import app
from flask import render_template, request
from devsearch.models import *
import re
import math
import time


@app.route('/')
def index():
    return render_template('index.html', title='Google for devs')


@app.route('/search')
def search():
    start_time = time.time()

    # get autocomplete data
    autocomplete_data = [qo.q for qo in Query.objects.limit(250).order_by('-frequency')]

    q = request.args.get('q', default=None)
    p = int(request.args.get('p', default=1))
    pages = None
    pages_count = 0
    pagination_data = None

    if q != None and q.strip() != '':
        # search
        q = re.sub(' +', ' ', q)
        words = re.sub('(\'s|\'|\")', '', q.lower()).split()
        per_page = 15
        skip = (p - 1) * per_page
        pipeline = [
            {'$match': {'word': {'$in': words}}},
            {'$lookup': {
                'from': 'page',
                'localField': 'page',
                'foreignField': '_id',
                'as': 'page',
            }},
            {'$unwind': '$page'},
            {'$group': {
                '_id': '$page',
                'total_score': {'$sum': '$score'},
            }},
            {'$sort': {'total_score': -1}},

            {'$group': {
                '_id': None,
                'pages_count': {'$sum': 1},
                'pages': {'$push': '$$ROOT'},
            }},
            {'$project': {
                'pages_count': 1,
                'pages': {'$slice': ['$pages', skip, per_page]},
            }},
        ]
        result = list(Index.objects.aggregate(*pipeline))
        pages = [] if not result else result[0]['pages']
        pages_count = 0 if not result else result[0]['pages_count']

        # pagination
        last_page = math.ceil(pages_count / per_page)
        start_page = p - 2 if (p - 2) > 0 else 1
        end_page = p + 2 if (p + 2) < last_page else last_page
        pagination_data = {
            'start_page': start_page,
            'end_page': end_page,
            'last_page': last_page,
        }

        # save search query
        sq = q.lower().replace('"', '')
        if Query.objects(q=sq).count() == 0:
            Query(q=sq).save()
        else:
            query = Query.objects.get(q=sq)
            query.update(frequency=query.frequency + 1)

    exec_time = time.time() - start_time

    return render_template(
        'search.html',
        title='Search pages...',
        autocomplete_data=autocomplete_data,
        q=q,
        p=p,
        pages=pages,
        pages_count=pages_count,
        pagination_data=pagination_data,
        exec_time=exec_time,
    )