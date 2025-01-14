.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

OpenTofu based management of my git repositories
################################################

:date: 2025-01-13
:modified: 2025-01-13
:tags: OpenTofu, Git, OpenSource, Automation, AWS, sr.ht, sourcehut, GitHub, Gitlab, Codeberg
:description:
:category: Code
:slug: opentofu-based-management-of-my-git-repositories
:author: Dominik Wombacher
:lang: en
:transid: opentofu-based-management-of-my-git-repositories
:status: published

Yesterday I've completed the migration to
`git-repo-mgmt <https://git.sr.ht/~wombelix/git-repo-mgmt>`_.
It's an OpenTofu based management of my git repositories at
Sourcehut with mirrors at Codeberg, Gitlab and GitHub.

I was tired to manually create repos across four platforms.
Now it takes me seconds and a couple lines of code to do it, for example:

.. code::

    # SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
    #
    # SPDX-License-Identifier: MIT

    module "git-repo-mgmt" {
      source      = "./modules/repos"
      repo_name   = "git-repo-mgmt"
      description = "OpenTofu based management of my git repositories"
    }

The heart of the solution is a self written
`OpenTofu / Terraform module <https://git.sr.ht/~wombelix/git-repo-mgmt/tree/main/item/modules/repos>`_
that does all the heavy lifting. It uses the
`sourcehut OpenTofu / Terraform provider <{filename}/posts/2024/release-sourcehut-srht-opentofu-terraform-provider-and-go-library_en.rst>`_
that I recently publish and leverages
`AWS KMS for OpenTofu State and Plan Encryption <{filename}/posts/2024/opentofu-state-and-plan-encryption-with-aws-kms_en.rst>`_.

On every push, `builds.sr.ht <https://builds.sr.ht>`_ is triggered and runs the :code:`mirror`, :code:`setup`, :code:`init`, :code:`plan`
and :code:`apply` phases as defined in `.build.yml <https://git.sr.ht/~wombelix/git-repo-mgmt/tree/main/item/.build.yml>`_

The overall workflow looks like this:

.. code::

    git push
             > git.sr.ht
                         > builds.sr.ht
                                        > tofu apply
                                                     > sr.ht
                                                     > codeberg.org
                                                     > github.com
                                                     > gitlab.com

I'm very satisfied with the result, this makes things so much easier.
