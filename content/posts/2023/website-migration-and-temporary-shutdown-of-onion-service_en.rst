.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Website migration and temporary shutdown of onion service
#########################################################

:date: 2023-07-02
:modified: 2023-07-02
:tags: Migration, Onion
:description: Migration and temporary shutdown of tor onion service
:category: Misc
:slug: website-migration-and-temporary-shutdown-of-onion-service
:author: Dominik Wombacher
:lang: en
:transid: website-migration-and-temporary-shutdown-of-onion-service 
:status: published

Since a few years, this website was running on a VPS, together with some other 
side projects and my mailboxes. I like self-hosting but don't have always the time for it 
and to take care about things right away. 

That's why I decided to move some components that I just want to work, like this website 
or my email, to hosted services from `Hetzner <https://www.hetzner.com>`_ (web) 
and `Mailbox.org <https://www.mailbox.org>`_ (mail).

For obvious reasons, a regular shared webhosting doesn't support Tor, so 
I will temporary shutdown the 
`onion service <{filename}/posts/2022/now_available_as_onion_service_through_the_tor_network_en.rst>`_ 
which will impact the reachability of this blog via 
:code:`http://2xwpdwnzmag3ewobwsdewpor4gmca4d5gltviol3u6upihb6m6m6xaad.onion/` 
until I setup the onion part on new virtual machine.

