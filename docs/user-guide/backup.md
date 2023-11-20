---
description: Backing up data in Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
tags:
- ISO 27001 A.12.3.1 Information Backup
- BSI IT-Grundschutz APP.4.4.A5
- HIPAA S23 - Contingency Plan - Data Backup Plan - § 164.308(a)(7)(ii)(A)
- MSBFS 2020:7 4 kap. 14 §
- MSBFS 2020:7 4 kap. 15 §
- HSLF-FS 2016:40 3 kap. 12 § Säkerhetskopiering
- GDPR Art. 17 Right to erasure ("right to be forgotten")
---

# Backups

!!!important
    Compliant Kubernetes comes with a default backup retention time of 30 days, which was assessed suitable for most use-cases.

    You should be aware that some data protection regulations put a **minimum requirement** on backup retention time, while some data protection regulations put a **maximum requirement** on backup retention time.

    For example, Swedish Patient Data Laws ([HSLF-FS 2016:40](https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/artikelkatalog/foreskrifter-och-allmanna-rad/2016-4-44.pdf) 3 kap. 13 §) says the following:

    > The healthcare provider must decide how long the backup copies are to be saved [...].

    This can be interpreted as setting a minimum backup retention time.

    At the other end, too long backup retention time clash with GDPR Art. 17 "Right to erasure (‘right to be forgotten’)". For more details, see [How do I comply with GDPR Art. 17](../ciso-guide/gdpr-art-17/).

    Make sure you research regulations applicable to your organization to determine if the default backup retention time is suitable for your organization.

Compliant Kubernetes (CK8S) includes backup functionality through Velero, a backup tool for Kubernetes Resources and Persistent Volumes. For backup of container images, Harbor is used instead.

## What is Velero?

[Velero](https://velero.io/) is an open source, cloud native tool for backing up and migrating Kubernetes Resources and Persistent Volumes. It has been developed by VMware since 2017. It allows for both manual and scheduled backups, and also allows for subsets of Resources in a cluster to be backed up rather than necessarily backing up everything.

## Usage

The following are instructions for backing up and restoring resources.

### Backing up

<!--user-demo-backup-start-->

Compliant Kubernetes takes a daily backup of all Kubernetes Resources in all user namespaces. Persistent Volumes will be backed up if they are tied to a Pod. If backups are not wanted the label `compliantkubernetes.io/nobackup` can be added to opt-out of the daily backups.

Application metrics (Grafana) and application log (Kibana) dashboards are also backup up by default.

By default, backups are stored for 720 hours (30 days).

<!--user-demo-backup-end-->

### Restoring

<!--user-demo-restore-start-->
Restoring from a backup with Velero is meant to be a type of disaster recovery. **Velero will not overwrite existing Resources when restoring.** As such, if you want to restore the state of a Resource that is still running, the Resource must be deleted first.

To restore a backup on demand, contact your Compliant Kubernetes administrator.
<!--user-demo-restore-end-->

## Protection of Backups

The Compliant Kubernetes administrator will take the following measure to ensure backups are protected:

1. Backups are encrypted at rest, if the underlying infrastructure provider supports it.

    **Why?** This ensures backups remain confidential, even if, e.g., hard drives are not safely disposed.

2. Backups are replicated to an off-site location, if requested. This process is performed from outside the cluster, hence the users -- or attackers gaining access to their application -- cannot access the off-site replicas.

    **Why?** This ensures backups are available even if the primary location is subject to a disaster, such as extreme weather. The backups also remain available -- though unlikely confidential -- in case an attacker manages to gain access to the cluster.

<!--

!!!note
    This safeguard is pending an internal investigation and process change.

3. The buckets holding the backups are configured with [object lock](https://docs.safespring.com/storage/object-locking/), if the underlying cloud provider supports it. This means that backups cannot be modified or erase until a given retention time, even with privileged credentials.

    **Why?** This ensures backups are available -- though unlikely confidential -- even if the whole Compliant Kubernetes environment is compromised.
-->
