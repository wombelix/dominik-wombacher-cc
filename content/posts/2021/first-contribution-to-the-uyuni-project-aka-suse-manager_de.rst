.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Mein erster Beitrag zum Uyuni Projekt aka SUSE Manager
######################################################

:date: 2021-03-24
:modified: 2021-03-24
:tags: SUSE Manager, Uyuni, Contribution
:description: Mein erster Beitrag zu Uyuni / SUSE Manager
:category: Code
:slug: mein-erster-beitrag-zum-uyuni-projekt-aka-suse-manager
:author: Dominik Wombacher
:lang: de
:transid: first-contribution-to-the-uyuni-project-aka-suse-manager
:status: published

Ich nutze viel Open Source Software und habe immer von der Arbeit der Community profitiert. 
Wann immer moeglich, versuche ich deshalb auch etwas beizutragen und zurueckzugeben.

Wie in anderen Beitraegen erwaehnt, verwende ich auf der Arbeit den SUSE Manager, das kommerzielle Produkt des Upstream 
Open Source Projekts `Uyuni <https://www.uyuni-project.org>`_, ein Fork von `Spacewalk <https://spacewalkproject.github.io>`_, 
den `SUSE 2018 <https://www.suse.com/c/were-back-to-earth-and-the-earth-is-flat-welcome-uyuni/>`__ angekuendigt hat 
(Archiv: `[1] <https://web.archive.org/web/20200421061926/https://www.suse.com/c/were-back-to-earth-and-the-earth-is-flat-welcome-uyuni/>`__,
`[2] <https://archive.today/2021.03.24-213548/https://www.suse.com/c/were-back-to-earth-and-the-earth-is-flat-welcome-uyuni/>`__).

Deshalb habe ich beschlossen, dass es an der Zeit ist, nach einem `good-first-issue <https://github.com/uyuni-project/uyuni/labels/good%20first%20issue>`_ zu suchen 
und das Uyuni Projekt zu unterstuetzen. Ich bin noch dabei, meine Java Skills zu verbessern, 
also dachte ich, dass einige Anpassungen am `Setup Bash Script <https://github.com/uyuni-project/uyuni/issues/1354>`__
(Archiv: `[1] <https://web.archive.org/web/20210324212349/https://github.com/uyuni-project/uyuni/issues/1354>`__,
`[2] <https://archive.today/2021.03.24-212400/https://github.com/uyuni-project/uyuni/issues/1354>`__) 
vielleicht das Richtige fuer den Anfang waeren.

Die Aufgabe war, den Produktnamen aus einer Standard Konfigurationsdatei auszulesen und diesen Wert, 
anstelle der fest hinterlegten Bezeichnung **SUSE Manager**, bei sichtbaren Ausgaben zu verwenden.

Heute ist mein `pull request <https://github.com/uyuni-project/uyuni/pull/3460>`__
(Archiv: `[1] <https://web.archive.org/web/20210324212223/https://github.com/uyuni-project/uyuni/pull/3460>`__,
`[2] <https://archive.today/2021.03.24-212223/https://github.com/uyuni-project/uyuni/pull/3460>`__) 
angenommen und in den main branch uebernommen worden :)

