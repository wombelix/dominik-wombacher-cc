Customized openSUSE Images, to run on Proxmox VE out of the box, build on OBS
#############################################################################

:date: 2022-04-26
:modified: 2022-04-26
:tags: openSUSE, OBS, Proxmox, Linux, cloud-init
:description: Building openSUSE Images for PVE on OBS
:category: Linux
:slug: customized_opensuse_images_to_run_on_proxmox_ve_out_of_the_box_build_on_obs 
:author: Dominik Wombacher
:lang: en
:transid: customized_opensuse_images_to_run_on_proxmox_ve_out_of_the_box_build_on_obs 
:status: published

I'm using openSUSE whenever possible but had some trouble to use the official images on `Proxmox <https://proxmox.com>`_. 
There is mostly a :code:`kvm-and-xen` image available, but that doesn't contain :code:`cloud-init` 
and / or :code:`qemu-guest-agent`, but for my use case, automated IPv6-only deployments, both are mandatory. 

Proxmox supports *cloud-init* to configure basics like search domain, nameserver, user, password and ssh key. 
If the *qemu-guest-agent* is installed, the IPv6 address configured via SLAAC is available through the 
API as soon the VM was booted.

In regards to openSUSE MicroOS the situation was even worse, only the :code:`OpenStack-Cloud` image 
includes *cloud-init* but relies on the package :code:`cloud-init-config-MicroOS` which installs a 
:code:`/etc/cloud/cloud.cfg` without a *default_user* section and enabled root user.

That way configuring a User account with sudo permissions via *cloud-init* will just not work.

So after some playing around with different approaches and especially due to the fact that I use a lot of different 
openSUSE Images, I decided to branch the relevant projects / packages on https://build.opensuse.org and let OBS do the 
heavy lifting for me to build and publish the different images.

Leap 15.3 and 15.4 required also an adjustment of the OBS Project Config, most important for automation was 
*staticlinks* to ensure the same link will work even after a new build.

.. code-block::

  %if "%_repository" == "images"
  Type: kiwi
  Repotype: staticlinks
  Patterntype: none
  %endif

  # slsaprovenance - as described at https://slsa.dev/provenance/v0.2
  BuildFlags: slsaprovenance

After some further testing, let's see which of my changes might be possible to get included upstream.

I'm also working on Proxmox VE "optimized" images for other Distributions like Rocky Linux or Debian, 
I will probably pick a different approach to customize them, but that's something for another Post some day.

.. contents::
        :local:

openSUSE MicroOS
================

Open Build Service (OBS) Project
--------------------------------

https://build.opensuse.org/package/show/home:wombelix:branches:devel:kubic:images/openSUSE-MicroOS

Download
--------

Local Webserver (Manual Sync): https://dominik.wombacher.cc/~files/proxmox_ve_kvm_images/

openSUSE Mirror (Automatic Build / Sync): https://download.opensuse.org/repositories/home:/wombelix:/branches:/devel:/kubic:/images/openSUSE_Tumbleweed/

Customizations
--------------

Please be aware: The below diff should give you an idea about the changes, it will not be updated, please check the OBS Project for the latest revision

