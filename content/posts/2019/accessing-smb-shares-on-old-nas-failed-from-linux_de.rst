.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Zugriff auf SMB Freigabe auf altem NAS von Linux aus
####################################################

:date: 2019-12-24 13:33
:modified: 2019-12-24 13:33
:tags: NAS, openSUSE, Samba, smb, Linux
:category: Linux
:slug: zugriff-auf-smb-freigabe-auf-altem-nas-von-linux-aus
:author: Dominik Wombacher
:lang: de
:transid: accessing-smb-share-on-old-nas-failed-from-linux
:status: published

Manchmal kann es herausfordernd sein alte Hardware zu verwenden.
In meinem Fall habe ich eine alte *Buffalo LinkStation LS-WTGL* NAS von 2008 gefunden.

Die Verbindung von einem aktuellen openSUSE System schlug allerdings ueberraschenderweise fehl:

:code:`Unable to initialize messaging context. protocol negotiation failed: NT_STATUS_CONNECTION_DISCONNECTED`

Aber warum und was ist das Problem? Auf meine *QNAP TS-253A* NAS konnte ich mich problemlos verbinden.
Ich habe verschiedene Parameter des smbclient cli tool ausprobiert, ohne Erfolg.

Nach einiger Zeit hat mich der Hinweis in einem `Ask Fedora! <https://ask.fedoraproject.org/t/unable-to-mount-samba-share-on-fedora-31-which-fedora-30-windows-has-no-problem-with/4077>`__
(Archive: `[1] <https://web.archive.org/web/20210225143935/https://ask.fedoraproject.org/t/unable-to-mount-samba-share-on-fedora-31-which-fedora-30-windows-has-no-problem-with/4077/4>`__,
`[2] <http://archive.today/2021.02.25-143929/https://ask.fedoraproject.org/t/unable-to-mount-samba-share-on-fedora-31-which-fedora-30-windows-has-no-problem-with/4077/1>`__) 
Thread von eeijlar auf die richtige Spur geschickt.
Der Workaround, auch in `Red Hat Bug 1768117 <https://bugzilla.redhat.com/show_bug.cgi?id=1768117>`__
(Archive: `[1] <https://web.archive.org/web/20201111203350/https://bugzilla.redhat.com/show_bug.cgi?id=1768117>`__,
`[2] <http://archive.today/2021.02.25-144057/https://bugzilla.redhat.com/show_bug.cgi?id=1768117>`__) 
beschrieben, loeste das Problem und ich konnte den SMB Share meines alten Buffalo NAS einbinden.

eeijlar::

> Update /etc/samba/smb.conf with:
> [global]
> client min protocol = NT1

Aus sicherheitsgruenden, ist das Protokol SMB1 / NT1 inzwischen by default in Samba 4.11 und hoeher deaktiviert.
Allerdings unterstuetzen einige alte NAS Geraete nur dieses Protokoll.

Ich rate dringend es nur voruebergehend zu aktivieren um Dateien zu migrieren.
