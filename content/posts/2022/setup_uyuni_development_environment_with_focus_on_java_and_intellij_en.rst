.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Setup Uyuni Development Environment with focus on Java and IntelliJ
###################################################################

:date: 2022-03-09
:modified: 2022-05-18
:tags: Uyuni, Java, Development, sumaform, IntelliJ
:description: Start hacking Uyuni and setup your dev environment
:category: Code
:slug: setup_uyuni_development_environment_with_focus_on_java_and_intellij
:author: Dominik Wombacher
:lang: en
:transid: setup_uyuni_development_environment_with_focus_on_java_and_intellij
:status: published

Hacking Uyuni, either to troubleshoot and fix bugs or to contribute new features / improvements 
is something I do since quite a while already, at least  whenever I find some time. 
Getting started wasn't that easy, there are a lot of resources available but sometimes there are outdated, 
too focused on SUSE employees instead community contributors or just didn't fully answered my questions.

So I want to share my experiences to Setup a Development Environment for Uyuni, 
with focus on the Java Codebase, on a openSUSE Tumbleweed System by using sumaform and IntelliJ IDEA.

.. contents::
        :local:

----

Resources
=========

You can find a lot of information in the `Uyuni Wiki <https://github.com/uyuni-project/uyuni/wiki/>`_ and a 
great `Presentation <http://bosdonnat.fr/slides/openSUSEAsiaSummit19/>`__
(`Archive <https://web.archive.org/web/20211001151412/http://bosdonnat.fr/slides/openSUSEAsiaSummit19/>`__,
`Source <https://github.com/cbosdo/openSUSEAsia19-uyuni-dev>`__) from `Cédric Bosdonnat <http://bosdonnat.fr>`_.

sumaform
========

See my Post `Uyuni Test Environment with sumaform on local libvirt host (openSUSE Tumbleweed) <{filename}/posts/2022/uyuni_test_environment_with_sumaform_on_local_libvirt_host_opensuse_tumbleweed_en.rst>`_

There are `Alternative Instructions <https://github.com/uyuni-project/uyuni/wiki/Development-Environment-Alternative-Instructions>`__
(Archive: `[1] <https://web.archive.org/web/20220309214954/https://github.com/uyuni-project/uyuni/wiki/Development-Environment-Alternative-Instructions>`__,
`[2] <https://archive.today/2022.03.09-214849/https://github.com/uyuni-project/uyuni/wiki/Development-Environment-Alternative-Instructions>`__)
available in case using sumaform isn't possible or not intended.

Install Packages
================

Add the *systemsmanagement:Uyuni:Utils* repository, especially for *obs-to-maven*, and install the necessary packages.

Manually:

.. code-block::

  sudo zypper addrepo obs://systemsmanagement:Uyuni:Utils systemsmanagement:uyuni:utils
  sudo zypper in java-11-openjdk-devel openssh rsync apache-ivy ant ant-junit servletapi5 cpio obs-to-maven tito yarn

Ansible snippet:

.. code-block:: yaml

 - name: Import systemsmanagement:/Uyuni:/Utils RPM Key
   rpm_key: 
     key: https://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Utils/openSUSE_Tumbleweed/repodata/repomd.xml.key
     state: present

 - name: Add systemsmanagement:/Uyuni:/Utils RPM Repository
   community.general.zypper_repository:
     name: systemsmanagement_uyuni_utils
     description: Several utilities to develop, build or release Uyuni (openSUSE_Tumbleweed)
     repo: https://download.opensuse.org/repositories/systemsmanagement:/Uyuni:/Utils/openSUSE_Tumbleweed/
     priority: 95
     state: present
   ignore_errors: true

 - name: Package Installation (Uyuni Development)
   community.general.zypper:
     name:
       - java-11-openjdk-devel
       - openssh
       - rsync
       - apache-ivy
       - ant
       - ant-junit
       - servletapi5
       - obs-to-maven
       - tito
       - yarn
     allow_vendor_change: true
     force_resolution: true
     force: true
     state: latest

Clone git repo and prepare files / folders
==========================================

Fork the `Uyuni Repository <https://github.com/uyuni-project/uyuni>`_ and clone it. 
I will use the placeholder :code:`<path_to_uyuni>` a lot, which refers to the local path of your cloned uyuni fork.

