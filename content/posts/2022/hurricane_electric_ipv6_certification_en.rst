Hurricane Electric IPv6 Certification - Sage level reached
##########################################################

:date: 2022-01-15
:modified: 2022-01-15
:tags: IPv6, Network, Administration, Certification
:description: Hurricane Electric IPv6 Certification
:category: Certification
:slug: hurricane_electric_ipv6_certification_sage_level_reached
:author: Dominik Wombacher
:lang: en
:transid: hurricane_electric_ipv6_certification_sage_level_reached
:status: published

IPv6 connectivity is quite important for me, fortunately IPv6 is a first class citizen for my ISP 
(Deutsche Glasfaser) and was also available with my previous one (1&1).
So I didn't have to use a Tunnel Broker at home yet to get IPv6 up and running but if I had to, 
I would go with Hurricane Eletric and their (free) `Tunnelbroker <https://www.tunnelbroker.net>`_ Service.

HE also offer a `IPv6 Certification <https://ipv6.he.net/certification/>`_, to test your theoretical 
as well as practical knowledge and verify that you are actually using IPv6 at home, your website, mail server and DNS.

There are seven Certification Level:

- NewB: Read the primer, be able to answer some quick and easy questions.

- Explorer: Verify that you can access an IPv6 website (ours!)

- Enthusiast: Verify that you have an IPv6 capable web server that we can connect to and fetch information from. This should be entered as a FQDN and not an IPv6 address.

- Administrator: Verify that you have a working IPv6 capable MTA by sending you an email only over IPv6.

- Professional: Verify that your MTA has working reverse DNS (ex: dig mx $domain +short ; dig aaaa $mx +short ; dig -x $mxAAAA +short)

- Guru: Verify that the authoritative NS for your domain have AAAA records, and respond to queries for the domain (ex: step 1 is dig ns $domain ; dig aaaa $ns | step 2 is dig aaaa $domain @$nsAAAA)

- Sage: Check to see if your domain's authoritative NS have IPv6 glue with their listed TLD servers. Meaning the TLD server can directly answer for the host record (ex: dig +trace ns $domain to get the TLD server list then dig aaaa $ns @TLD for the glue).

Source: https://forums.he.net/index.php?topic=304.0

They provide a lot of additional `learning material <https://ipv6.he.net/presentations.php>`_ 
and have a still quite active `community <https://forums.he.net/index.php?board=11.0>`_ as well. 

Sages also get a `Free IPv6 T-Shirt <https://forums.he.net/index.php?topic=922.0>`_ upon request, 
last batch run was *Fri Dec 10 2021*, so let's see when mine will arrive :)

Hint: Getting Sage Rank is a mandatory requirement to request HE to remove SMTP and IRC Port Filtering 
when using their IPv6 Tunnel, to avoid abuse those are blocked by default, see `FAQ <https://ipv6.he.net/certification/faq.php>`_.

It Was fun to work through the different level, test my knowledge and validate my IPv6 Setup. 
Due to the fact that all my Server already using IPv6, whenever possible IPv6-only, a few in Dual-Stack Mode,
I was able to reach the Sage Level quite fast, no re-configuration of my Services was required to pass all checks. 

Exception was enabling TLS v1.2 on my website, limit to v1.3 only was to strict for he.net 
to reach my Server and validate my Domain. Also disabling greylisting for sender ipv6@he.net 
was helpful to speed things up during verification of my mail setup.

.. raw:: html

  <img src="https://ipv6.he.net/certification/create_badge.php?pass_name=wombelix&amp;badge=3" style="border: 0; width: 229px; height: 137px" alt="IPv6 Certification Badge for wombelix"></img>

Certificate
***********

- Download

  - `Certificate </certificates/he.net_ipv6_certification_sage_level_dominik_wombacher.pdf>`_ (PDF, 1.2M)

