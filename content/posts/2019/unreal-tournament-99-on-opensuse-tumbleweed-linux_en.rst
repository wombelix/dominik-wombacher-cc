.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Unreal Tournament (UT99) on openSUSE Tumbleweed Linux
#####################################################

:date: 2019-12-05 13:38
:modified: 2021-02-26 21:52
:tags: Linux, openSUSE, UT
:category: Games
:slug: unreal-tournament-ut99-on-opensuse-tumbleweed-linux
:author: Dominik Wombacher
:lang: en
:transid: unreal-tournament-ut99-on-opensuse-tumbleweed-linux
:status: published

To be honest, i didn't played Unreal Tournament from 1999 for years but after i found the Game CD, i just had to install and play it on my Linux Notebook :D

TL;DR
*****

Summary how to install Unreal Tournament (Classic / 1999) on openSUSE Tumbleweed Linux:

(1) Add **games** Repository and install package **gtk**

  - either via YaST or through the `openSUSE Software repository`_

.. code-block::

	zypper addrepo https://download.opensuse.org/repositories/games/openSUSE_Tumbleweed/games.repo
	zypper refresh
	zypper install gtk

(2) Install missing 32bit libraries

.. code-block::

	zypper install libX11-6-32bit
	zypper install libXext6-32bit
	zypper install libglvnd-32bit
	zypper install Mesa-libGL1-32bit
	zypper install pulseaudio-utils-32bit

(3) Download and run the UT99 installer

  - Update 2021-02-26: The address used by wget below - pointing to **liflg.org** - isn't working anymore and redirect to Github, you can use `archive.org #2`_ instead.
  
.. code-block::
	
	# wget https://liflg.org/?what=dl&catid=6&gameid=51&filename=unreal.tournament_436-multilanguage.run
	
	wget https://web.archive.org/web/20180614001819if_/https://liflg.reto-schneider.ch/files/final/unreal.tournament_436-multilanguage.run
	chmod +x unreal.tournament_436-multilanguage.run
	./unreal.tournament_436-multilanguage.run

(4) Enjoy UT99

.. code-block::

	padsp <InstallPath>/ut

The whole journey
*****************

I own a `TUXEDO InfinityBook Pro 14 v5 <https://www.tuxedocomputers.com/en/Linux-Hardware/Linux-Notebooks/10-14-inch/TUXEDO-InfinityBook-Pro-14-v5.tuxedo>`__
(Archive: `[1] <http://archive.today/2021.02.20-153838/https://www.tuxedocomputers.com/en/Linux-Hardware/Linux-Notebooks/10-14-inch/TUXEDO-InfinityBook-Pro-14-v5.tuxedo>`__) 
with an Intel UHD Graphics 620 Chip, running openSUSE Tumbleweed Linux, should hopefully be sufficient to play an 20 year old Game ;)

Linux Installer
===============

The Installer can be downloaded from `Linux Installers for Linux Games`_,  
i picked :code:`unreal.tournament_436-multilanguage.run` and :code:`unreal.tournament.official.bonus.pack.collection.run` - the other one available is for the *Game of the Year* (goty) Edition.

- Update 2021-02-26: The above link to **Linux Installers for Linux Games** isn't working anymore and redirect to Github, you can use the following Backup Links instead:

  - **liflg.org** Page: `archive.org #1`_
  
  - UT99 Installer: `archive.org #2`_
  
  - UT99 BonusPack: `archive.org #3`_

.. _`Linux Installers for Linux Games`: https://liflg.org/?catid=6&amp;gameid=51
.. _`archive.org #1`: https://web.archive.org/web/20181027111203/https://www.liflg.org/?catid=6&gameid=51
.. _`archive.org #2`: https://web.archive.org/web/20180614001819if_/https://liflg.reto-schneider.ch/files/final/unreal.tournament_436-multilanguage.run
.. _`archive.org #3`: https://web.archive.org/web/20171203202118if_/https://liflg.reto-schneider.ch/files/final/unreal.tournament.official.bonus.pack.collection.run

Troubleshooting
===============

GTK in Version 1 is required by both installer, after some research i found the package in the `openSUSE Software repository`_.

.. _`openSUSE Software repository`: https://software.opensuse.org/package/gtk

After installing the GTK package and inserting the Game CD into my external Drive, i just started the installer, adjusted the Install Path and started the installation.

Seems just too easy!?

Yep, after starting UT, i received an error message that :code:`libX11.so.6 is missing`. 
Looks like the 32bit version is not installed by default, :code:`zypper install libX11-6-32bit` solved that problem. 
Same with the next missing library **libXext.so.6**, :code:`zypper install libXext6-32bit`.

Well, next Error:

.. code-block::

	Signal: SIGIOT [iot trap]
	Aborting.
	
Let's take a look into the log file by running :code:`cat ~/.loki/ut/System/UnrealTournament.log`:

.. code-block::

	Log: binding libGL.so.1
	Critical: appError called:
	Critical: Could not load OpenGL library

Ok, different kind of error message but after some research same as above, there is a 32bit version of **libGL.so.1** but, for sure, i only had the 64bit one installed by default. 
Running :code:`zypper install libglvnd-32bit` solved that issue too.

Hmm but again the **SIGIOT** error occurred, let's take a look into the log files:

.. code-block::

	Log: OpenGL
	Critical: appError called:
	Critical: Couldn't set video mode: Couldn't find matching GLX visual

Lesson learned, to get a 20 year old game running on a bleeding edge Distribution in 2019, you have to install a bunch of 32bit libraries ;) 
This time **Mesa-libGL1-32bit** was missing and need to be installed.

And voila, it's starting! without sound :O ... Quite sure it's a missing 32bit lib again ... 
I found some hints regarding PulseAudio in the `Debian Wiki <https://wiki.debian.org/Games/UT99>`__
(Archive: `[1] <https://web.archive.org/web/20201112021136/https://wiki.debian.org/Games/UT99>`__,
`[2] <http://archive.today/2017.11.01-215614/https://wiki.debian.org/Games/UT99>`__).
So i installed **pulseaudio-utils-32bit** and after starting the game with :code:`padsp ut` instead just :code:`ut` i had sound :D

Audio Issues
============

To get rid of delays in the Audio Output, it was necessary to adjust one line in the config file :code:`~/.loki/ut/System/UnrealTournament.ini` as well:

.. code-block::

    # Change this: 
    AudioDevice=ALAudio.ALAudioSubsystem

    # To that:
    AudioDevice=Audio.GenericAudioSubsystem

Play Online
===========

It looks like that lot of audio sample rates which are required to play Online are not supported using the GenericAudioSubsystem. 
Connection to most of the UT Server fail and you find an Error about **unsupported Rate** in your **UnrealTournament.log** file. 
The workaround so far was to use the ALAudioSubsystem with a delay in the Audio Output :(

Also lot Public Server require an installed NPLoader. 
Lot of different Version can be found at: http://utgl.unrealadmin.org/NPLoader/

You have to Download either the *Linux.tar.gz* or the *.dll*, *.so* as well *.u* file and copy all of them in your *System* folder of your UT Installation.

Well done
=========

Even if i had to look around for some time to locate and fix most of the issues, install a bunch of 32bit libraries, adjust something in the config as well start the game with an extra parameter, it's worth it!
Didn't know the exact FPS count but look and feel is like 20 years ago and i love it!

Btw. installing the Bonus Pack was very straight forward with the :code:`unreal.tournament.official.bonus.pack.collection.run` script.

Enjoy Unreal Tournament from 1999 on your Linux Machine!
