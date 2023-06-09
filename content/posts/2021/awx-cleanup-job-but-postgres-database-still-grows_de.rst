.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

AWX CleanUp Job aber Postgres Datenbank waechst weiter
######################################################

:date: 2021-02-22 22:43
:modified: 2021-02-22 22:43
:tags: AWX, Postgres, Database
:description: Interessante Situation, der Speicherplatz wird knapp da die Datenbank immer weiter anwaechst.
:category: Linux
:slug: awx-cleanup-job-aber-postgres-datenbank-waechst-weiter
:author: Dominik Wombacher
:lang: de
:transid: awx-cleanup-job-but-postgres-database-still-grows
:status: published

Ich bin heute auf der Arbeit auf eine interessante Situation gestossen, die Festplatte auf der die Daten unserer `Ansible AWX`_ Instanz abgelegt sind ist vollgelaufen.
Die Postgres Datenbank, oder um sehr genau zu sein die Tabelle **main_jobevent**, war ungefaehr 16GB gross und wuchs weiter an.

.. _`Ansible AWX`: https://github.com/ansible/awx

Vor einiger Zeit sind die CleanUp Jobs aktiviert worden, es sieht so aus als wuerden Daten vor diesem Zeitpunkt uebersprungen und nicht entfernt werden.
Ich musste ausserdem lernen, das selbst wenn Daten geloescht wuerden, Postgres nicht automatisch den Speicherplatz freigibt wenn er einmal belegt war.

Entfernung von Job Events
*************************

Zuerst habe ich alte job events, die bei den geplanten AWX Cleanup's uebersprungen wurden, via `awx-manage` innerhalb des Docker Container `awx_task` entfernt:

.. code-block:: bash

  docker exec -it awx_task /bin/bash
  awx-manage shell_plus

Der Wert fuer *range* muss nach den eigenen Anforderungen angepasst werden, in meinem Fall wollte ich die job events *1* bis *2949* loeschen:

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

Auch wenn es ein eher etwas *"gewaltsamer*" Ansatz war, in meinem Fall hat es ziemlich gut funktioniert, es sollte aber definitiv nicht die Standard Loesung sein.
Fuer die Zukunft erwarte ich eigentlich nicht das nochmal etwas vergleichbares erforderlich wird, nachdem noch **auto-vacuum** aktiviert und die **AWX Cleanup Schedules** angepasst wurden.

.. code-block:: bash

  docker exec -it awx_postgres /bin/bash
  psql -U awx
  
  \c awx

Wie zu erkennen ist, konnte mit **VACUUM FULL** (`mit Vorsicht behandeln!`_) etwa 11GB Speicherplatz freigegeben werden:

.. _`mit Vorsicht behandeln!`: https://www.postgresql.org/docs/10/sql-vacuum.html

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


auto-vacuum aktiviert
*********************

Es scheint so das in der Konfiguration die mit dem AWX Container mitgeliefert wird, das Feature **auto-vacuum** in Postgres deaktiviert ist.
Das kann allerdings relativ schnell mit zwei kleinen Aenderungen in **postgresql.conf** aktiviert werden:

.. code-block:: ini

  track_counts = on
  autovacuum = on

Damit die Aenderungen wirksam werden, muss die Postgres Datenbank neugestartet werden.
Alternativ kann natuerlich auch der AWX Stack via `docker-compose` einmal gestoppt und wieder gestartet werden.

AWX Job Schedules
*****************

Zu guter letzt, habe ich die Planung der AWX CleanUp Jobs angepasst, Sie werden jetzt taeglich ausgefuehrt und haben eine Vorhaltezeit von 14 Tagen.
Das reicht in unserer Umgebung aus und sollte helfen vergleichbare Probleme in Zukunft zu vermeiden.
