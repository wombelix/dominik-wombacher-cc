.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Giving up on Pagure - Almost 3 years of trying to keep it alive
###############################################################

:date: 2025-06-15
:modified: 2025-06-15
:tags: Pagure, OpenSource, Fedora
:description: After almost 3 years of maintaining Pagure, I give up ...
:category: Code
:slug: giving-up-on-pagure-almost-3-years-of-trying
:author: Dominik Wombacher
:lang: en
:transid: giving-up-on-pagure-almost-3-years-of-trying
:status: published

After almost 3 years of investing countless hours of my free time
in the attempt to keep Pagure alive, I give up. I can't motivate
myself anymore to continue and I simply don't have the time anymore
between my job, family life and all the other responsibilities people have.

It all started in January 2023 when I wrote to the pagure-devel
mailing list
`"Putting the Band back together - Road to Pagure v6.0" <https://lists.fedoraproject.org/archives/list/pagure-devel@lists.pagure.io/thread/XG4JQ7CUQCUKPE4QOZE5UGBJVRQXIRBY/>`__
(Archive: `[1] <https://web.archive.org/web/20250618080911/https://lists.fedoraproject.org/archives/list/pagure-devel@lists.pagure.io/thread/XG4JQ7CUQCUKPE4QOZE5UGBJVRQXIRBY/>`__,
`[2] <https://archive.today/2025.07.24-215702/https://lists.fedoraproject.org/archives/list/pagure-devel@lists.pagure.io/thread/XG4JQ7CUQCUKPE4QOZE5UGBJVRQXIRBY/>`__).
Pagure had been essentially abandoned since release 5.13.3 in 2021,
with over 600 open issues and 20 pull requests piling up. My attempt
to re-activate a community around it was unheard and failed, there
wasn't much of a user base outside Fedora left already.

I believed strongly that we needed Pagure as a true Open Source git
forge with a lightweight, extensible and well-designed codebase. So I
tried to bring all Pagure enthusiasts back together, clean up the
backlog, and work toward a major v6.0 release.

Over the following years, I fixed bugs, updated dependencies, got rid
of some tech debt, addressed three critical CVEs that emerged, worked
on the gitolite backend removal, and so much more I can't even remember anymore...
Eventually I managed to cut a
`new release in May 2024 <https://lists.fedoraproject.org/archives/list/pagure-devel@lists.pagure.io/thread/PEAFLHPOQXJPGVMWWSDUPH4BOKGHXLLY/>`__
(Archive: `[1] <https://web.archive.org/web/20250618080900/https://lists.fedoraproject.org/archives/list/pagure-devel@lists.pagure.io/thread/PEAFLHPOQXJPGVMWWSDUPH4BOKGHXLLY/>`__,
`[2] <https://archive.today/2025.07.24-215910/https://lists.fedoraproject.org/archives/list/pagure-devel@lists.pagure.io/thread/PEAFLHPOQXJPGVMWWSDUPH4BOKGHXLLY/>`__).

The work was sometimes really fun and educational. Going deep down the
rabbit hole to troubleshoot and fix problems, learning how everything
fit together, reverse engineering how things were implemented back
then. But it also became extremely frustrating at some point and the
opposite of fun and enjoyable.

The harsh truth is that Pagure's codebase is years old and honestly,
even though I've tried, it is basically all duct tape and chicken
wire after years of accumulated technical debt. Being most of the time on my own,
I started to question why I'm doing all this.

With the Fedora project investing since years in moving away from
Pagure instead of supporting it, the writing was on the wall. The
`git forge evaluation in April 2024 <https://communityblog.fedoraproject.org/2024-git-forge-evaluation/>`__
(Archive: `[1] <https://web.archive.org/web/20250612165209/https://communityblog.fedoraproject.org/2024-git-forge-evaluation/>`__,
`[2] <https://archive.today/2025.02.18-215148/https://communityblog.fedoraproject.org/2024-git-forge-evaluation/>`__)
made it clear that Pagure was no longer considered viable for Fedora's
future. The decision came in
`December 2024 when Fedora chose Forgejo <https://communityblog.fedoraproject.org/fedora-chooses-forgejo/>`__
(Archive: `[1] <https://web.archive.org/web/20241225090747/https://communityblog.fedoraproject.org/fedora-chooses-forgejo/>`__,
`[2] <https://archive.today/2025.02.18-213057/https://communityblog.fedoraproject.org/fedora-chooses-forgejo/>`__).

Since
`May 2025 <https://lists.fedoraproject.org/archives/list/devel-announce@lists.fedoraproject.org/message/DFKSOLS365SZIYN57QFNQMNXXPNUTZAJ/>`__
(Archive: `[1] <https://web.archive.org/web/20250612163448/https://lists.fedoraproject.org/archives/list/devel-announce@lists.fedoraproject.org/message/DFKSOLS365SZIYN57QFNQMNXXPNUTZAJ/>`__,
`[2] <https://archive.today/2025.07.24-220419/https://lists.fedoraproject.org/archives/list/devel-announce@lists.fedoraproject.org/message/DFKSOLS365SZIYN57QFNQMNXXPNUTZAJ/>`__),
even the creation of new projects on pagure.io is disabled and it is
just in keep the lights on mode without any future.

With Fedora's clear direction toward Forgejo and the platform
essentially in maintenance-only mode, I just couldn't motivate myself
anymore. The combination of a legacy codebase, lack of community
engagement, Fedora's move away from the platform, the enormous time
investment required, and three critical security vulnerabilities in
the past year made it clear that continuing would be unproductive.

Despite all the frustrations, I don't regret the journey. It was
sometimes educational and I learned a lot about maintaining legacy
open source projects and the importance of community. I'm grateful for
the experience and the few community members who did engage and
support the effort.

Sometimes projects have their time, and that time comes to an end.
I guess the future of git forges lies with more modern solutions
like Forgejo.

Thank you to everyone who supported Pagure over the years. It was a
good run, but all good things must come to an end.

I'm curious what Open Source project is going to draw my attention next.
