Merge PDF Files on Linux
########################

:date: 2019-10-28 15:38
:modified: 2019-10-28 15:38
:tags: Bash, CUPS, PDF, openSUSE
:category: Linux
:slug: merge-pdf-files-on-linux
:author: Dominik Wombacher
:lang: en
:transid: merge-pdf-files-on-linux
:status: published

I had to use Cups-PDF and "Print" bunch of Pages to Single PDF Files due to the fact that no Download as PDF was possible. 
But how to Merge tons of files named as **Pagetitle-job_id<Number>** on Linux via command line in a fast and easy way?

After some testing, :code:`pdfunite` - included in *Poppler* and already installed on openSUSE Tumbleweed - did the job, 
but the result with :code:`pdftk` - included in *Ghostscript* - was nearly identical and worked the same way.


.. code-block::

	pdfunite $(ls -cr *.pdf) output.pdf


With :code:`$()`, :code:`ls` will executed and the results are added to the :code:`pdfunite` command. 

All PDF Files in the same Folder will be merged to a single **output.pdf** File. 

The Parameter :code:`-cr` sorts by creation time in reverse order. 

That was necessary for me because the Job IDs were from 36 till 223, all other parameter mixed up the order and the merged PDF wasn't as expected.
