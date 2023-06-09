Why Open Source matter, experience of my last contribution to Uyuni
###################################################################

:date: 2022-12-22
:modified: 2022-12-22
:tags: Open Source, Uyuni, Contribution
:description: Experience of my last contribution to the Uyuni Project (Upstream of SUSE Manager)
:category: Code
:slug: why-open-source-matter-experience-of-my-last-contribution-to-uyuni
:author: Dominik Wombacher
:lang: en
:transid: why-open-source-matter-experience-of-my-last-contribution-to-uyuni 
:status: published

After being guest at `Friday Ketchup with Emiel Brok <{filename}/posts/2022/guest-at-emiel-broks-friday-ketchup_en.rst>`_, 
I had to think about my last contribution to Uyuni.

It’s a great example how even something small can have an impact and even if you can’t finish it on your own, 
you might be able to lead the way so other can, and will, pick your work up.

Back in May I wanted to further improve my Java skills, I tend to check some open source projects in such a case, 
that way I do something useful ;) I was skimming through the Uyuni Issues on GitHub to see if there is anything 
interesting I could work on. I found the Issue 
`complete set of parameters with smtp host, port, user and password for SUSE Manager <https://github.com/uyuni-project/uyuni/issues/5343>`__
(Archive: `[1] <https://archive.today/2022.12.23-214324/https://github.com/uyuni-project/uyuni/issues/5343>`__).

So far you could define an SMTP Server which Uyuni / SUMA will use to send out Notifications, but it wasn’t possible 
to configure a port other then 25 or to authenticate with a username and password. It was obvious that this is 
actually an important feature, most companies get rid of open SMTP relays.

I started to work on it and came up with a working, let’s call it `proof of concept <https://github.com/uyuni-project/uyuni/pull/5466>`__
(Archive: `[1] <https://archive.today/2022.12.23-214517/https://github.com/uyuni-project/uyuni/pull/5466>`__). 
It wasn’t the most elegant solution and still WIP, but it did the job already in my test environment. Unfortunately 
a lot of other things came up and during the next months I wasn’t able to find time to further work on the feature.

In September one of the Uyuni Maintainer `used my code, further brushed it up and merged it <https://github.com/uyuni-project/uyuni/pull/5886>`__
(Archive: `[1] <https://archive.today/2022.12.23-214530/https://github.com/uyuni-project/uyuni/pull/5886>`__) 
so it became a feature in the next Uyuni release.

THIS is in my opinion the most important part, THIS is one example why Open Source matters, a feature request was reported, 
I was interested to work on it, started with something but even though I couldn’t finish it, someone else found it useful, 
took it from there and completed it.

I would like to encourage everyone who’s interested in contributing to open source projects: Just do it! Start with something, 
give it a try, share and publish your results, further improve it if you can or let other from the community help you.

And last but not least, you don’t need coding skills to contribute, trust me, every project has a ton of non-code 
related things that could use some improvement and help :)
