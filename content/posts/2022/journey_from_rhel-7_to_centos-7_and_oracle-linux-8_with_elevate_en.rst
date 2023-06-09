.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Journey from RHEL 7 to CentOS 7 and Oracle Linux 8 with elevate
###############################################################

:date: 2022-03-28
:modified: 2022-03-28
:tags: RHEL, CentOS, OracleLinux, elevate
:description: Migration and In-Place Upgrade from RHEL 7 to Oracle Linux 8
:category: Linux
:slug: journey_from_rhel-7_to_centos-7_and_oracle-linux-8_with_elevate
:author: Dominik Wombacher
:lang: en
:transid: journey_from_rhel-7_to_centos-7_and_oracle-linux-8_with_elevate 
:status: published

From a technical point of view, every Red Hat Enterprise Linux derivate is as good as the original. 
If you are happy with community support, your use case doesn't require a specific vendor and their 
support services, you can choose from a lot of really good options.

At work we still have some RHEL 7 VMs in our Management Environment where 
we actually don't need any sort of support subscriptions. 
If there is anything broken, we have to fix it on our own, nothing where, 
in this case, Red Hat could and will help us.

But to have at least the option to pay for vendor support again, 
something you need in larger companies to calm down your management, 
we opted to migrate RHEL 7 Systems to `Oracle Linux <https://linux.oracle.com/>`_, 
even though I would personally pick `RockyLinux <https://rockylinux.org>`_ because of the community behind it.

The migration will be done in two Steps:

  1) From RHEL 7 to latest CentOS 7 release
  2) From CentOS 7 to Oracle Linux 8

Step 1 feels a little "hacky" and involves some manual steps, for Step 2 
we going to use `elevate from AlmaLinux <https://almalinux.org/elevate>`_.

I will not talk about RHEL 7 > CentOS 7 in detail, just some notes about potential pitfalls, 
there are tons of guides out to about that topic, for example 
`this one <https://jensd.be/32/linux/migrate-rhel7-to-centos7>`__
(Archive: `[1] <https://web.archive.org/web/20210721094132/https://jensd.be/32/linux/migrate-rhel7-to-centos7>`__,
`[2] <https://archive.today/2022.03.28-213128/https://jensd.be/32/linux/migrate-rhel7-to-centos7>`__), 
`this one <https://www.openlogic.com/blog/step-step-migration-rhel-74-centos-74>`__
(Archive: `[1] <https://web.archive.org/web/20220328213141/https://www.openlogic.com/blog/step-step-migration-rhel-74-centos-74>`__,
`[2] <https://archive.today/2022.03.28-213154/https://www.openlogic.com/blog/step-step-migration-rhel-74-centos-74>`__) or 
`this one <https://wiki.centos.org/HowTos/MigrationGuide>`__
(Archive: `[1] <https://web.archive.org/web/20220131030128/https://wiki.centos.org/HowTos/MigrationGuide>`__,
`[2] <https://archive.today/2022.03.28-213214/https://wiki.centos.org/HowTos/MigrationGuide>`__).

Some things you should keep in mind during RHEL 7 to CentOS 7:

  - If you use a HTTP Proxy, configure it correctly on OS Level and ensure the mirrors you going to use are whitelisted
  - You have a Red Hat Satellite 6 Server running and the VM registered? Remove also those packages when removing all other redhat / rhn related ones.
  - Disable, or even better, remove the subscription manager, you don't need it anymore and it will cause problems otherwise
  - Verify that there is enough free space available, you will probably need ~2GB for new downloaded packages

In-Place Upgrade from Enterprise Linux 7 to 8 is technically possible and something Red Hat even officially support for RHEL 7 to RHEL 8. 
It uses the leapp framework under the hood, which is also the basis of AlmaLinux elevate Project. They describe it as following:  
:code:`ELevate enables migration between major versions of RHEL® derivatives. Easily go from CentOS 7.x to any 8.x of your choice`.

So with the help of elevate we can jump directly from CentOS 7 to Oracle Linux 8 without much trouble? Let's see how that goes.

I followed the `elevate Quickstart Guide <https://wiki.almalinux.org/elevate/ELevate-quickstart-guide.html>`__
(Archive: `[1] <https://web.archive.org/web/20211108171501/https://wiki.almalinux.org/elevate/ELevate-quickstart-guide.html>`__,
`[2] <https://archive.today/2022.03.28-214850/https://wiki.almalinux.org/elevate/ELevate-quickstart-guide.html>`__), 
which works almost as easy as promised:

.. code-block::
  
  yum install -y http://repo.almalinux.org/elevate/elevate-release-latest-el7.noarch.rpm
  yum install -y leapp-upgrade leapp-data-oraclelinux
  yum remove subscription-manager* # If not already done, this is the right moment ;)
  rmmod pata_acpi
  leapp answer --section remove_pam_pkcs11_module_check.confirm=True  
  leapp preupgrade

