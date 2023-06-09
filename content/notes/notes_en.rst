Notes
#####

:title: Notes
:date: 2021-03-04
:modified: 2023-01-06
:description: Quick Notes about various topics
:slug: notes
:author: Dominik Wombacher
:lang: en
:transid: notes
:status: published

.. |date| date::
.. |time| date:: %H:%M

Just some quick Notes, too less for a Post but too much to not write it down somewhere.

|

.. .. topic:: yyyy-mm-dd: <TITLE>
..
..     <CONTENT>
..
.. `Directlink <>`__
.. (Archive: `[1] <>`__,
.. `[2] <>`__)
..

.. topic:: 2023-01-06: Pair Remote Control again to Xiaomi Computer Monitor Light Bar

  Recently one of my light bar's stopped recognizing the remote control, there isn't much online about factory reset or re-pair the remote control. 
  After searching around for a while, unplug the light bar, plugin it back in and then push and hold the knob on the remote control for a few seconds worked.
  Nothing happend on the light bar, doesn't blinked or something, but the remote control started working again that way.

|

.. topic:: 2021-04-18: Disable automatic BTRFS Snapshots (openSUSE Leap / SLES 12 & 15)
  
  By default openSUSE and SLES using BTRFS as root filesystem with automatic snapshots, triggered for example by running zypper. 
  It can be useful to (temporary) deactivate that feature. Change *"/etc/sysconfig/yast2"* and disable snapper: :code:`USE_SNAPPER=NO` also remove the zypp plugin: :code:`zypper remove --no-confirm snapper-zypp-plugin`. 
  To re-activate it, just set the config setting to *"YES"* and install the zypp plugin again.

|

.. topic:: 2021-03-21: Use freenode Nickname with matrix.org Client and IRC Bridge

	It's quite convenient to use IRC via matrix.org Bridge but lot of freenode Channel require a registered nick to join. 
	I have a registered nick, just had to figure out how to use it through the IRC Bridge. 
	I found what i needed in this 
	`gist <https://gist.github.com/fstab/ce805d3001600ac147b79d413668770d>`__
	(Archive: `[1] <https://web.archive.org/web/20201111205136/https://gist.github.com/fstab/ce805d3001600ac147b79d413668770d>`__,
	`[2] <https://archive.today/2017.09.20-143847/https://gist.github.com/fstab/ce805d3001600ac147b79d413668770d>`__) 
	as well this `issue comment <https://github.com/matrix-org/matrix-appservice-irc/issues/475#issuecomment-315969908>`__
	(Archive: `[1] <https://web.archive.org/web/20210321100007if_/https://github.com/matrix-org/matrix-appservice-irc/issues/475#issuecomment-315969908>`__,
	`[2] <https://archive.today/2021.03.21-100021/https://github.com/matrix-org/matrix-appservice-irc/issues/475#issuecomment-315969908>`__). 
	
	Summary: Start direct Chat with :code:`@appservice-irc:matrix.org`, Store your credentials :code:`!storepass <nick>:<password>`, Authenticate :code:`!nick <nick>`

|

.. topic:: 2021-03-13: Rotate a PDF Counterclockwise via Linux commandline

	Sometimes even easy things can be challenging, but nothing a Search Engine can't help to find: :code:`pdftk in.pdf cat 1-endwest output out.pdf` - 
	`Source <https://unix.stackexchange.com/questions/394065/command-line-how-do-you-rotate-a-pdf-file-90-degrees>`__
	(Archive: `[1] <https://web.archive.org/web/20190807193701/https://unix.stackexchange.com/questions/394065/command-line-how-do-you-rotate-a-pdf-file-90-degrees>`__,
	`[2] <https://archive.today/2021.03.14-115833/https://unix.stackexchange.com/questions/394065/command-line-how-do-you-rotate-a-pdf-file-90-degrees>`__)

|

.. topic:: 2021-03-04: Nice improvement how Translations show up in Pelican

	I found a very nice example, how to enhance the output of links to translated pages in Pelican, in the Blog from 
	`Bernhard Scheirle <https://bernhard.scheirle.de/posts/2016/August/17/pelican-improved-display-of-translations/>`__
	(Archive: `[1] <https://web.archive.org/web/20170707235324/https://bernhard.scheirle.de/posts/2016/August/17/pelican-improved-display-of-translations/>`__,
	`[2] <https://archive.today/2021.03.03-201325/https://bernhard.scheirle.de/posts/2016/August/17/pelican-improved-display-of-translations/>`__).
	
	By default, Pelican just shows the two letter Country Code. Was not thinking about how easy it is to 
	add a custom Jinja Filter, impressive, of course I had to change my theme right away :)
    
