.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

vCloud Usage Meter 4.5 Upgrade - Error(908) Command line option is invalid: --skipdigest
########################################################################################

:date: 2022-03-29
:modified: 2022-03-29
:tags: vCloud, VMWare, vSphere, Error, Upgrade
:description: Usage Meter Upgrade (upgrade-um.sh) failed, tdnf: No such option --skipdigest
:category: Linux
:slug: vcloud_usage_meter_45_upgrade_error_908_command_line_option_is_invalid_skipdigest
:author: Dominik Wombacher
:lang: en
:transid: vcloud_usage_meter_45_upgrade_error_908_command_line_option_is_invalid_skipdigest 
:status: published

Again a interesting bug, this time during the In-Place Upgrade of a VMWare vCloud Usage Meter 
from Version 4.4 to 4.5, which shouldn't be a big deal based on the 
`official Upgrade Guide <https://docs.vmware.com/en/vCloud-Usage-Meter/4.5/Getting-Started-vCloud-Usage-Meter/GUID-AE5A81E1-097A-4EED-9A8E-8BF7E0B378A4.html>`__
(Archive: `[1] <https://web.archive.org/web/20220329202039/https://docs.vmware.com/en/vCloud-Usage-Meter/4.5/Getting-Started-vCloud-Usage-Meter/GUID-AE5A81E1-097A-4EED-9A8E-8BF7E0B378A4.html>`__,
`[2] <https://archive.today/2022.03.29-201847/https://docs.vmware.com/en/vCloud-Usage-Meter/4.5/Getting-Started-vCloud-Usage-Meter/GUID-AE5A81E1-097A-4EED-9A8E-8BF7E0B378A4.html>`__).

Running :code:`bash /root/upgrade/upgrade-um.sh` ended in:

.. code-block:: 

  Error(908) : Command line error: option is invalid.
  No such option: --skipdigest. Please use /usr/bin/tdnf --help
  Upgrade fail during JRE update. Please, revert to latest snapshot and prior update execute 'tdnf clean cache'.`

I followed all steps exactly as described in the Guide so how is it possible that the Upgrade Script triggers :code:`tdnf` with unavailable options? 
Couldn't find anything related / similar in the VMWare KB, GitHub and a good old Google / DuckDuckGo Search.

Based on our internal documentation, we installed the Usage Meter a while back in Version 4.1 
and upgraded to 4.4 a year ago, probably there was also a 4.2 and / or 4.3 upgrade before. 

The result of :code:`tdnf --version` was a quite outdated version :code:`tdnf: 1.2.3` which seem to be released around mid of 2017, 
but option :code:`--skipdigest` was part of a `commit <https://github.com/vmware/tdnf/commit/7f23f9c2f5b5976d2ccd443ddc2b84e00cba81d0>`__
(Archive: `[1] <https://web.archive.org/web/20220329202918/https://github.com/vmware/tdnf/commit/7f23f9c2f5b5976d2ccd443ddc2b84e00cba81d0>`__,
`[2] <https://archive.today/2022.03.29-202915/https://github.com/vmware/tdnf/commit/7f23f9c2f5b5976d2ccd443ddc2b84e00cba81d0>`__) on April 12 2019.

vCloud Usage Meter is running on VMware Photon OS, *just* another Linux Distribution with yum as package manager and attached online repositories. 
So let's just try to update **tdnf** manually via :code:`yum update tdnf`:

.. code-block::

	Upgrading:
	rpm-libs          x86_64      4.14.3-1.ph3      photon-updates      937.03k 959523
	rpm               x86_64      4.14.3-1.ph3      photon-updates      356.38k 364930
	hawkey            x86_64      2017.1-8.ph3      photon-updates      150.05k 153656
	tdnf-cli-libs     x86_64      3.1.8-1.ph3       photon-updates       70.18k 71864
	tdnf              x86_64      3.1.8-1.ph3       photon-updates      309.71k 317139

	Total installed size:   1.78M 1867112

	Is this ok [y/N]: y

Looks good, installation of version :code:`tdnf: 3.1.8` was successful, a quick test, which ended earlier in the same *Error(908)* as above, 
worked this time, so obviously this version is new enough to know the option :code:`--skipdigest`:

.. code-block::

	tdnf update --skipdigest vmware-jre

Afterwards I could just follow the Guide from VMWare to perform the In-Place Upgrade to Version 4.5 without any further issues. 
I assume something went wrong during earlier Upgrades and :code:`tdnf` was never updated after the initial Installation. 
Earlier Upgrade Scripts probably didn't used the :code:`--skipdigest` option, so it was undetected until now.

All this would explain why no one else seem to hit that bug, was probably a rare edge case limited to our Environment.

