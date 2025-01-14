.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Release: sourcehut (sr.ht) OpenTofu / Terraform provider and Go library
#######################################################################

:date: 2024-12-28
:modified: 2024-12-28
:tags: sourcehut, sr.ht, Go, Golang, OpenTofu, Terraform, OpenSource
:description:
:category: Code
:slug: release-sourcehut-srht-opentofu-terraform-provider-and-go-library
:author: Dominik Wombacher
:lang: en
:transid: release-sourcehut-srht-opentofu-terraform-provider-and-go-library
:status: published

Today I released `terraform-provider-sourcehut <https://git.sr.ht/~wombelix/terraform-provider-sourcehut>`_
and the related Go library `sourcehut-go <https://git.sr.ht/~wombelix/sourcehut-go>`_ into the wild.
The majority of code is licensed under :code:`BSD-2-Clause`.
The provider is available in the `OpenTofu <https://search.opentofu.org/provider/wombelix/sourcehut/latest>`_
and `Terraform <https://registry.terraform.io/providers/wombelix/sourcehut/latest>`_ registry.
The online version of the Documentation can be found there as well.

:code:`sourcehut-go` is a Go SDK for accessing the sourcehut legacy REST API with oauth personal access tokens
created via `meta.sr.ht/oauth <https://meta.sr.ht/oauth>`_.

Both projects are based on the work of `Sam Whited <https://codeberg.org/SamWhited>`_ who archived
the former code base on August 22, 2022.

My motivation to improve and release it:
I plan to move my git repository management to OpenTofu.
Providers for my usual mirror targets GitHub, Gitlab and GitLab are available.
But there was no functional and published provider for sourcehut (sr.ht).
Which I use as my primary code hosting and build platform.

Now that the library and provider are in a working state,
I can continue to work on the actual project :D
