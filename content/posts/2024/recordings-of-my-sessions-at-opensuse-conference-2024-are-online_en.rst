.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Recordings of my sessions at openSUSE Conference 2024 are online
################################################################

:date: 2024-07-07
:modified: 2024-07-07
:tags: openSUSE, Speaking, Event, Session, NeuVector, Pagure, AWS
:description: I had the pleasure to speak at openSUSE Conference 2024, the recordings are now online!
:category: Misc
:slug: recordings-of-my-sessions-at-opensuse-conference-2024-are-online
:author: Dominik Wombacher
:lang: en
:transid: recordings-of-my-sessions-at-opensuse-conference-2024-are-online
:status: published

I had the great opportunity to speak at `openSUSE Conference 24 <https://events.opensuse.org/conferences/oSC24>`_ in Nuremberg about
`Pagure CI integration with AWS CodePipeline <https://events.opensuse.org/conferences/oSC24/program/proposals/4587>`_ and
`NeuVector Integration into AWS CodePipeline CI/CD workflow <https://events.opensuse.org/conferences/oSC24/program/proposals/4584>`_,
the recordings are now online.

Session 1: Pagure CI integration with AWS CodePipeline
------------------------------------------------------

Pagure is a lightweight git centered forge based on Python with a long usage history in the Fedora project.
It's well known in the openSUSE project too with an instance on code.opensuse.org.
I demonstrate in this talk the current state of the Pagure Plugin system.
How I implemented AWS CodePipeline as additional CI type.
And how this can serve as blueprint to optimize the Plugin system and add other CI types.
I will share the current status of my work to run Pagure on Kubernetes.
And some good-first-issues you can tackle if you want to contribute to Pagure.

- Slides: https://speakerdeck.com/wombelix/osc24-pagure-ci-integration-with-aws-codepipeline

- Recording: https://media.ccc.de/v/4587-pagure-ci-integration-with-aws-codepipeline

Session 2: NeuVector Integration into AWS CodePipeline CI/CD workflow
---------------------------------------------------------------------

NeuVector is a open source container security platform.
Key strengths are vulnerability and runtime scanning.
I demonstrate in this talk how you ensure that only container images without
a detected vulnerability move to the next stage in your Pipeline.
How you define the baseline of allowed activities of your application.
And how you can block the deployment into production if an unexpected behavior
at runtime was detected in your testing stage. I'll use AWS CodePipeline,
AWS CodeDeploy and AWS CloudFormation. The procedure is applicable to other
toolset and Hybrid environments as well.

- Slides: https://speakerdeck.com/wombelix/osc24-neuvector-integration-into-aws-codepipeline-ci-and-cd-workflow

- Recording: https://media.ccc.de/v/4584-neuvector-integration-into-aws-codepipeline-ci-cd-workflow
