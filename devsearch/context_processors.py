from devsearch import app
import re
import textwrap


@app.context_processor
def excerpt_processor():
    def get_excerpt(content, q):
        start = 0
        if re.search(q, content, re.IGNORECASE):
            try:
                start = content.lower().index(q.lower())
            except:
                pass
        return textwrap.shorten(content[start:], width=150, placeholder="...")

    return dict(get_excerpt=get_excerpt)