In case you see the following error message and are worried, you can 
`ignore it <https://bugzilla.redhat.com/show_bug.cgi?id=1747444>`__
(Archive: `[1] <https://web.archive.org/web/20220328215806/https://bugzilla.redhat.com/show_bug.cgi?id=1747444>`__,
`[2] <https://archive.today/2022.03.28-215731/https://bugzilla.redhat.com/show_bug.cgi?id=1747444>`__):

.. code-block:: 

  2022-03-25 15:26:22.757 DEBUG    PID: 18014 leapp.workflow.TargetTransactionFactsCollection.target_userspace_creator: Failed to create directory /var/lib/leapp/scratch/mounts/root_/system_overlay//sys/fs/selinux: Read-only file system
  2022-03-25 15:26:22.774 DEBUG    PID: 18014 leapp.workflow.TargetTransactionFactsCollection.target_userspace_creator: Failed to create directory /var/lib/leapp/scratch/mounts/root_/system_overlay//sys/fs/selinux: Read-only file system

Here comes the most important part if you have to use a http proxy to reach the internet, as I have to, which will by default just fail:

.. code-block::

  Loaded plugins: builddep, changelog, config-manager, copr, debug, debuginfo-install, download, generate_completion_cache, needs-restarting, playground, repoclosure, repodiff, repograph, repomanage, reposync
  DNF version: 4.0.9
  cachedir: /el8target/var/cache/dnf
  Unknown configuration option: autorefresh = 1 in /etc/yum.repos.d/elasticsearch.repo
  repo: downloading from remote: ol8_codeready_builder
  Oracle Linux 8 CodeReady Builder (x86_64)       0.0  B/s |   0  B     00:00
  Cannot download 'https://yum.oracle.com/repo/OracleLinux/OL8/codeready/builder/x86_64/': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried.
  repo: downloading from remote: ol8_addons
  Oracle Linux 8 Addons (x86_64)                  0.0  B/s |   0  B     00:00
  Cannot download 'https://yum.oracle.com/repo/OracleLinux/OL8/addons/x86_64/': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried.
  repo: downloading from remote: ol8_appstream
  Oracle Linux 8 Application Stream (x86_64)      0.0  B/s |   0  B     00:00
  Cannot download 'https://yum.oracle.com/repo/OracleLinux/OL8/appstream/x86_64/': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried.
  repo: downloading from remote: ol8_baseos_latest
  Oracle Linux 8 BaseOS Latest (x86_64)           0.0  B/s |   0  B     00:00
  Cannot download 'https://yum.oracle.com/repo/OracleLinux/OL8/baseos/latest/x86_64/': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried.
  repo: downloading from remote: ol8_UEKR6
  Latest Unbreakable Enterprise Kernel Release 6  0.0  B/s |   0  B     00:00
  Failed to synchronize cache for repo 'ol8_codeready_builder', ignoring this repo.
  Failed to synchronize cache for repo 'ol8_addons', ignoring this repo.
  Failed Cannot download 'https://yum.oracle.com/repo/OracleLinux/OL8/UEKR6/x86_64/': Cannot download repomd.xml: Cannot download repodata/repomd.xml: All mirrors were tried.
  No module defaults found
  No match for argument: dnf
  to synchronize cache for repo 'ol8_appstream', ignoring this repo.
  Failed to synNo match for argument: dnf-command(config-manager)
  chronize cache for repo 'ol8_baseos_latest', ignoring this repo.
  Failed to synchronize cache for repo 'ol8_UEKR6', ignoring this repo.
  Error: Unable to find a match: dnf dnf-command(config-manager)

Let's `configure the proxy in the leapp repo file <https://docs.oracle.com/en/operating-systems/oracle-linux/8/leapp/chap-leapp-upgrade.html#preupgrade-report>`__
(Archive: `[1] <https://web.archive.org/web/20220328220402/https://docs.oracle.com/en/operating-systems/oracle-linux/8/leapp/chap-leapp-upgrade.html>`__,
`[2] <https://archive.today/2022.03.28-220359/https://docs.oracle.com/en/operating-systems/oracle-linux/8/leapp/chap-leapp-upgrade.html%23preupgrade-report>`__), 
adjust the placeholder *<proxy>* based on your needs:

.. code-block:: 

  sed -i '/^enabled=.*/a proxy=<proxy>' /etc/leapp/files/leapp_upgrade_repositories.repo

Again the advice to take a look at your available space, you will need ~2GB on :code:`/var/cache` for the OL8 packages that leapp is going to download, otherwise you will see some nice error messages like:

