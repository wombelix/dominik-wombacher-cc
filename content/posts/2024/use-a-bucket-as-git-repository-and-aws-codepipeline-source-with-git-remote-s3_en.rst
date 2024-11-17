.. SPDX-FileCopyrightText: 2024 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Use a Bucket as Git repository and AWS CodePipeline source with git-remote-s3
#############################################################################

:date: 2024-11-17
:modified: 2024-11-17
:tags: AWS, S3, CodePipeline, Coding, Git, OpenSource
:description: How-to use a S3 Bucket as serverless git repository and source action for AWS CodePipeline with git-remote-s3
:category: Code
:slug: use-a-bucket-as-git-repository-and-aws-codepipeline-source-with-git-remote-s3
:author: Dominik Wombacher
:lang: en
:transid: use-a-bucket-as-git-repository-and-aws-codepipeline-source-with-git-remote-s3
:status: published

Let's talk about how to use a ordinary S3 Bucket as serverless Git repository with
the remote helper script `git-remote-s3 <https://github.com/awslabs/git-remote-s3>`_.
Release `v0.2.0 <https://github.com/awslabs/git-remote-s3/releases/tag/v0.2.0>`_,
contains a feature that let you use the repo as source for AWS CodePipeline as well.

I was looking for a way to replace AWS CodeCommit in a Workshop I build.
The reasons: `New customer access was closed <https://aws.amazon.com/blogs/devops/how-to-migrate-your-aws-codecommit-repository-to-another-git-provider/>`__
(Archive: `[1] <https://web.archive.org/web/20241013215252/https://aws.amazon.com/blogs/devops/how-to-migrate-your-aws-codecommit-repository-to-another-git-provider/>`__,
`[2] <https://archive.today/2024.07.28-001143/https://aws.amazon.com/blogs/devops/how-to-migrate-your-aws-codecommit-repository-to-another-git-provider/>`__)
on July 25, 2024. **git-remote-s3** looked promising for my use-case,
I can use a Bucket as remote, push and pull code, leverage AWS IAM to grant access.
The only challenge was AWS CodePipeline, more on that later.

First, how does **git-remote-s3** work under the hood?
It is a so called `remote helper <https://git-scm.com/docs/gitremote-helpers>`_ script.
And uses the `git bundle <https://git-scm.com/docs/git-bundle>`_ feature.
The bundle file is then then stored in the S3 bucket as :code:`<prefix>/<ref>/<sha>.bundle`.
**git-remote-s3** interacts with the bucket thought the S3 API. It performs a get or put
that either updates the bundle in the bucket or retrieves the file and adds the containing data
to the local git clone. When a push was successful, the previous bundle is removed. There is
only one bundle file per git *ref* at any point in time stored on the bucket.

To learn more, I recommend the `Under the hood <https://github.com/awslabs/git-remote-s3?tab=readme-ov-file#under-the-hood>`_
and `use S3 remotes <https://github.com/awslabs/git-remote-s3?tab=readme-ov-file#use-s3-remotes>`_
section in the **git-remote-s3** `README <https://github.com/awslabs/git-remote-s3?tab=readme-ov-file>`_.

`AWS CodePipeline <https://aws.amazon.com/codepipeline/>`_ offers an
`Amazon S3 source action <https://docs.aws.amazon.com/codepipeline/latest/userguide/integrations-action-type.html#integrations-source-s3>`_
as location for your code and application files. But this requires to upload the source files as a single ZIP file.
**git-remote-s3** can create and upload zip archives. Use :code:`s3+zip` as URI Scheme when you add the remote and **git-remote-s3**
will automatically place an archive on the S3 bucket that can be used by AWS CodePipeline.

You might wonder, where the archive file is located? Let's assume your bucket name is :code:`my-git-bucket` and the repo is called :code:`my-repo`.
Run :code:`git remote add origin s3+zip://my-git-bucket/my-repo` to use it as remote. When you now commit your changes and push to the remote,
an additional :code:`repo.zip` file will be uploaded to the bucket. For example, if you push to the main branch (:code:`git push origin main`),
the file is available under :code:`s3://my-git-bucket/my-repo/refs/heads/main/repo.zip`. When you push to a branch called :code:`fix_a_bug`,
it's available under :code:`s3://my-git-bucket/my-repo/refs/heads/fix_a_bug/repo.zip`. Or if you create and push a tag called :code:`v1.0`,
it will be :code:`s3://my-git-bucket/my-repo/refs/tags/v1.0/repo.zip`.

Your AWS CodePipeline Action configuration, to trigger on updates of your :code:`main` branch, would then look like this:

- Action Provider: :code:`Amazon S3`
- Bucket: :code:`my-git-bucket`
- S3 object key: :code:`my-repo/refs/heads/main/repo.zip`
- Change detection options: :code:`AWS CodePipeline`

Check out the Tutorial `Create a simple pipeline (S3 bucket) <https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-simple-s3.html>`_
to learn more about a S3 bucket as source action.

I'm proud that `my first contribution <https://github.com/awslabs/git-remote-s3/pull/16>`_,
to **git-remote-s3**, introduced the feature that allows using it together with AWS CodePipeline.
And while I was working on it, I had the opportunity to make a couple more code improvements.

If you have any other use-case that requires a ZIP archive, then this feature will work for you too, it's not limited to AWS CodePipeline.
