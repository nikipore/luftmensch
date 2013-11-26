#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

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
BOOTSTRAP_THEME = 'luftmensch'

STATIC_PATHS = (
    'images',
    'code',
    'theme'
)

LINKS =  ()

MENUITEMS = (
    ('archives', '/archives.html'),
)

SOCIAL = (
    ('feed', 'rss', '/feeds/all.atom.xml'),
    ('github', 'github', 'https://github.com/nikipore')
)
TAG_CLOUD_MAX_ITEMS = 100
TAG_LIST_SEPARATOR = u''

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

DEFAULT_DATE_FORMAT = '%Y-%m-%d'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'

GITHUB_USER = ''
GITHUB_SKIP_FORK = False
GITHUB_REPO_COUNT = 10
GITHUB_SORT_ATTRIBUTE = 'stargazers_count'
GITHUB_SORT_DESCENDING = True

"""
plugins
"""
PLUGIN_PATH = '../pelican-plugins'
PLUGINS = ()

PLUGINS += (
    'liquid_tags.img', 'liquid_tags.video', 'liquid_tags.youtube'
    , 'liquid_tags.include_code', 'liquid_tags.notebook'
)

"""
format
"""
TYPOGRIFY = True

