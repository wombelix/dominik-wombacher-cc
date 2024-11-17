.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Fluent Bit: Output Plugin for AWS CloudTrail Data Service
#########################################################

:date: 2024-11-12
:modified: 2024-11-12
:tags: FluentBit, Go, Coding, Plugin, AWS, CloudTrail, OpenSource
:description: Open Source AWS CloudTrail Data Service output plugin written in Go for Fluent Bit
:category: Code
:slug: fluent-bit-output-plugin-for-aws-cloudtrail-data-service
:author: Dominik Wombacher
:lang: en
:transid: fluent-bit-output-plugin-for-aws-cloudtrail-data-service
:status: published

I recently wrote a `AWS CloudTrail Data Service output plugin <https://git.sr.ht/~wombelix/fluent-bit-output-plugin-aws-cloudtrail-data>`__
(Mirror: `[1] <https://github.com/wombelix/fluent-bit-output-plugin-aws-cloudtrail-data>`__,
`[2] <https://gitlab.com/wombelix/fluent-bit-output-plugin-aws-cloudtrail-data>`__,
`[3] <https://codeberg.org/wombelix/fluent-bit-output-plugin-aws-cloudtrail-data>`__)
in Golang for `Fluent Bit <https://fluentbit.io/>`_. It's Open Source under the Apache-2.0 license.
The plugin ingest events into `AWS CloudTrail Lake <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake.html>`_
through the CloudTrail Data Service by making a
`PutAuditEvents <https://docs.aws.amazon.com/awscloudtraildata/latest/APIReference/API_PutAuditEvents.html>`_ API call.

I wrote a guest Article in the SUSE Blog:
`Send SUSE Security (NeuVector) events to AWS CloudTrail Lake <https://www.suse.com/c/send-suse-security-neuvector-events-to-aws-cloudtrail-lake/>`__
(Archive: `[1] <https://web.archive.org/web/20241117122619/https://www.suse.com/c/send-suse-security-neuvector-events-to-aws-cloudtrail-lake/>`__,
`[2] <https://archive.today/2024.11.17-122935/https://www.suse.com/c/send-suse-security-neuvector-events-to-aws-cloudtrail-lake/>`__).
It covers the Architecture and usage, in the context of SUSE Security (NeuVector) and Syslog as Fluent Bit input.
But given the modular nature of Fluent Bit, your Input can be one of the other `over 40 sources <https://docs.fluentbit.io/manual/pipeline/inputs>`_.
Which makes the Blog a blueprint for other use-cases too.

The Heart and Soul of the plugin is `out_aws-cloudtrail-data.go <https://git.sr.ht/~wombelix/fluent-bit-output-plugin-aws-cloudtrail-data/tree/main/item/out_aws-cloudtrail-data.go>`_,
which is based on the boilerplate example `out_gstdout.go <https://github.com/fluent/fluent-bit-go/blob/master/examples/out_gstdout/out_gstdout.go>`_.
It's my first Fluent Bit plugin and I enjoyed the nice coding exercise to hack a first working version together and release it.
There is, as always in life, room for improvement but it does the job and is more than enough to get started.

Looking forward for feedback to improve the plugin and to the next opportunity to write another one.

Helpful resources to understand the Fluent Bit concepts and to write a plugin in Go:

- `Fluent Bit - Key Concepts <https://docs.fluentbit.io/manual/concepts/key-concepts>`_
- `Fluent Bit - Golang Output Plugins <https://docs.fluentbit.io/manual/development/golang-output-plugins>`_
- `fluent-bit-go / examples <https://github.com/fluent/fluent-bit-go/tree/master/examples>`_

Recommended resources to learn more about the AWS CloudTrail Data Service and the API to ingest events into AWS CloudTrail Lake:

- `AWS CloudTrail – API Reference – PutAuditEvents <https://docs.aws.amazon.com/awscloudtraildata/latest/APIReference/API_PutAuditEvents.html>`_
- `AWS CloudTrail – User Guide – Create a custom integration with the console <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-event-data-store-integration-custom.html>`_
- `CloudTrail Lake integrations event schema <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-integration-event-schema.html>`_
