Notizen
#######

:title: Notizen
:date: 2021-03-04
:modified: 2023-01-06
:description: Kurze Notizen zu verschiedenen Themen
:slug: notizen
:author: Dominik Wombacher
:lang: de
:transid: notes
:status: published

.. |date| date::
.. |time| date:: %H:%M

Nur ein paar kurze Notizen, zu wenig fuer einen Post, aber zu viel, um es nicht irgendwo aufzuschreiben.

|

.. .. topic:: yyyy-mm-dd: <TITLE>
..
..     <CONTENT>
..
.. `Directlink <>`__
.. (Archive: `[1] <>`__,
.. `[2] <>`__)
..

.. topic:: 2023-01-06: Fernbedienung wieder mit Xiaomi Computer Monitor Light Bar koppeln

  Kürzlich hat einer meiner light bars aufgehört die Fernbedienung zu erkennen, es gibt nicht viele infos online über Werksreset oder re-pairing der Fernbedienung. 
  Nachdem ich eine Weile herumgesucht habe, habe ich den Stecker der Lichtleiste herausgezogen, ihn wieder eingesteckt und dann den Knopf auf der Fernbedienung ein 
  paar Sekunden lang gedrückt gehalten. Es passierte nichts, die light bar blinkte nicht oder so, aber die Fernbedienung funktionierte auf diese Weise wieder.

|

.. topic:: 2021-04-18: Automatische BTRFS Snapshots deaktivieren (openSUSE Leap / SLES 12 & 15)

  Standardmäßig verwenden openSUSE und SLES als root Dateisystem BTRFS mit automatischen Snapshots, ausgelöst z.B. durch das ausführen von zypper. 
  Es kann sinnvoll sein, diese Funktion (vorübergehend) abzuschalten. Ändere dazu *"/etc/sysconfig/yast2"* und deaktiviere snapper: :code:`USE_SNAPPER= NO` entferne ausserdem das zypp Plugin: :code:`zypper remove --no-confirm snapper-zypp-plugin`. 
  Um die Snapshots wieder zu aktivieren, setze einfach die Einstellung auf *"YES "* und installiere das zypp Plugin wieder.

|

.. topic:: 2021-03-21: Freenode Nickname mit matrix.org Client und IRC Bridge verwenden

	Es ist recht angenehm, IRC ueber eine matrix.org Bridge zu nutzen, aber viele freenode Channel verlangen einen registrierten Nick um zu joinen. 
	Ich habe zwar einen, musste nur herausfinden, wie ich Ihn ueber die IRC Bridge nutzen kann. 
	Was ich dazu brauchte habe ich in diesem `gist <https://gist.github.com/fstab/ce805d3001600ac147b79d413668770d>`__
	(Archive: `[1] <https://web.archive.org/web/20201111205136/https://gist.github.com/fstab/ce805d3001600ac147b79d413668770d>`__,
	`[2] <https://archive.today/2017.09.20-143847/https://gist.github.com/fstab/ce805d3001600ac147b79d413668770d>`__) 
	sowie diesem `issue comment <https://github.com/matrix-org/matrix-appservice-irc/issues/475#issuecomment-315969908>`__
	(Archive: `[1] <https://web.archive.org/web/20210321100007if_/https://github.com/matrix-org/matrix-appservice-irc/issues/475#issuecomment-315969908>`__,
	`[2] <https://archive.today/2021.03.21-100021/https://github.com/matrix-org/matrix-appservice-irc/issues/475#issuecomment-315969908>`__) gefunden. 
	
	Zusammenfassung: Direktchat start mit :code:`@appservice-irc:matrix.org`, Credentials speichern :code:`!storepass <nick>:<password>`, Authentifizieren :code:`!nick <nick>`

|

.. topic:: 2021-03-13: Per Linux Kommandozeile ein PDF im Uhrzeigersinn drehen

	Manchmal koennen selbst einfach Dinge herausfordernd sein, aber nichts was man dank einer Suchmaschine nicht finden kann: :code:`pdftk in.pdf cat 1-endwest output out.pdf` - 
	`Source <https://unix.stackexchange.com/questions/394065/command-line-how-do-you-rotate-a-pdf-file-90-degrees>`__
	(Archive: `[1] <https://web.archive.org/web/20190807193701/https://unix.stackexchange.com/questions/394065/command-line-how-do-you-rotate-a-pdf-file-90-degrees>`__,
	`[2] <https://archive.today/2021.03.14-115833/https://unix.stackexchange.com/questions/394065/command-line-how-do-you-rotate-a-pdf-file-90-degrees>`__)

|

.. topic:: 2021-03-04: Nette Verbesserung, wie Uebersetzungen in Pelican angezeigt werden

	Ein sehr schoenes Beispiel, wie man die Ausgabe von Links zu uebersetzten Seiten in Pelican verbessern kann, habe ich im Blog von 
	`Bernhard Scheirle <https://bernhard.scheirle.de/posts/2016/August/17/pelican-improved-display-of-translations/>`__
	(Archiv: `[1] <https://web.archive.org/web/20170707235324/https://bernhard.scheirle.de/posts/2016/August/17/pelican-improved-display-of-translations/>`__,
	`[2] <https://archive.today/2021.03.03-201325/https://bernhard.scheirle.de/posts/2016/August/17/pelican-improved-display-of-translations/>`__) gefunden.
	
	Pelican zeigt standardmaessig nur den zweistelligen Laendercode an. Ich habe nicht daran gedacht, wie einfach es ist, einen 
	benutzerdefinierten Jinja Filter hinzuzufuegen, beeindruckend, natuerlich musste ich mein Theme sofort aendern :)


