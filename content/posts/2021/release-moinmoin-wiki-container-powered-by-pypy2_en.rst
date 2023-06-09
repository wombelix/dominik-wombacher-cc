Release: MoinMoin Wiki Container, powered by PyPy2
##################################################

:date: 2021-10-09
:modified: 2021-10-09
:tags: MoinMoin, Wiki, Container, PyPy, Python, openSUSE
:description: Ready to use Container to run MoinMoin Wiki
:category: Code
:slug: release-moinmoin-wiki-container-powered-by-pypy2
:author: Dominik Wombacher
:lang: de
:transid: release-moinmoin-wiki-container-powered-by-pypy2
:status: published

Today I published the first version of **moinmoin-pypy2-container**, 
a ready to use image to run MoinMoin Wiki, based on openSUSE Leap. 

It contains some enhancements regarding the intial wiki setup to make it 
easier to get started and already ships with a pre-configured nginx.

Latest stable release of `MoinMoin <https://moinmo.in>`_ 
was 8th November 2020 and requires Python 2, development of the successor 
`moin2 <https://github.com/moinwiki/moin>`_ is ongoing but wasn't released yet. 

**moin2** supports Python 3, but there is still a lot to do and the Project could use some 
`help <https://github.com/moinwiki/moin/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22>`_, 
what about a `good first issue <https://github.com/moinwiki/moin/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22>`_?

It might be that User still want to keep using the latest stable 
release and wait with the migration for a while.

Besides minor enhancements, the main goal of **moinmoin-pypy2-container** 
is to provide a easy to use alternative to keep using MoinMoin.

The official Python 2 Runtime is `End-of-Life <https://www.python.org/doc/sunset-python-2/>`_. 
But PyPy will support Python 2 `"forever" <https://doc.pypy.org/en/latest/faq.html#how-long-will-pypy-support-python2>`_ 
and still provide updates in future.

Please check the **README** in the below linked Source code Repository 
for further details about the *features* and *usage*.

The repository is available on 
`Codeberg <https://codeberg.org/wombelix/moinmoin-pypy2-container>`_ (Primary), 
`Gitlab <https://gitlab.com/wombelix/moinmoin-pypy2-container>`_ (Mirror), 
`Github <https://github.com/wombelix/moinmoin-pypy2-container>`_ (Mirror).

Pre-build Container Images can be downloaded from 
`quay.io <https://quay.io/repository/wombelix/moinmoin-pypy2?tab=info>`_.
