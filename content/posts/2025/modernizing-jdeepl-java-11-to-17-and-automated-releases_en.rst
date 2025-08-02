.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Modernizing jDeepL: Java 11 to 17 and Automated Releases
########################################################

:date: 2025-08-02
:modified: 2025-08-02
:tags: DeepL, Java, JavaFX, Linux, GitHubActions
:description: Modernizing jDeepL with Java 17, updated dependencies, and automated GitHub releases
:category: Code
:slug: modernizing-jdeepl-java-11-to-17-and-automated-releases
:author: Dominik Wombacher
:lang: en
:transid: modernizing-jdeepl-java-11-to-17-and-automated-releases
:status: published

I had some time last night - the neighbors were having a
party and I couldn't sleep - so I decided to tackle a task
that's been sitting in my backlog for way too long: modernizing
jDeepL, my `unofficial DeepL translation app for Linux <{filename}/posts/2022/jdeepl_unofficial_deepl_app_for_linux_based_on_javafx_en.rst>`_.

For those who don't know jDeepL, it's a simple JavaFX desktop
application that lets you translate text using the DeepL API. Nothing
fancy, just a basic GUI with source and target text areas, language
selection, and the CTRL+C+C keyboard shortcut for quick translations.
I built it because I wanted something native on Linux instead of using
the web interface all the time.

The main problem was that the project was stuck on older dependencies
and had practically non-existent documentation. This became obvious
when people opened and commented `GitHub issue #1 <https://github.com/wombelix/jDeepL/issues/1>`_
back in March 2023. Around that time jDeepL was also mentioned in a Golem.de
Article and I received a couple of Emails. All pointing out that there wasn't
much instruction on how to build it and that they ran into compatibility
issues with newer Java versions. The project was using Java 11, JavaFX 11, and
a bunch of outdated libraries that caused build failures for anyone
trying to compile from source.

So last night I finally decided to modernize the whole thing a bit. The work
took me a few hours of checking new versions, reading changelogs, and
validating that updates wouldn't break anything. I bumped Java from 11
to 17 and updated all dependencies to their latest stable releases. So,
same libraries I was already using, but brought up to current versions.

The most interesting challenge was fixing the FXTrayIcon dependency.
It had a deprecated constructor that I was using, so I had to dig into
the `library's source code <https://github.com/dustinkredmond/FXTrayIcon>`_
to understand what the deprecated builder actually did and how to achieve
the same result with non-deprecated methods. The old approach let you define
image scaling directly in the constructor. The new way requires a two-step
approach: use the builder pattern, then call the image scaling method on the
returned object. Small change, but it took some detective work to
figure out the right replacement.

The documentation also needed some love. The README was more or less
just a description of what the app does, with not much information
about how to actually build or run it. I added a Quick Start section
and expanded the Build section with Maven setup instructions. More
importantly, I set up automated releases using GitHub Actions.

This is actually a huge step forward compared to how I handled releases
before. Back in `version 0.7.4 <{filename}/posts/2023/jdeepl-version-0-7-4-released-pre-build-binaries-available_en.rst>`_, I was manually
uploading pre-built JARs to my personal Nextcloud instance. This
worked fine and was documented in the README, but wasn't exactly
convenient. Now when I push a tag, the
`GitHub Actions workflow <https://git.sr.ht/~wombelix/jDeepL/tree/main/item/.github/workflows/release.yml>`_
automatically builds the JAR and creates a GitHub release with the
file attached. Users can just go to the
`GitHub releases page <https://github.com/wombelix/jDeepL/releases>`_
and download binaries instead of having to build from source.

One thing I discovered during this modernization is that jnativehook,
the library I use for the global :code:`CTRL+C+C` hotkey, is likely
on its way to becoming unmaintained. It only works with X11 sessions,
and with bleeding-edge distros pushing toward Wayland, I might need
to find a different approach for hotkey handling in a few years. But
that's a problem for future me.

The project now builds with Java 17, uses updated dependencies, has
expanded documentation, and automated releases. The original issue
about build problems should be resolved now. Users can either download
pre-built JARs from GitHub releases or follow the updated build
instructions to compile from the
`source code <https://git.sr.ht/~wombelix/jDeepL>`_.

It wasn't groundbreaking work, overall just maintenance that was overdue.
But sometimes that's what projects need, a bit of attention to keep them
current and usable.

Next, I'm thinking about creating OS-specific packages using :code:`jpackage`.
This would let me provide :code:`.deb` and :code:`.rpm` packages that ship
with all dependencies. This would make the usage even easier compared to the
current :code:`JAR` file approach.
