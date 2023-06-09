Unreal Tournament (UT99) unter openSUSE Tumbleweed Linux
########################################################

:date: 2019-12-05 13:38
:modified: 2021-02-26 21:52
:tags: Linux, openSUSE, UT
:category: Games
:slug: unreal-tournament-ut99-unter-opensuse-tumbleweed-linux
:author: Dominik Wombacher
:lang: de
:transid: unreal-tournament-ut99-on-opensuse-tumbleweed-linux
:status: published

Um ehrlich zu sein, ich habe jahrelang kein Unreal Tournament von 1999 gespielt, aber nachdem ich die Game CD gefunden habe, musste ich es einfach auf meinem Linux Notebook installieren und zocken :D

TL;DR
*****

Zusammenfassung der Installation von Unreal Tournament (Classic / 1999) unter openSUSE Tumbleweed Linux:

(1) **games** Repository hinzufuegen und Paket **gtk** installieren

  - Entweder via YaST oder ueber das `openSUSE Software repository`_

.. code-block::

	zypper addrepo https://download.opensuse.org/repositories/games/openSUSE_Tumbleweed/games.repo
	zypper refresh
	zypper install gtk

(2) Installation der fehlenden 32bit Bibliotheken

.. code-block::

	zypper install libX11-6-32bit
	zypper install libXext6-32bit
	zypper install libglvnd-32bit
	zypper install Mesa-libGL1-32bit
	zypper install pulseaudio-utils-32bit

(3) Herunterladen und ausfuehren des UT99 installer

  - Update 26.02.2021: Die nachfolgend von wget benutzte Adresse - Ziel: **liflg.org** - funktioniert nicht mehr und leitet auf Github weiter, du kannst stattdessen `archive.org #2`_ benutzen.
  
.. code-block::
	
	# wget https://liflg.org/?what=dl&catid=6&gameid=51&filename=unreal.tournament_436-multilanguage.run
	
	wget https://web.archive.org/web/20180614001819if_/https://liflg.reto-schneider.ch/files/final/unreal.tournament_436-multilanguage.run
	chmod +x unreal.tournament_436-multilanguage.run
	./unreal.tournament_436-multilanguage.run

(4) Geniesse UT99

.. code-block::

	padsp <InstallPath>/ut

Die ganze Reise
***************

Ich besitze ein `TUXEDO InfinityBook Pro 14 v5 <https://www.tuxedocomputers.com/en/Linux-Hardware/Linux-Notebooks/10-14-inch/TUXEDO-InfinityBook-Pro-14-v5.tuxedo>`__
(Archive: `[1] <http://archive.today/2021.02.20-153838/https://www.tuxedocomputers.com/en/Linux-Hardware/Linux-Notebooks/10-14-inch/TUXEDO-InfinityBook-Pro-14-v5.tuxedo>`__) 
mit einem Intel UHD Graphics 620 Chip, worauf openSUSE Tumbleweed Linux laeuft, es sollte hoffentlich ausreichen um ein 20 Jahre altes Spiel zu spielen ;)

Linux Installer
===============

Der Install kann von `Linux Installers for Linux Games`_ heruntergeladen werden, 
ich habe :code:`unreal.tournament_436-multilanguage.run` und :code:`unreal.tournament.official.bonus.pack.collection.run` ausgewaehlt - der andere verfuegbare ist fuer die *Game of the Year* (goty) Edition.

- Update 26.02.2021: Der obige link auf **Linux Installers for Linux Games** funktioniert nicht mehr und leitet auf Github weiter, du kannst stattdessen die folgenden Backup Links nutzen:

  - **liflg.org** Seite: `archive.org #1`_
  
  - UT99 Installer: `archive.org #2`_
  
  - UT99 BonusPack: `archive.org #3`_

.. _`Linux Installers for Linux Games`: https://liflg.org/?catid=6&amp;gameid=51
.. _`archive.org #1`: https://web.archive.org/web/20181027111203/https://www.liflg.org/?catid=6&gameid=51
.. _`archive.org #2`: https://web.archive.org/web/20180614001819if_/https://liflg.reto-schneider.ch/files/final/unreal.tournament_436-multilanguage.run
.. _`archive.org #3`: https://web.archive.org/web/20171203202118if_/https://liflg.reto-schneider.ch/files/final/unreal.tournament.official.bonus.pack.collection.run

Fehlerbehebung
==============

GTK in Version 1 ist erforderlich fuer beide Installer, nach etwas Recherche habe ich es im `openSUSE Software repository`_ gefunden.

.. _`openSUSE Software repository`: https://software.opensuse.org/package/gtk

