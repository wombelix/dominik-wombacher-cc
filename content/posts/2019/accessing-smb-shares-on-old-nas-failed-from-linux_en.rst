.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Accessing SMB Share on old NAS failed from Linux
################################################

:date: 2019-12-24 13:33
:modified: 2019-12-24 13:33
:tags: NAS, openSUSE, Samba, smb, Linux
:category: Linux
:slug: accessing-smb-share-on-old-nas-failed-from-linux
:author: Dominik Wombacher
:lang: en
:transid: accessing-smb-share-on-old-nas-failed-from-linux
:status: published

Sometimes it can be challenging to use some old Hardware. 
In my case I found an old *Buffalo LinkStation LS-WTGL* NAS from around 2008. 

Connecting from an up-to-date openSUSE System surprisingly failed with the Error Message:
 
:code:`Unable to initialize messaging context. protocol negotiation failed: NT_STATUS_CONNECTION_DISCONNECTED`

But what's the issue? I was able to connect to my *QNAP TS-253A* NAS without problems. 
So i played around with different parameters of the smbclient cli tool, no success.

After a while the Hint in a `Ask Fedora! <https://ask.fedoraproject.org/t/unable-to-mount-samba-share-on-fedora-31-which-fedora-30-windows-has-no-problem-with/4077>`__
(Archive: `[1] <https://web.archive.org/web/20210225143935/https://ask.fedoraproject.org/t/unable-to-mount-samba-share-on-fedora-31-which-fedora-30-windows-has-no-problem-with/4077/4>`__,
`[2] <http://archive.today/2021.02.25-143929/https://ask.fedoraproject.org/t/unable-to-mount-samba-share-on-fedora-31-which-fedora-30-windows-has-no-problem-with/4077/1>`__) 
Thread from eeijlar put me into the right Direction. 
The workaround, also mentioned in `Red Hat Bug 1768117 <https://bugzilla.redhat.com/show_bug.cgi?id=1768117>`__
(Archive: `[1] <https://web.archive.org/web/20201111203350/https://bugzilla.redhat.com/show_bug.cgi?id=1768117>`__,
`[2] <http://archive.today/2021.02.25-144057/https://bugzilla.redhat.com/show_bug.cgi?id=1768117>`__), 
solved the issue and i was able to mount my SMB Shares from the old Buffalo NAS.
 
.. _Ask Fedora!: https://ask.fedoraproject.org/t/unable-to-mount-samba-share-on-fedora-31-which-fedora-30-windows-has-no-problem-with/4077
.. _Red Hat Bug 1768117: https://bugzilla.redhat.com/show_bug.cgi?id=1768117

eeijlar::

> Update /etc/samba/smb.conf with:
> [global]
> client min protocol = NT1

For security reasons, the SMB1 / NT1 protocol is disabled by default in Samba 4.11 and higher. 
But some old NAS only support these outdated protocol. 

I highly suggest that you only enable it temporary and migrate your files.