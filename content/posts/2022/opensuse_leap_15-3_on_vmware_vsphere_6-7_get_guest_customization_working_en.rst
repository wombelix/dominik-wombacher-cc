.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

openSUSE Leap 15.3 on VMware vSphere 6.7: Get Guest Customization working
#########################################################################

:date: 2022-03-10
:modified: 2022-03-10
:tags: openSUSE, Leap, VMWare, vSphere
:description: How-to use vSphere Guest Customization with openSUSE Leap 15.3
:category: Linux
:slug: opensuse_leap_15-3_on_vmware_vsphere_6-7_get_guest_customization_working
:author: Dominik Wombacher
:lang: en
:transid: opensuse_leap_15-3_on_vmware_vsphere_6-7_get_guest_customization_working 
:status: published

Technically *openSUSE Leap 15.3* is equal to *SUSE Linux Enterprise Server 15 SP3*, both share the same code and binary packages, 
the only difference is community vs. commercial support. It's even possible to quickly 
`migrate from Leap 15.3 to SLES 15 SP3 <https://en.opensuse.org/SDB:How_to_migrate_to_SLE#Migration_from_openSUSE_Leap_to_SUSE_Linux_Enterprise_Server>`__ 
(Archive: `[1] <https://web.archive.org/web/20220210180820/https://en.opensuse.org/SDB:How_to_migrate_to_SLE>`__,                                                   
`[2] <https://archive.today/2022.03.10-225629/https://en.opensuse.org/SDB:How_to_migrate_to_SLE>`__) 
if you decide vendor support is preferred at a later point.

VMWare still doesn't officially support Leap 15.3 as VM on vSphere neither allows Guest Customization, 
but for sure, when you run SLES 15 SP3 it's not a problem and fully supported?!

As explained `here <https://cstan.io/?p=12416&lang=en>`__ 
(Archive: `[1] <https://web.archive.org/web/20210420173348/https://cstan.io/?p=12416&lang=en>`__,                                                   
`[2] <https://archive.today/2022.03.10-225051/https://cstan.io/?p=12416&lang=en>`__) in regards to Leap 15.2, 
one option is to replace to content of :code:`/etc/issue` with :code:`SUSE Linux Enterprise Server 15`.

Keep in mind that :code:`/etc/issue` is a symlink to :code:`/run/issue`, a *volatile and temporary file*, 
managed by systemd service :code:`issue-generator`. So you have to remove the symlink and create a new 
:code:`/etc/issue` file, otherwise your changes will be lost after the next reboot.

.. code-block::

  sudo rm /etc/issue && echo "SUSE Linux Enterprise Server 15" > /etc/issue

In addition I had to change the OS Type in the VM Settings on vSphere to "SUSE Linux Enterprise Server 15" as well, 
otherwise the Guest Customization couldn't even be started without an error message.

I like the generated issue file and the additional information, so after the new deployed VM is up and running, let's just revert the change:

.. code-block::

  sudo rm /etc/issue && ln -s /run/issue /etc/issue

Little more complicated, but also possible, is to replace :code:`/etc/os-release` with the content 
from a SLES 15 SP3 System. It has the same effect as changing :code:`/etc/issue`, the Guest 
Customization will think it's a SUSE Linux Enterprise Server and apply all settings.

.. code-block::

  NAME="SLES"
  VERSION="15-SP3"
  VERSION_ID="15.3"
  PRETTY_NAME="SUSE Linux Enterprise Server 15 SP3"
  ID="sles"
  ID_LIKE="suse"
  ANSI_COLOR="0;32"
  CPE_NAME="cpe:/o:suse:sles:15:sp3"

