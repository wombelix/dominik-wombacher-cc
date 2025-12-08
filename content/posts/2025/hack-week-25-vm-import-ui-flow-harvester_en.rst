.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Hack Week 25: VM Import UI flow for SUSE Virtualization (Harvester)
###################################################################

:date: 2025-12-08
:modified: 2025-12-08
:tags: SUSE, HackWeek, Harvester, Virtualization, VueJS, Rancher, OpenSource
:description: My Hack Week 25 project to integrate the VM Import Controller flow into the SUSE Virtualization (Harvester) UI
:category: Code
:slug: hack-week-25-vm-import-ui-flow-harvester
:author: Dominik Wombacher
:lang: en
:transid: hack-week-25-vm-import-ui-flow-harvester
:status: published

I finished my Hack Week 25 project last night, with just two days delay ;) 
`SUSE Virtualization (Harvester): VM Import UI flow <https://hackweek.opensuse.org/projects/suse-virtualization-harvester-vm-import-ui-flow>`_.

But what exactly was it about and why did I pick that topic this year?
Some Background: SUSE Virtualization (Harvester) includes a 
`vm-import-controller addon <https://docs.harvesterhci.io/v1.7/advanced/addons/vmimport>`_
that allows migrating VMs from VMware and OpenStack. Currently, users need to write
manifest files and apply them with :code:`kubectl`. VMware and OpenStack admins might
not have deep Kubernetes knowledge yet. I wanted to integrate this feature directly
into the Harvester UI. This makes it accessible without writing YAML manually.

The project was also a good opportunity to improve my Vue.js skills and
dive deeper into the Rancher Extensions and their architecture.

Now it becomes a bit more nerdy and techy. Background knowledge in Harvester, reading
through the hack week project description and comments as well as the code in
`my feature branch <https://github.com/harvester/harvester-ui-extension/compare/main...wombelix:fork_harvester_harvester-ui-extension:suse-hack-week-25>`_
should help you to easier follow along.

The biggest technical challenge for me was the side navigation. I wanted
the new **VM Import** menu group to appear only when the
`vm-import-controller <https://github.com/harvester/vm-import-controller>`_
addon is enabled. Harvester behaves differently in standalone mode compared
to a normal Rancher environment. The usual `ifHaveType` allowlist logic
for extensions did not work as I expected.

I solved this by writing a helper function, :code:`registerAddonSideNav`.
It watches the specific addon resource in the cluster. If the addon is active,
the function adds the relevant menu items to the allowlist, which un-hides it.
If the addon is disabled, it removes / hides them again. The UI always reflects
the actual state of the cluster features, which I like very much.

I implemented the custom create/edit forms for :code:`VmwareSource`, :code:`OpenstackSource`
and the :code:`VirtualMachineImport` resource. I also added support for the new
:code:`OvaSource` resource (included in the upcoming version 1.7.0). Users can enter
credentials directly in the form, which creates a new Kubernetes Secret. Or they can
alternatively select an existing secret if they want. The UI also validates inputs,
for example if the VM name follows RFC-1123 which is required by Kubernetes.

The result is a decent UI flow that allows users to configure import sources and track
the status directly in the browser. I submitted the outcome of my hack week project 
as Pull Request to the
`harvester-ui-extension repository <https://github.com/harvester/harvester-ui-extension>`_.
Let's see if other people like it and I can help to bring in this, or a comparable feature, 
into one of the next Harvester releases.

GitHub Pull Request, you can also see it in action including a brief walkthrough here:
`[feat] Introduce VM Import UI flow and ability to hide/unhide navi groups when addons are enabled/disabled <https://github.com/harvester/harvester-ui-extension/pull/642>`_

This work picks up on a feature request from the community:
`[FEATURE] VM Migration Controller UI Flow <https://github.com/harvester/harvester/issues/4663>`_

And completes the UI part that was outlined 2022 in the
`VM Controller - Harvester Enhancement Proposal (HEP) <https://github.com/harvester/harvester/blob/master/enhancements/20220726-vm-migration.md#user-experience-in-detail>`_

Highly recommended learning resources for Rancher Development and Extensions:
 - `Rancher Extension <https://extensions.rancher.io/extensions/next/home>`_
 - `Rancher Developer Documentation <https://extensions.rancher.io/internal/docs>`_
