Apple AirPods on Linux?
#######################

:date: 2019-10-26 12:55
:modified: 2019-10-26 12:55
:tags: AirPods, Apple, Bluetooth, Linux, openSUSE
:category: Linux
:slug: apple-airpods-on-linux
:author: Dominik Wombacher
:lang: en
:transid: apple-airpods-on-linux
:status: published

I was wondering if my Apple AirPods would work on openSUSE Linux out of the Box. 
Just enable pairing mode, click on connect and all fine? Not exactly, it failed with the default settings and some additional Steps were necessary.

(1) Set :code:`ControllerMode = dual` in config File **/etc/bluetooth/main.conf**

- On openSUSE Tumbleweed (Patch Level 10/2019) the config file doesn't seem exist by default. I copied the example of the bluez Package located in **/usr/share/doc/packages/bluez/**

.. code-block::

	sudo cp /usr/share/doc/packages/bluez/main.conf /etc/bluetooth/main.conf
	sudo vim /etc/bluetooth/main.conf

	# Restricts all controllers to the specified transport. Default value
	# is "dual", i.e. both BR/EDR and LE enabled (when supported by the HW).
	# Possible values: "dual", "bredr", "le"
	ControllerMode = dual

	sudo systemctl restart bluetooth

(2) Add Parameter :code:`--noplugin=avrcp` at the end of :code:`ExecStart` in **bluetooth.service**, otherwise the AirPods running with poor Sound Quality and very low volume

- Source: https://wiki.archlinux.org/index.php/Bluetooth_headset#Apple_Airpods_have_low_volume 
  (Archive: `[1] <https://web.archive.org/web/20190908054157/https://wiki.archlinux.org/index.php/Bluetooth_headset>`__,
  `[2] <http://archive.today/2021.02.25-235417/https://wiki.archlinux.org/index.php/Bluetooth_headset%23Apple_Airpods_have_low_volume>`__)

.. code-block::

	sudo systemctl edit --full bluetooth.service

	[...]
	ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=avrcp
	[...]

	sudo systemctl restart bluetooth

After those few adjustments they actually working quite good as Headphone. 
The Microphone is not working yet, maybe i will take a look into that later.
