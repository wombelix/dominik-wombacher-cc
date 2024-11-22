.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

SUSE Hack Week 2024 - Day 4
###########################

:date: 2024-11-21
:modified: 2024-11-21
:tags: SUSE, openSUSE, pagure, HackWeek, AWS, CodePipeline, Coding, OpenSource
:description: Experiences and outcome of my fourth day at SUSE Hack Week 2024
:category: Code
:slug: suse-hack-week-2024-day-4
:author: Dominik Wombacher
:lang: en
:transid: suse-hack-week-2024-day-4
:status: published

Today was the focus on writing the pagure ci plugin and fine-tune my design and architecture assumptions on the way. 
Basically transferring the outcome of `day 3 <{filename}/posts/2024/suse-hack-week-2024-day-3_en.rst>`_ into some code. 
I decided to use a Test-Driven approach and to keep a close eye on existing pagure ci related tests while 
I have to refactor some existing code too. 

Before I started to write tests, I wanted to validate a couple of assumptions on my pagure dev instance. 
Unfortunately I had to fix a couple errors over there (file permissions, pagure_worker runs as apache and 
not git user, db scheme forgotten to upgrade...) before I finally could start. It's always a good opportunity, 
you learn most when things are broken. But I lost quite some coding time that way...

Speaking of coding, the main challenge was that some information I want/need in my generic plugin are currently not passed. 

What we currently have doesn't leaves much room for the plugin to get additional data:

.. code:: python

    def trigger_build(
        project_path,
        url,
        job,
        token,
        branch,
        branch_to,
        cause,
        ci_username=None,
        ci_password=None,
    ):

What I want in future to make things more flexible:

.. code:: python

    def trigger_build(
            project: model.Project,
            ci_url: str,
            ci_job: str,
            ci_token: str,
            branch: str,
            branch_to: str,
            is_pull_request: bool = False,
            is_commit: bool = False,
            commit_hash: str = None,
            pull_request_id: str = None,
            pull_request_uid: str = None,
            ci_username = None,
            ci_password = None,
    ) -> None:

This could be further improved by passing :code:`model.PullRequest` instead of :code:`pull_request_id` and :code:`pull_request_uid`. 
Then it's up to the pagure ci plugin to decide what data are needed, similar as with :code:`project`. 
When I'm done with the :code:`generic` plugin then the existing :code:`jenkins` need some refactoring to work with the new parameters. 

I started to write the tests and iterate through the different plugin functionality. 
All that went well until I hit a problem that still drives me crazy. 
It shouldn't be hard to verify that a method was called with the expected args by using :code:`assert_called_once_with`.
But it throws a nice :code:`AssertionError: expected call not found.` even though :code:`Expected` and :code:`Actual` match:

.. code:: python

    E           AssertionError: expected call not found.
    E           Expected: trigger_build(project=Project(1, name:test, namespace:None, url:None, is_fork:False, parent_id:None), ci_url='https://ci.example.com/', ci_job='pagure', ci_token='random_token', branch='feature', branch_to='main', is_pull_request=True, is_commit=False, commit_hash=None, pull_request_id='1', pull_request_uid='720a0568c1274e74966e54b433b2003e', ci_username=None, ci_password=None)
    E           Actual:   trigger_build(project=Project(1, name:test, namespace:None, url:None, is_fork:False, parent_id:None), ci_url='https://ci.example.com/', ci_job='pagure', ci_token='random_token', branch='feature', branch_to='main', is_pull_request=True, is_commit=False, commit_hash=None, pull_request_id='1', pull_request_uid='720a0568c1274e74966e54b433b2003e', ci_username=None, ci_password=None)

I take a break and try it again tomorrow after some sleep. Maybe I'm tired and missing something obvious. 
But for me both look the same and there shouldn't be an assertion error. 

Let's hope I can figure out tomorrow what's going wrong here...