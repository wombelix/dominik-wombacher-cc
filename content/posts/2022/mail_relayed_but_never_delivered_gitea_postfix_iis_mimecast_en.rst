.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Mail relayed but never delivered?! Gitea > Postfix > IIS > Mimecast
###################################################################

:date: 2022-03-07
:modified: 2022-03-07
:tags: mail, relay, postfix, iis, mimecast, gitea
:description: How Mails from Gitea silently got lost during relaying
:category: Linux
:slug: mail_relayed_but_never_delivered_gitea_postfix_iis_mimecast
:author: Dominik Wombacher
:lang: en
:transid: mail_relayed_but_never_delivered_gitea_postfix_iis_mimecast 
:status: published

You can learn something new every day, for example how mails just got lost during relaying through mulitple smtp server without noticing. 

At work we running a simple Postfix mail relay in a management environment so various services can send notifications through the regular company mail infrastructure. 
No big deal actually, it's running since years without much hassle. 

Some time ago I was wondering why our internal Gitea Instance wasn't sending Emails and thought we just forgot to configure the smtp server. 
But everything was in place, testmails where accepted by postfix, successfully send to the configured relayhost, but never arrived in my Inbox. 

So no chance to further troubleshoot it without some insights and logs from the mail server after the relayhost postfix is using. 
A colleague from Group IT did some analysis and came back with some useful but surprising information.

I learned that the Mailflow is: Gitea > Postfix > IIS > IIS > Mimecast. Also that the second IIS 6.0 SMTP Service accepted my Mails but couldn't deliver them to the Mimecast SMTP.

.. code-block::

  smtp;554 5.6.1 Body type not supported by Remote Host

He also mentioned *7bit* and *8bit* MIME and that there are either unsupported characters used in the mail or the encoding is not supported.

First thought: WTF?! Second: OK, never saw something like that before, let's take a look and figure out whats going on.

An early RFC defined 7bit encoding for SMTP, 8bit support was added at a later point and there are two related configuration 
parameter available in postfix :code:`disable_mime_output_conversion` (default: *no*) and :code:`smtpd_discard_ehlo_keywords` (default: not set).

It looks like that by default IIS 6.0 SMTP Services advertise *8BITMIME* and allow such messages to be relayed. 
If Postfix receives a Mail in 8bit and the relayhost provides the keyword *8BITMIME* in his *EHLO*, Postfix will just forward the 
message, otherwise it will automatically convert from 8bit to 7bit first (*mime output conversion*).

And that's exactly what happened in our case, Gitea is sending 8bit, Postfix receive *8BITMIME* from the IIS relayhost, the next relay, 
again IIS, will also accept 8bit but the last one, in our case Mimecast, expect 7bit and therefore reject. 
Even worse, we choose a noreply@ non existing sender address and therefore never received the non-delivery report (NDR) from the second IIS.

The Solution is now quite easy, we discard the *8BITMIME* keyword from *EHLO* messages which will enforce a conversion from 8bit to 7bit for every relayed Mail.

.. code-block::

  # /etc/postfix/main.cf

  smtpd_discard_ehlo_keywords = 8BITMIME

  disable_mime_output_conversion = no

After restarting the Postfix service you should see messages like :code:`postfix/smtpd: discarding EHLO keywords: 8BITMIME` 
in */var/log/mail* and mails which where earlier just lost during relaying will now start to arrive if there was never any issue.

Lesson learned, using a valid mail address as sender will make things easier, mime encoding matters and 7bit still seem to be the safe choice for email delivery.

