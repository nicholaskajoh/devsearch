import os
from flask import Flask
from dotenv import load_dotenv

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(APP_ROOT, '.env'))

app = Flask(__name__)

# configs
app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
if os.getenv('SPIDER_ALLOWED_DOMAINS'):
    SPIDER_ALLOWED_DOMAINS = os.getenv('SPIDER_ALLOWED_DOMAINS').split(',')
else:
    SPIDER_ALLOWED_DOMAINS = None
app.config['SPIDER_ALLOWED_DOMAINS'] = SPIDER_ALLOWED_DOMAINS
app.config['CLOSESPIDER_PAGECOUNT'] = os.getenv('CLOSESPIDER_PAGECOUNT')

import devsearch.models
import devsearch.views
import devsearch.commands