.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

How changing '<' to '>=' introduced a weird and hard to track bug
#################################################################

:date: 2022-03-22
:modified: 2022-03-22
:tags: Uyuni, reposync, urlgrabber, bug, proxy
:description: Even small changes can have a massic and unexpected impact
:category: Code
:slug: how_changing_less-than_to_greater-equal_introduced_a_weird_and_hard_to_track_bug 
:author: Dominik Wombacher
:lang: en
:transid: how_changing_less-than_to_greater-equal_introduced_a_weird_and_hard_to_track_bug 
:status: published

After upgrading to `Uyuni 2022.2 <https://www.uyuni-project.org>`_ I wasn't able to sync openSUSE Leap 15.3 
and Oracle Linux 8 repositories anymore, the configured HTTP Proxy was ignored. Multiple people reported similar issues: 
`#4932 <https://github.com/uyuni-project/uyuni/issues/4932>`__
(Archive: `[1] <https://web.archive.org/web/20220322220517/https://github.com/uyuni-project/uyuni/issues/4932>`__,
`[2] <https://archive.today/2022.03.22-220522/https://github.com/uyuni-project/uyuni/issues/4932>`__),  
`#4850 <https://github.com/uyuni-project/uyuni/issues/4850>`__
(Archive: `[1] <https://web.archive.org/web/20220322220540/https://github.com/uyuni-project/uyuni/issues/4850>`__,
`[2] <https://archive.today/2022.03.22-220553/https://github.com/uyuni-project/uyuni/issues/4850>`__), 
`#4826 <https://github.com/uyuni-project/uyuni/issues/4826>`__
(Archive: `[1] <https://web.archive.org/web/20220322220605/https://github.com/uyuni-project/uyuni/issues/4826>`__,
`[2] <https://archive.today/2022.03.22-220613/https://github.com/uyuni-project/uyuni/issues/4826>`__).

During multiple troubleshooting sessions I learned a lot about 
the Python Codebase and the reposync tool.

It took my quite a while to track down the Issue to the :code:`urlgrabber` package.

What happened? Method :code:`find_proxy` in :code:`urlgrabber.grabber.URLGrabberOptions` 
will identify the proxy server that should be used based on the provided URL Scheme.

Let's assume :code:`server.satellite.http_proxy` in :code:`/etc/rhn/rhn.conf` is set to :code:`http://10.11.12.13:80`. 

.. code-block:: python

  >>> from urlgrabber.grabber import URLGrabberOptions
  >>> opts = URLGrabberOptions(proxy=None, proxies={'http': 'http://10.11.12.13:80', 'https': 'http://10.11.12.13:80', 'ftp': 'http://10.11.12.13:80'})
  >>> opts.find_proxy(b'http://test.example.com', b'http')

That's the simplified version of the relevant Code, a Instance of :code:`URLGrabberOptions` contains a list of proxies, 
one per URL Scheme, the method :code:`find_proxy` is used to choose the right proxy from :code:`opts.proxies` 
based on two parameter, :code:`url` and :code:`scheme`, both are passed as type :code:`bytes`.

The expected result, :code:`opts.proxy` contains the value :code:`http://10.11.12.13:80` from type :code:`str`, 
actual result, :code:`None`.

The package :code:`urlgrabber` is quite old and not that actively maintained. 
Python 3 support was added in Version 4, the last release is from October 2019. 

It looks like that the above issues, that proxy is None, comes from an inconsistent bytes / string conversion. 
If you pass the scheme as string instead bytes, you get the expected result:

.. code-block:: python

  >>> from urlgrabber.grabber import URLGrabberOptions
  >>> opts = URLGrabberOptions(proxy=None, proxies={'http': 'http://10.11.12.13:80', 'https': 'http://10.11.12.13:80', 'ftp': 'http://10.11.12.13:80'})
  >>> opts.find_proxy(b'http://test.example.com', 'http')
  >>> opts.proxy
  'http://10.11.12.13:80'

To get the Sync of openSUSE Leap 15.3 and Oracle Linux 8 Repositories working again 
through a http proxy, a small change was already sufficient:

.. code-block:: diff

  diff --git a/backend/satellite_tools/download.py b/backend/satellite_tools/download.py
  index 3d064e5c6ce..3b7a02d5176 100644
  --- a/backend/satellite_tools/download.py
  +++ b/backend/satellite_tools/download.py
  @@ -114,7 +114,7 @@ def __init__(self, url, filename, opts, curl_cache, parent):
           self.parent = parent
           (url, parts) = opts.urlparser.parse(url, opts)
           (scheme, host, path, parm, query, frag) = parts
  -        opts.find_proxy(url, scheme)
  +        opts.find_proxy(url, scheme.decode("utf-8"))
           super().__init__(url, filename, opts)
   
       def _do_open(self):

Pull Request `#4953 <https://github.com/uyuni-project/uyuni/pull/4953>`__
(Archive: `[1] <https://web.archive.org/web/20220322220636/https://github.com/uyuni-project/uyuni/pull/4953>`__,
`[2] <https://archive.today/2022.03.22-220654/https://github.com/uyuni-project/uyuni/pull/4953>`__)
was accepted and merged, unfortunately a few user still reported issues, especially related to CentOS 7 this time.

