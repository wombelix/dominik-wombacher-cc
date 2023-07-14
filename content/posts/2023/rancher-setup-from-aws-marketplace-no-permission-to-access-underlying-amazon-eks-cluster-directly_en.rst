.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

Rancher Setup from AWS Marketplace, no permissions to access the underlying Amazon EKS Cluster directly
#######################################################################################################

:date: 2023-04-28
:modified: 2023-04-28
:tags: AWS, Rancher, EKS
:description: There might be issues with direct access to the Amazon EKS Cluster in a Rancher Setup deployment
:category: Container
:slug: rancher-setup-from-aws-marketplace-no-permission-to-access-underlying-amazon-eks-cluster-directly
:author: Dominik Wombacher
:lang: en
:transid: rancher-setup-from-aws-marketplace-no-permission-to-access-underlying-amazon-eks-cluster-directly 
:status: published

`Rancher Setup <https://aws.amazon.com/marketplace/pp/prodview-go7ent7goo5ae>`__
(Archive: `[1] <https://web.archive.org/web/20230713090231/https://aws.amazon.com/marketplace/pp/prodview-go7ent7goo5ae>`__,
`[2] <https://archive.today/2023.07.13-090237/https://aws.amazon.com/marketplace/pp/prodview-go7ent7goo5ae>`__) 
from AWS Marketplace deploys an EKS cluster and installs `Rancher <https://www.rancher.com/products/rancher>`__
(Archive: `[1] <https://web.archive.org/web/20230713093613/https://www.rancher.com/products/rancher>`__, 
`[2] <https://archive.today/2023.07.13-093617/https://www.rancher.com/products/rancher>`__) on top. 
It will create all necessary resources, the outcome is a high-available and production 
ready Rancher Manager environment. Which is great and I highly recommend it for people that 
don't need to customize every detail and just want to get started quickly.

If you want to learn more about Rancher Setup, SUSE provides a comprehensive 
`installation guide <https://documentation.suse.com/trd/kubernetes/single-html/gs_rancher_aws-marketplace/>`__ 
(Archive: `[1] <https://web.archive.org/web/20230713095305/https://documentation.suse.com/trd/kubernetes/single-html/gs_rancher_aws-marketplace/#id-upgrade-to-latest-version>`__,
`[2] <https://archive.today/2023.07.13-095312/https://documentation.suse.com/trd/kubernetes/single-html/gs_rancher_aws-marketplace/%23id-upgrade-to-latest-version>`__).

By default, access to EKS is tunneled through Rancher, in the event of a problem with the Rancher 
installation, direct access to EKS via kubectl could be required to get Rancher up and running again. 

But as much I like the Rancher Setup Wizard, the way resources get deployed will most likely causing a problem 
when you try to directly access the underlying EKS cluster that was deployed by Rancher Setup.

Let me quote from the `GitHub Issue <https://github.com/SUSE-Enceladus/suse-rancher-setup/issues/217>`__
(Archive: `[1] <https://web.archive.org/web/20230713091405/https://github.com/SUSE-Enceladus/suse-rancher-setup/issues/217>`__,
`[2] <https://archive.today/2023.07.13-091412/https://github.com/SUSE-Enceladus/suse-rancher-setup/issues/217>`__) I opened:

  | The problem is, only the user or assumed Role that created the EKS Cluster has :code:`system:masters` access permissions by default. 
  | In case of the Rancher Setup, that's the IAM Role / Instance Profile I created prior the setup and attached to the EC2 instance. 
  | Without an additional step, access to the EKS Cluster is only possible through Rancher but not directly.

I make the assumption you have some understanding about AWS and IAM Roles as well as EC2 Instance Profiles are not new to you.  
Rancher Setup is a EC2 Instance with a Web Wizard, you grant the necessary permissions to deploy resources as IAM Role which 
will be attached to the EC2 Instance. That makes this Role to the owner of the new deployed EKS Cluster.

Right now, the setup doesn't provide a option to change the owner or print a warning that this is something the 
User should take care of before proceeding. This can be achieved by manually editing the :code:`aws-auth` configmap 
by running the command :code:`kubectl edit configmap aws-auth --namespace kube-system`

.. code-block:: yaml

  [...]
      - rolearn: arn:aws:iam::1234567890:role/MyRole
        username: admin
        groups:
          - system:masters
  [...]

I made the suggestion to include it in the actual setup to make it more customer friendly, 
but wanted to document the workaround to help other people that might run into the same problem I did.

