PDF Dateien zusammenfuehren unter Linux
#######################################

:date: 2019-10-28 15:38
:modified: 2019-10-28 15:38
:tags: Bash, CUPS, PDF, openSUSE
:category: Linux
:slug: pdf-dateien-zusammenfuehren-unter-linux
:author: Dominik Wombacher
:lang: de
:transid: merge-pdf-files-on-linux
:status: published

Ich musste mit Cups-PDF einen Haufen Seiten als einzelne PDF Dateien "ausdrucken", da es nicht moeglich war Sie als PDF herunterzuladen.
Aber wie fuehrt man Tonnen an PDF Dokumenten die **Pagetitle-job_id<Number>** heissen unter Linux per command line moeglichst schnell und einfach zusammen?

Nach einigen Tests, :code:`pdfunite` - inkludiert in *Poppler* und bereits unter openSUSE Tumbleweed vorinstalliert - hat die Aufgabe erledigt, 
aber die Ergebnisse mit :code:`pdftk` - inkludiert in *Ghostscript* - war beinahe identisch und hat auf die gleiche Art funktioniert.

.. code-block::

	pdfunite $(ls -cr *.pdf) output.pdf

Mit :code:`$()`, :code:`ls` wird ausgefuehrt und die Ergebnisse an den Befehl :code:`pdfunite` angehangen. 

Alle PDF Dateien im gleichen Ordner werden zusammengefuehrt zu einer einzelnen **output.pdf** Datei. 

Der Parameter :code:`-cr` sortiert nach dem Erstelldatum in umgedrehter Reihenfolge.

Das war in meinem Fall erforderlich, weil die Job IDs von 36 bis 223 gingen, alle anderen Parameter haben die Reihenfolge durcheinander gebracht und das Resultat war nicht wie erwartet.
