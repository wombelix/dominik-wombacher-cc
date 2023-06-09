.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

openSUSE Tumbleweed - Python 3.10 - No package metadata was found for vorta
###########################################################################

:date: 2022-07-17
:modified: 2022-07-17
:tags: openSUSE, Tumbleweed, Vorta, BorgBase, BorgBackup
:description: Fix "no package metadata was found" error when starting vorta
:category: Linux
:slug: opensuse_tumbleweed_python_3-10_no_package_metadata_was_found_for_vorta
:author: Dominik Wombacher
:lang: en
:transid: opensuse_tumbleweed_python_3-10_no_package_metadata_was_found_for_vorta 
:status: published

I'm using `Vorta <https://vorta.borgbase.com>`_, a Desktop Client for `BorgBackup <https://www.borgbackup.org>`_, 
on my Notebook with openSUSE Tumbleweed, which stopped working after upgrading 
Tumbleweed to a Version that started using Python 3.10 as default.

Error message when starting vorta from the command line:

.. code-block:: 

  vorta

  Traceback (most recent call last):
    File "/usr/bin/vorta", line 33, in <module>
      sys.exit(load_entry_point('vorta==0.8.2', 'gui_scripts', 'vorta')())
    File "/usr/bin/vorta", line 22, in importlib_load_entry_point
      for entry_point in distribution(dist_name).entry_points
    File "/usr/lib64/python3.10/importlib/metadata/__init__.py", line 957, in distribution
      return Distribution.from_name(distribution_name)
    File "/usr/lib64/python3.10/importlib/metadata/__init__.py", line 548, in from_name
      raise PackageNotFoundError(name)
  importlib.metadata.PackageNotFoundError: No package metadata was found for vorta

I use the openSUSE Tumbleweed build from https://copr.fedorainfracloud.org/coprs/luminoso/vorta/, 
first tried to update it, but that dropped a dependency error:

.. code-block::

  sudo zypper up vorta

  Loading repository data...
  Reading installed packages...
  Resolving package dependencies...

  Problem: nothing provides 'python3-secretstorage' needed by the to be installed vorta-0.8.7-2.suse.tw.x86_64
   Solution 1: do not install vorta-0.8.7-2.suse.tw.x86_64
   Solution 2: break vorta-0.8.7-2.suse.tw.x86_64 by ignoring some of its dependencies

Well, sure that there is no secretstorage package for python installed? Let's see:

.. code-block::

  sudo zypper se secretstorage

  Loading repository data...
  Reading installed packages...

  S | Name                    | Summary                                              | Type
  --+-------------------------+------------------------------------------------------+--------
  i | python38-SecretStorage  | Python bindings to FreeDesktoporg Secret Service API | package
    | python39-SecretStorage  | Python bindings to FreeDesktoporg Secret Service API | package
  i | python310-SecretStorage | Python bindings to FreeDesktoporg Secret Service API | package

Looks good but the vorta package expects *"python3-secretstorage"* and not *"python310-SecretStorage"*, 
let's ignore the zypper warning about missing dependencies and just install the latest version of vorta:

.. code-block::

  sudo zypper up vorta

  Loading repository data...
  Reading installed packages...
  Resolving package dependencies...

  Problem: nothing provides 'python3-secretstorage' needed by the to be installed vorta-0.8.7-2.suse.tw.x86_64
   Solution 1: do not install vorta-0.8.7-2.suse.tw.x86_64
   Solution 2: break vorta-0.8.7-2.suse.tw.x86_64 by ignoring some of its dependencies
  
  Choose from above solutions by number or cancel [1/2/c/d/?] (c): 2
  Resolving dependencies...
  Resolving package dependencies...
  
  The following package is going to be upgraded:
    vorta
  
  1 package to upgrade.
  Overall download size: 492.3 KiB. Already cached: 0 B. After the operation, additional 215.5 KiB will be used.
  Continue? [y/n/v/...? shows all options] (y): y
  Retrieving package vorta-0.8.7-2.suse.tw.x86_64                          (1/1), 492.3 KiB (  1.7 MiB unpacked)
  Retrieving: vorta-0.8.7-2.suse.tw.x86_64.rpm ...........................................................[done]
  
  Checking for file conflicts: ...........................................................................[done]
  (1/1) Installing: vorta-0.8.7-2.suse.tw.x86_64 .........................................................[done]
 
Great, started vorta again from the CLI, but now *"PyQt5"* is missing:

.. code-block::

  vorta

  Traceback (most recent call last):
    File "/usr/bin/vorta", line 33, in <module>
      sys.exit(load_entry_point('vorta==0.8.7', 'gui_scripts', 'vorta')())
    File "/usr/bin/vorta", line 25, in importlib_load_entry_point
      return next(matches).load()
    File "/usr/lib64/python3.10/importlib/metadata/__init__.py", line 171, in load
      module = import_module(match.group('module'))
    File "/usr/lib64/python3.10/importlib/__init__.py", line 126, in import_module
      return _bootstrap._gcd_import(name[level:], package, level)
    File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
    File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
    File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
    File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
    File "<frozen importlib._bootstrap_external>", line 883, in exec_module
    File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
    File "/usr/lib/python3.10/site-packages/vorta/__main__.py", line 7, in <module>
      from vorta.i18n import trans_late, translate
    File "/usr/lib/python3.10/site-packages/vorta/i18n/__init__.py", line 7, in <module>
      from PyQt5.QtCore import QLocale, QTranslator
  ModuleNotFoundError: No module named 'PyQt5'


There is no rpm package so I installed it globally via pip:

.. code-block:: 

  sudo pip3 install PyQt5
  
  Collecting PyQt5
    Downloading PyQt5-5.15.7-cp37-abi3-manylinux1_x86_64.whl (8.4 MB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.4/8.4 MB 29.4 MB/s eta 0:00:00
  Collecting PyQt5-Qt5>=5.15.0
    Downloading PyQt5_Qt5-5.15.2-py3-none-manylinux2014_x86_64.whl (59.9 MB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 59.9/59.9 MB 26.1 MB/s eta 0:00:00
  Collecting PyQt5-sip<13,>=12.11
    Downloading PyQt5_sip-12.11.0-cp310-cp310-manylinux1_x86_64.whl (359 kB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 359.7/359.7 KB 21.9 MB/s eta 0:00:00
  Installing collected packages: PyQt5-Qt5, PyQt5-sip, PyQt5
  Successfully installed PyQt5-5.15.7 PyQt5-Qt5-5.15.2 PyQt5-sip-12.11.0

Afterwards :code:`vorta` could be started without issues, 
immediatly created a backup and uploaded the files to `BorgBase <https://www.borgbase.com>`_

Overall not a big deal, the fact that the vorta rpm is expecting a dependency that can't be 
found on openSUSE Tumbleweed, even though it's installed but with a different name, 
is more of a cosmetic issue in my opinion, writing this blog post took probably longer 
than fixing the actual problem ;)