.. code-block::

  (742/943): gpm-libs-1.20.7-17.el8.x86_64.rpm    2.4 MB/s |  39 kB     00:00
  [MIRROR] golang-bin-1.16.12-1.module+el8.5.0+20456+eee863d9.x86_64.rpm: Curl error (23): Failed writing received data to disk/application for https://yum.oracle.com/repo/OracleLinux/OL8/appstream/x86_64/getPackage/golang-bin-1.16.12-1.module%2bel8.5.0%2b20456%2beee863d9.x86_64.rpm [Failed writing body (924 != 16384)]
  Process Process-425:
  Traceback (most recent call last):
    File "/usr/lib64/python2.7/multiprocessing/process.py", line 258, in _bootstrap
      self.run()
    File "/usr/lib64/python2.7/multiprocessing/process.py", line 114, in run
      self._target(self._args, *self._kwargs)
    File "/usr/lib/python2.7/site-packages/leapp/repository/actor_definition.py", line 72, in _do_run
      actor_instance.run(args, *kwargs)
    File "/usr/lib/python2.7/site-packages/leapp/actors/_init_.py", line 335, in run
      self.process(*args)
    File "/usr/share/leapp-repository/repositories/system_upgrade/common/actors/dnfpackagedownload/actor.py", line 48, in process
      xfs_info=xfs_info, storage_info=storage_info, plugin_info=plugin_info, on_aws=on_aws
    File "/usr/share/leapp-repository/repositories/system_upgrade/common/libraries/dnfplugin.py", line 344, in perform_rpm_download
      test=True, on_aws=on_aws
    File "/usr/lib64/python2.7/contextlib.py", line 35, in _exit_
      self.gen.throw(type, value, traceback)
      yield overlay
    File "/usr/share/leapp-repository/repositories/system_upgrade/common/libraries/mounting.py", line 367, in _exit_
      self.umount()
    File "/usr/share/leapp-repository/repositories/system_upgrade/common/libraries/mounting.py", line 360, in umount
      self._cleanup()
    File "/usr/share/leapp-repository/repositories/system_upgrade/common/libraries/mounting.py", line 326, in _cleanup
      run(['umount', '-fl', self.target], split=False)
    File "/usr/lib/python2.7/site-packages/leapp/libraries/stdlib/_init_.py", line 175, in run
      api.current_logger().debug('External command has started: {0}'.format(str(args)))
    File "/usr/lib64/python2.7/logging/_init_.py", line 1137, in debug
      self._log(DEBUG, msg, args, **kwargs)
    File "/usr/lib64/python2.7/logging/_init_.py", line 1268, in _log
      self.handle(record)
    File "/usr/lib64/python2.7/logging/_init_.py", line 1278, in handle
      self.callHandlers(record)
    File "/usr/lib64/python2.7/logging/_init_.py", line 1318, in callHandlers
      hdlr.handle(record)
    File "/usr/lib64/python2.7/logging/_init_.py", line 749, in handle
      self.emit(record)
    File "/usr/lib/python2.7/site-packages/leapp/logger/_init_.py", line 40, in emit
      self._do_emit(log_data)
    File "/usr/lib/python2.7/site-packages/leapp/logger/_init_.py", line 45, in _do_emit
      Audit(**log_data).store()
    File "/usr/lib/python2.7/site-packages/leapp/utils/audit/_init_.py", line 88, in store
      self.do_store(connection)
    File "/usr/lib/python2.7/site-packages/leapp/utils/audit/_init_.py", line 371, in do_store
      self.message.message_id if self.message else None, self.data))
  OperationalError: unable to open database file
  [

  =====================================================================================================
  Actor dnf_package_download unexpectedly terminated with exit code: 1 - Please check the above details
  =====================================================================================================

If you are ready, run :code:`leapp preupgrade` again, should complete without errors this time.

.. code-block::

  A reboot is required to continue. Please reboot your system.

  Debug output written to /var/log/leapp/leapp-upgrade.log

  ============================================================
                             REPORT
  ============================================================

  A report has been generated at /var/log/leapp/leapp-report.json
  A report has been generated at /var/log/leapp/leapp-report.txt

  ============================================================
                         END OF REPORT
  ============================================================

Reboot your VM and, if available, watch the rest of the Upgrade through the VMWare / KVM or whatever other Console your Hypervisor provides. 
It will boot into *ELevate-Upgrade-Initramfs*, perform the whole CentOS 7 to Oracle Linux 8 magic and boot into your new OL8 System afterwards.

Some additional steps I did as soon the System was up and running again:

.. code-block:: 

  alternatives --set python /usr/bin/python3
  # link 'python' to 'python3' for backward compatibility

  dnf remove puppet
  # we don't need the old puppet agent which was connected to satellite, forgot to remove it earlier...

  cat /etc/redhat-release
  cat /etc/os-release
  rpm -qa | grep centos
  rpm -qa | grep el7
  # Verify that we running on the expected OS, in case of some el7 leftover, check if that's related to installed applications that might also require a update

  dnf clean
  dnf upgrade

  grubby --set-default /boot/vmlinuz-5.4.17-2136.305.5.3.el8uek.x86_64
  # Change from Standard EL8 Kernel to OL UEK

  reboot

And that's it, except the extra step to configure http proxy, which isn't mention in the AlmaLinux Quickstart Guide yet, 
it went very smoothly and seem to result in a stable system, so far I'm happy with the results and can recommend to give elevate a try.
 
