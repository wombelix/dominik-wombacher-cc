.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Sky Ticket TV Stick (Roku) failed to connect without Pi-hole whitelisting
#########################################################################

:date: 2021-10-10
:modified: 2021-10-10
:tags: Sky, Roku, Pi-hole
:description: Roku TV Stick requires Pi-hole whitelisting
:category: Misc
:slug: sky-ticket-tv-stick-roku-failed-to-connect-without-pihole-whitelisting
:author: Dominik Wombacher
:lang: en
:transid: sky-ticket-tv-stick-roku-failed-to-connect-without-pihole-whitelisting 
:status: published

I'm using Sky Ticket (Germany) from time to time and got one of their TV Sticks, powered by Roku, for free. 
Had to learn that Roku connects to a few Domains which are on blacklists used by Pi-hole and uBlock Origin.

Was surprised that I can use Sky Ticket directly from a (Windows...) Notebook, 
without adjusting anything on my Pi-hole settings, but it fails when using the Roku Stick.

Without adding :code:`scribe.logs.roku.com` and :code:`dpm.demdex.net` to the Pi-hole whitelist, 
it's impossible to connect to Sky Ticket, Roku complains always that *"something went wrong"*.

Both seem to receive a lot of usage data and track everything what's done on the UI. 
I think that's just weird and unnecessary, looks like something all Roku devices do.

Not really what I expect, paying for a Service and running in such issues, 
but if they happy to track how I navigate in the UI and decide what to watch, so it be...