After a quick check, I had the impression that syncing EL8 based Distributions like Oracle Linux 8 
share the same Code as EL7 based Distributions like CentOS 7. 
More or less right, but due to things like *mirrorlist*, there are some additional steps and further 
calls of :code:`urlgrabber` split across the reposync code.

I had to find another way to fix it without touching multiple files and methods. 
So I gave some hacky `Monkey Patching <https://en.wikipedia.org/wiki/Monkey_patch>`_ a try. 
First I reverted the previous workaround:

.. code-block:: diff

  diff --git a/python/spacewalk/satellite_tools/download.py b/python/spacewalk/satellite_tools/download.py
  index 3b7a02d5176..3d064e5c6ce 100644
  --- a/python/spacewalk/satellite_tools/download.py
  +++ b/python/spacewalk/satellite_tools/download.py
  @@ -114,7 +114,7 @@ def __init__(self, url, filename, opts, curl_cache, parent):
           self.parent = parent
           (url, parts) = opts.urlparser.parse(url, opts)
           (scheme, host, path, parm, query, frag) = parts
  -        opts.find_proxy(url, scheme.decode("utf-8"))
  +        opts.find_proxy(url, scheme)
           super().__init__(url, filename, opts)
   
       def _do_open(self):

Then I created a new :code:`find_proxy` method, which just triggers the original one 
but performs the bytes to string conversion. The magic happens in the two lines after 
the method, :code:`urlgrabber_find_proxy` becomes the method from :code:`urlgrabber` 
and my own version replaces the original one. That way it doesn't matter where in 
:code:`yum_src.py` anything related to :code:`urlgrabber` will be triggered, scheme 
will always be converted to a string a the proxy set as configured and expected.

.. code-block:: diff

  diff --git a/python/spacewalk/satellite_tools/repo_plugins/yum_src.py b/python/spacewalk/satellite_tools/repo_plugins/yum_src.py
  index 85013cfb36a..39f36be61e5 100644
  --- a/python/spacewalk/satellite_tools/repo_plugins/yum_src.py
  +++ b/python/spacewalk/satellite_tools/repo_plugins/yum_src.py
  @@ -80,6 +80,17 @@
   APACHE_USER = 'wwwrun'
   APACHE_GROUP = 'www'
   
  +
  +# Monkey Patch 'urlgrabber.grabber' method 'find_proxy' to enforce type string for variable 'scheme'
  +# Workaround due to wrong byte/string handling in 'urlgrabber' package
  +# Required by reposync to connect through http_proxy as configured
  +def find_proxy(self, url, scheme):
  +    urlgrabber_find_proxy(self, url, scheme.decode('utf-8'))
  +
  +urlgrabber_find_proxy = urlgrabber.grabber.URLGrabberOptions.find_proxy
  +urlgrabber.grabber.URLGrabberOptions.find_proxy = find_proxy
  +
  +
   class ZyppoSync:
       """
       This class prepares a environment for running Zypper inside a dedicated reposync root

There is a `Issue <https://github.com/rpm-software-management/urlgrabber/issues/33>`__
(Archive: `[1] <https://web.archive.org/web/20220322220711/https://github.com/rpm-software-management/urlgrabber/issues/33>`__,
`[2] <https://archive.today/2022.03.22-220733/https://github.com/rpm-software-management/urlgrabber/issues/33>`__)
in the urlgrabber repository, until that's fixed, it looks like that a 
workaround in the Uyuni / reposync Codebase will be required.

I created a new `Pull Request <https://github.com/uyuni-project/uyuni/pull/5051>`__
(Archive: `[1] <https://web.archive.org/web/20220322220814/https://github.com/uyuni-project/uyuni/pull/5051>`__,
`[2] <https://archive.today/2022.03.22-220809/https://github.com/uyuni-project/uyuni/pull/5051>`__) 
in the Uyuni Project based on the above described fix, let's see if anyone comes 
up with a more elegant solution or if the guys are happy with that one and agree to merge it.

Based on my tests, by syncing *openSUSE Leap 15.3*, *Oracle Linux 8*, *CentOS 7* and *Ubuntu 20.04* repositories, 
it should finally resolve all, so far known, Issues related to reposync and HTTP Proxy.

And what had all this to do with a change of '<' to '>='?

In PR `#4604 <https://github.com/uyuni-project/uyuni/pull/4604>`__
(Archive: `[1] <https://web.archive.org/web/20220322220815/https://github.com/uyuni-project/uyuni/pull/4604>`__,
`[2] <https://archive.today/2022.03.22-220831/https://github.com/uyuni-project/uyuni/pull/4604>`__) 
the version was bumped, changing :code:`python3-urlgrabber < 4` to 
:code:`python3-urlgrabber >= 4` caused all that trouble and lot of issues 
where syncing repositories behind a http proxy was just not possible anymore.
