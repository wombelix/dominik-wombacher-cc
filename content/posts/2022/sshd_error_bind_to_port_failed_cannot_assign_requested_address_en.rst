sshd error - Bind to port failed: Cannot assign requested address
#################################################################

:date: 2022-03-02
:modified: 2022-03-02
:tags: sshd, error, failed, system, linux, debian
:description: sshd failed to start on boot when ListenAddress configured
:category: Linux
:slug: sshd_error_bind_to_port_failed_cannot_assign_requested_address
:author: Dominik Wombacher
:lang: en
:transid: sshd_error_bind_to_port_failed_cannot_assign_requested_address 
:status: published

I faced a very weird issue today, sshd failed to start on boot because *ListenAddress* was set 
but *network.target* doesn't mean IP addresses are already assigned and ready. So the configured 
IP isn't available, therefore sshd can't bind a Port and failed with *fatal: Cannot bind any address*.

I thought this can be fixed by adjusting the sshd systemd unit, everything I found online also pointed 
into that direction, for example a `Debian <https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=982950>`__
(Archive: `[1] <https://web.archive.org/web/20220302224510/https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=982950>`__,
`[2] <https://archive.today/2022.03.02-224450/https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=982950>`__) 
and `Ubuntu <https://bugs.launchpad.net/ubuntu/+source/openssh/+bug/216847/>`__
(Archive: `[1] <https://web.archive.org/web/20210901133033/https://bugs.launchpad.net/ubuntu/+source/openssh/+bug/216847/>`__,
`[2] <https://archive.today/2022.03.02-224617/https://bugs.launchpad.net/ubuntu/+source/openssh/+bug/216847/>`__) Bug report.

.. code-block:: 

  /etc/systemd/system/ssh.service.d/override.conf

  [Unit]
  After=network-online.target auditd.service

The above systemd override seem to be one of the popular solutions which works for a lot of people. 
Unfortunately none of the various After/Wants combinations worked in my case on Debian 11.

I had to go with the workaround to allow system wide port binding to not (yet) assigned IP addresses 
by adjusting two sysctl values as described on `serverfault <https://serverfault.com/a/941426>`__
(Archive: `[1] <https://web.archive.org/web/20220302224659/https://serverfault.com/questions/941421/servers-fail-to-bind-to-addresses-at-boot/941426>`__,
`[2] <https://archive.today/2022.03.02-224737/https://serverfault.com/questions/941421/servers-fail-to-bind-to-addresses-at-boot/941426%23941426>`__).

.. code-block:: 
  
  net.ipv4.ip_nonlocal_bind=1
  net.ipv6.ip_nonlocal_bind=1

Probably not the most elegant solution but it's working and due to the fact that multiple IP addresses are 
assigned to the Server, I have to specify on which the SSH Daemon is listening and can't just let em bind to all.
