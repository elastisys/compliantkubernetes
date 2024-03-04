---
tags:
- ISO 27001 A.12.3.1 Information Backup
- ISO 27001 A.17.1.1 Planning Information Security Continuity
- HIPAA S24 - Contingency Plan - Disaster Recovery Plan - § 164.308(a)(7)(ii)(B)
- MSBFS 2020:7 4 kap. 14 §
- MSBFS 2020:7 4 kap. 15 §
- MSBFS 2020:7 4 kap. 22 §
- HSLF-FS 2016:40 3 kap. 13 § Säkerhetskopiering
- NIST SP 800-171 3.6.3
---
# Disaster Recovery

This document details disaster recovery procedures for Compliant Kubernetes. These procedures must be executed by the administrator.

## Compliant Need

Disaster recovery is mandated by several regulations and information security standards. For example, in ISO 27001:2013, the annexes that mostly concerns disaster recovery are:

- [A.12.3.1 Information Backup](https://www.isms.online/iso-27001/annex-a-12-operations-security/)
- [A.17.1.1 Planning Information Security Continuity](https://www.isms.online/iso-27001/annex-a-17-information-security-aspects-of-business-continuity-management/)

## Object storage providers

## Off-site backups

Backups can be set up to be replicated off-site using CronJobs.

In version v0.23 these can be **encrypted** before they are sent off-site, which means they must first be restored to be usable. <br/>
It is possible to restore services directly from **unencrypted** off-site backups with some additional steps.

See [the instructions in `compliantkubernetes-apps`](https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts/restore-sync) for how to restore off-site backups.

## When a new region/Infrastructure Provider is used

- Configure and set base ck8s-configs:

  sc-config.yaml:

  `harbor.persistence.swift.*`,`objectStorage.sync.*`

  common-config.yaml:

  `objectStorage.s3.region`, `objectStorage.s3.regionEndpoint`

  secrets.yaml:

  `dex.connectors.*`, `harbor.persistence.swift.username`, `harbor.persistence.swift.password`, `objectStorage.s3.accessKey`, `objectStorage.s3.secretKey`

  .state/s3cfg.ini:

  `access_key`, `secret_key`, `host_base`, `host_bucket`

- Configure and set custom ck8s-configs:

  Examples can be files containing Identity Provider, Infrastructure Provider, or DNS critical information.

## OpenSearch

### Backup

OpenSearch is set up to store backups in an S3 bucket. There is a CronJob called `opensearch-backup` in the cluster that is invoking the snapshot process in OpenSearch.

To take a snapshot on-demand, execute

```
./bin/ck8s ops kubectl sc -n opensearch-system create job --from=cronjob/opensearch-backup <name-of-job>
```

### Restore

Set the following variables

1. OpenSearch user with permissions to manage snapshots, usually `admin`
1. The password for the above user
1. The URL to OpenSearch

```bash
user=admin
password=$(sops -d ${CK8S_CONFIG_PATH}/secrets.yaml | yq4 '.opensearch.adminPassword')
os_url=https://opensearch.$(yq4 '.global.opsDomain' ${CK8S_CONFIG_PATH}/common-config.yaml)
```

!!!important "Restoring from off-site backup"
    - To restore from an **encrypted** off-site backup:

        First import the backup into the main S3 service and register the restored bucket as a new snapshot repository:
        ```bash
        curl -kL -u "${user}:${password}" -X PUT "${os_url}/_snapshot/backup-repository?pretty" -H 'Content-Type: application/json' -d'
        {
          "type": "s3",
          "settings": {
            "bucket": "<restored-bucket>",
            "readonly": true
          }
        }
        '
        ```
        Then restore from this snapshot repository (`backup-repositroy`) in OpenSearch.

    - To restore from an **unencrypted** off-site backup:

        Configure the remote and bucket as the main S3 service and bucket for apps and OpenSearch respectively, then update the OpenSearch Helm releases and perform the restore.
        It is recommended to either suspend or remove the OpenSearch backup CronJob to prevent it from running while restoring.

        Remember to revert to the regular S3 service afterwards and reactivate the backup CronJob! <br/>
        Replace the previous snapshot repository if it is unusable.

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
# Use "-.*" if index per namespace is enabled
indices="kubernetes-*,kubeaudit-*,other-*,authlog-*"

curl -kL -u "${user}:${password}" -X POST "${os_url}/_snapshot/${snapshot_repo}/${snapshot_name}/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "'${indices}'"
}
'
```

Read the [documentation](https://opensearch.org/docs/latest/opensearch/snapshot-restore/) to see the API, all parameters and their explanations.

#### Restoring OpenSearch Dashboards data

Data in OpenSearch Dashboards (saved searches, visualizations, dashboards, etc) is stored in the index `.opensearch_dashboards_x`. To restore that data you first need to delete the index and then do a restore.

This will overwrite anything in the current `.opensearch_dashboards_x` index. If there is something new that should be saved, then [export](https://www.elastic.co/guide/en/kibana/7.10/managing-saved-objects.html#_export) the saved objects and [import](https://www.elastic.co/guide/en/kibana/7.10/managing-saved-objects.html#_import) them after the restore.

There can be multiple `.opensearch_dashboards` indices in Opensearch, the current index should be the one you want to restore. To view your dashboard indices, follow these steps.

```bash
snapshot_name=<Snapshot name from previous step>

curl -kL -u "${user}:${password}" -X GET ${os_url}'/.opensearch_dashboard*?pretty' | jq 'keys'
```

If multiple `.opensearch_dashboards_x` indices show up, run this to see the index that the alias is currently looking at.

```bash
curl -kL -u "${user}:${password}" -X GET ${os_url}'/_alias/.opensearch_dashboard*?pretty' | jq 'keys'
```

Make sure that the index you want to restore also exists on the snapshot. (May be an issue if you are using an old snapshot)

```bash
curl -kL -u "${user}:${password}" -X GET "${os_url}/_snapshot/${snapshot_repo}/${snapshot_name}?pretty" | jq '.snapshots[].indices' | grep .opensearch_dashboards
```

!!!note
    If you visit the `"<os_url>/app/dashboards"` page in the Opensearch GUI after deleting the index and before restoring the index, another empty index `.opensearch_dashboards` will be created. You need to delete this manually, which can be done with
    ```bash
    `curl -kL -u "${user}:${password}" -X DELETE "${os_url}/.opensearch_dashboards?pretty"`
    ```

```bash
index_to_restore=<Index name from previous step>

curl -kL -u "${user}:${password}" -X DELETE "${os_url}/${index_to_restore}?pretty"

curl -kL -u "${user}:${password}" -X POST "${os_url}/_snapshot/${snapshot_repo}/${snapshot_name}/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "'${index_to_restore}'"
}
'
```

### Start new cluster from snapshot

This process is very similar to the one described above, but there are a few extra steps to carry out.

Before you install OpenSearch you can preferably disable the initial index creation to make the restore process leaner by setting the following configuration option:

```bash
opensearch.createIndices: false
```

Install the OpenSearch suite:

```bash
./bin/ck8s ops helmfile sc -l group=opensearch apply
```

Wait for the installation to complete.

After the installation, go back up to the **Restore** section to proceed with the restore.
If you want to restore all indices, use the following `indices` variable

```bash
indices="kubernetes-*,kubeaudit-*,other-*,authlog-*"
```

!!!note
    This process assumes that you are using the same S3 bucket as your previous cluster. If you aren't:

    - Register a new S3 snapshot repository to the old bucket as [described here](https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#register-repository)
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

!!!important "Restoring from off-site backup"
    Since Harbor stores both database backups and images in the same bucket it is recommended to restore the off-site backup into the main S3 service first, reconfigure Harbor to use it, then restore the database from it.

Instructions for how to restore Harbor can be found in `compliantkubernetes-apps`: <https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts/restore#restore-harbor>

## Velero

These instructions make use of the Velero CLI, you can download it [here](https://github.com/vmware-tanzu/velero/releases/tag/v1.7.1) (version 1.7.1).
The CLI needs the env variable `KUBECONFIG` set to the path of a decrypted kubeconfig.
Read more about Velero [here](../user-guide/backup.md).

!!!note
    This documentation uses the Velero CLI, as opposed to Velero CRDs, since that is what is encouraged by upstream documentation.

### Backup

Velero is set up to take daily backups and store them in an S3 bucket.
The daily backup will not take backups of everything in a Kubernetes cluster, it will instead look for certain labels and annotations.
Read more about those labels and annotations [here](../user-guide/backup.md#backing-up).

It is also possible to take on-demand backups.
Then you can freely chose what to backup and do not have to base it on the same labels.
A basic example with the Velero CLI would be `velero backup create manual-backup`, which would take a backup of all Kubernetes resources (though not the data in the volumes by default).

If you want to create a latest backup from existing schedule , Velero CLI would be `velero backup create --from-schedule velero-daily-backup --wait`.

Check which arguments you can use by running `velero backup create --help`.

### Restore


!!!note

    If you are restoring an environment under a new domain name then there is a possibility to reconfigure image references with [Velero](https://velero.io/docs/main/restore-reference/#changing-poddeploymentstatefulsetdaemonsetreplicasetreplicationcontrollerjobcronjob-image-repositories), but ingresses must be updated manually.

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

### Restore from off-site backup

- Restoring from **encrypted** off-site backup:

    Recover the encrypted bucket into the main S3 service and reconfigure Velero to use this bucket, then follow the regular instructions.

    The references in Kubernetes might need to be deleted so Velero can resync from the bucket:

    ```bash
    # Note that this is only backup metadata
    ./bin/ck8s ops kubectl sc -n velero delete backups.velero.io --all

    ./bin/ck8s ops kubectl wc -n velero delete backups.velero.io --all
    ```

- Restoring from **unencrypted** off-site backup:

    To recover directly from off-site backup the backup-location must be reconfigured:

    ```bash
    export S3_BUCKET="<off-site-s3-bucket>"
    export S3_PREFIX="<service-cluster|workload-cluster>"
    export S3_ACCESS_KEY=$(sops -d --extract '["objectStorage"]["sync"]["s3"]["accessKey"]' "$CK8S_CONFIG_PATH/secrets.yaml")
    export S3_SECRET_KEY=$(sops -d --extract '["objectStorage"]["sync"]["s3"]["secretKey"]' "$CK8S_CONFIG_PATH/secrets.yaml")
    export S3_REGION=$(yq r "$CK8S_CONFIG_PATH/sc-config.yaml" "objectStorage.sync.s3.region")
    export S3_ENDPOINT=$(yq r "$CK8S_CONFIG_PATH/sc-config.yaml" "objectStorage.sync.s3.regionEndpoint")
    export S3_PATH_STYLE=$(yq r "$CK8S_CONFIG_PATH/sc-config.yaml" "objectStorage.sync.s3.forcePathStyle")

    # Delete default backup location
    velero backup-location delete default

    # Delete backups from default backup location, note that this is only the backup metadata
    ./bin/ck8s ops kubectl sc -n velero delete backups.velero.io --all

    ./bin/ck8s ops kubectl wc -n velero delete backups.velero.io --all

    # Create off-site credentials
    kubectl -n velero create secret generic velero-backup \
      --from-literal=cloud="$(echo -e "[default]\naws_access_key_id: ${S3_ACCESS_KEY}\naws_secret_access_key: ${S3_SECRET_KEY}\n")"

    # Create off-site backup location
    velero backup-location create backup \
        --access-mode ReadOnly \
        --provider aws \
        --bucket "${S3_BUCKET}" \
        --prefix "${S3_PREFIX}" \
        --config="region=${S3_REGION},s3Url=${S3_ENDPOINT},s3ForcePathStyle=${S3_PATH_STYLE}" \
        --credential=velero-backup=cloud
    ```

    Check that the backup-location becomes available:
    ```console
    $ velero backup-location get
    NAME     PROVIDER   BUCKET/PREFIX       PHASE       LAST VALIDATED   ACCESS MODE   DEFAULT
    backup   aws        <bucket>/<prefix>   Available   <timestamp>      ReadOnly
    ```

    Then check that the backups becomes available using `velero backup get`.
    When they are available restore one of them using `velero restore create <name-of-restore> --from-backup <name-of-backup>`.

    After the restore is complete Velero should be reconfigured to use the main S3 service again, with a new bucket if the previous one is unusable.
    Updating or syncing the Helm chart:
    ```bash
    ./bin/ck8s ops helmfile sc -f helmfile -l app=velero -i apply

    ./bin/ck8s ops helmfile wc -f helmfile -l app=velero -i apply
    ```

    The secret and the backup metadata from the off-site backups can be deleted:
    ```bash
    ./bin/ck8s ops kubectl sc -n velero delete secret velero-backup
    ./bin/ck8s ops kubectl sc -n velero delete backups.velero.io --all
    ./bin/ck8s ops kubectl sc -n velero delete backupstoragelocations.velero.io backup

    ./bin/ck8s ops kubectl wc -n velero delete secret velero-backup
    ./bin/ck8s ops kubectl wc -n velero delete backups.velero.io --all
    ./bin/ck8s ops kubectl wc -n velero delete backupstoragelocations.velero.io backup
    ```

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
    ./bin/ck8s ops kubectl sc delete deploy -n monitoring user-grafana
    ./bin/ck8s ops kubectl sc delete pvc -n monitoring user-grafana
    ```

- Restore the velero backup

    ```bash
    velero restore create --from-schedule velero-daily-backup --wait
    ```
