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

Velero takes a daily backup of all Kubernetes Resources with the label `velero: backup`. Persistent Volumes will be backed up if they are tied to a Pod with the previously mentioned label and if that Pod is annotated with `backup.velero.io/backup-volumes=<volume1>,<volume2>,...`, where the value is a comma separated list of the volume names. For user applications deployed in the workload cluster, make sure to add these labels and annotations to the resources that need to be backed up.

In the service cluster, Grafana (and its associated Persistent Volume) is configured to be backed up.

Backups are stored for 720 hours (30 days).

### Restoring

Restoring from a backup with Velero is meant to be a type of disaster recovery. **Velero will not overwrite existing Resources when restoring.** As such, if you want to restore the state of a Resource that is still running, the Resource must be deleted first.

To restore the state from the latest daily backup, first download the Velero cli: https://github.com/vmware-tanzu/velero/releases/tag/v1.1.0 (version 1.1.0). Then, to restore your Resources from the backup, run:

`velero restore create --from-schedule velero-daily-backup -w`

This command will wait until the restore has finished. Make sure that `KUBECONFIG` is exported as an environment variable when you run the restore command.

Persistent Volumes are only restored if a Pod with the backup annotation is restored. Multiple Pods can have an annotation for the same Persistent Volume. When restoring the Persistent Volume it will overwrite any existing files with the same names as the files to be restored. Any other files will be left as they were before the restoration started. So a restore will not wipe the volume clean and then restore. If a clean wipe is the desired behaviour, then the volume must be wiped manually before restoring.

To restore the service cluster from a Velero backup, set `restore.velero` in your `{CK8S_CONFIG_PATH}/sc-config.yaml` to `true`, and then reapply the service cluster apps (in `compliantkubernetes-apps`: `bin/ck8s apply sc`). By default, the latest daily backup is chosen; to restore from a different backup, set `restore.veleroBackupName` to the desired backup name.