.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

No Sound in DOSBox on Linux
###########################

:date: 2019-12-06 18:53
:modified: 2019-12-06 18:53
:tags: Audio, DOSBox, Midi, Sound, Games, Linux, openSUSE, Tumbleweed, Discworld
:category: Linux
:slug: no-sound-in-dosbox-on-linux
:author: Dominik Wombacher
:lang: en
:transid: no-sound-in-dosbox-on-linux
:status: published

I installed DOSBox to play some old DOS Games like Discworld on Linux (openSUSE Tumbleweed) but didn't had sound prior figure out the correct MIDI Port and adjusting the dosbox config accordingly.

Due to the fact that i installed Unreal Tournament from 1999 already (successful!) on my Linux Notebook, it's obvious that i had to do the same with some even older Games too :D

I thought executing "pmidi -l" would show the correct MIDI Port, but at least in my case, further steps were necessary.

The troubleshooting approach described in the `AskUbuntu Forum <https://askubuntu.com/questions/79944/dosbox-has-no-sound>`__
(Archive: `[1] <https://web.archive.org/web/20180102021001/https://askubuntu.com/questions/79944/dosbox-has-no-sound>`__,
`[2] <http://archive.today/2021.02.25-232132/https://askubuntu.com/questions/79944/dosbox-has-no-sound>`__) 
is my favorite and did the trick.

You have to Download a test MIDI File, start a MIDI Server, start the playback and if you have audio, put the correct Port into your dosbox config.

.. code-block:: 

	zypper install timidity
	zypper install pmidi

	cd /tmp
	wget http://www.angelfire.com/fl/herky/images/teddybear.mid

	pmidi -l
	#    Port     Client name                       Port name
	#    14:0     Midi Through                      Midi Through Port-0

	timidity -iA
	#    Requested buffer size 32768, fragment size 8192
	#    ALSA pcm 'default' set buffer size 32768, period size 8192 bytes
	#    TiMidity starting in ALSA server mode
	#    Opening sequencer port: 128:0 128:1 128:2 128:3

	pmidi -p 128:0 teddybear.mid
	
In my case, pmidi identified Port "14:0" but based on the test with timidity i have to use "128:0" instead.

So i changed the corresponding parameter in my dosbox config:

.. code-block:: ini

	[midi]
	midiconfig=128:0

When you start dosbox from the console, you should see something like the following an hear the nicest MIDI sound when starting an old Game ;)

.. code-block::

	ALSA:Client initialised [128:0]
	MIDI:Opened device:alsa

I will play around with ScummVM as well within the next days, so i'm quite sure further Posts regarding some sort of gaming on Linux will follow soon!

