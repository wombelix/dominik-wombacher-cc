.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Automated AWS Neuron Driver Source Code Publishing from Official RPM Packages
#############################################################################

:date: 2025-07-31
:modified: 2025-07-31
:tags: AWS, Neuron, GPL, OpenSource, Go, Automation
:description: Building automation to extract and publish AWS Neuron Driver source code with full verification
:category: Code
:slug: automated-aws-neuron-driver-source-code-publishing-from-official-rpm-packages
:author: Dominik Wombacher
:lang: en
:transid: automated-aws-neuron-driver-source-code-publishing-from-official-rpm-packages
:status: published

When you're working with open source drivers, you expect to find the
code public available, for example in a git repository, where you can
track changes and development. A couple of months ago, I saw that the
`official AWS Neuron Driver repository <https://github.com/aws-neuron/aws-neuron-driver>`_
`hasn't been updated since October 2020 <https://github.com/aws-neuron/aws-neuron-driver/commits/master/>`_.
New driver releases are only available as RPM package with DKMS
wrappers. The source code exists inside those package and is licensed
under GPL-2.0-only.

**Disclaimer**: This is a personal project and not related to, or
endorsed by, Amazon Web Services (AWS).

I built two projects to solve this problem. First,
`aws-neuron-driver-publish-source <https://git.sr.ht/~wombelix/aws-neuron-driver-publish-source>`_,
a Go command-line tool that extracts source code from official RPM
packages. Second,
`aws-neuron-driver <https://git.sr.ht/~wombelix/aws-neuron-driver>`_ -
the repository where the extracted source code gets published, with
mirrors on GitHub, GitLab, and Codeberg.

The `aws-neuron-driver-publish-source` tool handles the extraction
workflow: download repository metadata and rpms from
yum.repos.neuron.amazonaws.com, verify GPG signatures and SHA256
checksums, extract source code from RPM packages, and create git
commits with package metadata and release notes when available.

The verification happens at two levels. GPG signatures are checked on
the RPM packages to confirm they come from AWS. Then individual files
are verified against their checksums to ensure nothing was corrupted
or modified.

Each commit the tool creates includes detailed metadata, for example:

.. code-block:: text

    commit 053a860d1eb7fbeb68aa1e887eb4368ddece27f6 (tag: 1.1)
    Author: Dominik Wombacher <dominik@wombacher.cc>
    Date:   Wed Feb 5 08:48:09 PM UTC 2025 +0000

        feat: Neuron Driver 1.1

        Source code extracted from file: aws-neuron-dkms-1.1-2.0.noarch.rpm
        Downloaded from repository: https://yum.repos.neuron.amazonaws.com


        Metadata
        --------
        Package: aws-neuron-dkms
        Version: 1.1
        License: Unknown
        Summary: aws-neuron 1.1 dkms package
        Description: Kernel modules for aws-neuron 1.1 in a DKMS wrapper.
        Filename: aws-neuron-dkms-1.1-2.0.noarch.rpm
        Checksum: d994cd63745e7306bf9583c74468a40f46e199d698e2fd28610209483c311d6a
        Buildhost: 0cbde921ec7e
        Buildtime: 2020-10-19 18:45:40 +0000 UTC
        GPG key primary uid: Amazon AWS Neuron <neuron-maintainers@amazon.com>
        GPG key creation time: 2019-11-11 17:29:27 +0000 UTC
        GPG key fingerprint: 00FA2C1079260870A76D2C285749CAD8646D9185
        GPG check: OK
        SHA256 check: OK
        --------


        Files
        -----
        - M: src/README.md
        - M: src/postinstall
        - ?: archive/rpm/aws-neuron-dkms-1.1-2.0.noarch.rpm
        - ?: archive/rpm/aws-neuron-dkms-1.1-2.0.noarch.rpm.sha256
        - M: src/aws-neuron-dkms-mkrpm.spec
        - M: src/postremove
        - M: src/aws-neuron-dkms-mkdeb/debian/rules
        - M: src/dkms.conf
        - M: src/neuron_dma.c
        - M: src/neuron_module.c
        - M: src/aws-neuron-dkms-mkdeb/debian/postinst
        - M: src/aws-neuron-dkms-mkdeb/debian/prerm
        - D: src/LICENSE
        - M: src/preinstall
        -----

The `aws-neuron-driver` repository contains the extracted source code
and maintains an archive of all processed files. The structure is:

.. code-block:: text

    aws-neuron-driver/
    ├── src/                    # Driver source code
    │   ├── Makefile
    │   ├── neuron.c
    │   └── [other driver files]
    └── archive/                # Verification files
        ├── rpm/                # RPM packages and checksums
        ├── repomd.xml
        └── GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB

You can use the files in :code:`archive/` to verify that the
source code in :code:`src/` matches what AWS published.

The automation is based on two parts. A
`GitHub Actions workflow <https://git.sr.ht/~wombelix/aws-neuron-driver/tree/main/item/.github/workflows/check-neuron-driver.yml>`_
checks for new releases every Sunday and can be triggered manually.
When new releases are detected, it triggers an
`sr.ht build <https://git.sr.ht/~wombelix/aws-neuron-driver/tree/main/item/.build.yaml>`_
that runs the publishing tool and pushes updates to the repository.

Each commit gets tagged with the version number, making it easy to
track changes between releases.

This provides a git repository with AWS Neuron Driver source code
where you can see what changed between releases. The driver is
GPL-2.0 licensed and the automation keeps it current with official
releases. I intend to do this until the upstream repository
becomes active again.
