.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Pagure on FreeBSD in Bastille powered Jail - Part 1
###################################################

:date: 2021-03-13
:modified: 2021-03-13
:tags: FreeBSD, Pagure, Git, Bastille, Port
:description: Pagure within Bastille Jail on FreeBSD
:category: Unix
:slug: pagure-on-freebsd-in-bastille-powered-jail-part1
:author: Dominik Wombacher
:lang: en
:transid: pagure-on-freebsd-in-bastille-powered-jail-part1
:status: published

A few months ago I started experimenting with `FreeBSD <https://www.freebsd.org>`_ and 
Jails managed by `Bastille <https://www.bastillebsd.org>`_. 

And tbh, I love it, simple, lightweight, it's just fun to work with, but that's a 
different Story for future Posts ;)

More important, I wanted to start self-host my Git repositories and to use `Github <https://www.github.com>`_, 
`Gitlab <https://www.gitlab.com>`_, `Codeberg <https://www.codeberg.org>`_ and `Notabug <https://www.notabug.org>`_ 
primary as Mirror. That should improve the visibility, compared to only self-hosting and help to reach 
potential contributors, independent of the Platform.

So I decided to setup `Pagure <https://pagure.io/pagure>`_, it's written in Python and seem to be the 
only Solution, that support pull requests from remote repositories. 

But just installing the RPM Packages on a Supported OS like openSUSE or Fedora would be too easy ;)

This Project was therefore the perfect candidate, to get some more Hands on Experience with FreeBSD and Bastille.

I created a new Jail, mounted the Ports Tree from my FreeBSD Host and connected to the new Instance.

.. code-block::

	bastille create pagure 12.2-RELEASE 172.31.255.30 bastille0
	bastille mount pagure /usr/ports /usr/ports nullfs rw 0 0
	bastille console pagure

Based on the `Pagure Documentation <https://docs.pagure.org/pagure/install.html>`_ and some research, 
I installed the following packages:

.. code-block::

	pkg install git libgit2 python3-3_3 apache24-2.4.46 py37-pip-20.2.3 py37-wheel-0.30.0_1 wget py37-pillow-7.0.0 py37-Flask-1.1.2 vim-tiny

The available libgit2 Port was to old and due to some further dependencies, an official update wasn't 
available yet, so I had to update it on my own. Further reading: https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=252098

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

Patch applied, compiled and installed:

.. code-block::

	patch -u -b Makefile -i Makefile.patch
	make makesum
	make install clean

Pagure Release 5.13.2 build and installed

.. code-block::

	cd
	mkdir src
	cd src
	git clone https://pagure.io/pagure.git
	cd pagure
	git checkout -b 5.13.2 e1a8b5e4a2a347ab29de7cc21d9d2c89f55dd076

	python3 setup.py build
	python3 setup.py install

I wrote a little helper Script, to create some necessary folder structures and copy 
config files to the right location.

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

Dedicated Git User and Group created, would be cool in one single command, but 
that's `not yet implemented <https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=172965>`_

.. code-block::

	pw group add -n git
	pw user add -n git -d /usr/local/git -c "Pagure Git User" -g git

That's all I have so far, unfortunately there wasn't enough time to finish the Installation.

Next Step based on the Pagure Install Guide is to set specific ACLs, but the syntax between 
Linux and FreeBSD differ, first I have to figure out how to adapt them.

Also there might be further adjustments required until Pagure is working as expected and 
behave similar as on a Linux system.

As soon I find some time to proceed, I will publish Part 2.

