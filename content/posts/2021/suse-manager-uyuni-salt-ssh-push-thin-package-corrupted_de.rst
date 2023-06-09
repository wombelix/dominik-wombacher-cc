SUSE Manager / Uyuni - Salt SSH Push: Thin Paket beschaedigt
############################################################

:date: 2021-03-02
:modified: 2021-03-02
:tags: Uyuni, SUSE Manager, SSH, Salt, Exception
:description: SUSE Manager / Uyuni beschaedigtes thin Paket verursacht "ImportError: No module named 'salt.exceptions'"
:category: Linux
:slug: suse-manager-uyuni-salt-ssh-push-thin-paket-beschaedigt
:author: Dominik Wombacher
:lang: de
:transid: suse-manager-uyuni-salt-ssh-push-thin-package-corrupted
:status: published

Bei der Arbeit hatten wir monatelang Probleme mit fast allen Salt-SSH / SSH-Push verbundenen Clients aufgrund einer unbehandelten Ausnahme :code:`ImportError: Kein Modul namens 'salt.exceptions'`, die regelmaessig auftrat. Es hat mich viel Zeit gekostet, das Problem zusammen mit SUSE zu finden, daher moechte ich meine Erfahrungen teilen.

Fehler
******

.. code::

  [...]
  "stderr": "Traceback (most recent call last):\n File
  \"/var/tmp/.user_a567dc_salt/salt-call\", line 26, in \n from
  salt.scripts import salt_call\n File
  \"/var/tmp/.user_a567dc_salt/pyall/salt/scripts.py\", line 21, in \n
  from salt.exceptions import SaltSystemExit, SaltClientError,
  SaltReqTimeoutError\nImportError: No module named 'salt.exceptions'"
  [...]

Hintergrund
***********

Normalerweise verwendet Salt einen Agenten (Salt-Minion), unterstuetzt aber auch einen agentenlosen Ansatz genannt Salt-SSH. 
Ein Paket (*"thin.tgz"*), das den gesamten Python Code und alle Dateien enthaelt, die Salt benoetigt, um Jobs auf einem Server auszufuehren, wird hochgeladen und nach **/var/tmp/.<user>_<id>_salt/** auf dem Zielserver entpackt. 
Die "*id*" bezieht sich auf die verwendete Salt-Version, der "*user*" ist derjenige, der auf dem Salt-Master - in diesem Fall der SUSE Manager - konfiguriert ist, der auf dem Ziel volle sudo Rechte hat und sich per SSH anmelden darf.

Jedes Mal, wenn Salt eine Verbindung herstellt, um einen Job auszufuehren, werden einige Pruefungen durchgefuehrt, um den Zustand des Thin Pakets zu ueberpruefen:

- Existiert der Ordner fuer den angegebenen Benutzer mit der passenden ID in */var/tmp/*

- Ist die Datei *"code-checksum "* vorhanden und stimmt die darin enthaltene Pruefsumme mit dem thin.tgz Archiv auf dem Salt Master ueberein

Solange beide Pruefungen erfolgreich sind, wird der Salt Master _keine_ neue *thin.tgz* hochladen - das ist wichtig zu verstehen.

Fehlersuche
***********

Zunaechst war voellig unklar, woher das Problem kam, es konnte bei jedem Auftragstyp auftreten, auf verschiedenen Servern und zu unterschiedlichen Zeiten. 
Das Thin Paket war immer ab irgendeinem Punkt beschaedigt, was die unbehandelte Ausnahme verursachte. 
Der Workaround bestand darin, den gesamten Ordner des Salt Thin Pakets auf dem Zielserver manuell zu loeschen, damit der Salt Master beim naechsten Mal eine frische Kopie hochlaedt.

SUSE hat mir dabei geholfen, Unmengen von Protokollen durchzugehen und eine Zeitleiste zu erstellen, auf der zu erkennen war, dass das Problem scheinbar alle 7 Tage auftritt.

Weitere Untersuchungen bestaetigten, dass das Problem in diesem Fall leider selbst verursacht war. Jemand aus dem Team hat systemd so konfiguriert, dass der tmp Ordner auf vielen Servern automatisch aufgeraeumt wird und hat dies weder ausreichend getestet noch gut dokumentiert. 
Das Entfernen des Thin Package Ordners waere an sich kein Problem, er wuerde einfach neu hochgeladen werden, solange es richtig gemacht wird, aber das war nicht der Fall.

.. code::

  /etc/tmpfiles.d/clean_tmp.conf
  
  D /tmp 1777 root root 7d
  D /var/tmp 1777 root root 7d

Die tmpfiles Konfiguration entfernte nur Dateien und Ordner, die dem Benutzer *root* gehoeren, aber ein paar Dateien, wie "*code-checksum*", des Thin Pakets gehoeren Salt. 
So wurden alle 7 Tage die meisten Dateien entfernt und somit Salt thin beschaedigt, aber der Salt Master fand den Ordner und die "*code-checksum*" Datei mit dem richtigen Hash und dachte, Thin sei in Ordnung und auf dem aktuellen Stand.

Loesung
*******

Am Ende habe ich einfach die benutzerdefinierte tmpfiles Konfiguration und noch einmal den Thin Ordner manuell auf allen betroffenen Servern entfernt. 

Fuer uns hatte es keinen wirklichen Nutzen, das Thin Paket woechentlich zu loeschen und hohe Last zu erzeugen sowie Bandbreite zu verbrauchen, um es erneut hochzuladen. Falls du die regelmaessige Bereinigung der tmp Ordner bevorzugst, stelle unbedingt sicher, dass der gesamte Thin Ordner und alle Dateien von deinem Regelwerk abgedeckt sind und entweder vollstaendig entfernt oder ignoriert werden.

Auch wenn es ein menschlicher Fehler war und nicht direkt mit SUSE Manager / Uyuni oder Salt zusammenhaengt, hat es doch gezeigt, wie anfaellig solche Komponenten sein koennen. 
Aus technischer Sicht verstehe ich, warum es nur ein paar Ueberpruefungen und eine Validierung des Hashs in einer Datei gibt. 
Das fuer den gesamten Ordnerinhalt bei jedem Job zu machen, waere einfach zu langsam und wuerde die Last unnoetig erhoehen. 
Aber wie wir sehen, hat das im Zweifel auch seinen Preis und kann durch etwas beeintraechtigt werden, das man nicht erwartet.