Let's start with some files and folders which are required at a later point for unittest and deployment. 

Create the folders */usr/share/rhn/config-defaults*, */var/log/rhn* and */srv/susemanager*, owner and group should match with your user account.

Ansible snippet:

.. code-block:: yaml

 - name: Create Folders for Uyuni Development Unittests and Build
   file:
     path: "{{ item }}"
     state: directory
     owner: wombelix
     group: users
   loop:
     - /usr/share/rhn/config-defaults
     - /var/log/rhn
     - /srv/susemanager

Create a *rhn.conf* used by JUnit:

.. code-block::

  cp <path_to_uyuni_root>/java/buildconf/test/rhn.conf.postgresql-example <path_to_uyuni_root>/java/buildconf/test/rhn.conf

Get / update java libraries and dependencies:

.. code-block::

  cd <path_to_uyuni_root>/java
  ant -f manager-build.xml ivy

Compile branding jar for the first time:

.. code-block::

  cd <path_to_uyuni_root>/java
  ant -f manager-build.xml refresh-branding-jar

Configure IntelliJ IDEA
=======================

I will focus on IntelliJ IDEA but can also use 
`Eclipse <https://github.com/uyuni-project/uyuni/wiki/Eclipse-specific-development-instructions>`__ 
(Archive: `[1] <https://web.archive.org/web/20220309215457/https://github.com/uyuni-project/uyuni/wiki/Eclipse-specific-development-instructions>`__,
`[2] <https://archive.today/2022.03.09-215319/https://github.com/uyuni-project/uyuni/wiki/Eclipse-specific-development-instructions>`__) 
or `VSCode <https://github.com/uyuni-project/uyuni/wiki/VS-Code-specific-development-instructions>`__ 
(Archive: `[1] <https://web.archive.org/web/20220309215449/https://github.com/uyuni-project/uyuni/wiki/VS-Code-specific-development-instructions>`__,
`[2] <https://archive.today/2022.03.09-215515/https://github.com/uyuni-project/uyuni/wiki/VS-Code-specific-development-instructions>`__), if you want.

The following Steps are heavily based on 
`IntelliJ IDEA specific development instructions <https://github.com/uyuni-project/uyuni/wiki/IntelliJ-IDEA-specific-development-instructions>`__ 
(Archive: `[1] <https://web.archive.org/web/20220309215526/https://github.com/uyuni-project/uyuni/wiki/IntelliJ-IDEA-specific-development-instructions>`__,
`[2] <https://archive.today/2022.03.09-215715/https://github.com/uyuni-project/uyuni/wiki/IntelliJ-IDEA-specific-development-instructions>`__) 
and `Java Development Environment <https://github.com/uyuni-project/uyuni/wiki/Java-Development-Environment>`__ 
(Archive: `[1] <https://web.archive.org/web/20220309215601/https://github.com/uyuni-project/uyuni/wiki/Java-Development-Environment>`__,
`[2] <https://archive.today/2022.03.09-215915/https://github.com/uyuni-project/uyuni/wiki/Java-Development-Environment>`__) 
with some adjustments, additional information and tested on IntelliJ IDEA Ultimate 2022.1 EAP.

The JetBrain Toolbox is in my opinion the easiest way to install and update IntelliJ. 
If you installed it manually, please check the documentation where / how you can configure the *vmoptions*.

**Toolbox App > three dots next to "IntelliJ IDEA" > Settings > Configuration > Java Virtual Machine options "Edit..."**

	Replace :code:`-Xmx2048m` with :code:`-Xmx4G`

Source:  
`https://intellij-support.jetbrains.com <https://intellij-support.jetbrains.com/hc/en-us/articles/206544869-Configuring-JVM-options-and-platform-properties>`__
(Archive: `[1] <https://web.archive.org/web/20211213213449/https://intellij-support.jetbrains.com/hc/en-us/articles/206544869-Configuring-JVM-options-and-platform-properties>`__,
`[2] <https://archive.today/2022.03.09-220705/https://intellij-support.jetbrains.com/hc/en-us/articles/206544869-Configuring-JVM-options-and-platform-properties>`__)

Afterwards start IntelliJ IDEA to proceed with the actual configuration.

