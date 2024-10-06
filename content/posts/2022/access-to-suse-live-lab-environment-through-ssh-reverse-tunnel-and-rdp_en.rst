.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Access to SUSE Live Lab Environment through SSH reverse Tunnel and RDP
######################################################################

:date: 2022-09-10
:modified: 2024-10-06
:tags: SUSE, Training, Lab, SSH, RDP, Tunnel
:description: RDP to SUSE Lab via SSH reverse Tunnel
:category: Linux
:slug: access-to-suse-live-lab-environment-through-ssh-reverse-tunnel-and-rdp
:author: Dominik Wombacher
:lang: en
:transid: access-to-suse-live-lab-environment-through-ssh-reverse-tunnel-and-rdp 
:status: published

SUSE provides some great Training Courses with a lot of Exercises and Online Labs are also available for most of them. 
But, at least in the Environment available to SUSE Partners, the Labs can only be accessed through a Browser, 
with a fixed size of 1080x800, no support for Resize, Full-screen or Copy/Paste. 

**Update 2024-10-06**: There is a new *Open in new window* button available which allows higher resolutions than 1080x800 because it uses the full browser window. But all other limitations are the same since I wrote about it two years ago. Therefore I still prefer to reverse tunnel into the Lab machine and use an RDP client as explained in this post.

The Tech Stack used to provide those access: 
`hastexo XBlock <https://github.com/hastexo/hastexo-xblock>`__
(Archive: `[1] <https://web.archive.org/web/20200914165434/https://github.com/hastexo/hastexo-xblock>`__,
`[2] <https://archive.today/2022.09.10-092646/https://github.com/hastexo/hastexo-xblock>`__), 
`Apache Guacamole <https://guacamole.apache.org>`__
(Archive: `[1] <https://web.archive.org/web/20220829145641/https://guacamole.apache.org/>`__,
`[2] <https://archive.today/2020.06.25-070620/https://guacamole.apache.org/>`__), and 
`Open edX <https://openedx.org>`__
(Archive: `[1] <https://web.archive.org/web/20220901141818/https://openedx.org/>`__,
`[2] <https://archive.today/2022.04.01-170921/https://openedx.org/>`__).

As much I love the provided Trainings, that's just not really comfortable in my opinion. 
It's fine for a few quick Exercises, but if you have some complex ones or do multiple hours of hands on Training, 
a more direct way to connect, with support for Full-screen and Copy/Paste, would be way better.

The alternative is to setup the Lab Environment locally, but that requires additional time and resources.

SUSE Labs are based on a *main* server, which runs all other virtual machines, relevant for the lab, via KVM. 
You always access this main server and from there you can either use SSH or the 
Virtual Machine Manager Console to connect to the other systems. 

The good thing, this *main* server has full Internet Access via NAT (IPv4), we can establish outgoing connections 
without restrictions and also have full root permissions. So by establishing a SSH Reverse Tunnel to a 
public server, as rendezvous point, it's possible to access the Lab Server quite easy via RDP, 
which is enabled by default, because of the used Tech Stack to provide Browser access.

.. code-block::

  -----------------------                                           ------------------------                
  | Local Workstation   |          -----------------------          | SUSE Live Lab Server |   ------------------------------
  |                     | tcp/22 > | VPS (Public Server) | < tcp/22 |                      | > | Other Lab Virtual Machines |
  | SSH Tunnel to VPS   |          -----------------------          | SSH Tunnel to VPS    |   ------------------------------
  | Outgoing Connection |                                           | Outgoing Connection  |
  -----------------------                                           ------------------------
                                 
      localhost:3389         >            SSH Tunnel            >        localhost:3389

Steps:

  1) Create VPS

  - Any cheap Virtual Machine, for example `Hetzner Cloud (Referral Link) <https://hetzner.cloud/?ref=9YU0qvtaSmQI>`_ 
    with Public IPv4 address does the trick, you can also re-use any Server you might already have.

  2) Create additional User Account on the VPS used for SSH Tunneling

  - You have to type the User and Password into the SUSE Live Lab Server (no copy/paste), 
    so I picked something simple and didn't used my regular User for the tunneling, but it's up to you.

  3) Establish a SSH Reverse Tunnel from the Lab Server to the VPS and also from your local Workstation to the VPS

  - The commands used below are based on the Article 
    `SSH tunnel between two servers behind firewalls <https://www.sweetprocess.com/procedures/_AmM86Weq31FO0WDp5kRZFDBKRjB/ssh-tunnel-between-two-servers-behind-firewalls/>`__
    (Archive: `[1] <https://web.archive.org/web/20220910092054/https://www.sweetprocess.com/procedures/_AmM86Weq31FO0WDp5kRZFDBKRjB/ssh-tunnel-between-two-servers-behind-firewalls/>`__,
    `[2] <https://archive.today/2022.09.10-092054/https://www.sweetprocess.com/procedures/_AmM86Weq31FO0WDp5kRZFDBKRjB/ssh-tunnel-between-two-servers-behind-firewalls/>`__)

  4) Connect via RDP
  
  - I'm running openSUSE Tumbleweed and use Remmina, any other Client with RDP support will work as well.

  - It's a connection on your local Workstation to :code:`localhost:3389`, 
    which then goes through the established SSH Tunnel and hit Port 3389 (RDP) on the Lab Server.

Commands:

.. code-block::

  # VPS (Hetzner Cloud, CX11, Falkenstein Germany, 0.0071 € / hour, Rocky Linux 9)
  useradd -c "SSH Tunnel" -m -U sshtunnel
  passwd sshtunnel

  # SUSE Live Lab Server
  ssh -o TCPKeepAlive=no -o ServerAliveInterval=15 -nNT -R 3389:localhost:3389 sshtunnel@<vps-public-ip>

  # Local Workstation
  ssh -o TCPKeepAlive=no -o ServerAliveInterval=15 -nNT -L 3389:localhost:3389 sshtunnel@<vps-public-ip>

  # Lab Server
  # The password for user "tux" is unknown so you have to reset it
  sudo su -
  passwd tux

  # Local Workstation
  # Open an RDP Client, connect to localhost as user "tux" with the password you set earlier on the Lab Server

Important: 

  1) Leave the Web Browser with the Live Lab HTML Viewer open, if you close it the VM will be suspended, 
  keep an eye on it, move the mouse from time to time when the windows is active or click the confirmation 
  that you still want to keep the VM running when you are inactive for a while.

  2) This *hack* will affect the access to the lab server through the Browser, you will see a 
  **login failed for display :0** error message, click ok and on the XRDP prompt, select **xorg**, 
  user **tux** and the password you set earlier.

This is just a quick & dirty way to interact a little more comfortable with the Lab Environment, 
you can tunnel through SSH whatever you want, SSH Sessions or X Forwarding, whatever you prefer.

Especially the fact that your VM get suspended when you leave the website, makes it not really reliable, 
but for me it worked quite well to prepare for some Exams.

Happy hacking and enjoy your next SUSE Training :)
