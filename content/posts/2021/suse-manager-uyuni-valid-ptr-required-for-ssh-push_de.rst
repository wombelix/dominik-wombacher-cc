SUSE Manager / Uyuni - Gueltiger PTR Eintrag erforderlich fuer SSH-Push Clients
###############################################################################

:date: 2021-02-23
:modified: 2021-02-23
:tags: Uyuni, SUSE Manager, SSH, Salt, DNS
:description: Clients die an SUSE Manager / Uyuni angebunden sind brauchen PTR DNS Eintrag
:category: Linux
:slug: suse-manager-uyuni-gueltiger-ptr-eintrag-erforderlich-fuer-ssh-push
:author: Dominik Wombacher
:lang: de
:transid: suse-manager-uyuni-valid-ptr-required-for-ssh-push
:status: published

Ich bin fuer eine `SUSE Manager <https://www.suse.com/products/suse-manager/>`_ Installation, das kommerzielle 
Produkt basierend auf `Uyuni <https://www.uyuni-project.org>`_, mit beinahe 900 angebundenen Servern verantwortlich.

Die empfohlene Verbindungsmethode ist Salt Minion, aber SSH-Push - basierend auf Salt-SSH - ist die agentenlose Alternative.
In unserer Umgebung nutzen etwa 200 Server diese Variante, weil bereits ein Salt Minion installiert und mit einem anderen 
Salt Master verbunden ist.

Problem
*******

In den letzten Wochen kam es immer mal wieder vor, das der **salt-api** Dienst wegen einer unbehandelten Ausnahme abgestuerzt ist.

Die Untersuchung gemeinsam mit SUSE laeuft noch, aber bisher sieht es danach aus, das in seltenen faellen, ein Server mit Verbindungsmethode 
SSH-Push und ohne gueltigen PTR DNS Eintrag tatsaechtlich eine Exception in der Salt Codebasis ausloesen kann.

Hintergrund
***********

Funktion :code:`ip_to_host`, zu finden in **/usr/lib/python3.6/site-packages/salt/utils/network.py** uebergibt einen FQDN zur Python built-in Funktion 
:code:`socket.gethostbyaddr`. Das fuehrt zu einer Exception die von code:`ip_to_host` abgefangen wird und :code:`None` zurueck gibt 
(Es sollte eigentlich ein Hostname sein).

Basierend auf dem Rueckgabewert wird ein neuer Minion Job fuer den Server :code:`None` gestartet und endet in einer **unhandled Exception** die dazu fuehrt 
das **salt-api** abstuerzt, wie in nachfolgenden Fehlermeldungen zu sehen (*Salt* als auch *Taskomatic* muessen sich im Debug Modus befinden):

*/var/log/salt/api_error*

