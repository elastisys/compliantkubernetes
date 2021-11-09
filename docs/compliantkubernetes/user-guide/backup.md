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
