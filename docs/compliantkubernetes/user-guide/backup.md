# Backups

Compliant Kubernetes (CK8S) includes backup functionality through Velero, a backup tool for Kubernetes Resources and Persistent Volumes. For backup of container images, Harbor is used instead.

## Compliance needs

The requirements to comply with ISO 27001 are stated in ISO [27001:2013](https://www.isms.online/iso-27001/). The annexes that are relevant to backups are:

- [Annex 12](https://www.isms.online/iso-27001/annex-a-12-operations-security/), article A.12.3.1 "Information Backup".

## What is Velero?

[Velero](https://velero.io/) is an open source, cloud native tool for backing up and migrating Kubernetes Resources and Persistent Volumes. It has been developed by VMware since 2017. It allows for both manual and scheduled backups, and also allows for subsets of Resources in a cluster to be backed up rather than necessarily backing up everything.

## Usage

Velero is deployed in both the workload cluster and the service cluster. Following are instructions for backing up and restoring resources.

### Backing up

<!--user-demo-backup-start-->

Compliant Kubernetes takes a daily backup of all Kubernetes Resources in all user namespaces. Persistent Volumes will be backed up if they are tied to a Pod. If backups are not wanted the label `compliantkubernetes.io/nobackup` can be added to opt-out of the daily backups.

Application metrics (Grafana) and application log (Kibana) dashboards are also backup up by default.

By default, backups are stored for 720 hours (30 days).

<!--user-demo-backup-end-->

### Restoring

Restoring from a backup with Velero is meant to be a type of disaster recovery. **Velero will not overwrite existing Resources when restoring.** As such, if you want to restore the state of a Resource that is still running, the Resource must be deleted first.

To restore a backup on demand, contact your Compliant Kubernetes administrator.

## Protection of Backups

The Compliant Kubernetes administrator will take the following measure to ensure backups are protected:

1. Backups are encrypted at rest, if the underlying infrastructure provider supports it.

    **Why?** This ensures backups remain confidential, even if, e.g., hard drives are not safely disposed.

2. Backups are replicated to an off-site location, if requested. This process is performed from the service cluster, hence the users -- or attackers gaining access to their application -- cannot access the off-site replicas.

    **Why?** This ensures backups are available even if the primary location is subject to a disaster, such as extreme weather. The backups also remain available -- though unlikely confidential -- in case an attacker manages to gain access to the workload cluster.

<!--

!!!note
    This safeguard is pending an internal investigation and process change.

3. The buckets holding the backups are configured with [object lock](https://docs.safespring.com/storage/object-locking/), if the underlying cloud provider supports it. This means that backups cannot be modified or erase until a given retention time, even with privileged credentials.

    **Why?** This ensures backups are available -- though unlikely confidential -- even if the whole Compliant Kubernetes environment is compromised.
-->
