.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

AWX CleanUp Job but Postgres Database still grows
#################################################

:date: 2021-02-22 16:27
:modified: 2021-02-22 16:27
:tags: AWX, Postgres, Database
:description: Interesting situation, running out of space due to continuously growing Database.
:category: Linux
:slug: awx-cleanup-job-but-postgres-database-still-grows
:author: Dominik Wombacher
:lang: en
:transid: awx-cleanup-job-but-postgres-database-still-grows
:status: published

I encountered a interesting situation at work today, the disk were the persistent data of our `Ansible AWX`_ instance are located was running out of space.
The Postgres Database, or to be very specific the Table **main_jobevent** was around 16GB in size and still growing.

.. _`Ansible AWX`: https://github.com/ansible/awx

Some time ago the CleanUp Jobs were activated / scheduled, so it looks like that data prior that time was skipped and not removed.
Also I had to learn that even in case some data will be deleted, Postgres will not automatically free-up previously allocated storage.

Job Event removal
*****************

First I removed old job events, which were skipped by the AWX Cleanup Schedule, via `awx-manage` within the Docker Container `awx_task`:

.. code-block:: bash

  docker exec -it awx_task /bin/bash
  awx-manage shell_plus

The range value need to be adjusted based on your needs, in my Case I wanted to remove the job event *1* till *2949*:

.. code-block:: python

  from awx.main.models import Job
  for record_id in range(1, 2949):
  try:
      db_object = Job.objects.get(id=record_id)
      db_object.delete()
  except:
      pass

Source: https://tobschall.de/2019/05/07/ansible-tower-cleanup/ 
(Archive: `[1] <http://web.archive.org/web/20210222141052/https://tobschall.de/2019/05/07/ansible-tower-cleanup/>`__,
`[2] <http://archive.today/2021.02.22-212548/https://tobschall.de/2019/05/07/ansible-tower-cleanup/>`__)


Postgres Cleanup
****************

So even though it was a little *"forcible"* approach, it worked quite well in my case, but that shouldn't be the Standard Solution on a day-to-day basis.
Actually I expect that something similar will not be necessary in future due to enabling of **auto-vacuum** and adjusted **AWX Cleanup Schedules**.

.. code-block:: bash

  docker exec -it awx_postgres /bin/bash
  psql -U awx
  
  \c awx

As you can see, **VACUUM FULL** (`handle with care!`_) was able to free up approx. 11GB space:

.. _`handle with care!`: https://www.postgresql.org/docs/10/sql-vacuum.html

.. code-block:: sql

  SELECT pg_size_pretty( pg_total_relation_size('public.main_jobevent') );
  
  # pg_size_pretty
  #----------------
  # 16 GB
  # (1 row)

  VACUUM FULL public.main_jobevent;
  SELECT pg_size_pretty( pg_total_relation_size('public.main_jobevent') );

  # pg_size_pretty
  #----------------
  # 4915 MB
  # (1 row)


auto-vacuum enabling
********************

It seems like that in the config delivered with the AWX Docker Container, the **auto-vacuum** feature is disabled in Postgres.
Can be quickly enabled with two minor adjustments in **postgresql.conf**:

.. code-block:: ini

  track_counts = on
  autovacuum = on

For the change to take effect, the Postgres Database need to be restarted.
You can for sure also just stop and start the AWX Stack via `docker-compose`, whatever you prefer.

AWX Job Schedules
*****************

Last but not least, I adjusted to AWX CleanUp Jobs to run Daily with a Retention of 14 days, that's sufficient in our Environment and should help to avoid similar issues.

