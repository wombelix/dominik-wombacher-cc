.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

How-to ace the CKAD, CKA and CKS exam in just one month
#######################################################

:date: 2023-09-30
:modified: 2023-09-30
:tags: CKA, CKAD, CKS, Kubernetes, Certification, Exam
:description: I passed all three Kubernetes Certification exams in one month, here is how.
:category: Certification
:slug: how-to-ace-the-ckad-cka-and-cks-exam-in-just-one-month
:author: Dominik Wombacher
:lang: en
:transid: how-to-ace-the-ckad-cka-and-cks-exam-in-just-one-month
:status: published

Between 31st July and 21st August 2023, I passed the
`CKA <{filename}/posts/certifications/cka-certified-kubernetes-administrator_en.rst>`_,
`CKAD <{filename}/posts/certifications/ckad-certified-kubernetes-application-developer_en.rst>`_ and
`CKS <{filename}/posts/certifications/cks-certified-kubernetes-security-specialist_en.rst>`_ Exam.
It was quite a ride and required some discipline. Everything boils down to a lot of hands-on practice.

I know that something like this isn't common, most people need much more time
to prepare, which is totally fine. I do a lot of different trainings and certification exams
on a regular basis. I'm also a quick learner, have a lot of knowledge across a vast variaty
of topics. During the years, I developed mechanisms to effectively prepare and take exams.
But I'm not a role model, take all the time you need, don't rush it!

Key learning resources
----------------------

The CKA, CKAD and CKS courses from Mumshad Mannambeth are pretty good.
Quality is exactly in that order, CKA is superb, CKAD is ok and CKS the lowest.
They are available as subscription on `KodeKloud <https://kodekloud.com>`_
and from time to time on-sale for ~$15 on `Udemy <https://www.udemy.com/user/mumshad-mannambeth/>`_.

`killercoda.com <https://killercoda.com>`_ gives you free access to lab environments to practice various scenarios.
Make use of it! When the Exam date comes closer, you should get bored by this excercises and just know what to-do while reading the instructions.

`killer.sh <https://killer.sh>`_ with every Exam you purchase, you will get two session vouchers for free.
This should be your last preparation step before the actual Exam.
As soon you feel ready, use the killer.sh exam simulator to validate your knowledge.
Think of it like the real thing, block time, focus on the tasks, keep an eye on the timer.
Afterwards take a close look on the questions that you had wrong.
The environment is available for 24h, try to solve failed questions again.
If necessary practice again with KodeKloud and/or killercoda.
Take the second killer.sh session a day or two before your Exam as final preparation.
When you ace killer.sh, you ace the actual Exam too :)

"common" knowledge
------------------

You can call it common knowledge, basic knowledge or whatever name you think fits for all those
skills you should already have or brush up real quickly, because you will need them for the
kubernetes trifecta.

Linux
~~~~~

You should feel at home in a shell like bash, navigating around through different folder,
becoming root, starting/stopping services, copying or editing files, all this should be
your daily business.

If I ask you to start and enable service :code:`xyz`, you should right away have
something like :code:`systemctl enable --now xyz` in mind.

Copy file :code:`abc.yaml` to :code:`/etc/` on server :code:`node01`, for sure you know
that you can achieve this by running something like :code:`scp ./abc.yaml node01:/etc/`.

YAML
~~~~

Widely used markup language, Kubernetes Manifests are written in YAML but also
Ansible Playbooks and much more. You should familiar with the overall syntax.
How to spot syntax errors and perform the correct indentation.

vim
~~~

Vim is everywhere and in most shells set as default editor.
I highly recommend you brush up your skills.
Navigating and basic editing should be something you are familiar with.
YAML friendly settings in your :code:`.vimrc` are life safers.
The good news: In your Exam environment, that's pre-configured already :)

Some relevant settings from my vim rc file:

.. code::

  set fileencoding=UTF-8
  set syntax=on
  set ts=2
  set sw=2
  set sts=2
  set et nu

kubectl
-------

During the Exams, you use :code:`kubectl`, or the alias :code:`k`, all the time.
It is key that you life and breathe it, for example:

- Which sub-commands are available?
- How to find and show resources?
- How can you do a dry-run and redirect the output as YAML into a file?
- When should you use it to create/edit a resource and when write a Manifest?

Focus during your study on these things and practice, practice, practice!

Get used to type quickly and use tab-completion.
Copy & Paste is fine but I recommend to do it only for names or values.
This way you avoid typos but don't slow yourself down.

Before the Exam
---------------

Read all instructions about the PSI testing environment carefully!
They have comprehensive FAQ that will cover everything.
It is important that you do exactly what they expect.
Otherwise your risk that your Exam will be terminated by the proctor.

Perform a complete system test and fix any issues.
Trust me, you don't want that stress on the Exam day.

Remove everything from your Desk. If you have an external monitor and camera, I suggest you use them!
The display resolution should be as large as possible, I used a 4k display.
Don't try it with the standard Laptop Display, it will not provide enough space, you have to scroll around all the time.

Exam day
--------

You did all the practice and preparation, go relaxed into the Exam.
Get a good night sleep, stay hydrated but keep in mind that you can't pause the Exam.
So don't drink too much and use the Restroom before you start.
You going to focus for quite some time, your brain needs energy.
I always eat a Banana right before sitting the Exam.

Reading and understanding is key. Ensure you fully understand what you have to do.
For example, you might have a question about creating a backup of etcd.
Then there will be additional details like the node where you have to do it.
The path of the etcd database that you have to backup. The path where you have to store it.
All those details matter, don't waste points by overseeing parts of the instructions.

Prioritize questions with a high point count and start with them.
Read the instructions very carefully, if you feel comfortable, do it right away, if not flag it.
Pick the next question and repeat. Don't waste time on questions you can't solve.
Don't waste time with 5 questions that give you 1 point when you can solve 2 questions with 10 points each in the same time.
If there is time left at the end, go for the low score questions.
But solving the majority of high score question will make you pass.

Conclusion
----------

I found it extremely valuable to take all three Exams.
I learned so much during the preparation.
It helped me a lot in my Job as well.
I would do it again and if you decide to tackle them, I wish you all the best!
