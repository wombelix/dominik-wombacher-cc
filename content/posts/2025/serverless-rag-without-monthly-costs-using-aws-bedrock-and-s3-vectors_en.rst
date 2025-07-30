.. SPDX-FileCopyrightText: 2025 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Serverless RAG without monthly costs using AWS Bedrock and S3 Vectors
#####################################################################

:date: 2025-07-30
:modified: 2025-07-30
:tags: AWS, Bedrock, S3, Vectors, RAG, AI
:description: Building serverless RAG with AWS Bedrock Knowledge Base and S3 Vectors without monthly fixed costs
:category: Cloud
:slug: serverless-rag-without-monthly-costs-using-aws-bedrock-and-s3-vectors
:author: Dominik Wombacher
:lang: en
:transid: serverless-rag-without-monthly-costs-using-aws-bedrock-and-s3-vectors
:status: published

I was curious if it's possible to build a Retrieval-Augmented
Generation (RAG) system for an AI chatbot in a pure serverless way without
monthly fixed costs. The main goal was to test some ideas without
investing much in infrastructure upfront. When AWS launched S3 Vectors
on July 15th, it immediately caught my attention because it promised
exactly what I was looking for.

Part of the 
`S3 Vectors announcement <https://aws.amazon.com/blogs/aws/introducing-amazon-s3-vectors-first-cloud-storage-with-native-vector-support-at-scale/>`_
was that it can be used as a vector store in AWS Bedrock Knowledge Base
too, which made it even more interesting. This combination could potentially
solve the cost challenge I was facing with traditional vector databases that
come with monthly fees regardless of usage.

S3 Vectors is currently in preview and available in five regions:
US East (N. Virginia), US East (Ohio), US West (Oregon), EU Central 1
(Frankfurt), and Asia Pacific (Sydney). I picked eu-central-1, which 
is closest to me, for my tests and pricing calculations.
I use around 500 markdown files from the
`Rancher Manager Documentation <https://github.com/rancher/rancher-docs>`_
as my test dataset. Unlike regular S3 buckets, S3 Vectors doesn't
require a globally unique name since you reference it by ARN, which
means it only needs to be unique within the same account and region.

Setting up the Bedrock Knowledge Base was overall pretty straightforward.
The wizard guides you through all the steps, though I created the S3 bucket
and S3 Vectors bucket upfront. I had the
`Bedrock Knowledge Base documentation <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html>`_
and
`S3 Vectors documentation <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html>`_
open in parallel to learn more and make decisions about parsing strategy, chunking,
vector dimensions and configuration options. The knowledge base, data
source, and vector store all need to be in the same region, which makes
sense from performance and traffic costs perspective.

I chose the Amazon Bedrock default parser as my parsing strategy. This
parser claims to work well with various file formats including markdown, HTML,
PDF, and Office documents. The main advantage is that it doesn't incur
additional charges, making it perfect for projects where you want to
keep costs low. Since my content was primarily text-based markdown
files, the default parser seems more than sufficient for this use case.

For the vector configuration, I used a 1024-dimension index aligned
with the
`Amazon Titan Text Embeddings V2 <https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html>`_
model. I also went with the default chunking strategy, which splits
content into approximately 300-token chunks while preserving sentence
boundaries. I want to play around with this another time and see if it
would make sense and bring an improvement raising the chunk size. The
embedding model can handle up to 8192 tokens.

The data flow is now: From the S3 source bucket through the AWS Bedrock
parser, processed by the embedding model, stored in the
vector storage. Testing the result and interacting with the synced
data is easy using the
`Chat with your document <https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-chatdoc.html>`_
feature in the Amazon Bedrock console. So, to see first results,
you don't have to build out your Chatbot interface yet.

Several things became clear during my test setup. The overall
process is simpler as expected, with the wizard handling
resource creation and permissions.
Since S3 Vectors is in preview, it's not yet available in
infrastructure-as-code tools like the AWS Terraform provider. I didn't
check if it's available in CloudFormation though. I would love to
manage the knowledge base and related resources through IaC next time
instead of the click-ops through the console.

The cost aspect, which was my primary motivation, exceeded expectations.
With S3 Vectors, we're talking about the cost of a cup of coffee when
testing or building a proof of concept. This opens up possibilities for
builders who want to experiment with ideas without upfront investment.

One challenge I encountered was with permissions. The Knowledge Base
wizard is strict and defaults to claiming ownership of the entire
bucket, at least from an IAM role perspective. The managed roles don't
cover individual subfolders / prefixes someone might create when uploading data.
Manual IAM adjustments work but can cause issues when editing the
knowledge base later. There's likely a better way to configure this
properly from the start. I have to figure out if the answer is
really one source S3 bucket per knowledge base or if there's a better
way to leverage prefixes without the clunky IAM role and policy
handling.

I'm also curious about further reducing costs for the S3 data source,
which could grow over time.
`S3 Intelligent-Tiering <https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering-overview.html>`_
might help reduce ongoing storage costs. The knowledge base index can be
recreated from the source data in the S3 bucket, though that will cause
costs for using the embedding model again.

Embedding tokens are another cost factor, though not a major one. My
test with approximately 5MB of Rancher documentation in markdown format
resulted in about 1 million tokens, translating to roughly $0.02 USD
with Amazon Titan Text Embeddings V2, which doesn't seem like much.
Using batch processing outside of Bedrock could potentially cut costs
in half, but batch processing doesn't work in the context of Bedrock
Knowledge Base. The knowledge base is convenient to use, but if you
build your own stack instead, then batching can become a cost saver,
especially at a higher scale beyond simple testing.

I ran into an issue with metadata handling. Using S3 Vectors as vector
storage with Bedrock Knowledge Base requires adding the Bedrock-related
metadata keys as non-filterable, otherwise the sync fails. By default,
all metadata keys in S3 Vectors are considered filterable, but Bedrock's
metadata exceeds the 2KB limit for filterable metadata. I found the
solution in the
`S3 Vectors documentation <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html>`_
and this
`AWS re:Post discussion <https://repost.aws/questions/QUWezLMjc0S8GOiaa3jOOKGQ/s3-vector-big-metadata-error>`_:
create the vector index with :code:`AMAZON_BEDROCK_TEXT` and
:code:`AMAZON_BEDROCK_METADATA` as non-filterable metadata keys.

Additional (slight) costs occur when interacting with the knowledge base,
for the input and output tokens of the leveraged LLM
through AWS Bedrock. For example, something between $0.05 and $0.10 USD
per 1 Million Tokens when using one of the
`Amazon Nova Models <https://aws.amazon.com/bedrock/pricing/>`_.
Based on the S3 Vectors pricing for :code:`eu-central-1`,
storage costs $0.064 per GB per month, PUT requests cost $0.214 per GB,
and query requests are $0.0027 per 1,000 requests. For small datasets
like my 5MB test, these costs remain minimal.

With my tests I achieved what I wanted. Vector storage
was previously the component with higher monthly costs in Bedrock
Knowledge Base, but S3 Vectors makes this purely pay-per-use. Now
we're talking about costs comparable to a cup of coffee for testing and
building MVPs, just perfect for experimentation and idea validation.
Even though I didn't run the numbers, I wouldn't be surprised if this
is even up to a specific scale extremely interesting and cost efficient.
