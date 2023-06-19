---
tags:
- HIPAA S44 - Access Control - Unique User Identification - § 164.312(a)(2)(i)
- HSLF-FS 2016:40 4 kap. 2 § Styrning av behörigheter
---
Use of Credentials
==================
Compliant Kubernetes interacts with a lot of credentials. This document captures all of them in an orderly fashion, layer-by-layer.

Terminology
-----------
* Purpose: Why are these credentials necessary, what can be done with them.
* Owner: The person (e.g., John Smith) or computing system (e.g., control plane Node, Pod) who controls the credentials, and is responsible for their safe storage and usage.
* Type: Individual credentials identify a person, while service accounts identify a computing system.
* Use for: What should these credentials be used for.
* Do not use for: When should these credentials NOT be used, although they technically could.

Single Sign-On (SSO) Credentials
--------------------------------

* Example: Company Google Accounts
* Purpose: authenticate a person with various system, in particular
    * Kubernetes API via Dex
    * Grafana via Dex
    * OpenSearch Dashboards via Dex
    * Harbor via Dex
* Owner: individual person (user or administrator)
* Type: individual credentials
* Use for: identifying yourself
* Do not use for:
    * These credentials are super valuable and should not be shared with anyone, not even family, friends, workmates, etc., even if requested. Report such sharing requests.
* Misc:
    * Protect using [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication)

Cloud Provider (Infrastructure) Credentials
-------------------------------------------

* Purpose: create infrastructure, e.g., VMs, load balancers, networks, buckets.
* Owner: administrator
* Type: individual credentials
* Use for:
    * Terraform layer in Kubespray
    * Creating and destroying buckets via helper scripts
* Do not use for:
    * Kubernetes [cloud-controller integration](https://github.com/kubernetes-sigs/kubespray/blob/master/inventory/sample/group_vars/all/openstack.yml#L38), use [Cloud Controller Credentials](#cloud-controller-integration-credentials) instead.
    * Access to object storage / S3 bucket, use [backup credentials](#backup-and-long-term-logging-credentials) instead.

SSH Keys
--------

* Purpose: access Nodes for setup, break glass or disaster recovery
* Owner: administrator
* Type: individual credentials
* Use for:
    * Accessing Nodes via SSH
* Do not use for:
    * Giving a system access to a Git repository. Create a separate SSH key only for that purpose instead.
* Important considerations:
    * When generating an SSH key, see [Cryptography](cryptography.md).

PGP Keys
--------

* Purpose: encrypt/decrypt sensitive information, e.g., service account credentials, application developer names, incident reports, financial information, etc.
* Owner: administrator
* Type: individual credentials
* Use for:
    * Encrypting/decrypting sensitive information
* Do not use for:
    * Encrypting/decrypting individual credentials. These are meant to be individual and never shared.
    * Encrypting/decrypting SSH key. These are meant to be individual and never shared. Prefer [protecting your SSH key with a passphrase](https://martin.kleppmann.com/2013/05/24/improving-security-of-ssh-private-keys.html) or storing it on a [YubiKey](https://en.wikipedia.org/wiki/YubiKey).
    * Encrypting non-sensitive information. This leads to a culture of "security by obscurity" in which people over-rely on encryption. Prefer being mindful about what data you store and why. If unsure, prefer not storing credentials, as Cloud Provider Credentials and SSH keys should be enough to restore any access.
* Important considerations:
    * When generating a GPG key, see [Cryptography](cryptography.md).

Cloud Controller (Integration) Credentials
------------------------------------------

* Purpose: allow Kubernetes control Nodes, specifically the [cloud-controller-manager](https://kubernetes.io/docs/concepts/architecture/cloud-controller/), to create LoadBalancers and PersistentVolumes
* Owner: each Kubernetes cluster should have their own
* Type: service account
* Use for:
    * Configuring Kubespray to set up a Kubernetes cluster with cloud integration
* Do not use for:
    * AWS. Use [AWS IAM Node Roles](https://github.com/kubernetes-sigs/kubespray/blob/master/contrib/terraform/aws/modules/iam/main.tf) instead.
    * Exoscale. We currently don't integrate with Exoscale for LoadBalancer or PersistentVolumes.
    * Terraform layer in Kubespray

Backup and Long-Term Logging Credentials
----------------------------------------

* Purpose:
    * Allow backup of various components, e.g., PVCs via Velero, Thanos metrics, OpenSearch Indexes, PostgreSQL databases.
    * Allow long-term logging, e.g., Management Cluster logs
* Owner: each Compliant Kubernetes cluster should have their own
* Type: service account
* Use for:
    * Backup
    * Logging
* Do not use for:
    * Other object storage, e.g., Harbor container images
    * Disaster recovery, investigations. Use Cloud Provider credentials instead.
* Misc:
    * Ensure these credentials are **write-only**, if supported by the underlying cloud provider, to comply with [ISO 27001 A.12.3.1 Information Backup](https://www.isms.online/iso-27001/annex-a-12-operations-security/) and [ISO 27001 A.12.4.2 Protection of Log Information](https://www.isms.online/iso-27001/annex-a-12-operations-security/). As of 2021-05-20, this is supported by AWS S3, Exoscale S3, GCP and SafeSpring S3.

OpsGenie Credentials
--------------------

* Purpose:
    * Allow the Cluster to issue alerts to OpsGenie.
* Owner: each Compliant Kubernetes cluster should have their own
* Type: service account
* Use for: alerting
* Do not use for:
    * Operator access to OpsGenie. Prefer [Single Sign-On (SSO)](https://support.atlassian.com/opsgenie/docs/configure-google-sso/).

Dex OpenID Client Secret
------------------------

* Purpose:
    * Complete the "OAuth dance" between Grafana, OpenSearch Dashboard, Harbor and kubectl, on one side, and Dex, on the other side.
    * Used both by administrators and users.
* Owner: each Compliant Kubernetes cluster should have their own
* Type: not secret
* Misc:
    * We have determined that the OpenID client secret should not be treated as a secret. See risk analysis [here](https://github.com/dexidp/dex/issues/469) and [here](https://security.stackexchange.com/questions/225809/what-is-the-worst-i-can-do-if-i-know-openid-connect-client-secret).

Kubeconfig with OpenID Authentication
-------------------------------------

* Purpose: access the Kubernetes API in normal situations
* Owner: shared between administrators and users
* Type: not secret
* Use for:
    * Routine checks
    * Routine maintenance
    * Investigations
    * "Simple" recovery
* Misc:
    * If these credentials become unusable, you are in a "break glass" situation. Use cloud provider credentials or SSH keys to initiate disaster recovery.

Kubeconfig with Client Certificate Key
--------------------------------------

* Purpose: access the Kubernetes API for disaster recovery, break glass or initial setup
* Owner: shared between administrators
* Type: special
* Use for:
    * Initial setup
    * Break glass
    * Disaster recovery
* Do not use for:
    * Routine maintenance or investigation. Use Kubeconfig with OpenID Authentication
* Misc:
    * Such a Kubeconfig is available on all control plane Nodes at `/etc/kubernetes/admin.conf`. SSH into a control plane Node then type `sudo su` and you can readily use `kubectl` commands.
    * Unless absolutely necessary, avoid storing this file outside the control plane Nodes.
    * If, for some good reason, you downloaded this file, `shred` it after usage.
