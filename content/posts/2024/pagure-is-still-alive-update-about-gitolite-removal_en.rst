.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Pagure is still alive! Update about the gitolite backend removal
################################################################

:date: 2024-04-30
:modified: 2024-04-30
:tags: Pagure, Contribution
:description: Pagure is still alive, I'm contributing and there will be a new release soon.
:category: Code
:slug: pagure-is-still-alive-update-about-gitolite-removal
:author: Dominik Wombacher
:lang: en
:transid: pagure-is-still-alive-update-about-gitolite-removal
:status: published

Yes pagure is alive, yes I'm still contributing, yes there will be a new release soon ;)
I didn't have the time to contribute as I wished for, but whenever possible I contributed.
So recently I fixed again the unit tests, updated dependencies, got rid of some tech depts.

Now it was time to tackle on of the larger clean up activities in the project Backlog.
The removal of the gitolite authentication backend. It wasn't really working
and in use anymore. The pagure auth backend is supposed to be the new standard.

So I went hunting to identify all the gitolite related code.
I learned that there was this concept of a static and dynamic backend.
Static is basically gitolite, you have to trigger the re-build of ACLs whenever
you change something on a repo. Dynamic is for example the pagure backend.
Everything is in the Database and becomes active right away.

It was fun to reverse engineer how it was implemented back then.
To identify the relevant parts, remove them, rewrite a couple functions and
get the unit tests back to green. When I started there were so many failing tests,
I thought I will never fix that again :D

A couple of days later I finished that monster PR and we merged it fairly quickly.
Otherwise merge conflicts with even minor changes would be likely.

How I did, if I missed a part or broke functionality that wasn't discovered by the
tests will the next major release 6.0 tell.

If you want all the details, check out to
`PR #5469 Remove gitolite support <https://pagure.io/pagure/pull-request/5469>`__
(Archive: `[1] <https://web.archive.org/web/20240717123151/https://pagure.io/pagure/pull-request/5469>`__,
`[2] <https://archive.today/2024.07.17-123146/https://pagure.io/pagure/pull-request/5469>`__)
