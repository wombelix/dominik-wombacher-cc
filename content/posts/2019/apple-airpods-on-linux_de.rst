Apple AirPods unter Linux?
##########################

:date: 2019-10-26 12:55
:modified: 2019-10-26 12:55
:tags: AirPods, Apple, Bluetooth, Linux, openSUSE
:category: Linux
:slug: apple-airpods-unter-linux
:author: Dominik Wombacher
:lang: de
:transid: apple-airpods-on-linux
:status: published

Ich habe mich gefragt ob meine Apple AirPods unter openSUSE Linux funktionieren wuerden.
Einfach den Pairing Mode einschalten, auf verbinden klicken und es laeuft? 
Nicht ganz, mit den Standard Einstellungen ist es fehlgeschlagen und es waren ein paar Anpassungen notwendig.

(1) Setze :code:`ControllerMode = dual` in der config Datei **/etc/bluetooth/main.conf**

- Unter openSUSE Tumbleweed (Patch Level 10/2019) existiert die config datei scheinbar nicht standardmaessig. 
  Ich habe das Beispiel aus dem bluez Paket aus dem Ordner **/usr/share/doc/packages/bluez/** kopiert.

.. code-block::

	sudo cp /usr/share/doc/packages/bluez/main.conf /etc/bluetooth/main.conf
	sudo vim /etc/bluetooth/main.conf

	# Restricts all controllers to the specified transport. Default value
	# is "dual", i.e. both BR/EDR and LE enabled (when supported by the HW).
	# Possible values: "dual", "bredr", "le"
	ControllerMode = dual

	sudo systemctl restart bluetooth

(2) Fuege den Parameter :code:`--noplugin=avrcp` am Ende von :code:`ExecStart` in **bluetooth.service** ein,
andernfalls werden die AirPods nur mit sehr schlechter Qualitaet und sehr geringer Lautstaerke funktionieren.

- Quelle: https://wiki.archlinux.org/index.php/Bluetooth_headset#Apple_Airpods_have_low_volume 
  (Archive: `[1] <https://web.archive.org/web/20190908054157/https://wiki.archlinux.org/index.php/Bluetooth_headset>`__,
  `[2] <http://archive.today/2021.02.25-235417/https://wiki.archlinux.org/index.php/Bluetooth_headset%23Apple_Airpods_have_low_volume>`__)

.. code-block::

	sudo systemctl edit --full bluetooth.service

	[...]
	ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=avrcp
	[...]

	sudo systemctl restart bluetooth

Nach diese kleinen Anpassungen funktionieren Sie eigentlich schon ziemlich gut als Headset.
Das Mikrofon funktioniert noch nicht, vielleicht schaue ich mir das spaeter noch an.