**File > New > Project from existing Source**

	| Select <path_to_uyuni_root>
	| Create Project from existing Source
	| Accept the project format defaults
	| Also accept auto discovered source directories
	| From the Libraries list, uncheck all items
	| From the Modules list, only check the items corresponding to the following directories:

		| :code:`uyuni/java/code` (change the name to code)
		| :code:`uyuni/branding/java/code` (change the name to branding)

	| Select a Java 11 runtime e.g. the previously installed openJDK
	| Ultimate Edition: Unselect eventually found frameworks

Enable automatic building
-------------------------

**File > Settings... > Build, Execution, Deployment > Compiler and select "Build project automatically"**

Configure Code Style
--------------------

**File > Settings... > Editor > Code Style > Java > Imports**

	Click on the cog / settings icon next to the "Scheme: Default" field at the top, then "Import Scheme", "IntelliJ IDEA code style XML" and select the :code:`<path_to_uyuni_root>/java/conf/intellij-codestyle.xml` file.

Remote Debugging
----------------

**Run > Edit Configurations... > + sign**

	| Accept all defaults, except from Host and Port, configure them based on the service you want to debug.
	| 8000 for Tomcat, 8001 for Taskomatic, 8002 for Search (defaults if deployed with sumaform)

Further reading: `IntelliJ IDEA Debugging Guide <https://www.jetbrains.com/help/idea/debugging-code.html#general-procedure>`__ 
(Archive: `[1] <https://web.archive.org/web/20220218091806/https://www.jetbrains.com/help/idea/debugging-code.html>`__,
`[2] <https://archive.today/2022.03.09-220232/https://www.jetbrains.com/help/idea/debugging-code.html%23general-procedure>`__)

Ivy integration
---------------

**File > Settings... > Plugins > Browse repositories... > search for "IvyIDEA" > Install the Ivy plugin**

	Restart IntelliJ IDEA (if asked) to activate the plugin

**File > Project Structure... > Modules -> right click on code > + sign > click on "ivyIDEA" to enable the plugin for the project**

	| Click on folder icon at the right side to select the Ivy configuration path: :code:`<path_to_uyuni_root>/java/buildconf/ivy/ivy-suse.xml`
	| Check "Use module specific ivy settings"
	| Click on folder icon at the right side to select the Ivy configuration path: :code:`<path_to_uyuni_root>/java/buildconf/ivy/ivyconf.xml`

**Tools > IvyIDEA > "Resolve for all modules" to get updated Ivy dependencies**

*Note: When switching branches that have different dependencies (notably, major versions) you have to:*

	| Tools > IvyIDEA > Remove all resolved libraries
	| Tools > IvyIDEA > Resolve for all modules
	| Build > Rebuild project

CheckStyle integration
----------------------

**File > Settings... > Plugins > Browse repositories... > search for "CheckStyle" -> Install the CheckStyle IDEA plugin**

	Restart IntelliJ IDEA to activate the plugin

**File > Settings... > Tools > Checkstyle**

	| Change the Checkstyle version to the one in :code:`<path_to_uyuni_root>/java/buildconf/ivy/ivy-suse.xml` (currently 8.30)
	| Click on the + sign next to Configuration File
	|
	| Description: Uyuni
	| Check "Use a local Checkstyle file", select :code:`<path_to_uyuni_root>/java/buildconf/checkstyle.xml`
	| Check "Store relative to project location", click on Next

	Set the following values for properties:

	.. code-block:: 

		checkstyle.cache.file: <path_to_uyuni_root>/java/build/checkstyle.cache.src
		checkstyle.header.file: <path_to_uyuni_root>/java/buildconf/LICENSE.txt
		checkstyle.suppressions.file: <path_to_uyuni_root>/java/buildconf/checkstyle-suppressions.xml
		javadoc.lazy: false
		javadoc.method.scope: public
		javadoc.type.scope: package
		javadoc.var.scope: package

	Click on Finish, mark the file as Active, click on Apply and leave the Settings. 

Afterwards a new mini-tab will appear at the bottom named "CheckStyle".

Avoid CheckStyle violations
---------------------------

These are recommended settings, which might already be set as default, that help respecting style guidelines independent of the CheckStyle plugin:

enabling automatic import completion
************************************

**File > Settings... > Editor > General > Auto Import**

	| Set "Insert imports on paste" to "Always"
	| Select "Add unambiguous imports on the fly" and "Optimize imports on the fly" in the Java Section.

