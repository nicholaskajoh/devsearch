from devsearch import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', title='Google for devs')


@app.route('/search')
def search():
    return render_template('search.html', title='Search results...')