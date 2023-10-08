#!/usr/bin/env python

# SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
#
# SPDX-License-Identifier: CC0-1.0

# -*- coding: utf-8 -*- #

AUTHOR = 'Dominik Wombacher'
SITENAME = 'The Wombelix Post'
SITEURL = ''

PATH = 'content'
TIMEZONE = 'Europe/Berlin'
DEFAULT_LANG = 'en'

DEFAULT_METADATA = {
    'status': 'draft',
}
MENUITEMS = (('Home', '/index.html'),
             ('Posts', '/posts/index.html'),
             ('Notes', '/pages/notes.html'),
             ('Code', '/~git/'),
             ('Contact', '/pages/contact.html'),
             ('Resume', '/pages/resume.html'),)
LINKS = (('Privacy', '/pages/privacy.html'),
         ('Acknowledgements', '/pages/acknowledgements.html'),
         ('RSS', '/feeds'),
         ('Tags', '/tags.html'),)
PAGE_PATHS = ['pages', 'redirects', 'notes', 'projects']
ARTICLE_PATHS = ['posts']
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'Misc'
STATIC_PATHS = [
    'extra/favicon.ico',
    'extra/robots.txt',
    'extra/feeds.htaccess',
    'extra/root.htaccess',
    'certificates',
    'images'
    ]
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/feeds.htaccess': {'path': 'feeds/.htaccess'},
    'extra/root.htaccess': {'path': '.htaccess'},
    }
RSS_FEED_SUMMARY_ONLY = True
CATEGORY_FEED_ATOM = 'feeds/category_{slug}.atom.xml'
CATEGORY_FEED_RSS = 'feeds/category_{slug}.rss.xml'
TAG_FEED_ATOM = 'feeds/tag_{slug}.atom.xml'
TAG_FEED_RSS = 'feeds/tag_{slug}.rss.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ATOM = 'feeds/atom.xml'
FEED_RSS = 'feeds/rss.xml'
TRANSLATION_FEED_ATOM = 'feeds/{lang}.atom.xml'
TRANSLATION_FEED_RSS = 'feeds/{lang}.rss.xml'
ARTICLE_SAVE_AS = 'posts/{slug}.html'
ARTICLE_URL = 'posts/{slug}.html'
ARTICLE_LANG_SAVE_AS = 'posts/{slug}.html'
ARTICLE_LANG_URL = 'posts/{slug}.html'
DRAFT_LANG_SAVE_AS = 'drafts/{slug}.html'
DRAFT_LANG_URL = 'drafts/{slug}.html'
DRAFT_PAGE_LANG_SAVE_AS = 'drafts/pages/{slug}.html'
DRAFT_PAGE_LANG_URL = 'drafts/pages/{slug}.html'
PAGE_LANG_SAVE_AS = 'pages/{slug}.html'
PAGE_LANG_URL = 'pages/{slug}.html'
ARTICLE_TRANSLATION_ID = 'transid'
PAGE_TRANSLATION_ID = 'transid'
AUTHOR_SAVE_AS = 'authors/{slug}.html'
AUTHOR_URL = 'authors/{slug}.html'
AUTHORS_SAVE_AS = 'authors/index.html'
AUTHORS_URL = 'authors/'
ARCHIVES_URL = 'posts'
ARCHIVES_SAVE_AS = 'posts/index.html'
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'
DAY_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/index.html'
SOCIAL = ''
OUTPUT_SOURCES = True
OUTPUT_SOURCES_EXTENSION = '.rst'
DELETE_OUTPUT_DIRECTORY = True
THEME = 'theme/xlii'
WITH_FUTURE_DATES = False
FEED_DOMAIN = SITEURL
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = False
DEFAULT_PAGINATION = 10
CATEGORIES_SAVE_AS = 'category/index.html'
CATEGORIES_URL = 'category/'
CATEGORY_URL = 'category/{slug}.html'
CATEGORY_SAVE_AS = 'category/{slug}.html'
TAGS_SAVE_AS = 'tags.html'
TAGS_URL = 'tags.html'
SUMMARY_MAX_LENGTH = 30
SUMMARY_END_SUFFIX = ' ... '
READ_MORE_LINK = ' [read more]'
READ_MORE_LINK_FORMAT = '<a class="read-more" href="/{url}">{text}</a>'
CSS_FILE = 'base.css'
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 1,
        "indexes": 0.5,
        "pages": 1
    },
    "changefreqs": {
        "articles": "daily",
        "indexes": "daily",
        "pages": "weekly"
    },
    "exclude": ["drafts/", "tag/", "category/", "authors/"]
}

# https://bernhard.scheirle.de/posts/2016/August/17/pelican-improved-display-of-translations/
language_lookup = {
    'en': 'English',
    'de': 'Deutsch',
}

def lookup_lang_name(lang_code):
    return language_lookup[lang_code]

from datetime import datetime
def filter_strptime(datestring, formatin, formatout):
    return datetime.strftime(datetime.strptime(datestring, formatin), formatout)

JINJA_FILTERS = {
    'lookup_lang_name': lookup_lang_name,
    'strptime': filter_strptime,
}
