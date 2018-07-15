from devsearch import app
import re
import textwrap


@app.context_processor
def excerpt_processor():
    def get_excerpt(content, q):
        start = 0
        if re.search(q, content, re.IGNORECASE):
            start = content.lower().index(q.lower())
        return textwrap.shorten(content[start:], width=150, placeholder="...")

    return dict(get_excerpt=get_excerpt)