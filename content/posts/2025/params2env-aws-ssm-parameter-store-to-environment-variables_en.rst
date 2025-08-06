.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

params2env: AWS SSM Parameter Store to Environment variables
############################################################

:date: 2025-08-07
:modified: 2025-08-07
:tags: AWS, SSM, Go, Golang, CLI, OpenSource, ParameterStore, AI
:description: A Go CLI tool to manage AWS SSM Parameter Store parameters and convert them to environment variables
:category: Code
:slug: params2env-aws-ssm-parameter-store-to-environment-variables
:author: Dominik Wombacher
:lang: en
:transid: params2env-aws-ssm-parameter-store-to-environment-variables
:status: published

I recently released `params2env <https://git.sr.ht/~wombelix/params2env>`_,
a CLI tool written in Go that manages AWS SSM Parameter Store parameters and converts them to environment variables.
The project is available under the MIT license with mirrors on
`Codeberg <https://codeberg.org/wombelix/params2env>`_,
`GitLab <https://gitlab.com/wombelix/params2env>`_ and
`GitHub <https://github.com/wombelix/params2env>`_.
Pre-built binaries for Linux, macOS, and Windows are available on the
`GitHub Releases <https://github.com/wombelix/params2env/releases>`_ page.

My motivation was using AWS SSM Parameter Store as a low-cost password manager
for applications and pipelines. I don't need advanced features like rotation
that AWS Secrets Manager offers, so Parameter Store is much cheaper, basically free,
compared to Secrets Manager with costs per managed secret. I did some research and
there wasn't a tool that did exactly what and how I wanted it, so I built it myself.

This tool is for you if you store configuration or secrets in AWS SSM Parameter Store
and need to get them into environment variables for your applications. It doesn't
matter if your workload runs on AWS, on-premises, or anywhere else. As long as your
application reads environment variables, params2env can provide them from Parameter Store.

Parameter Store standard parameters with AWS-managed encryption are free, so using
params2env with standard parameters has no additional AWS costs beyond your existing setup.
Advanced parameters cost $0.05 per parameter per month. If you use customer-managed KMS keys
for SecureString parameters, each key costs $1 per month. See the
`AWS Systems Manager pricing <https://aws.amazon.com/systems-manager/pricing/>`_ and
`AWS KMS pricing <https://aws.amazon.com/kms/pricing/>`_ pages for current details.

:code:`params2env` provides four main subcommands for complete parameter management.
The **read** command retrieves parameters and outputs them as environment variables,
either to stdout or files. You can customize variable names, add prefixes,
control case conversion, and read multiple parameters from a YAML configuration file.
The **create** command creates new parameters with support for both String and SecureString types.
The **modify** command updates existing parameter values and descriptions while preserving the original parameter type.
The **delete** command removes parameters from Parameter Store.

The tool uses the AWS Go SDK for authentication and supports all standard AWS
credential methods including IAM roles, profiles, and environment variables.
Role assumption is built-in for working across different AWS accounts and regions.
For SecureString parameters, it handles KMS encryption and supports both AWS-managed
and customer-managed KMS keys. When working with replicas, it automatically handles
KMS key ARN conversion between regions.

Configuration can be managed through YAML files with a clear precedence order:
command line arguments override local config files (:code:`.params2env.yaml`),
which override global config files (:code:`~/.params2env.yaml`).
This makes it flexible for both one-off commands and repeatable workflows.
The `usage instructions <https://git.sr.ht/~wombelix/params2env/tree/main/item/docs/INSTRUCTIONS.md>`_
include detailed examples and configuration options.

You can install directly with Go:

.. code::

    go install git.sr.ht/~wombelix/params2env@latest

or pre-build binaries from the `Releases <https://github.com/wombelix/params2env/releases>`_ page.

Basic usage to read a parameter and set it as an environment variable:

.. code::

    # Output to stdout
    params2env read --path "/my/secret"

    # Set in current shell
    eval $(params2env read --path "/my/secret")

    # Write to file
    params2env read --path "/my/secret" --file ~/.env

Note: Only use eval with trusted sources. Since params2env outputs shell commands,
ensure you trust the parameter values and the tool itself before executing the output in your shell.

Creating parameters:

.. code::

    # String parameter
    params2env create --path "/my/param" --value "hello"

    # SecureString with KMS
    params2env create --path "/my/secret" --value "s3cret" \
      --type SecureString --kms "alias/myapp-key"

For managing multiple parameters, you can use a YAML configuration file:

.. code::

    region: eu-central-1
    role: arn:aws:iam::123456789012:role/my-role
    env_prefix: APP_
    params:
      - name: /app/db/url
        env: DB_URL
      - name: /app/db/password
        env: DB_PASSWORD

Then run :code:`params2env read` to process all configured parameters.

The replica feature is not an AWS native feature, it is something I've built into the tool.
It performs create, edit, or delete operations in two regions
instead of just one. AWS KMS supports custom keys to have identical backup keys
in another region. This way you have your key material and secrets region redundant
if you want that with minimal overhead and costs. This is useful for disaster recovery
scenarios or when you need the same secrets available in multiple regions for your applications.

The code is organized into packages: :code:`cmd` handles CLI interactions,
:code:`internal/aws` manages AWS SDK operations, :code:`internal/config` handles YAML parsing,
:code:`internal/validation` provides input validation, and :code:`internal/logger` manages logging.
Input validation happens before AWS API calls to check parameter paths, regions,
KMS key formats, and IAM role ARNs.

The project includes both unit tests and integration tests.
Unit tests focus on business logic validation.
Integration tests in :code:`tests/integration-tests.sh` validate real AWS service interactions,
including parameter creation, modification, deletion, and role assumption.
The build system uses a Makefile with targets for :code:`build`, :code:`tests`, and :code:`clean`.

Parts of the tool were built with AI assistance. I started with Cursor about
half a year ago, curious how well it would work to describe the program features
and implementation details, let AI create a design document, then use the AI agent
to build out structure and functionality based on that guide. It went surprisingly
well but required many iterations and improvements.

When I recently continued work on :code:`params2env`, I used Amazon Q Developer to get
up to speed on what I had implemented in an unfinished feature branch.
I compared it with existing features and the original planning doc to identify
what was missing.

I still wrote the majority of the code myself and worked on improvements through multiple iterations.
But AI saved time and suggested ideas and solutions I might not have thought of
or would have taken longer to develop.

Overall I think such AI tools are a positive thing and can make
some tasks easier and faster. But they are not a magic solution that builds applications
automatically end to end. Similar to my experience with
`DNS management with OpenTofu and some AI assistance <{filename}/posts/2025/dns-migration-with-opentofu-and-some-ai-assistance_en.rst>`_,
it was a useful experiment in understanding what these tools can contribute.

Building :code:`params2env` was another great opportunity to improve my skills in Go development,
AWS SDK usage, and CLI tool design.
