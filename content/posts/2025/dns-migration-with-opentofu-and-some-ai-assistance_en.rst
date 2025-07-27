.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

DNS management with OpenTofu and some AI assistance
###################################################

:date: 2025-07-27
:modified: 2025-07-27
:tags: AI, GenAI, DNS, Terraform, OpenTofu, Automation, Gemini
:description: Using AI assistance to migrate DNS records from BIND zone files to OpenTofu configuration
:category: Code
:slug: dns-management-with-opentofu-and-some-ai-assistance
:author: Dominik Wombacher
:lang: en
:transid: dns-management-with-opentofu-and-some-ai-assistance
:status: published

Today I migrated dozens of DNS records from manual to OpenTofu based management.
My DNS provider allows downloading zone files in BIND format, but other
information like record IDs needed for OpenTofu imports are buried in
the HTML of their web interface.

Manual migration would have been time-consuming and error-prone.
Perfect opportunity to test AI assistance. I'm not expecting magic, but
to handle the repetitive parsing while I focus on validation and logic.

I used Google's Gemini Code Assistant for this experiment. Over the
past months I've worked with Amazon Q Developer, GitHub Copilot,
Cursor, and Roo Code with various models.

The key was, and in my experience always is, to provide specific
context instead of vague requests. I had already built the OpenTofu
modules and project structure to manage Domains and DNS records months ago.
So, I knew exactly what I needed and how things should work. This allowed
me to give precise guidance to the assistant without relying on it to figure
out implementation details.

I provided the AI with full context: existing record files, OpenTofu
module structure, and clear objectives. I essentially train the coding
assistant on the patterns and conventions of my existing codebase.
This doesn't mean hours of actual training, just a few well-crafted prompts.

For tasks like this (processing large amounts of data that humans
can barely read, finding patterns, applying logic, and transforming
data into different formats) LLMs are naturally a good fit.

For converting a BIND zone file, my instruction was:

.. code::

    Here is the BIND zone file for mycloudoffice.de. I need you to create
    a records_mycloudoffice_de.tf file. Please follow the syntax and naming
    conventions you see in my existing records_wombacher_cc.tf file, and be
    sure to ignore irrelevant records like SOA and RRSIG or CAA that are handled
    in a different place and are not in scope now.

Of course, I then pasted the complete BIND zone file content after
this instruction as well. By providing both raw data and a clear example of
desired output, the model understood the pattern, identified relevant
records, and produced properly formatted OpenTofu code. The "Magic" here
is that popular LLMs of course know what DNS records are and how BIND Zone
files are structured. So, they don't need handholding to understand and parse them.

The next step was generating import commands. To get these resources
into my OpenTofu state without destroying and recreating them, I
needed :code:`tofu import` commands for each record. The unique IDs are
somewhere in the HTML code from my DNS provider's web interface.

My prompt was:

.. code::

    Now, I need you to generate the tofu import commands for the resources
    you just created. Here is the raw HTML containing the record IDs. The
    command format is "tofu import <resource_address> <domain>:<record_id>".

Again, I included the full HTML source after this instruction.
A while later, I had a complete list of shell commands ready to
execute. A task that would have involved manually matching dozens of
records to their IDs was done in seconds without errors.

But this wasn't about blindly accepting AI responses. When we encountered
a URL record type specific to my DNS provider, the AI's first attempt
was based on its general knowledge of resource options. Since none of
my shared examples contained details for this specific URL type, it
made a reasonable but non-functional guess.

I researched the provider's documentation and fed that back to the
model to get the right syntax. Even then, :code:`tofu plan` revealed
subtle drift that required my analysis and guidance to resolve.
But two short iterations later, we had a working solution.

This collaboration - where AI handles repetitive tasks while I
provide direction and validation - is practical and effective. It's
not about replacing developers but freeing us from repetitive work so
we can focus on architecture and problem-solving.

As models improve, we stay in the driver's seat, making decisions and
reviewing results. Work quality depends on clear instructions and
critical evaluation of results, not on expecting AI to solve everything
automatically.

Personally, I never want to go back to do all this manually.
It isn't fun to read through hundreds of lines of BIND zone files
and HTML code to find the right IDs in a weirdly nested div tag.

If you are interested in the outcome, some of what Gemini came up with
today made it into my
`OpenTofu based domain management <https://git.sr.ht/~wombelix/domain-mgmt>`_.