.. code-block::

	Traceback (most recent call last):
		File "/usr/lib/python3.6/site-packages/salt/netapi/rest_cherrypy/app.py", line 860, in hypermedia_handler
			ret = cherrypy.serving.request._hypermedia_inner_handler(*args, **kwargs)
		File "/usr/lib/python3.6/site-packages/cherrypy/_cpdispatch.py", line 54, in __call__
 			return self.callable(*self.args, **self.kwargs)
 		File "/usr/lib/python3.6/site-packages/salt/netapi/rest_cherrypy/app.py", line 2140, in POST
			'return': list(self.exec_lowstate()),
		File "/usr/lib/python3.6/site-packages/salt/netapi/rest_cherrypy/app.py", line 1187, in exec_lowstate
			ret = self.api.run(chunk)
		File "/usr/lib/python3.6/site-packages/salt/netapi/__init__.py", line 152, in run
			return l_fun(*f_call.get('args', ()), **f_call.get('kwargs', {}))
		File "/usr/lib/python3.6/site-packages/salt/netapi/__init__.py", line 218, in ssh
			return ssh_client.cmd_sync(kwargs)
		File "/usr/lib/python3.6/site-packages/salt/client/ssh/client.py", line 159, in cmd_sync
			**kwargs)
		File "/usr/lib/python3.6/site-packages/salt/client/ssh/client.py", line 123, in cmd
			for ret in ssh.run_iter(jid=kwargs.get('jid', None)):
		File "/usr/lib/python3.6/site-packages/salt/client/ssh/__init__.py", line 696, in run_iter
			self.cache_job(jid, host, ret[host], fun)
		File "/usr/lib/python3.6/site-packages/salt/client/ssh/__init__.py", line 720, in cache_job
			'fun': fun})
		File "/usr/lib/python3.6/site-packages/salt/returners/local_cache.py", line 147, in returner
			hn_dir = os.path.join(jid_dir, load['id'])
		File "/usr/lib64/python3.6/posixpath.py", line 94, in join
			genericpath._check_arg_types('join', a, *p)
		File "/usr/lib64/python3.6/genericpath.py", line 149, in _check_arg_types
			(funcname, s.__class__.__name__)) from None
	TypeError: join() argument must be str or bytes, not 'NoneType'

	During handling of the above exception, another exception occurred:

	Traceback (most recent call last):
 		File "/usr/lib/python3.6/site-packages/cherrypy/_cprequest.py", line 638, in respond
			self._do_respond(path_info)
		File "/usr/lib/python3.6/site-packages/cherrypy/_cprequest.py", line 697, in _do_respond
			response.body = self.handler()
		File "/usr/lib/python3.6/site-packages/cherrypy/lib/encoding.py", line 219, in __call__
			self.body = self.oldhandler(*args, **kwargs)
		File "/usr/lib/python3.6/site-packages/salt/netapi/rest_cherrypy/app.py", line 894, in hypermedia_handler
			if cherrypy.config['debug']
		File "/usr/lib64/python3.6/traceback.py", line 167, in format_exc
			return "".join(format_exception(*sys.exc_info(), limit=limit, chain=chain))
		File "/usr/lib64/python3.6/traceback.py", line 121, in format_exception
			type(value), value, tb, limit=limit).format(chain=chain))
		File "/usr/lib64/python3.6/traceback.py", line 498, in __init__
			_seen=_seen)
		File "/usr/lib64/python3.6/traceback.py", line 509, in __init__
			capture_locals=capture_locals)
		File "/usr/lib64/python3.6/traceback.py", line 338, in extract
			if limit >= 0:

	TypeError: '>=' not supported between instances of 'TypeError' and 'int'


*/var/log/salt/api*

.. code-block::

	[...]
	2021-02-08 01:08:01,229 [salt.utils.network:239 ][DEBUG ][38989] salt.utils.network.ip_to_host('server.example.com') failed: [Errno 0] Resolver Error 0 (no error)
	[...]
	2021-02-08 01:08:02,801 [salt.loaded.int.returner.local_cache:252 ][DEBUG ][38989] Adding minions for job 20210208000802780236: [None]
	[...]
	2021-02-08 01:08:02,839 [salt.utils.process:767 ][ERROR ][5340] An un-handled exception from the multiprocessing process 'Process-1:335' was caught:
	[...]
	2021-02-08 01:08:02,916 [salt.client.ssh :644 ][ERROR ][38989] Target 'None' did not return any data, probably due to an error.
	2021-02-08 01:08:02,917 [salt.loaded.int.netapi.rest_cherrypy.app:887 ][DEBUG ][38989] Error while processing request for: /run


*/var/log/rhn/rhn_taskomatic_daemon.log*

