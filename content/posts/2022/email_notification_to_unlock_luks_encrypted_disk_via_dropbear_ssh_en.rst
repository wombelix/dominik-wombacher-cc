EMail Notification to Unlock LUKS encrypted disk via Dropbear SSH
#################################################################

:date: 2022-03-16
:modified: 2022-03-16
:tags: Debian, Proxmox, Dropbear, SSH, LUKS, EMail
:description: Get notified by mail when your System is waiting to be unlocked
:category: Linux
:slug: email_notification_to_unlock_luks_encrypted_disk_via_dropbear_ssh
:author: Dominik Wombacher
:lang: en
:transid: email_notification_to_unlock_luks_encrypted_disk_via_dropbear_ssh 
:status: published

I'm running Proxmox VE Hosts with full encrypted disks and Dropbear SSH to unlock them remotely. 
I wanted to get notified when I have to login and enter the key, e.g. in case of an unexpected reboot. 

My setup is based on the `mailjet <https://www.mailjet.com>`_ Free Tier (6000 Mails / Month, 200 Mails / Day) 
and some initramfs customizing to include curl, a few other required libraries and 
a simple script to send an API request, tested on PVE 7.1 / Debian 11 (bullseye)

I will enclose placeholder in **< >**, please replace them with appropriate values based on your Environment.

The hook script :code:`/etc/initramfs-tools/hooks/curl` take care that *curl*, 
*libnss_dns* and a *resolv.conf* are included in the initramfs:

.. code-block:: bash

  #!/bin/sh

  PREREQ=""

  prereqs()
  {
          echo "$PREREQ"
  }

  case $1 in
  prereqs)
          prereqs
          exit 0
          ;;
  esac

  . /usr/share/initramfs-tools/hook-functions

  copy_exec /usr/bin/curl /bin

  # Fix DNS resolver
  cp -a /usr/lib/x86_64-linux-gnu/libnss_dns* $DESTDIR/usr/lib/x86_64-linux-gnu/
  printf "nameserver <dns_server1_ipv4_address>\nnameserver <dns_server2_ipv4_address>\n" > $DESTDIR/etc/resolv.conf

The actual notification will be send by :code:`/etc/initramfs-tools/scripts/init-premount/notification` through the mailjet API. 
You shouldn't have a problem to adjust it to use any other Service as long you can trigger a API via curl :)

.. code-block:: bash

  #!/bin/sh

  PREREQ=""

  prereqs()
  {
          echo "$PREREQ"
  }

  case $1 in
  prereqs)
          prereqs
          exit 0
          ;;
  esac

  . /scripts/functions

  configure_networking

  /bin/curl --insecure -s \
  -X POST \
  --user "<mailjet_api_user>:<mailjet_api_pass>" \
  https://api.mailjet.com/v3.1/send \
  -H 'Content-Type: application/json' \
  -d '{
    "Messages":[
      {
        "From": {
          "Email": "<sender_email>",
          "Name": "<sender_name>"
        },
        "To": [
          {
            "Email": "<recipient_mail>",
            "Name": "<recipient_name>"
          },
          {
            "Email": "<recipient2_mail>",
            "Name": "Pushover"
          }        
        ],
        "Subject": "Action required: Unlock <fqdn>!",
        "TextPart": "Server <fqdn> was restarted and need to be unlocked to proceed boot sequence.",
        "CustomID": "DropbearUnlockRequest"
      }
    ]
  }'

I'm also using `Pushover <https://pushover.net>`_ to receive notifications on my mobile, they offer mail2push, 
so I just added my personal pushover address as second recipient to get notified by Mail and Pushover.

Make both scripts executable:

.. code-block::

  chmod +x /etc/initramfs-tools/hooks/curl`
  chmod +x /etc/initramfs-tools/scripts/init-premount/notification

Run :code:`update-initramfs -u` and you are good to go, during the next reboot you should receive 
an Email Notification to enter your LUKS Key and unlock your disk.

