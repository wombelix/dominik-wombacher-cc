Kein Sound in DOSBox unter Linux
################################

:date: 2019-12-06 18:53
:modified: 2019-12-06 18:53
:tags: Audio, DOSBox, Midi, Sound, Games, Linux, openSUSE, Tumbleweed, Discworld
:category: Linux
:slug: kein-sound-in-dosbox-unter-linux
:author: Dominik Wombacher
:lang: de
:transid: no-sound-in-dosbox-on-linux
:status: published

Ich habe DOSBox installiert um mir die Zeit mit ein paar alten Spielen wie Discworld auf meinem Linux System (openSUSE Tumbleweed) zu vertreiben.
Aber ohne Sound Ausgabe, bis ich den korrekten MIDI Port herausgefunden und die dosbox config entsprechend angepasst hatte.

Aufgrund der Tatsache, das ich bereits erfolgreich Unreal Tournament von 1999 auf meinem Linux Notebook installiert habe, lag es auf der Hand das mit ein paar noch viel aelteren Speielen ebenfalls zu tun :D

Ich dachte wenn ich `pmidi -l` ausfuehre, wuerde mir der richtige MIDI Port angezeigt werden, aber zumindest in meinem Fall waren weitere Schritte notwendig.

Der Loesungsansatz der im `AskUbuntu Forum <https://askubuntu.com/questions/79944/dosbox-has-no-sound>`__
(Archive: `[1] <https://web.archive.org/web/20180102021001/https://askubuntu.com/questions/79944/dosbox-has-no-sound>`__,
`[2] <http://archive.today/2021.02.25-232132/https://askubuntu.com/questions/79944/dosbox-has-no-sound>`__) 
beschrieben ist, war dabei mein Favorit und hat letztlich funktioniert.

Man muss sich eine test MIDI File herunterladen - falls man wie ich keine hat, einen MIDI Server starten, die Datei abspielen und den angezeigten Port in die dosbox config eintragen.

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

In meinem Fall hat `pmidi` den Port *14:0* identifiziert aber basierend auf dem test mit `timidity`, ist *128:0* der richtige.

Dementsprechend habe ich den entsprechenden Parameter in meiner dosbox config angepasst:

.. code-block:: ini

	[midi]
	midiconfig=128:0

Wenn man jetzt ein altes Spiel mit dosbox von der Konsole aus startet, sollte die Ausgabe etwa wie folgt aussehen und die schoensten MIDI Toene zu hoeren sein ;)

.. code-block::

	ALSA:Client initialised [128:0]
	MIDI:Opened device:alsa

Ich werde in den naechsten Tagen ein wenig mit ScummVM experimentieren, ich bin sicher das bald weitere Posts ueber Linux Gaming folgen werden!
