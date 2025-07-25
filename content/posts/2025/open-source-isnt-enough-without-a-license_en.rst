.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Open Source isn't enough without a License
###########################################

:date: 2025-05-01
:modified: 2025-05-01
:tags: OpenSource, License, GitHub, Rancher
:description: Why public source code availability doesn't make it open source without proper licensing
:category: Code
:slug: open-source-isnt-enough-without-a-license
:author: Dominik Wombacher
:lang: en
:transid: open-source-isnt-enough-without-a-license
:status: published

Just because source code is publicly available doesn't automatically make it :code:`open source`.
Without a proper license, that code exists in a legal grey area that can cause significant problems
for anyone trying to use, modify, or contribute to it.

A while back I encountered a perfect example of this with
`Rancher Quickstart <https://github.com/rancher/quickstart>`__.
This repository contains a lot of handy Terraform / OpenTofu code to deploy examples for the Rancher by SUSE product portfolio on various infrastructures / cloud providers.
But it comes without any license whatsoever. This means the code is actually fully copyrighted
and legally almost unusable, or at least exists in a very extreme grey area.

The `GitHub Terms of Service <https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#5-license-grant-to-other-users>`__
do provide some limited rights - they allow forking
(creating a copy in your own GitHub account), of every public repo, which is exactly what I did with my
`fork <https://github.com/wombelix/fork_rancher_quickstart>`__.
This fork contains all my upstream pull requests that haven't been merged, either due to the licensing issues of the rancher quickstart repository and because
it is essentially abandoned without active maintainers.

To work around these limitations, I created a separate :code:`backports` branch
in my fork where I've collected various fixes and feature updates.
I've released all my contributions under the `MIT-0 <https://opensource.org/license/mit-0>`__ license,
giving people the freedom to use them however they want:

.. code::

    # Fork / Backports

    The `backports` branch of this fork contains open pull requests from
    [upstream](https://github.com/rancher/quickstart) to fix bugs and add features.

    Feel free to use it until the pending PRs are merged and this branch becomes obsolete.

    All code contributions authored by me are released under the
    [MIT-0](https://opensource.org/license/mit-0) license.

    Included Patches:
    - [fix(rancher-common): Helm error, could not download chart](https://github.com/rancher/quickstart/pull/238)
    - [feat(rancher/aws): Use AWS env vars, use null defaults](https://github.com/rancher/quickstart/pull/239)
    - [feat(rancher/aws): Bump rancher, rke2, k3s, cert-manager version](https://github.com/rancher/quickstart/pull/240)
    - [feat(rancher): Use latest SLES 15 SP6 PAYG AMI](https://github.com/rancher/quickstart/pull/241)
    - [feat(rancher): AWS - Switch Rancher Server public ip to EIP](https://github.com/rancher/quickstart/pull/243)
    - [fix(rancher): AWS - destroy helm_release.cert_manager timeout](https://github.com/rancher/quickstart/pull/245)
    - [feat(rancher): AWS - Variable to adjust security group ingress cidr](https://github.com/rancher/quickstart/pull/246)
    - [fix: windows ami does not exist](https://github.com/rancher/quickstart/pull/236)

While this approach allows me to share improvements in a somewhat compliant way,
the fact that all this complexity is necessary demonstrates how crucial proper
licensing is for open source projects. A license provides the legal framework
that tells users what they can and can't do with the code.

The solution is straightforward: choose an appropriate open source license.
Whether it's MIT, Apache 2.0, GPL, or any other OSI-approved license,
having *some* license is much better than having none.

For the Rancher Quickstart repository, adding even a simple MIT or Apache 2.0 license
would immediately resolve the legal issues and make the code truly usable
by the community it's intended to serve.

Open source isn't just about making code visible - it's about making it legally
accessible and usable. Without a proper license, you're not really doing open source,
you're just publishing code.

If you maintain a public repository without a license, I encourage you to add one today.
