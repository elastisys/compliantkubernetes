# Disaster Recovery

This document details disaster recovery procedures for Compliant Kubernetes. These procedures must be executed by the operator.

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

## Elasticsearch

### Backup

Elasticsearch is set up to store backups in an S3 bucket. There is a CronJob called `elasticsearch-backup` in the cluster that is invoking the snapshot process in Elasticsearch.

To take a snapshot on-demand, execute

```
./bin/ck8s ops kubectl sc -n elastic-system create job --from=cronjob/elasticsearch-backup <name-of-job>
```

### Restore

Set the following variables

- `user` - Elasticsearch user with permissions to manage snapshots, usually `snapshotter`
- `password` - password for the above user
- `es_url` - url to Elasticsearch

List snapshot repositories

```bash
# Simple
❯ curl -kL -u "${user}:${password}" "${es_url}/_cat/repositories?v"
id              type
s3_exoscale_7.x   s3

# Detailed
❯ curl -kL -u "${user}:${password}" "${es_url}/_snapshot/?pretty"
{
  "s3_exoscale_7.x" : {
    "type" : "s3",
    "settings" : {
      "bucket" : "es-backup",
      "client" : "default"
    }
  }
}
```

List available snapshots

```bash
snapshot_repo=<name/id from previous step>

# Simple
❯ curl -kL -u "${user}:${password}" "${es_url}/_cat/snapshots/${snapshot_repo}?v&s=id"
id                         status start_epoch start_time end_epoch  end_time duration indices successful_shards failed_shards total_shards
snapshot-20200929_093941z SUCCESS 1601372382  09:39:42   1601372390 09:39:50     8.4s       6                 6             0            6
snapshot-20200930_000008z SUCCESS 1601424008  00:00:08   1601424035 00:00:35    27.4s      20                20             0           20
snapshot-20201001_000006z SUCCESS 1601510407  00:00:07   1601510530 00:02:10       2m      75                75             0           75

# Detailed list of all snapshots
curl -kL -u "${user}:${password}" "${es_url}/_snapshot/${snapshot_repo}/_all?pretty"

# Detailed list of specific snapshot
❯ curl -kL -u "${user}:${password}" "${es_url}/_snapshot/${snapshot_repo}/snapshot-20201001_000006z?pretty"
{
  "snapshots" : [
    {
      "snapshot" : "snapshot-20201001_000006z",
      "uuid" : "Fq0EusFYRV2nI9G9F1DX1A",
      "version_id" : 7080099,
      "version" : "7.8.0",
      "indices" : [
        "kubernetes-default-2020.09.30-000032",
        "other-default-2020.09.30-000005",
        ..<redacted>..
        "kubeaudit-default-2020.09.30-000009"
      ],
      "include_global_state" : false,
      "state" : "SUCCESS",
      "start_time" : "2020-10-01T00:00:07.344Z",
      "start_time_in_millis" : 1601510407344,
      "end_time" : "2020-10-01T00:02:10.828Z",
      "end_time_in_millis" : 1601510530828,
      "duration_in_millis" : 123484,
      "failures" : [ ],
      "shards" : {
        "total" : 75,
        "failed" : 0,
        "successful" : 75
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

curl -kL -u "${user}:${password}" -X POST "${es_url}/_snapshot/${snapshot_repo}/${snapshot_name}/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "'${indices}'"
}
'
```

Read the [API](https://www.elastic.co/guide/en/elasticsearch/reference/current/restore-snapshot-api.html#restore-snapshot-api-request-body) to see all parameters and their explanations.


### Start new cluster from snapshot

This process is very similar to the one described above, but there are a few extra steps to carry out.

Before you install Elasticsearch you can preferably disable the initial index creation by setting

```bash
configurer.createIndices: false
```

in the values file for opendistro. This will make the restore process leaner.

Install the Elasticsearch suite:

```bash
./bin/ck8s ops helmfile sc -l app=opendistro apply
```

Wait for the the installation to complete.

After the installation, go back up to the **Restore** section to proceed with the restore.
If you want to restore all indices, use the following `indices` variable

```bash
indices="kubernetes-*,kubeaudit-*,other-*"
```

!!!note
    This process assumes that you are using the same S3 bucket as your previous cluster. If you aren't:

    - Register a new S3 snapshot repository to the old bucket as [described here](https://www.elastic.co/guide/en/elasticsearch/plugins/7.9/repository-s3-usage.html#repository-s3-usage)
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
