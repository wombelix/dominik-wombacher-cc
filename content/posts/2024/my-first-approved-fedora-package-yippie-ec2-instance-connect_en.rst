.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

My first approved Fedora Package, yippie! ec2-instance-connect
##############################################################

:date: 2024-05-19
:modified: 2024-05-19
:tags: AWS, Fedora, EPEL, Packages, Packaging
:description: The first Fedora package I created was approved and published! ec2-instance-connect
:category: Linux
:slug: my-first-approved-fedora-package-yippie-ec2-instance-connect
:author: Dominik Wombacher
:lang: en
:transid: my-first-approved-fedora-package-yippie-ec2-instance-connect
:status: published

A while ago I was asked if I want to package **ec2-instance-connect** for Fedora and eventually EPEL.
More specific *"with Packit"*, which did send me down a weird path as I explain
in more detail in `Fedoda dist-git packit onboarding <{filename}/posts/2024/fedora-dist-git-packit-onboarding_en.rst>`.
After learning what Packit can and can't do for me, I started to make good progress ;)

I spend quite some time to learn about Fedora Packaging. The does and don't when
writing spec files. How package testing, reviewing and publishing works.
More about this in a later Blog, now I focus on my first approved package.

I was lucky that my Reviewer was Neal Gompa. People describe Neal with *"he is just everywhere"*.
And that's true in the most positive way. It's nearly impossible to be active in
the open source world without crossing paths :) He has a lot of experience and is a great mentor.
Receiving feedback from him is always a great opportunity to learn.

First I thought `ec2-instance-connect <https://github.com/aws/aws-ec2-instance-connect-config>`_
will be an easy package, great for the first one. Technically it's just a handful of
files and a systemd unit. How hard can that be? Spoiler: Very hard.

The challenge is the way how ec2-instance-connect works.
It adjusts the authcommand from sshd so that, by default, all authentication attempts go through it.
This is fine for brand new systems but becomes a problem when you deploy
on existing systems with a already customized config. Or if someone wants to apply
a custom config after the initial deployment and ec2-instance-connect installation.

So there are a lot of ways to break ssh login to the system which is discussed on
`GitHub <https://github.com/aws/aws-ec2-instance-connect-config/issues/19>`_.
But keeping this fact aside, there is obviously demand for a
`Fedora and EPEL package <https://github.com/aws/aws-ec2-instance-connect-config/issues/49>`_.
So I was encouraged to improve the user experience and make it available :)

Upstream has a `generic spec file <https://github.com/aws/aws-ec2-instance-connect-config/blob/master/rpmsrc/SPECS/generic.spec>`_
so this became my starting point. But I had to learn quickly that shell snippets
and nested if/else statements are not what is expected from a high quality spec
file in Fedora. So I had to find a way to replace the pretty unique logic that
was implemented with rpm macros and in a way that aligns with Fedora packaging
guidelines. The result is a good compromise, not perfect but it gives users
flexibility and reduces the risk of problems.

So after a couple iterations and very valuable feedback from Neal, he approved
my request and I was good to bring my first package into Fedora :)
If you are interested in the details, feel free to take a look at
the `Fedora Review Request <https://bugzilla.redhat.com/show_bug.cgi?id=2274150>`_ ticket.

In the meantime the package is available in all Fedora and EPEL repositories. It
is also on it's way to be pre-installed in Fedora Cloud images in future :D

It was an awesome experience and I can't wait to work on more packages!
