.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Uyuni Test Environment with sumaform on local libvirt host (openSUSE Tumbleweed)
################################################################################

:date: 2022-03-08
:modified: 2022-03-08
:tags: uyuni, sumaform, terraform, libvirt, openSUSE
:description: A convenient way to quickly setup a local Uyuni Instance
:category: Linux
:slug: uyuni_test_environment_with_sumaform_on_local_libvirt_host_opensuse_tumbleweed
:author: Dominik Wombacher
:lang: en
:transid: uyuni_test_environment_with_sumaform_on_local_libvirt_host_opensuse_tumbleweed
:status: published

A convenient way to quickly setup a local Uyuni Instance inclusive Clients, either for Development or Testing, is sumaform. 
It supports different backends and provides a ton of options, check it out: https://github.com/uyuni-project/sumaform

I just want to run a Uyuni Server and a few Clients (openSUSE, EL, Debian) on my Laptop so I can verify reported bugs, 
try some configs as well as deploy and test changes during development, without investing much time.

Following a overview of the, in my case, relevant steps, examples of my config and some Ansible snippets. 

**Setup**

.. code-block::

  sudo zypper addrepo http://download.opensuse.org/repositories/systemsmanagement:/sumaform/openSUSE_Tumbleweed/systemsmanagement:sumaform.repo
  sudo zypper install git-core
  sudo zypper install --from systemsmanagement_sumaform terraform terraform-provider-libvirt
  git clone https://github.com/uyuni-project/sumaform.git

Follow the *First-time configuration (libvirt)* instructions in the 
`README <https://github.com/uyuni-project/sumaform/blob/2082e344b9cdde5c3befb11fc358d80eb50de346/backend_modules/libvirt/README.md>`_, 
but use the uyuni example file instead: :code:`copy main.tf.uyuni.example to main.tf`

**Config & Deployment**

.. code-block::

  vim main.tf

  terraform init
  terraform validate
  terraform apply

**My terraform main.cf based on the uyuni example file**

.. code-block:: shell

  terraform {
   required_version = "1.0.10"
   required_providers {
     libvirt = {
       version = "0.6.3"
     }
   }
  }
  provider "libvirt" {
  }
  module "base" {
    cc_username = ""
    cc_password = ""
    images = ["centos7", "opensuse153o", "ubuntu1804"]
  }
  module "server" {
    base_configuration = module.base.configuration
    product_version = "uyuni-master"
    name = "server"
    image = "opensuse153o"
    use_os_released_updates = true
    create_first_user = false
    auto_accept = false
    skip_changelog_import = false
    mgr_sync_autologin = false
    create_sample_channel = false
    create_sample_activation_key = false
    create_sample_bootstrap_script = false
    publish_private_ssl_key = false
    java_debugging = true
    provider_settings = {
      memory = 8192
      vcpu = 4
    }
  }
  module "redhat-minion" {
    base_configuration = module.base.configuration
    product_version = "uyuni-master"
    name = "minion-centos7"
    image = "centos7"
    server_configuration = module.server.configuration
    provider_settings = {
      memory = 1024
    }
    auto_connect_to_master = true
  }
  module "debian-minion" {
    base_configuration = module.base.configuration
    product_version = "uyuni-master"
    name = "minion-ubuntu1804"
    image = "ubuntu1804"
    server_configuration = module.server.configuration
    provider_settings = {
      memory = 1024
    }
    auto_connect_to_master = true

  }

**Ansible Snippets for the Setup steps**

.. code-block:: yaml

 - name: Import systemsmanagement:/sumaform RPM Key
   rpm_key: 
     key: https://download.opensuse.org/repositories/systemsmanagement:/sumaform/openSUSE_Tumbleweed/repodata/repomd.xml.key
     state: present
 
 - name: Add systemsmanagement:/sumaform RPM Repository
   community.general.zypper_repository:
     name: systemsmanagement_sumaform
     description: Using Terraform to create a SUSE Manager test environment (openSUSE_Tumbleweed)
     repo: https://download.opensuse.org/repositories/systemsmanagement:/sumaform/openSUSE_Tumbleweed/
     priority: 90
     state: present
   ignore_errors: true
 
 - name: Package Installation (Uyuni Development - sumaform)
   community.general.zypper:
     name:
       - terraform
       - terraform-provider-libvirt
       - git-core
     allow_vendor_change: true
     force_resolution: true
     force: true
     state: latest

