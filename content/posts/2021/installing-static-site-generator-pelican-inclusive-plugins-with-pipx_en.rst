.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Installing static site generator Pelican inclusive Plugins with pipx
####################################################################

:date: 2021-09-25
:modified: 2021-09-25
:tags: Pelican, Python, pipx
:description: Use pipx to install Pelican
:category: Misc 
:slug: installing-static-site-generator-pelican-inclusive-plugins-with-pipx
:author: Dominik Wombacher
:lang: en
:transid: installing-static-site-generator-pelican-inclusive-plugins-with-pipx
:status: published

Quick one, after re-installing my Notebook, I had to configure lot of things again and I wasn't happy with my earlier Python venv setup. 

I was taking a deeper look into pipx and I think that's way easier to use. 
It just take care about a venv per package that I'm going to install, I don't have to take care about anything on my own.

I tried it and after learning about the *inject* feature, mentioned by 
`cs01 in a GitHub Issue <https://github.com/getpelican/pelican/issues/2554#issuecomment-485136726>`__
(Archive: `[1] <https://web.archive.org/web/20200920144105/https://github.com/getpelican/pelican/issues/2554>`__,
`[2] <https://archive.today/2021.09.28-125020/https://github.com/getpelican/pelican/issues/2554>`__) 
it was no problem to install Pelican including some Plugins via pipx:

.. code-block::

  pipx install pelican
  pipx inject pelican pelican-pdf
  pipx inject pelican markdown
  pipx inject pelican pelican-read-more


