.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

AWS Neuron Kernel Modules on OpenShift with KMM
################################################

:date: 2025-07-24
:modified: 2025-07-24
:tags: AWS, OpenShift, AI/ML, Neuron, KMM, Kubernetes, RedHat
:description: How I built automated tooling for AWS Neuron kernel modules on Red Hat OpenShift using KMM
:category: Code
:slug: aws-neuron-kernel-modules-on-openshift-with-kmm
:author: Dominik Wombacher
:lang: en
:transid: aws-neuron-kernel-modules-on-openshift-with-kmm
:status: published

As part of my work at AWS, I've been diving deep into running AI/ML
workloads with the `AWS Neuron SDK <https://awsdocs-neuron.readthedocs-hosted.com/en/latest/index.html>`__
on `Inferentia <https://aws.amazon.com/ai/machine-learning/inferentia/>`__
and `Trainium <https://aws.amazon.com/ai/machine-learning/trainium/>`__
instances on `Red Hat OpenShift Services on AWS (ROSA) <https://aws.amazon.com/rosa/>`__.
What started as exploring concepts quickly turned into building actual
tooling to solve real problems.

The challenge: how do you get AWS Neuron drivers working reliably
across different OpenShift versions? The solution turned out to be more
interesting than I initially thought.

I developed and published
`kmod-with-kmm-for-ai-chips-on-aws <https://github.com/awslabs/kmod-with-kmm-for-ai-chips-on-aws>`__,
a project that automates building Kernel Module Management (KMM)
compatible container images for AWS Neuron drivers.

Running specialized hardware like AWS Inferentia and Trainium chips
requires kernel modules. Kernel modules are tied to specific kernel
versions, and new driver releases need to be built against different
kernel versions. This creates ongoing maintenance work that grows with each supported
platform version.

Red Hat's `Kernel Module Management (KMM) operator <https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/specialized_hardware_and_driver_enablement/kernel-module-management-operator>`__
solves this by automating kernel module lifecycle management. But you
still need to build the container images that contain your modules for
each kernel version.

That's where the `Driver Toolkit <https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/specialized_hardware_and_driver_enablement/driver-toolkit#about-driver-toolkit_driver-toolkit>`__
comes in - it provides the exact kernel headers and build environment
for each OpenShift release.

I fully automated this using GitHub Actions with nightly scans for new
OpenShift releases, automated builds triggered by driver or mapping
changes, and minimal container images containing only busybox and the
compiled kernel module.

GitHub Actions proved surprisingly powerful for this automation. The
dual tagging strategy works well - images get both kernel-specific and
OpenShift-specific tags for different use cases. The build script also
works locally for development, automatically detecting the environment
and adapting accordingly.

This removes the manual work of tracking releases and building modules
for each kernel version. The process now happens automatically. The
approach is reusable for other specialized hardware drivers on
OpenShift.

If you're running specialized hardware on OpenShift, KMM and the
Driver Toolkit are powerful tools once you understand how to use them
effectively.
