# Disaster Recovery

This document details disaster recovery procedures for Compliant Kubernetes. These procedures must be executed by the administrator.

## Compliant Need

Disaster recovery is mandated by several regulations and information security standards. For example, in ISO 27001:2013, the annexes that mostly concerns disaster recovery are:

- [A.12.3.1 Information Backup](https://www.isms.online/iso-27001/annex-a-12-operations-security/)
- [A.17.1.1 Planning Information Security Continuity](https://www.isms.online/iso-27001/annex-a-17-information-security-aspects-of-business-continuity-management/)

## Object storage providers

### Feature matrix

Provider       | Write-only credentials
-------------  | -------------
AWS S3         | Yes
Citycloud S3   | No
Exoscale S3    | Yes
GCP            | Yes
Safespring S3  | Yes

## OpenSearch

!!!note
    For Open Distro for Elasticsearch used in v0.18 and earlier, the same approach for backup and restore can be used with different naming, using `elasticsearch` for the CronJob and `elastic` for the namespace instead of `opensearch`.

### Backup

OpenSearch is set up to store backups in an S3 bucket. There is a CronJob called `opensearch-backup` in the cluster that is invoking the snapshot process in OpenSearch.

To take a snapshot on-demand, execute

```
./bin/ck8s ops kubectl sc -n opensearch-system create job --from=cronjob/opensearch-backup <name-of-job>
```

### Restore


Set the following variables

- `user` - OpenSearch user with permissions to manage snapshots, usually `snapshotter`
- `password` - password for the above user
- `os_url` - URL to OpenSearch

List snapshot repositories

```bash
# Simple
❯ curl -kL -u "${user}:${password}" "${os_url}/_cat/repositories?v"
id                   type
opensearch-snapshots   s3

# Detailed
❯ curl -kL -u "${user}:${password}" "${os_url}/_snapshot/?pretty"
{
  "opensearch-snapshots" : {
    "type" : "s3",
    "settings" : {
      "bucket" : "opensearch-backup",
      "client" : "default"
    }
  }
}
```

List available snapshots

```bash
snapshot_repo=<name/id from previous step>

# Simple
❯ curl -kL -u "${user}:${password}" "${os_url}/_cat/snapshots/${snapshot_repo}?v&s=id"
id                         status start_epoch start_time end_epoch  end_time duration indices successful_shards failed_shards total_shards
snapshot-20211231_120002z SUCCESS 1640952003  12:00:03   1640952082 12:01:22     1.3m      54                54             0           54
snapshot-20220101_000003z SUCCESS 1640995203  00:00:03   1640995367 00:02:47     2.7m      59                59             0           59
snapshot-20220101_120002z SUCCESS 1641038403  12:00:03   1641038533 12:02:13     2.1m      57                57             0           57
...

# Detailed list of all snapshots
curl -kL -u "${user}:${password}" "${os_url}/_snapshot/${snapshot_repo}/_all?pretty"

# Detailed list of specific snapshot
❯ curl -kL -u "${user}:${password}" "${os_url}/_snapshot/${snapshot_repo}/snapshot-20220104_120002z?pretty"
{{
  "snapshots" : [
    {
      "snapshot" : "snapshot-20220104_120002z",
      "uuid" : "oClQdNAyTeiEmZb5dVh0SQ",
      "version_id" : 135238127,
      "version" : "1.2.3",
      "indices" : [
        "authlog-default-2021.12.20-000001",
        "authlog-default-2021.12.30-000011",
        "authlog-default-2022.01.03-000015",
        "other-default-2021.12.30-000011",
        ...
      ],
      "data_streams" : [ ],
      "include_global_state" : false,
      "state" : "SUCCESS",
      "start_time" : "2022-01-04T12:00:02.596Z",
      "start_time_in_millis" : 1641297602596,
      "end_time" : "2022-01-04T12:01:07.833Z",
      "end_time_in_millis" : 1641297667833,
      "duration_in_millis" : 65237,
      "failures" : [ ],
      "shards" : {
        "total" : 66,
        "failed" : 0,
        "successful" : 66
      }
    }
  ]
}


```

You usually select the latest snapshot containing the indices you want to restore.
Restore one or multiple indices from a snapshot

!!!note
    You cannot restore a write index (the latest index) if you already have a write index connected to the same index alias (which will happen if you have started to receive logs).

```bash
snapshot_name=<Snapshot name from previous step>
indices="<list of comma separated indices/index patterns>"

curl -kL -u "${user}:${password}" -X POST "${os_url}/_snapshot/${snapshot_repo}/${snapshot_name}/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "'${indices}'"
}
'
```

Read the [documentation](https://opensearch.org/docs/latest/opensearch/snapshot-restore/) to see the API, all parameters and their explanations.

#### Restoring OpenSearch Dashboards data

Data in OpenSearch Dashboards (saved searches, visualizations, dashboards, etc) is stored in the index `.opensearch_dashboards_1`. To restore that data you first need to delete the index and then do a restore.

This will overwrite anything in the current `.opensearch_dashboards_1` index. If there is something new that should be saved, then [export](https://www.elastic.co/guide/en/kibana/7.10/managing-saved-objects.html#_export) the saved objects and [import](https://www.elastic.co/guide/en/kibana/7.10/managing-saved-objects.html#_import) them after the restore.

```bash
snapshot_name=<Snapshot name from previous step>

curl -kL -u "${user}:${password}" -X DELETE "${os_url}/.opensearch_dashboards_1?pretty"

curl -kL -u "${user}:${password}" -X POST "${os_url}/_snapshot/${snapshot_repo}/${snapshot_name}/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "'.opensearch_dashboards_1'"
}
'
```

!!!note
    For Open Distro for Elasticsearch and Kibana used in v0.18 and earlier, the same approach can be used with different naming, using `.kibana_1` for the index name instead of `.opensearch_dashboards_1`.

### Start new cluster from snapshot

This process is very similar to the one described above, but there are a few extra steps to carry out.

Before you install OpenSearch you can preferably disable the initial index creation to make the restore process leaner by setting the following configuration option:

```bash
opensearch.configurer.createIndices: false
```

Install the OpenSearch suite:

```bash
./bin/ck8s ops helmfile sc -l group=opensearch apply
```

Wait for the the installation to complete.

After the installation, go back up to the **Restore** section to proceed with the restore.
If you want to restore all indices, use the following `indices` variable

```bash
indices="kubernetes-*,kubeaudit-*,other-*"
```

!!!note
    This process assumes that you are using the same S3 bucket as your previous cluster. If you aren't:

    - Register a new S3 snapshot repository to the old bucket as [described here](https://opensearch.org/docs/latest/opensearch/snapshot-restore/#register-repository)
    - Use the newly registered snapshot repository in the restore process

## Harbor

### Backup

Harbor is set up to store backups of the database in an S3 bucket (note that this does not include the actual images, since those are already stored in S3 by default).
There is a CronJob called `harbor-backup-cronjob` in the cluster that is taking a database dump and uploading it to a S3 bucket.

To take a backup on-demand, execute

```bash
./bin/ck8s ops kubectl sc -n harbor create job --from=cronjob/harbor-backup-cronjob <name-of-job>
```

### Restore

Instructions for how to restore Harbor can be found in `compliantkubernetes-apps`: <https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts/restore#restore-harbor>

## InfluxDB

### Backup

InfluxDB is set up to store backups of the data in an S3 bucket.
There is a CronJob called `influxdb-backup` in the cluster that is invoking influxDB's backup function and uploading the backup to a S3 bucket.

To take a backup on-demand, execute

```bash
./bin/ck8s ops kubectl sc -n influxdb-prometheus create job --from=cronjob/influxdb-backup <name-of-job>
```

### Restore

When restoring the data, InfluxDB must not already contain the databases that are going to be restored.
This will make sure that the databases are not created.

- If you are planning on restoring InfluxDB on a new installation, then before installing InfluxDB set `influxDB.createdb: false` in `sc-config.yaml`.
- If you are restoring to an existing InfluxDB instance, then first drop the databases:

    ```bash
    # Enter the InfluxDB container
    ./bin/ck8s ops kubectl sc exec -n influxdb-prometheus influxdb-0 -it -- bash
    # Start the influx CLI
    influx -username ${INFLUXDB_ADMIN_USER} -password ${INFLUXDB_ADMIN_PASSWORD} -precision rfc3339
    # Drop the databases
    DROP DATABASE service_cluster
    DROP DATABASE workload_cluster
    # Exit the influx CLI
    exit
    # Exit the InfluxDB container
    exit
    ```

You will then create a kubernetes job that will restore InfluxDB.
Run the following from root of `comliantkubernetes-apps`.:

```bash
export INFLUX_BACKUP_NAME="<name of your backup>"
export INFLUX_ADDR="influxdb.influxdb-prometheus.svc:8088"
export S3_INFLUX_BUCKET_NAME=$(yq read "${CK8S_CONFIG_PATH}/sc-config.yaml" objectStorage.buckets.influxDB)
export S3_REGION_ENDPOINT=$(yq read "${CK8S_CONFIG_PATH}/sc-config.yaml" objectStorage.s3.regionEndpoint)
export S3_REGION=$(yq read "${CK8S_CONFIG_PATH}/sc-config.yaml" objectStorage.s3.region)
export S3_ACCESS_KEY=$(sops -d "${CK8S_CONFIG_PATH}/secrets.yaml" | yq read - objectStorage.s3.accessKey)
export S3_SECRET_KEY=$(sops -d "${CK8S_CONFIG_PATH}/secrets.yaml" | yq read - objectStorage.s3.secretKey)
envsubst < manifests/restore/restore-influx.yaml | ./bin/ck8s ops kubectl sc apply -n influxdb-prometheus -f -
```

Then make sure that out influxDB users have the correct permissions (this assumes you are using default usernames for the prometheus writers):

```bash
# Enter the InfluxDB container
./bin/ck8s ops kubectl sc exec -n influxdb-prometheus influxdb-0 -it -- bash
# Start the influx CLI
influx -username ${INFLUXDB_ADMIN_USER} -password ${INFLUXDB_ADMIN_PASSWORD} -precision rfc3339
# Update permissions
GRANT WRITE ON service_cluster TO scWriter
GRANT WRITE ON workload_cluster TO wcWriter
# Exit the influx CLI
exit
# Exit the InfluxDB container
exit
```

## Velero

These instructions make use of the Velero CLI, you can download it here: <https://github.com/vmware-tanzu/velero/releases/tag/v1.5.3> (version 1.5.3).
The CLI needs the env variable `KUBECONFIG` set to the path of a decrypted kubeconfig.
Read more about Velero here: <https://compliantkubernetes.io/user-guide/backup/>

!!!note
    This documentation uses the Velero CLI, as opposed to Velero CRDs, since that is what is encouraged by upstream documentation.

### Backup

Velero is set up to take daily backups and store them in an S3 bucket.
The daily backup will not take backups of everything in a kubernetes cluster, it will instead look for certain labels and annotations.
Read more about those labels and annotations here: <https://compliantkubernetes.io/user-guide/backup/#backing-up>

It is also possible to take on-demand backups.
Then you can freely chose what to backup and do not have to base it on the same labels.
A basic example with the Velero CLI would be `velero backup create manual-backup`, which would take a backup of all kubernetes resources (though not the data in the volumes by default).
Check which arguments you can use by running `velero backup create --help`.

### Restore

Restoring from a backup with Velero is meant to be a type of disaster recovery.
**Velero will not overwrite existing Resources when restoring.**
As such, if you want to restore the state of a Resource that is still running, the Resource must be deleted first.

To restore the state from the latest daily backup, run:

```bash
velero restore create --from-schedule velero-daily-backup --wait
```

This command will wait until the restore has finished.
You can also do partial restorations, e.g. just restoring one namespace, by using different arguments.
You can also restore from manual backups by using the flag `--from-backup <backup-name>`

Persistent Volumes are only restored if a Pod with the backup annotation is restored.
Multiple Pods can have an annotation for the same Persistent Volume.
When restoring the Persistent Volume it will overwrite any existing files with the same names as the files to be restored.
Any other files will be left as they were before the restoration started.
So a restore will not wipe the volume clean and then restore.
If a clean wipe is the desired behavior, then the volume must be wiped manually before restoring.

## Grafana

This refers to the user Grafana, not the ops Grafana.

### Backup

Grafana is set up to be included in the daily Velero backup.
We then include the Grafana deployment, pod, and PVC (including the data).
Manual backups can be taken using velero (include the same resources).

### Restore

To restore the Grafana backup you must:

- Have Grafana installed
- Delete the grafana deployment, PVC and PV

    ```bash
    kubectl delete deploy -n monitoring user-grafana
    kubectl delete pvc -n monitoring user-grafana
    ```

- Restore the velero backup

    ```bash
    velero restore create --from-schedule velero-daily-backup --wait
    ```

You can also restore Grafana by setting `restore.velero` in your `{CK8S_CONFIG_PATH}/sc-config.yaml` to `true`, and then reapply the service cluster apps:

```bash
.bin/ck8s apply sc
```

 This will go through the same steps as above.
 By default, the latest daily backup is chosen; to restore from a different backup, set `restore.veleroBackupName` to the desired backup name.
