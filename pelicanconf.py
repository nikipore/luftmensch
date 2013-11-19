#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jan Müller'
SITENAME = u'luft·mensch'
SITESUBTITLE = u'One more concerned with intellectual pursuits than practical matters.'
SITEURL = ''

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

THEME = 'pelican-bootstrap3'
BOOTSTRAP_THEME = 'cosmo'

LINKS =  ()

SOCIAL = (
    ('github', 'https://github.com/nikipore'),
)
TAG_CLOUD_MAX_ITEMS = 15

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

DEFAULT_DATE_FORMAT = '%Y-%m-%d'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'

GITHUB_USER = 'nikipore'
GITHUB_SKIP_FORK = False

STATIC_PATHS = (
    'images',
    'code'
)

"""
plugins
"""
PLUGIN_PATH = '../pelican-plugins'
PLUGINS = ()

PLUGINS += (
    'liquid_tags.img', 'liquid_tags.video', 'liquid_tags.youtube'
    , 'liquid_tags.include_code', 'liquid_tags.notebook'
)
CODE_DIR = 'code'

"""
format
"""
TYPOGRIFY = True