disabling "star imports"
************************

**File > Settings... > Editor > Code Style > Java > Imports**

	| Class count to use import with '*' > 999
	| Names count to use static import with '*' > 999

wrapping and braces
*******************

**File > Settings... > Editor > Code Style > Java > Wrapping and Braces**

	| Under 'try' statement check 'catch' on new line and 'finally' on new line
	| Under 'if' statement check 'else' on new line

Faster deployments via manager-build.xml
----------------------------------------

Change the output directory to enable quick *manager-build.xml* deploys:

**File -> Project Structure... -> Modules -> code -> Paths**

	|	Click on "Use module compile output path" and set:
	| "Output path" to :code:`<path_to_uyuni_root>/java/build/classes`
	| "Test output path" to :code:`<path_to_uyuni_root>/java/build/tests`

Enable usage of precompiled files by adding :code:`precompiled=true` to :code:`<path_to_uyuni_root>/java/buildconf/manager-developer-build.properties`, 
if the file not exist, copy :code:`<path_to_uyuni_root>/java/buildconf/manager-developer-build.properties.example`, rename and edit the new file.

Configure JUnit tests
---------------------

**File > Project Structure... > Modules > code > Dependencies**

  Click the + sign > Module dependency > branding > OK to include branding classes and files in the build

**File > Project Structure... -> Modules -> code**

	Mark the directory webapp as Resources

**Run > Edit Configurations... > + sign > JUnit**

	| Name: JUnit
	| Run on: Local machine
	| Build and run:

	.. code-block::

			JRE: Java 11
			-cp: -cp code
			-ea: -ea -Drhn.config.dir=$MODULE_DIR$/../buildconf/test/ -Dlog4j.threshold=debug

	Select "All in package" to execute all available Unittests, if you want to limit to a specific class or package adjust the dropdown and filepath accordingly

To start the JUnit tests, click on **Run > Run**. 

*Important: Start the test database docker container first, otherwise almost all tests will just fail*

.. code-block::

  cd <path_to_uyuni_root>/java
  make -f Makefile.docker dockerrun_pg


Deploying Java code or CSS
==========================

If you created a terraform based VM with sumaform, you can easily deploy code:

1) Run checkstyle

.. code-block::

  cd <path_to_uyuni_root>/java
  ant -f manager-build.xml checkstyle

2) Deploy

.. code-block::

  cd <path_to_uyuni_root>/java
  ant -f manager-build.xml refresh-branding-jar deploy -Ddeploy.host=uyuni-server.tf.local restart-tomcat restart-taskomatic

You can configure the *deploy.host* in :code:`<path_to_uyuni_root>/java/buildconf/manager-developer-build.properties` 
and omit the command line parameter.

Contribute
==========

`Uyuni <https://www.uyuni-project.org>`_ exist since July 2018, the initial release (4.0.0) was based on SUSE Manager 3.2, since 
then Uyuni is the Upstream Project of SUSE Manager. SUSE Manager is based on Spacewalk, which was sponsored by Red Hat and 
abandoned, so SUSE decided to start a own `Fork <https://news.opensuse.org/2018/05/26/uyuni-forking-spacewalk-with-salt-and-containers/>`__ 
(Archive: `[1] <https://web.archive.org/web/20210418110047/https://news.opensuse.org/2018/05/26/uyuni-forking-spacewalk-with-salt-and-containers/>`__,
`[2] <https://archive.today/2022.03.09-211509/https://news.opensuse.org/2018/05/26/uyuni-forking-spacewalk-with-salt-and-containers/>`__), Uyuni was born. 

Still a lot of development comes from SUSE but there is a growing `Community <https://www.uyuni-project.org/pages/contact.html>`__ 
(Archive: `[1] <https://web.archive.org/web/20220309221253/https://www.uyuni-project.org/pages/contact.html>`__,
`[2] <https://archive.today/2022.03.09-221014/https://www.uyuni-project.org/pages/contact.html>`__) 
with more and more independent Contributions. 

If your dev environment is ready and you want to jump in, but didn't contributed to the Uyuni Project before, 
I suggest you take a look at some `Good first Issues <https://github.com/uyuni-project/uyuni/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22>`_.