Nach der Installation des GTK Pakets und dem Einlegen der Spiel-CD in mein externes Laufwerk, habe ich einfach das Installationsprogramm gestartet, den Installationspfad angepasst und die Installation gestartet.

Scheint fast zu einfach zu sein!?

Yep, nachdem ich UT gestartet habe, erschien die Fehlermeldung: :code:`libX11.so.6 is missing` 
Scheint so das die 32bit Version standardmaessig nicht installiert ist, :code:`zypper install libX11-6-32bit` hat geholfen. 
Das selbe mit der naechsten fehlenden Bibliothek **libXext.so.6**, :code:`zypper install libXext6-32bit`.

Gut, naechster Fehler:

.. code-block::

	Signal: SIGIOT [iot trap]
	Aborting.

Werfen wir einen Blick in die log Datei: :code:`cat ~/.loki/ut/System/UnrealTournament.log`:

.. code-block::

	Log: binding libGL.so.1
	Critical: appError called:
	Critical: Could not load OpenGL library

Ok, andere Art der Fehlermeldung, aber nach etwas Recherche zeigt sich, doch identisch zu weiter oben, es fehlt die *32bit* Version von **libGL.so.1**, denn natuerlich ist nur die *64bit* Variante standardmaessig installiert. 
Und wieder hat :code:`zypper install libglvnd-32bit` das Problem geloest.

Hmm aber trotzdem trat schon wieder der **SIGIOT** Fehler auf, schauen wir nochmal in die Log Datei:

.. code-block::

	Log: OpenGL
	Critical: appError called:
	Critical: Couldn't set video mode: Couldn't find matching GLX visual

Lektion gelernt, um ein 20 Jahre altes Spiel auf einer Bleeding-Edge Distribution im Jahr 2019 zum Laufen zu bringen, muss man einen Haufen 32bit-Bibliotheken installieren ;) 
Dieses Mal hat **Mesa-libGL1-32bit** gefehlt und musste installiert werden.

Und siehe da, es startet, ohne Ton :O ... Ziemlich sicher fehlt wieder eine 32bit Library ... 
Ich habe einige Hinweise zu *PulseAudio* im `Debian Wiki <https://wiki.debian.org/Games/UT99>`__
(Archive: `[1] <https://web.archive.org/web/20201112021136/https://wiki.debian.org/Games/UT99>`__,
`[2] <http://archive.today/2017.11.01-215614/https://wiki.debian.org/Games/UT99>`__) gefunden.
Also habe ich **pulseaudio-utils-32bit** installiert, danach das Spiel mit :code:`padsp ut` anstelle von nur :code:`ut` gestartet und hatte Sound :D

Audio Probleme
==============

Um die Verzoegerungen in der Audio Wiedergabe los zu werden, war es auch noch erforderlich eine Zeile in der Config Datei :code:`~/.loki/ut/System/UnrealTournament.ini` anzupassen:

.. code-block::

    # Aendere das: 
    AudioDevice=ALAudio.ALAudioSubsystem

    # In das:
    AudioDevice=Audio.GenericAudioSubsystem

Online spielen
==============

Es sieht danach aus das viele Audio Sample Raten, die benoetigt werden um Online zu spielen, nicht vom *GenericAudioSubsystem* unterstuetzt werden. 
Die Verbindung zu den meisten UT Servern schlaegt fehl und in der **UnrealTournament.log** Datei tauchen **unsupported Rate** Fehlermeldungen auf. 

Der bisherige Workaround war es das *ALAudioSubsystem* zu nutzen, was aber zu Delays in der Audio Ausgabe fuehrt :(

Zusaetzlich verlangen viele oeffentliche Server einen installierten **NPLoader**. 
Verschiedene Versionen koennen unter http://utgl.unrealadmin.org/NPLoader/ heruntergeladen werden.

Du musst entweder die *Linux.tar.gz* oder die *.dll*, *.so* sowie *.u* Datei herunterladen und in das *System* Verzeichnis deiner UT Installation kopieren.

Well done
=========

Selbst wenn ich etwas Zeit investieren musste um zu recherchieren, einige 32bit libraries zu installieren, configs anzupassen sowie diverse Fehler zu finden und zu beheben, es ist es wert! 
Ich weiss die genauen FPS nicht, aber es sieht aus und fuehlt sich an wie vor 20 Jahren, ich liebe es!

Uebrigens, die Installation des Bonus Pack war auf Basis des :code:`unreal.tournament.official.bonus.pack.collection.run` sehr einfach und selbsterklaerend.

Geniesse Unreal Tournament von 1999 auf deinem Linux System!
