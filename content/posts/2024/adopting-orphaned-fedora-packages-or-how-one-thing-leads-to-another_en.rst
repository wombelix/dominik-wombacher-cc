.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Adopting orphaned Fedora packages or how one thing leads to another
###################################################################

:date: 2024-05-01
:modified: 2024-05-01
:tags: Fedora, Packaging, Packager
:description: Adopting one orphaned Fedora packaging can lead to many more
:category: Linux
:slug: adopting-orphaned-fedora-packages-or-how-one-thing-leads-to-another
:author: Dominik Wombacher
:lang: en
:transid: adopting-orphaned-fedora-packages-or-how-one-thing-leads-to-another
:status: published

Recently I started to become an active Fedora packager, which is
something I really enjoy. It happens, for various reasons, that a
package gets orphaned by its maintainer. Lack of time, changes in
upstream that make it hard to package a new version, or incompatibilities
and no updates. In such a case, packages can be adopted by other packagers.

I stumbled across `php-aws-sdk3 <https://src.fedoraproject.org/rpms/php-aws-sdk3>`_ and even though
I'm not actively using the SDK right now, I found it appealing to maintain this package.
Might be a good opportunity to understand PHP packaging for Fedora better and brush up my
old PHP knowledge a bit. And then I started to realize how fast one package can become many ;)

The magic word: Dependencies. Of course, php-aws-sdk3 depends on other packages. Some of them
are orphaned to. Some need and update to be compatible. Others don't exist yet in Fedora.
I ended up adopting three other packages and with ~14 new packages on my list :O

So it will take me some time to reach my goal, to keep php-aws-sdk3 alive.
But I will learn a lot on that journey and build some cool and valuable packages.