.. code-block:: diff

  Index: _multibuild
  ===================================================================
  --- _multibuild (revision 105)
  +++ _multibuild (revision 8)
  @@ -1,8 +1,15 @@
   <multibuild>
  +        <flavor>pve</flavor>
  +        <flavor>ContainerHost-pve</flavor>
  +        <flavor>Kubic-kubeadm-pve</flavor>
  +        <flavor>k3s-pve</flavor>
  +        
           <!-- Special case: Pi2, VBox and onie only get plain MicroOS -->
  +        <!--
           <flavor>RaspberryPi2</flavor>
           <flavor>VirtualBox</flavor>
           <flavor>onie</flavor>
  +        -->
           <!--
                   for a in kvm-and-xen VMware MS-HyperV OpenStack-Cloud Pine64 Rock64 RaspberryPi Vagrant hardware; do
                           for f in "" "ContainerHost-" "Kubic-kubeadm-"; do
  @@ -10,6 +17,7 @@
                           done
                   done
           -->
  +        <!--
           <flavor>kvm-and-xen</flavor>
           <flavor>ContainerHost-kvm-and-xen</flavor>
           <flavor>Kubic-kubeadm-kvm-and-xen</flavor>
  @@ -48,4 +56,5 @@
           <flavor>k3s-Vagrant</flavor>
           <flavor>k3s-SelfInstall</flavor>
           <flavor>k3s-DigitalOcean-Cloud</flavor>
  +        -->
   </multibuild>


  Index: config.sh
  ===================================================================
  --- config.sh (revision 105)
  +++ config.sh (revision 8)
  @@ -157,6 +157,7 @@
  
   ignition_platform='metal'
   case "${kiwi_profiles}" in
  +	*pve*) ignition_platform='qemu' ;;
   	*kvm*) ignition_platform='qemu' ;;
   	*DigitalOcean*) ignition_platform='digitalocean' ;;
   	*VMware*) ignition_platform='vmware' ;;
  @@ -281,3 +282,21 @@
           chmod 0600 /home/vagrant/.ssh/authorized_keys
           chown -R vagrant /home/vagrant
   fi
  +
  +#======================================
  +# Configure PVE specifics
  +#--------------------------------------
  +if [[ "$kiwi_profiles" == *"pve"* ]]; then
  +	cat > /etc/cloud/cloud.cfg.d/default_user.cfg <<-EOF
  +		users:
  +		  - default
  +		disable_root: true
  +		system_info:
  +		  default_user:
  +		    name: geeko
  +		    lock_passwd: True
  +		    groups: [cdrom, users]
  +		    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
  +		    shell: /bin/bash
  +	EOF
  +fi


  Index: openSUSE-MicroOS.kiwi
  ===================================================================
  --- openSUSE-MicroOS.kiwi (revision 105)
  +++ openSUSE-MicroOS.kiwi (revision 8)
  @@ -13,6 +13,7 @@
           <profile name="k3s" description="MicroOS with k3s"/>
           <profile name="Kubic-kubeadm" description="MicroOS with CRI-O and kubeadm"/>
           <!-- Platforms -->
  +        <profile name="pve" description="Proxmox VE (pve) for x86_64" arch="x86_64"/>
           <profile name="kvm-and-xen" description="kvm-and-xen" arch="x86_64,aarch64"/>
           <profile name="VMware" description="VMware for x86_64" arch="x86_64"/>
           <profile name="MS-HyperV" description="Hyper-V for x86_64" arch="x86_64"/>
  @@ -27,6 +28,10 @@
           <profile name="SelfInstall" description="Self Installing Image" arch="x86_64,aarch64"/>
           <profile name="onie" description="ONIE Installer Image" arch="x86_64"/>
           <!-- Images (flavor + platform) -->
  +        <profile name="ContainerHost-pve" description="MicroOS with Podman for Proxmox VE (pve)" arch="x86_64">
  +            <requires profile="pve"/>
  +            <requires profile="ContainerHost"/>
  +        </profile>
           <profile name="ContainerHost-kvm-and-xen" description="MicroOS with Podman for KVM and HVM Xen" arch="x86_64,aarch64">
               <requires profile="kvm-and-xen"/>
               <requires profile="ContainerHost"/>
  @@ -59,6 +64,10 @@
               <requires profile="Vagrant"/>
               <requires profile="ContainerHost"/>
           </profile>
  +        <profile name="Kubic-kubeadm-pve" description="kubeadm with CRI-O for Proxmox VE (pve)" arch="x86_64">
  +            <requires profile="pve"/>
  +            <requires profile="Kubic-kubeadm"/>
  +        </profile>
           <profile name="Kubic-kubeadm-kvm-and-xen" description="kubeadm with CRI-O for KVM and HVM Xen" arch="x86_64,aarch64">
               <requires profile="kvm-and-xen"/>
               <requires profile="Kubic-kubeadm"/>
  @@ -103,6 +112,10 @@
               <requires profile="SelfInstall"/>
               <requires profile="Kubic-kubeadm"/>
           </profile>
  +        <profile name="k3s-pve" description="MicroOS with k3s for Proxmox VE (pve)" arch="x86_64">
  +            <requires profile="pve"/>
  +            <requires profile="k3s"/>
  +        </profile>
           <profile name="k3s-kvm-and-xen" description="MicroOS with k3s for KVM and HVM Xen" arch="x86_64,aarch64">
               <requires profile="kvm-and-xen"/>
               <requires profile="k3s"/>
  @@ -144,6 +157,39 @@
               <requires profile="k3s"/>
           </profile>
       </profiles>
  +    <preferences profiles="pve" arch="x86_64">
  +        <version>16.0.0</version>
  +        <packagemanager>zypper</packagemanager>
  +        <bootloader-theme>openSUSE</bootloader-theme>
  +        <rpm-excludedocs>true</rpm-excludedocs>
  +        <locale>en_US</locale>
  +        <type
  +            image="vmx"
  +            filesystem="btrfs"
  +            format="qcow2"
  +            firmware="uefi"
  +            bootpartition="false"
  +            bootkernel="custom"
  +            devicepersistency="by-uuid"
  +            btrfs_root_is_snapshot="true"
  +            btrfs_root_is_readonly_snapshot="true"
  +            btrfs_quota_groups="true"
  +            spare_part="5G" spare_part_mountpoint="/var" spare_part_fs="btrfs" spare_part_is_last="true" spare_part_fs_attributes="no-copy-on-write"
  +        >
  +            <bootloader name="grub2" console="gfxterm" />
  +            <systemdisk>
  +                <volume name="home"/>
  +                <volume name="root"/>
  +                <volume name="opt"/>
  +                <volume name="srv"/>
  +                <volume name="boot/grub2/i386-pc"/>
  +                <volume name="boot/grub2/x86_64-efi" mountpoint="boot/grub2/x86_64-efi"/>
  +                <volume name="boot/writable"/>
  +                <volume name="usr/local"/>
  +            </systemdisk>
  +            <size unit="G">20</size>
  +        </type>
  +    </preferences>
       <preferences profiles="kvm-and-xen" arch="x86_64">
           <version>16.0.0</version>
           <packagemanager>zypper</packagemanager>
  @@ -720,6 +766,10 @@
           <package name="patterns-containers-kubic_loadbalancer"/>
           <package name="patterns-containers-kubic_worker"/>
       </packages>
  +    <packages type="image" profiles="pve">
  +        <package name="qemu-guest-agent"/>
  +        <package name="patterns-microos-cloud"/>
  +    </packages>
       <packages type="image" profiles="kvm-and-xen">
           <!-- KVM and Xen specific packages -->
           <package name="xen-tools-domU" arch="x86_64"/>


