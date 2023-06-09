Hyperskill EduTools Plugin "Solve in IDE" Button without response / does not open IDE
#####################################################################################

:date: 2022-09-09
:modified: 2022-09-09
:tags: Learning, Programming, Hyperskill
:description: Hyperskill / JetBrains Academy EduTools Plugin not working
:category: Code
:slug: hyperskill-edutools-plugin-solve-in-ide-button-without-response-does-not-open-ide
:author: Dominik Wombacher
:lang: en
:transid: hyperskill-edutools-plugin-solve-in-ide-button-without-response-does-not-open-ide 
:status: published

I'm using Hyperskill since a while, nice platform to learn Coding, 
also with daily challenges which I love to solve. 
Some of them are question based, others require actual programming 
which can be done in a local installed IDE like *IntelliJ IDEA*. 

With the installed **EduTools Plugin**, you normally just hit the 
:code:`Solve in IDE` Button on the Website and it will automatically 
open the Challenge in your locally installed IDE. 

It wasn't working recently, nothing happened when clicking the button, no obvious error message. 
I saw a lot of **ERR_CONNECTION_REFUSED** message in the developer tools console, 
but only found one issue in the 
`JetBrains Issue Tracker <https://youtrack.jetbrains.com/issue/EDU-3351>`__
(Archive: `[1] <https://archive.today/2022.09.09-145026/https://youtrack.jetbrains.com/issue/EDU-3351>`__) 
which was unfortunately not related to my problem.

But it helped me to understand that I was just looking at the wrong place, 
the **EduTools Plugin** spins up a webserver listening on localhost, 
but inside a port range, by default it's not predictable which port exactly.

Technically, the Hyperskill page can't be aware about the used port, 
it will just try all ports until the Plugin answers on one of them, 
that's why **ERR_CONNECTION_REFUSED** works as designed. 

The more interesting message was:

.. code-block::

  127.0.0.1:63342/api/edu/hyperskill?step_id=5012&language=java&user_id=xxxxxxx:1
  Failed to load resource: the server responded with a status of 500 (Internal Server Error)

So the connection to the Plugin, running on :code:`127.0.0.1:63342` was successful 
but returned an error 500, the full message after opening the link in a Browser Tab:

.. code-block::

  500 Internal Server Error

  java.lang.IllegalStateException: 
  Refresh token is null at com.jetbrains.edu.learning.api.EduOAuthConnector.getNewTokens(EduOAuthConnector.kt:152) at 
  com.jetbrains.edu.learning.api.EduOAuthConnector.refreshTokens(EduOAuthConnector.kt:187) at 
  com.jetbrains.edu.learning.api.EduOAuthConnector.access$refreshTokens(EduOAuthConnector.kt:26) at 
  com.jetbrains.edu.learning.stepik.hyperskill.api.HyperskillConnector.getUserInfo(HyperskillConnector.kt:395) at 
  com.jetbrains.edu.learning.stepik.hyperskill.api.HyperskillConnector.getUserInfo(HyperskillConnector.kt:35) at 
  com.jetbrains.edu.learning.api.EduOAuthConnector.getCurrentUserInfo(EduOAuthConnector.kt:122) at 
  com.jetbrains.edu.learning.stepik.hyperskill.HyperskillUtilsKt$getSelectedProjectIdUnderProgress$1.invoke(HyperskillUtils.kt:131) at 
  com.jetbrains.edu.learning.stepik.hyperskill.HyperskillUtilsKt$getSelectedProjectIdUnderProgress$1.invoke(HyperskillUtils.kt:130) at 
  com.jetbrains.edu.learning.OpenApiExtKt$computeUnderProgress$1.compute(openApiExt.kt:118) at 
  com.intellij.openapi.progress.Task$WithResult.run(Task.java:335) at 
  com.intellij.openapi.progress.impl.CoreProgressManager.startTask(CoreProgressManager.java:442) at 
  com.intellij.openapi.progress.impl.ProgressManagerImpl.startTask(ProgressManagerImpl.java:114) at 
  com.intellij.openapi.progress.impl.CoreProgressManager.lambda$runProcessWithProgressSynchronously$8(CoreProgressManager.java:526) at 
  com.intellij.openapi.progress.impl.ProgressRunner.lambda$new$0(ProgressRunner.java:84) at 
  com.intellij.openapi.progress.impl.ProgressRunner.lambda$submit$3(ProgressRunner.java:252) at 
  com.intellij.openapi.progress.impl.CoreProgressManager.lambda$runProcess$2(CoreProgressManager.java:188) at 
  com.intellij.openapi.progress.impl.CoreProgressManager.lambda$executeProcessUnderProgress$12(CoreProgressManager.java:608) at 
  com.intellij.openapi.progress.impl.CoreProgressManager.registerIndicatorAndRun(CoreProgressManager.java:683) at 
  com.intellij.openapi.progress.impl.CoreProgressManager.computeUnderProgress(CoreProgressManager.java:639) at 
  com.intellij.openapi.progress.impl.CoreProgressManager.executeProcessUnderProgress(CoreProgressManager.java:607) at 
  com.intellij.openapi.progress.impl.ProgressManagerImpl.executeProcessUnderProgress(ProgressManagerImpl.java:60) at 
  com.intellij.openapi.progress.impl.CoreProgressManager.runProcess(CoreProgressManager.java:175) at 
  com.intellij.openapi.progress.impl.ProgressRunner.lambda$submit$4(ProgressRunner.java:252) at 
  java.base/java.util.concurrent.CompletableFuture$AsyncSupply.run(CompletableFuture.java:1768) at 
  java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1136) at 
  java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:635) at 
  java.base/java.util.concurrent.Executors$PrivilegedThreadFactory$1$1.run(Executors.java:702) at 
  java.base/java.util.concurrent.Executors$PrivilegedThreadFactory$1$1.run(Executors.java:699) at 
  java.base/java.security.AccessController.doPrivileged(AccessController.java:399) at 
  java.base/java.util.concurrent.Executors$PrivilegedThreadFactory$1.run(Executors.java:699) at 
  java.base/java.lang.Thread.run(Thread.java:833)

The error messages indicate that something with OAuth and Tokens (Authentication) went wrong, 
maybe related to the expire of my trial license which I changed to a payed subscription? 

Simple logout and login from Hyperskill directly in ItelliJ IDE solved the issue, afterwards 
I just refreshed the Website, clicked on the Button and the Challenge was opened in my IDE as expected.

Was my first time that I had any issues with the platform and to be honest, 
the Official Troubleshooting Guides and Issue Tracker were not really helpful to solve it :(
