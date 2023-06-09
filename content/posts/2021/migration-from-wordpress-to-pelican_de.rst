Migration von Wordpress zu Pelican
##################################

:date: 2021-03-01
:modified: 2021-03-01
:tags: Wordpress, Pelican, Migration
:description: Anfang meiner Reise von Wordpress zu Pelican
:category: Misc
:slug: migration-von-wordpress-zu-pelican
:author: Dominik Wombacher
:lang: de
:transid: migration-from-wordpress-to-pelican
:status: published

Vor ein paar Jahren habe ich meine persoenliche Website auf Basis von Wordpress eingerichtet und war damit recht zufrieden. 
Aber nach einiger Zeit war ich mir nicht mehr sicher, ob das wirklich das ist, was ich will:

- Erstens musste ich mich alle paar Wochen um Updates kuemmern und hatte immer ein ungutes Gefuehl wegen moeglicher Sicherheitsprobleme. 

- Außerdem konnten die Inhalte, die ich hinzugefuegt hatte, nicht einfach in andere Formate konvertiert werden oder der Quellcode ohne Plugins geteilt werden.

- Zu guter letzt, mussten einige Megabyte uebertragen werden, mehrere Cookies gesetzt und viel Javascript geladen werden, nur um einen kurzen Beitrag zu lesen.

Ich fing an, mich umzusehen und fand den Ansatz gut, einen statischen Seitengenerator zu verwenden und mich auf reines HTML und CSS zu fokusieren.

Nach einigen Recherchen und Tests entschied ich mich fuer `Pelican <https://www.getpelican.com>`_, es basiert auf Python und kann durch 
durch `Plugins <https://github.com/pelican-plugins/>`_ erweitert werden.

Also machte ich mich an die Arbeit:

- Ein eigenes Theme zu erstellen

- Mitzuhelfen, `alte Plugins <https://github.com/getpelican/pelican-themes>`_ zu aktualisieren und zu migrieren, die ich verwenden wollte

- Inhalte, die auf verschiedene Orte verteilt sind, nach reStructuredText zu migrieren

Ich bin noch nicht fertig, aber wie man sehen kann, gab es schon einige Fortschritte :)

Ich plane, mein Theme in Kuerze zu veroeffentlichen und auch mehr Zeit in die Mitarbeit am Pelican Projekt zu investieren.