openSUSE Tubmleweed JeOS
========================

Open Build Service (OBS) Project
--------------------------------

https://build.opensuse.org/package/show/home:wombelix:branches:Virtualization:Appliances:Images:openSUSE-Tumbleweed/kiwi-templates-JeOS

Download
--------

Local Webserver (Manual Sync): https://dominik.wombacher.cc/~files/proxmox_ve_kvm_images/

openSUSE Mirror (Automatic Build / Sync): https://download.opensuse.org/repositories/home:/wombelix:/branches:/Virtualization:/Appliances:/Images:/openSUSE-Tumbleweed/images/

Customizations
--------------

Please be aware: The below diff should give you an idea about the changes, it will not be updated, please check the OBS Project for the latest revision

.. code-block:: diff

  Index: JeOS.kiwi
  ===================================================================
  --- JeOS.kiwi (revision 70)
  +++ JeOS.kiwi (revision 2)
  @@ -9,6 +9,7 @@
           <specification>openSUSE Tumbleweed JeOS</specification>
       </description>
       <profiles>
  +        <profile name="pve" description="JeOS for Proxmox VE (pve)" arch="x86_64"/>
           <!-- Those two are only used as deps -->
           <profile name="kvm-and-xen" description="JeOS for KVM and Xen" arch="aarch64,x86_64"/>
           <profile name="VMware" description="JeOS for VMware" arch="x86_64"/>
  @@ -17,6 +18,39 @@
           <profile name="OpenStack-Cloud" description="JeOS for OpenStack Cloud" arch="x86_64"/>
           <profile name="RaspberryPi" description="JeOS for the Raspberry Pi" arch="aarch64"/>
       </profiles>
  +    <preferences profiles="pve" arch="x86_64">
  +        <version>15.1.0</version>
  +        <packagemanager>zypper</packagemanager>
  +        <bootloader-theme>openSUSE</bootloader-theme>
  +        <rpm-excludedocs>true</rpm-excludedocs>
  +        <type
  +            image="vmx"
  +            filesystem="btrfs"
  +            format="qcow2"
  +            bootloader="grub2"
  +            firmware="uefi"
  +            efipartsize="33"
  +            kernelcmdline="rw quiet systemd.show_status=1 console=ttyS0,115200 console=tty0"
  +            bootpartition="false"
  +            bootkernel="custom"
  +            devicepersistency="by-uuid"
  +            btrfs_quota_groups="true"
  +            btrfs_root_is_snapshot="true"
  +        >
  +            <systemdisk>
  +                <volume name="home"/>
  +                <volume name="root"/>
  +                <volume name="opt"/>
  +                <volume name="srv"/>
  +                <volume name="boot/grub2/i386-pc"/>
  +                <volume name="boot/grub2/x86_64-efi" mountpoint="boot/grub2/x86_64-efi"/>
  +                <volume name="usr/local"/>
  +                <volume name="var" copy_on_write="false"/>
  +            </systemdisk>
  +            <size unit="G">24</size>
  +        </type>
  +    </preferences>
  +
       <preferences profiles="kvm-and-xen" arch="x86_64">
           <version>15.1.0</version>
           <packagemanager>zypper</packagemanager>
  @@ -284,6 +318,15 @@
           <package name="zypper-needs-restarting"/> <!-- Some deployment script use this (bsc#1173548) -->
       </packages>
  
  +    <packages type="image" profiles="pve">
  +        <package name="btrfsprogs"/>
  +        <package name="btrfsmaintenance"/>
  +        <package name="grub2-snapper-plugin"/>
  +        <package name="snapper-zypp-plugin"/>
  +        <package name="snapper"/>
  +        <package name="firewalld"/>
  +    </packages>
  +  
       <!-- Not needed in OpenStack as it uses XFS and cloud-init -->
       <packages type="image" profiles="kvm-and-xen,VMware,MS-HyperV,RaspberryPi">
           <!-- Only for btrfs -->
  @@ -305,7 +348,7 @@
           <package name="firewalld"/>
       </packages>
  
  -    <packages type="image" profiles="kvm-and-xen,VMware,MS-HyperV,OpenStack-Cloud">
  +    <packages type="image" profiles="kvm-and-xen,VMware,MS-HyperV,OpenStack-Cloud,pve">
           <!-- Shim for secure boot everywhere except for RPi -->
           <package name="shim" arch="aarch64,x86_64"/>
       </packages>
  @@ -315,14 +358,14 @@
           <package name="xen-libs"/>
           <package name="kernel-default-base"/>
       </packages>
  -    <packages type="image" profiles="kvm-and-xen,OpenStack-Cloud">
  +    <packages type="image" profiles="kvm-and-xen,OpenStack-Cloud,pve">
           <package name="qemu-guest-agent"/>
       </packages>
       <packages type="image" profiles="VMware">
           <package name="open-vm-tools" arch="x86_64"/>
           <package name="kernel-default-base"/>
       </packages>
  -    <packages type="image" profiles="OpenStack-Cloud">
  +    <packages type="image" profiles="OpenStack-Cloud,pve">
           <package name="cloud-init"/>
           <package name="cloud-init-config-suse" />
           <package name="xfsprogs"/>
  @@ -360,7 +403,7 @@
           <package name="gzip"/>
       </packages>
  
  -    <packages type="bootstrap" profiles="kvm-and-xen">
  +    <packages type="bootstrap" profiles="kvm-and-xen,pve">
           <package name="openSUSE-release-appliance-kvm"/>
       </packages>
       <packages type="bootstrap" profiles="OpenStack-Cloud">


  Index: _multibuild
  ===================================================================
  --- _multibuild (revision 70)
  +++ _multibuild (revision 2)
  @@ -1,7 +1,10 @@
   <multibuild>
  +  <flavor>pve</flavor>
  +  <!--
     <flavor>kvm-and-xen</flavor>
     <flavor>VMware</flavor>
     <flavor>MS-HyperV</flavor>
     <flavor>OpenStack-Cloud</flavor>
     <flavor>RaspberryPi</flavor>
  +  -->
   </multibuild>


openSUSE Leap 15.3 JeOS
=======================

Open Build Service (OBS) Project
--------------------------------

https://build.opensuse.org/package/show/home:wombelix:branches:Virtualization:Appliances:Images:openSUSE-Leap-15.3/kiwi-templates-JeOS

Download
--------

Local Webserver (Manual Sync): https://dominik.wombacher.cc/~files/proxmox_ve_kvm_images/

openSUSE Mirror (Automatic Build / Sync): https://download.opensuse.org/repositories/home:/wombelix:/branches:/Virtualization:/Appliances:/Images:/openSUSE-Leap-15.3/images/

Customizations
--------------

Please be aware: The below diff should give you an idea about the changes, it will not be updated, please check the OBS Project for the latest revision

.. code-block:: diff

  Index: JeOS.kiwi
  ===================================================================
  --- JeOS.kiwi (revision 13)
  +++ JeOS.kiwi (revision 3)
  @@ -9,6 +9,7 @@
           <specification>openSUSE Leap 15.3 JeOS</specification>
       </description>
       <profiles>
  +        <profile name="pve" description="JeOS for Proxmox VE (pve)" arch="x86_64"/>
           <profile name="kvm-and-xen" description="JeOS for KVM and Xen" arch="x86_64"/>
           <profile name="kvm" description="JeOS for KVM" arch="aarch64"/>
           <profile name="VMware" description="JeOS for VMware" arch="x86_64"/>
  @@ -16,6 +17,47 @@
           <profile name="OpenStack-Cloud" description="JeOS for OpenStack Cloud" arch="x86_64"/>
           <profile name="RaspberryPi" description="JeOS for the Raspberry Pi" arch="aarch64"/>
       </profiles>
  +    <preferences profiles="pve">
  +        <version>15.3</version>
  +        <packagemanager>zypper</packagemanager>
  +        <bootsplash-theme>openSUSE</bootsplash-theme>
  +        <bootloader-theme>openSUSE</bootloader-theme>
  +    <!-- those settings are applied by suseConfig in config.sh
  +        <locale>en_US</locale>
  +        <keytable>us.map.gz</keytable>
  +        <timezone>Europe/Berlin</timezone>
  +        <hwclock>utc</hwclock>
  +    -->
  +        <rpm-excludedocs>true</rpm-excludedocs>
  +        <type
  +            image="vmx"
  +            filesystem="btrfs"
  +            format="qcow2"
  +            bootloader="grub2"
  +            firmware="uefi"
  +            efipartsize="33"
  +            kernelcmdline="systemd.show_status=1 console=ttyS0,115200 console=tty0 quiet"
  +            bootpartition="false"
  +            bootkernel="custom"
  +            devicepersistency="by-uuid"
  +            btrfs_quota_groups="true"
  +            btrfs_root_is_snapshot="true"
  +        >
  +            <systemdisk>
  +                <volume name="home"/>
  +                <volume name="root"/>
  +                <volume name="tmp"/>
  +                <volume name="opt"/>
  +                <volume name="srv"/>
  +                <volume name="boot/grub2/i386-pc"/>
  +                <volume name="boot/grub2/x86_64-efi" mountpoint="boot/grub2/x86_64-efi"/>
  +                <volume name="usr/local"/>
  +                <volume name="var" copy_on_write="false"/>
  +            </systemdisk>
  +            <size unit="G">24</size>
  +        </type>
  +    </preferences>
  +
       <preferences profiles="kvm-and-xen">
           <version>15.3</version>
           <packagemanager>zypper</packagemanager>
  @@ -296,10 +338,19 @@
       </packages>
  
       <!-- Shim for secure boot everywhere except for RPi -->
  -    <packages type="image" profiles="kvm-and-xen,kvm,VMware,MS-HyperV,OpenStack-Cloud">
  +    <packages type="image" profiles="kvm-and-xen,kvm,VMware,MS-HyperV,OpenStack-Cloud,pve">
           <package name="shim" arch="aarch64,x86_64"/>
       </packages>
  
  +    <packages type="image" profiles="pve">
  +        <package name="btrfsprogs"/>
  +        <package name="btrfsmaintenance"/>
  +        <package name="grub2-snapper-plugin"/>
  +        <package name="snapper-zypp-plugin"/>
  +        <package name="snapper"/>
  +        <package name="firewalld"/>
  +    </packages>
  +
       <!-- Not needed in OpenStack as it uses XFS and cloud-init -->
       <packages type="image" profiles="kvm-and-xen,kvm,VMware,MS-HyperV,RaspberryPi">
           <!-- Only for btrfs -->
  @@ -322,17 +373,17 @@
           <package name="xen-tools-domU" arch="x86_64"/>
           <package name="xen-libs" arch="x86_64"/>
       </packages>
  -    <packages type="image" profiles="kvm-and-xen,kvm">
  +    <packages type="image" profiles="kvm-and-xen,kvm,pve">
           <package name="kernel-default-base"/>
       </packages>
  -    <packages type="image" profiles="kvm-and-xen,kvm,OpenStack-Cloud">
  +    <packages type="image" profiles="kvm-and-xen,kvm,OpenStack-Cloud,pve">
           <package name="qemu-guest-agent"/>
       </packages>
       <packages type="image" profiles="VMware">
           <package name="open-vm-tools" arch="x86_64"/>
           <package name="kernel-default-base"/>
       </packages>
  -    <packages type="image" profiles="OpenStack-Cloud">
  +    <packages type="image" profiles="OpenStack-Cloud,pve">
           <package name="cloud-init" />
           <package name="cloud-init-config-suse" />
           <package name="xfsprogs" />
  @@ -363,7 +414,7 @@
           <package name="openSUSE-release"/>
       </packages>
  
  -    <packages type="bootstrap" profiles="kvm,kvm-and-xen">
  +    <packages type="bootstrap" profiles="kvm,kvm-and-xen,pve">
           <package name="openSUSE-release-appliance-kvm"/>
       </packages>
       <packages type="bootstrap" profiles="OpenStack-Cloud">


  Index: _multibuild
  ===================================================================
  --- _multibuild (revision 13)
  +++ _multibuild (revision 3)
  @@ -1,8 +1,11 @@
   <multibuild>
  +  <flavor>pve</flavor>
  +  <!--
     <flavor>kvm-and-xen</flavor>
     <flavor>kvm</flavor>
     <flavor>VMware</flavor>
     <flavor>MS-HyperV</flavor>
     <flavor>OpenStack-Cloud</flavor>
     <flavor>RaspberryPi</flavor>
  +  -->
   </multibuild>

openSUSE Leap 15.4 JeOS
=======================

Open Build Service (OBS) Project
--------------------------------

https://build.opensuse.org/package/show/home:wombelix:branches:Virtualization:Appliances:Images:openSUSE-Leap-15.4/kiwi-templates-JeOS

Download
--------

Local Webserver (Manual Sync): https://dominik.wombacher.cc/~files/proxmox_ve_kvm_images/

openSUSE Mirror (Automatic Build / Sync): https://download.opensuse.org/repositories/home:/wombelix:/branches:/Virtualization:/Appliances:/Images:/openSUSE-Leap-15.4/images/

Customizations
--------------

Please be aware: The below diff should give you an idea about the changes, it will not be updated, please check the OBS Project for the latest revision

.. code-block:: diff

  Index: JeOS.kiwi
  ===================================================================
  --- JeOS.kiwi (revision 2)
  +++ JeOS.kiwi (revision 3)
  @@ -9,6 +9,7 @@
           <specification>openSUSE Leap 15.4 JeOS</specification>
       </description>
       <profiles>
  +        <profile name="pve" description="JeOS for Proxmox VE (pve)" arch="x86_64"/>
           <profile name="kvm-and-xen" description="JeOS for KVM and Xen" arch="x86_64"/>
           <profile name="kvm" description="JeOS for KVM" arch="aarch64"/>
           <profile name="VMware" description="JeOS for VMware" arch="x86_64"/>
  @@ -16,6 +17,47 @@
           <profile name="OpenStack-Cloud" description="JeOS for OpenStack Cloud" arch="x86_64"/>
           <profile name="RaspberryPi" description="JeOS for the Raspberry Pi" arch="aarch64"/>
       </profiles>
  +    <preferences profiles="pve">
  +        <version>15.4</version>
  +        <packagemanager>zypper</packagemanager>
  +        <bootsplash-theme>openSUSE</bootsplash-theme>
  +        <bootloader-theme>openSUSE</bootloader-theme>
  +    <!-- those settings are applied by suseConfig in config.sh
  +        <locale>en_US</locale>
  +        <keytable>us.map.gz</keytable>
  +        <timezone>Europe/Berlin</timezone>
  +        <hwclock>utc</hwclock>
  +    -->
  +        <rpm-excludedocs>true</rpm-excludedocs>
  +        <type
  +            image="vmx"
  +            filesystem="btrfs"
  +            format="qcow2"
  +            bootloader="grub2"
  +            firmware="uefi"
  +            efipartsize="33"
  +            kernelcmdline="rw systemd.show_status=1 console=ttyS0,115200 console=tty0 quiet"
  +            bootpartition="false"
  +            bootkernel="custom"
  +            devicepersistency="by-uuid"
  +            btrfs_quota_groups="true"
  +            btrfs_root_is_snapshot="true"
  +        >
  +            <systemdisk>
  +                <volume name="home"/>
  +                <volume name="root"/>
  +                <volume name="tmp"/>
  +                <volume name="opt"/>
  +                <volume name="srv"/>
  +                <volume name="boot/grub2/i386-pc"/>
  +                <volume name="boot/grub2/x86_64-efi" mountpoint="boot/grub2/x86_64-efi"/>
  +                <volume name="usr/local"/>
  +                <volume name="var" copy_on_write="false"/>
  +            </systemdisk>
  +            <size unit="G">24</size>
  +        </type>
  +    </preferences>
  +
       <preferences profiles="kvm-and-xen">
           <version>15.4</version>
           <packagemanager>zypper</packagemanager>
  @@ -298,10 +340,19 @@
       </packages>
  
       <!-- Shim for secure boot everywhere except for RPi -->
  -    <packages type="image" profiles="kvm-and-xen,kvm,VMware,MS-HyperV,OpenStack-Cloud">
  +    <packages type="image" profiles="kvm-and-xen,kvm,VMware,MS-HyperV,OpenStack-Cloud,pve">
           <package name="shim" arch="aarch64,x86_64"/>
       </packages>
  
  +    <packages type="image" profiles="pve">
  +        <package name="btrfsprogs"/>
  +        <package name="btrfsmaintenance"/>
  +        <package name="grub2-snapper-plugin"/>
  +        <package name="snapper-zypp-plugin"/>
  +        <package name="snapper"/>
  +        <package name="firewalld"/>
  +    </packages>
  +
       <!-- Not needed in OpenStack as it uses XFS and cloud-init -->
       <packages type="image" profiles="kvm-and-xen,kvm,VMware,MS-HyperV,RaspberryPi">
           <!-- Only for btrfs -->
  @@ -324,17 +375,17 @@
           <package name="xen-tools-domU" arch="x86_64"/>
           <package name="xen-libs" arch="x86_64"/>
       </packages>
  -    <packages type="image" profiles="kvm-and-xen,kvm">
  +    <packages type="image" profiles="kvm-and-xen,kvm,pve">
           <package name="kernel-default-base"/>
       </packages>
  -    <packages type="image" profiles="kvm-and-xen,kvm,OpenStack-Cloud">
  +    <packages type="image" profiles="kvm-and-xen,kvm,OpenStack-Cloud,pve">
           <package name="qemu-guest-agent"/>
       </packages>
       <packages type="image" profiles="VMware">
           <package name="open-vm-tools" arch="x86_64"/>
           <package name="kernel-default-base"/>
       </packages>
  -    <packages type="image" profiles="OpenStack-Cloud">
  +    <packages type="image" profiles="OpenStack-Cloud,pve">
           <package name="cloud-init" />
           <package name="cloud-init-config-suse" />
           <package name="xfsprogs" />
  @@ -365,7 +416,7 @@
           <package name="openSUSE-release"/>
       </packages>
  
  -    <packages type="bootstrap" profiles="kvm,kvm-and-xen">
  +    <packages type="bootstrap" profiles="kvm,kvm-and-xen,pve">
           <package name="openSUSE-release-appliance-kvm"/>
       </packages>
       <packages type="bootstrap" profiles="OpenStack-Cloud">


  Index: _multibuild
  ===================================================================
  --- _multibuild (revision 2)
  +++ _multibuild (revision 3)
  @@ -1,8 +1,11 @@
   <multibuild>
  +  <flavor>pve</flavor>
  +  <!--
     <flavor>kvm-and-xen</flavor>
     <flavor>kvm</flavor>
     <flavor>VMware</flavor>
     <flavor>MS-HyperV</flavor>
     <flavor>OpenStack-Cloud</flavor>
     <flavor>RaspberryPi</flavor>
  +  -->
   </multibuild>

Getting started with OBS took a while but then it's really amazing how easy it is to branch existing 
packages, doesn't matter if it's classic rpm, vm or container images, apply changes and get results.
