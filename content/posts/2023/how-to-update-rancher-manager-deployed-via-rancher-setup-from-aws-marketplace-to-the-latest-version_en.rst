.. SPDX-FileCopyrightText: 2023 Dominik Wombacher <dominik@wombacher.cc>
..
.. SPDX-License-Identifier: CC-BY-SA-4.0

How-to update Rancher Manager - deployed via Rancher Setup from AWS Marketplace - to the latest version
#######################################################################################################

:date: 2023-05-05
:modified: 2023-05-05
:tags: AWS, Rancher, EKS
:description: How-to update Rancher to the latest version if the initial deployment done via Rancher Setup from AWS Marketplace
:category: Container
:slug: how-to-update-rancher-manager-deployed-via-rancher-setup-from-aws-marketplace-to-the-latest-version 
:author: Dominik Wombacher
:lang: en
:transid: how-to-update-rancher-manager-deployed-via-rancher-setup-from-aws-marketplace-to-the-latest-version
:status: published

If you used `Rancher Setup <https://aws.amazon.com/marketplace/pp/prodview-go7ent7goo5ae>`__
(Archive: `[1] <https://web.archive.org/web/20230713090231/https://aws.amazon.com/marketplace/pp/prodview-go7ent7goo5ae>`__,
`[2] <https://archive.today/2023.07.13-090237/https://aws.amazon.com/marketplace/pp/prodview-go7ent7goo5ae>`__) 
from AWS Marketplace to deploy Ranger Manager, you can perform a update to the latest version via Helm, 
the initial Rancher Setup tool isn't involved in this process.

The `installation guide from SUSE <https://documentation.suse.com/trd/kubernetes/single-html/gs_rancher_aws-marketplace/>`__ 
(Archive: `[1] <https://web.archive.org/web/20230713095305/https://documentation.suse.com/trd/kubernetes/single-html/gs_rancher_aws-marketplace/#id-upgrade-to-latest-version>`__,
`[2] <https://archive.today/2023.07.13-095312/https://documentation.suse.com/trd/kubernetes/single-html/gs_rancher_aws-marketplace/%23id-upgrade-to-latest-version>`__) 
in Section 4 - *Upgrade to latest version* - refers to Section 3 - *Upgrade Rancher* - in the official 
`Rancher upgrade guide <https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster/upgrades#3-upgrade-rancher>`__ 
(Archive: `[1] <https://web.archive.org/web/20230713095342/https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster/upgrades#3-upgrade-rancher>`__, 
`[2] <https://archive.today/2023.07.13-095344/https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster/upgrades>`__). 

You can follow this guide, but there is one major difference, the deployment is called :code:`rancher-stable` 
and not :code:`rancher` if Rancher Setup from AWS Marketplace was used. Ensure to replace it accordingly, otherwise 
you will see some error messages that the Helm deployment can't be found. 

Following  a short summary of the plain commands, adjusted to match the deployment name, for further details about all 
required commands, the specific order and what they are doing, please take a look into the above linked upgrade guide.

.. code-block::

  helm get values rancher-stable -n cattle-system -o yaml > values.yaml

  helm upgrade rancher-stable rancher-<CHART_REPO>/rancher \
  --namespace cattle-system \
  -f values.yaml \
  --version=2.6.8

I created a `GitHub Issue <https://github.com/SUSE/technical-reference-documentation/issues/75>`__ 
(Archive: `[1] <https://web.archive.org/web/20230713095250/https://github.com/SUSE/technical-reference-documentation/issues/75>`__,
`[2] <https://archive.today/2023.07.13-095255/https://github.com/SUSE/technical-reference-documentation/issues/75>`__) 
to get a hint added to the section in the installation guide that the Helm deployment name is different. 
I think this would safe time and avoid frustration when it comes to a upgrade.