.. code-block::

	2021-02-08 01:08:02,976 [Thread-70313] ERROR com.redhat.rhn.taskomatic.task.SSHPush - com.suse.salt.netapi.
	exception.SaltException: Response code: 500
	java.lang.RuntimeException: com.suse.salt.netapi.exception.SaltException: Response code: 500
 		at com.suse.manager.webui.services.impl.SaltService.callSync(SaltService.java:235)
 		at com.suse.manager.webui.services.impl.SaltService.ping(SaltService.java:244)
 		at com.redhat.rhn.taskomatic.task.sshpush.SSHPushWorkerSalt.performCheckin(SSHPushWorkerSalt.java:337)
 		at com.redhat.rhn.taskomatic.task.sshpush.SSHPushWorkerSalt.lambda$run$0(SSHPushWorkerSalt.java:122)
 		at java.base/java.util.Optional.ifPresent(Optional.java:183)
 		at com.redhat.rhn.taskomatic.task.sshpush.SSHPushWorkerSalt.run(SSHPushWorkerSalt.java:110)
 		at EDU.oswego.cs.dl.util.concurrent.PooledExecutor$Worker.run(PooledExecutor.java:732)
 		at java.base/java.lang.Thread.run(Thread.java:834)
	Caused by: com.suse.salt.netapi.exception.SaltException: Response code: 500
 		at com.suse.salt.netapi.client.impl.HttpAsyncClientImpl.createSaltException(HttpAsyncClientImpl.java:
		145)
 		at com.suse.salt.netapi.client.impl.HttpAsyncClientImpl.access$000(HttpAsyncClientImpl.java:27)
 		at com.suse.salt.netapi.client.impl.HttpAsyncClientImpl$1.completed(HttpAsyncClientImpl.java:121)
 		at com.suse.salt.netapi.client.impl.HttpAsyncClientImpl$1.completed(HttpAsyncClientImpl.java:101)
 		at org.apache.http.concurrent.BasicFuture.completed(BasicFuture.java:123)
 		at org.apache.http.impl.nio.client.DefaultClientExchangeHandlerImpl.responseCompleted
	(DefaultClientExchangeHandlerImpl.java:181)
 		at org.apache.http.nio.protocol.HttpAsyncRequestExecutor.processResponse(HttpAsyncRequestExecutor.java:
		442)
 		at org.apache.http.nio.protocol.HttpAsyncRequestExecutor.inputReady(HttpAsyncRequestExecutor.java:332)
 		at org.apache.http.impl.nio.DefaultNHttpClientConnection.consumeInput(DefaultNHttpClientConnection.java:
		265)
 		at org.apache.http.impl.nio.client.InternalIODispatch.onInputReady(InternalIODispatch.java:81)
 		at org.apache.http.impl.nio.client.InternalIODispatch.onInputReady(InternalIODispatch.java:39)
 		at org.apache.http.impl.nio.reactor.AbstractIODispatch.inputReady(AbstractIODispatch.java:121)
 		at org.apache.http.impl.nio.reactor.BaseIOReactor.readable(BaseIOReactor.java:162)
 		at org.apache.http.impl.nio.reactor.AbstractIOReactor.processEvent(AbstractIOReactor.java:337)
 		at org.apache.http.impl.nio.reactor.AbstractIOReactor.processEvents(AbstractIOReactor.java:315)
 		at org.apache.http.impl.nio.reactor.AbstractIOReactor.execute(AbstractIOReactor.java:276)
 		at org.apache.http.impl.nio.reactor.BaseIOReactor.execute(BaseIOReactor.java:104)
 		at org.apache.http.impl.nio.reactor.AbstractMultiworkerIOReactor$Worker.run
	(AbstractMultiworkerIOReactor.java:588)
 	... 1 more


Mit zwei Python basierenden befehlen, kann schnell geprueft werden, ob reverse lookup fuer einen FQDN funktioniert.
In diesem Beispiel nehmen wir an, das der FQDN **server.example.com** und die IP Adresse **10.11.12.13** ist:


.. code-block::

	python3 -c 'import socket; print(socket.gethostbyaddr("server.example.com"))'
	python3 -c 'import socket; print(socket.getaddrinfo("server.example.com", 0, 0, 0, 0))'


Wenn alles in Ordnung ist sollten beide etwas vergleichbares ausgeben:


.. code-block::

	('server.example.com', [], ['10.11.12.13'])
	[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('10.11.12.13', 0)), 
		(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('10.11.12.13', 0)), 
		(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_RAW: 3>, 0, '', ('10.11.12.13', 0))]


Weitere Lektuere zu *gethostbyaddr*: https://docs.python.org/3/library/socket.html#socket.gethostbyaddr

Loesung
*******

Ich gehe davon aus das SUSE einen Patch in zukuenftige SUSE Manager und Uyuni release einbinden wird, bei dem Server 
wahrscheinlich uebersprungen werden, wenn es keinen gueltigen PTR Eintrag gibt. Daher sollte geprueft werden, das in 
der Umgebung alle Systeme die per SSH-Push / Salt-SSH verbunden sind, die erforderlichen DNS Eintraege haben und ueber 
den FQDN als auch die IP Adresse aufgeloest werden koennen, um etwaige Probleme zu vermeiden.
