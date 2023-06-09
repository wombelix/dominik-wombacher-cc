.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Pagure unter FreeBSD in Jail mit Bastille - Teil 1
##################################################

:date: 2021-03-13
:modified: 2021-03-13
:tags: FreeBSD, Pagure, Git, Bastille, Port
:description: Pagure in Bastille Jail unter FreeBSD
:category: Unix
:slug: pagure-unter-freebsd-in-jail-mit-bastille-teil1
:author: Dominik Wombacher
:lang: de
:transid: pagure-on-freebsd-in-bastille-powered-jail-part1
:status: published

Vor ein paar Monaten habe ich angefangen mit `FreeBSD <https://www.freebsd.org>`_ und Jails, verwaltet 
von `Bastille <https://www.bastillebsd.org>`_, zu experimentieren.

Und ehrlich, ich liebe es, einfach, leichtgewichtig, es macht Spaß damit zu arbeiten, aber das ist eine 
andere Geschichte fuer zukuenftige Posts ;)

Viel wichtiger ist, dass ich anfangen wollte, meine Git Repositories selbst zu hosten und `Github <https://www.github.com>`_, 
`Gitlab <https://www.gitlab.com>`_, `Codeberg <https://www.codeberg.org>`_ und `Notabug <https://www.notabug.org>`_ 
primär als Mirror zu verwenden. Das sollte die Sichtbarkeit im Vergleich zum reinen Self-Hosting verbessern und helfen,  
potentielle Mitwirkende zu erreichen, unabhaengig von der Plattform.

Ich habe mich fuer `Pagure <https://pagure.io/pagure>`_ entschieden, es ist in Python geschrieben und scheint die 
einzige Loesung zu sein, die Pull Requests von entfernten Repositories unterstuetzt. 

Aber einfach nur die RPM Pakete auf einem unterstuetzten OS, wie openSUSE oder Fedora, zu installieren, waere zu einfach ;)

Dieses Projekt war daher der perfekte Kandidat, um noch etwas mehr Erfahrungen mit FreeBSD und Bastille zu sammeln.

Ich habe eine neues Jail erstellt, den Ports Tree von meinem FreeBSD Host gemountet und mich mit der neuen Instanz verbunden.

.. code-block::

	bastille create pagure 12.2-RELEASE 172.31.255.30 bastille0
	bastille mount pagure /usr/ports /usr/ports nullfs rw 0 0
	bastille console pagure

Basierend auf der `Pagure Dokumentation <https://docs.pagure.org/pagure/install.html>`_ und weiterer Recherche, 
habe ich folgende Pakete installiert:

.. code-block::

	pkg install git libgit2 python3-3_3 apache24-2.4.46 py37-pip-20.2.3 py37-wheel-0.30.0_1 wget py37-pillow-7.0.0 py37-Flask-1.1.2 vim-tiny

Der libgit2 Port war zu alt und aufgrund einiger weiterer Abhaengigkeiten, war ein offizielles Update noch nicht verfuegbar, 
so dass ich es selbst aktualisieren musste. Weitere Informationen: https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=252098

*/usr/ports/devel/libgit2/Makefile.patch*

.. code-block:: diff

	--- Makefile.orig       2021-03-10 23:58:49.921923000 +0100
	+++ Makefile    2021-03-11 00:13:22.452236000 +0100
	@@ -6,7 +6,7 @@
	 # Tools/scripts/search_lib_depends_and_bump.sh devel/libgit2
 
	 PORTNAME=      libgit2
	-PORTVERSION=   1.0.1
	+PORTVERSION=   1.1.0
	 CATEGORIES=    devel
	 MASTER_SITES=  https://github.com/libgit2/libgit2/releases/download/v${PORTVERSION}/
 
	@@ -37,7 +37,7 @@
	 .if ${SSL_DEFAULT} == base
	 post-patch:
	        @${REINPLACE_CMD} -e "/LIBGIT2_PC_REQUIRES.*openssl/ d" \
	-               ${WRKSRC}/cmake/Modules/SelectHTTPSBackend.cmake
	+               ${WRKSRC}/cmake/SelectHTTPSBackend.cmake
	 .endif
	 
	 do-test:

Patch applied, libgit2 compiled und installiert:

.. code-block::

	patch -u -b Makefile -i Makefile.patch
	make makesum
	make install clean

Pagure Release 5.13.2 erstellt und installiert

.. code-block::

	cd
	mkdir src
	cd src
	git clone https://pagure.io/pagure.git
	cd pagure
	git checkout -b 5.13.2 e1a8b5e4a2a347ab29de7cc21d9d2c89f55dd076

	python3 setup.py build
	python3 setup.py install

Ich habe ein kleines hilfs Script geschrieben, um die erforderlichen Ordnerstrukturen 
zu erstellen und die config Dateien an die richtige Stelle zu kopieren.

.. code-block::

	#!/bin/sh
	mkdir -p /usr/local/etc/pagure
	mkdir -p /usr/local/share/pagure

	cp pagure/files/pagure.cfg.sample /usr/local/etc/pagure/pagure.cfg
	cp pagure/files/alembic.ini /usr/local/etc/pagure/alembic.ini
	cp pagure/files/pagure-apache-httpd.conf /usr/local/etc/apache24/Includes/pagure.conf
	cp pagure/files/pagure.wsgi /usr/local/share/pagure/pagure.wsgi
	cp pagure/createdb.py /usr/local/share/pagure/pagure_createdb.py

	mkdir -p /usr/local/www/apache24/data/releases
	chown git:git /usr/local/www/apache24/data/releases

	mkdir -p /usr/local/git/repositories/{docs,forks,tickets,requests,remotes}

Dedizierten Git Benutzer und Gruppe erstellt, waere cool wenn das in einem Befehl gehen wuerde, 
aber das `wurde noch nicht implementiert <https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=172965>`_

.. code-block::

	pw group add -n git
	pw user add -n git -d /usr/local/git -c "Pagure Git User" -g git

Das ist alles, was ich bis jetzt habe, leider war nicht genug Zeit, um die Installation zu beenden.

Der naechste Schritt, basierend auf der Pagure Installationsanleitung, ist das Setzen von spezifischen ACLs, 
aber die Syntax zwischen Linux und FreeBSD unterscheidet sich, ich muss erst noch herausfinden, wie es anzupassen ist.

Außerdem sind wahrscheinlich noch weitere Aenderungen erforderlich, bis Pagure wie erwartet funktioniert und 
sich unter FreeBSD aehnlich verhaelt, wie auf einem Linux System.

Sobald ich etwas Zeit finde um weiterzumachen, werde ich Teil 2 veroeffentlichen.

