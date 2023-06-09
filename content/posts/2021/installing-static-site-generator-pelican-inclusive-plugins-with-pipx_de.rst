.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Installation des statischen Seiten generators Pelican inklusive Plugins via pipx
################################################################################

:date: 2021-09-25
:modified: 2021-09-25
:tags: Pelican, Python, pipx
:description: Verwende pipx zur Installation von Pelican
:category: Misc 
:slug: installation-des-statischen-seiten-generators-pelican-inklusive-plugins-via-pipx
:author: Dominik Wombacher
:lang: de
:transid: installing-static-site-generator-pelican-inclusive-plugins-with-pipx
:status: published

Nach der Neuinstallation meines Notebooks musste ich eine Menge Dinge neu konfigurieren und war mit meinem frueheren Python venv Setup nicht zufrieden.

Ich habe mir pipx genauer angesehen und ich denke, dass es viel einfacher zu benutzen ist. 
Es kuemmert sich selbst um ein venv pro Paket, das ich installieren will, ich muss mich um nichts mehr selbst kuemmern.

Ich habe es ausprobiert und nachdem `cs01 in einem GitHub Issue <https://github.com/getpelican/pelican/issues/2554#issuecomment-485136726>`__
(Archive: `[1] <https://web.archive.org/web/20200920144105/https://github.com/getpelican/pelican/issues/2554>`__,
`[2] <https://archive.today/2021.09.28-125020/https://github.com/getpelican/pelican/issues/2554>`__) 
von der `inject` Funktion gesprochen hatte, war es kein Problem Pelican inklusive einiger Plugins mit `pipx` zu installieren:

.. code-block::

  pipx install pelican
  pipx inject pelican pelican-pdf
  pipx inject pelican markdown
  pipx inject pelican pelican-read-more
