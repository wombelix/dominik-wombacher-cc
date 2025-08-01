.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Open Graph Support in my Pelican Theme
######################################

:date: 2025-08-01
:modified: 2025-08-01
:tags: Pelican, OpenGraph, Theme
:description: Adding Open Graph and meta tag support to improve social media sharing previews
:category: Code
:slug: open-graph-support-in-my-pelican-theme
:author: Dominik Wombacher
:lang: en
:transid: open-graph-support-in-my-pelican-theme
:status: published

When sharing blog articles on LinkedIn, I noticed they showed
:code:`The Wombelix Post` instead of the actual article titles.
After taking a closer look, it seems like social media platforms
prefer `Open Graph <https://ogp.me/>`_
(Archive: `[1] <https://web.archive.org/web/20250727115258/https://ogp.me/>`__,
`[2] <https://archive.today/2025.06.17-152831/https://ogp.me/>`__)
meta tags to generate previews.

I didn't implement these tags when I created my
`Pelican theme xlii <https://git.sr.ht/~wombelix/pelican-theme-xlii>`_
almost 5 years ago. Even though my HTML title contains the individual
page and article title as suffix, some platforms only seem to pick up
the overall page title and ignore them.

I added Open Graph tags now across all relevant template files using a
Jinja2 block-based pattern. The base template includes the Open Graph
namespace and default tags for the homepage. Article and page
templates override these with content-specific information like
title, URL, description, publication date, category, and author.

I also added HTML meta tags with author information and keywords
for tag and category pages.

Testing with
`LinkedIn's Post Inspector <https://www.linkedin.com/post-inspector/>`_
confirmed it works. The inspector now shows article titles,
descriptions, publication dates, and author information instead of
generic site data.

LinkedIn ignores the :code:`og:site_name` tag and displays the domain
name instead. This bothers me a bit since I'd prefer to have my site
name included, but I can't change how they interpret the tags. Other
platforms like Facebook and Mastodon should behave as expected when
they follow the Open Graph specification closer.
