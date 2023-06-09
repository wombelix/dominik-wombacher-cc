SUSE Manager / Uyuni - Upcoming feature: Salt Bundle (venv-salt-minion)
#######################################################################

:date: 2021-09-11
:modified: 2021-09-11
:tags: SUSE Manager, Uyuni, Salt
:description: Salt Bundle (venv-salt-minion)
:category: Linux
:slug: suse-manager-uyuni-upcoming-feature-salt-bundle-venv-salt-minion
:author: Dominik Wombacher
:lang: en
:transid: suse-manager-uyuni-upcoming-feature-salt-bundle-venv-salt-minion 
:status: published

I want to share what I already could find about it, how it seem to work, it's going to be implemented and what issues / challenges it's going to address / resolve.

Background
**********

Salt is more or less the heart of SUSE Manager / Uyuni, handling all configuration and communication with the registered systems and replaced the Traditional Client, which is still supported and around but new features only are developed for Salt.

That said, Salt has it's strength compared to Solutions like Ansible in the Master <> Minion Architecture, where Salt-Minions listening on a zeroMQ Bus for Messages/Actions send by the Master.

So compared to pure SSH connections, that's very fast and scales pretty well. But it requires an installed Salt-Minion on the Client which need to be connected to the SUSE Manager.

Let's assume you already use Salt somehow in your Environment and all your Server are connected to a Salt Master already, which is not SUSE Manager / Uyuni, then you can only use *SSH-Push* (Salt-SSH) to register them to SUMA / Uyuni.

So far it's not possible to have multiple Minions running on a Client connected to different Salt-Master, at least not in combination with SUSE Manager / Uyuni.

At work there are roughly 200 Server connected via SSH-Push because we can't change the existing Salt-Minion Setup, which leads to lot of issues. Even though SUSE is really committed to help, as stated earlier, SSH-Push just doesn't scale well...

Future?
*******

There is a new feature on the horizon, which wasn't really communicated our announced yet: **Salt Bundle aka venv-salt-minion**

SUSE describes it as *"Virtual environment jail for Salt"* and *"salt-minion in a bundled package"*.

So it's a package which contains a Salt-Minion including all dependencies in a own Python Virtual Environment and therefore doesn't affect any Salt Package that might already be installed on a System.

It's still in active development and my opinion is, that it will probably not officially arrive as stable in SUSE Manager before Version 4.3 (Summer 2022).

Implementation
**************

There are two parts:

  * The actual venv-salt-minion package, which provides a Salt-Minion that could be connected to most likely every Salt-Master and doesn't necessary require Uyuni or SUSE Manager

  * The Uyuni / SUSE Manager specific changes, mostly related to Salt States / Formulas as well as mgr_bootstrap components.

Package on OBS
==============

Main Project: https://build.opensuse.org/package/show/systemsmanagement:saltstack:bundle/venv-salt-minion

Results of pre-build Packages for various Distributions: https://build.opensuse.org/search?search_text=systemsmanagement%3Asaltstack%3Abundle

Almost the whole Implementation is handled in the spec file, it takes all dependencies, creates a venv, prepares configs, systemd unit files and build a self containing rpm or deb package: https://build.opensuse.org/package/view_file/systemsmanagement:saltstack:bundle/venv-salt-minion/venv-salt-minion.spec

Uyuni / SUSE Manager
====================

Based on Issues and Pull Requests from the Uyuni Project (https://github.com/uyuni-project/uyuni) Development is at least ongoing and some progress visible in public since March 2021.

Related PRs:

  * https://github.com/uyuni-project/uyuni/pull/3645

  * https://github.com/uyuni-project/uyuni/pull/3895

  * https://github.com/uyuni-project/uyuni/pull/4065

Based on comments in the Source (https://github.com/uyuni-project/uyuni/pull/3895/files) it looks like that, sooner or later, venv-salt-minion might be the preferred way to bootstrap a new System with Salt-Minion.

The adjustments in the Salt States are related to identify the correct name (either "salt-minion" or "venv-salt-minion") as well as the paths to binaries and configs because, obviously, they differ depending if package salt-minion or venv-salt-minion was installed.

In Uyuni *venv-salt-minion* is already available in a early testing stage for a few Distributions and the overall approach looks very promising.

