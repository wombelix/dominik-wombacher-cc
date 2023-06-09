.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

openSUSE Tumbleweed: Issues on resume from hibernate / suspend to disk
######################################################################

:date: 2021-10-03
:modified: 2021-10-03
:tags: openSUSE, Tumbleweed, Linux
:description: Issues on resume from hibernate / suspend to disk
:category: Linux
:slug: opensuse-tumbleweed-issues-on-resume-from-hibernate-suspend-to-disk
:author: Dominik Wombacher
:lang: en
:transid: opensuse-tumbleweed-issues-on-resume-from-hibernate-suspend-to-disk 
:status: published

So far I always used **sleep** when closing the lid of my Notebook, 
was ok even though you risk that your battery runs empty and your system shutdown. 
Wanted to activate **hibernate** which then would also support **hybrid sleep**, 
what seem to be compareable with what Apple does to achieve a massive *standby* and short wakeup time on the MacBook.

During the Setup I already created a Swap Partition equal to the size of my Memory, 
so I thought this should all work out of the box, but didn't.

Found a `Post on reddit <https://www.reddit.com/r/openSUSE/comments/hjec9g/resume_from_hibernation_is_not_working/>`__
(Archive: `[1] <https://archive.today/2021.10.03-102238/https://www.reddit.com/r/openSUSE/comments/hjec9g/resume_from_hibernation_is_not_working/>`__) 
and a related `Bug Report <https://bugzilla.suse.com/show_bug.cgi?id=1187381>`__
(Archive: `[1] <https://web.archive.org/web/20211003103337/https://bugzilla.suse.com/show_bug.cgi?id=1187381>`__,
`[2] <https://archive.today/2021.10.03-103302/https://bugzilla.suse.com/show_bug.cgi?id=1187381>`__), both contained contrary information. 
Based on Reddit the *resume* module would be missing in *initrd* and should be included. 
The Bug makes clear that *systemd-hibernate-resume* is used and _not_ the *resume* module that could be added by *dracut*.

I trust the Bug Report more, but adding *resume=/dev/mapper/system-swap* 
(Has to be the path to your Swap Partition and might differ) 
to **/etc/default/grub** didn't solved the issue. 
So I generated a new *initramfs* by running *dracut -f*, without modifying any config, 
afterwards **hibernate** and **hybrid sleep** were working. 

.. code-block::

  grep resume /etc/default/grub 
  GRUB_CMDLINE_LINUX_DEFAULT="splash=silent mitigations=auto quiet resume=/dev/mapper/system-swap"

  sudo grub2-mkconfig -o /boot/efi/EFI/opensuse/grub.cfg

  sudo dracut -f

No Idea why I had to rebuild the *initramfs*, should already be done (automatically) during the last Kernel Upgrade, 
anyway, I can now use **hybrid sleep** which looks actually very good so far. 
Roughtly 30 - 60 sec until sleep after closing the lid, resume just a few seconds, 
not really different to **sleep** as far I can see.
