#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from stageconf import *

SITEURL = 'http://luftmensch.net'

ADDTHIS_PROFILE = 'luftmensch'
DISQUS_SITENAME = 'luftmensch'
GOOGLE_ANALYTICS = 'UA-40656153-1'

PLUGINS += ('sitemap', )

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
