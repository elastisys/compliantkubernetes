# Work in progress

Please check back soon!

## Elasticsearch

### Backup

Elasticsearch is set up to to store backups in an S3 bucket. There is a CronJob called `elasticsearch-backup` in the cluster that is invoking the snapshot process in elasticsearch.

To take a snapshot on-demand, execute

```
./bin/ck8s ops kubectl sc -n elastic-system create job --from=cronjob/elasticsearch-backup <name-of-job>
```


### Restore

Set the following variables

- `user` - elasticsearch user with permissions to manage snapshots, usually `snapshotter`
- `password` - password for the above user
- `es_url` - url to elasticsearch

List snapshot repositories

```bash
# Simple
❯ curl -k -u "${user}:${password}" "${es_url}/_cat/repositories?v"
id              type
s3_exoscale_7.x   s3

# Detailed
❯ curl -k -u "${user}:${password}" "${es_url}/_snapshot/?pretty"
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
❯ curl -k -u "${user}:${password}" "${es_url}/_cat/snapshots/${snapshot_repo}?v&s=id"
id                         status start_epoch start_time end_epoch  end_time duration indices successful_shards failed_shards total_shards
snapshot-20200929_093941z SUCCESS 1601372382  09:39:42   1601372390 09:39:50     8.4s       6                 6             0            6
snapshot-20200930_000008z SUCCESS 1601424008  00:00:08   1601424035 00:00:35    27.4s      20                20             0           20
snapshot-20201001_000006z SUCCESS 1601510407  00:00:07   1601510530 00:02:10       2m      75                75             0           75

# Detailed list of all snapshots
curl -k -u "${user}:${password}" "${es_url}/_snapshot/${snapshot_repo}/_all?pretty"

# Detailed list of specific snapshot
❯ curl -k -u "${user}:${password}" "${es_url}/_snapshot/${snapshot_repo}/snapshot-20201001_000006z?pretty"
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

You usually select the latest snapshot continaing the indices you want to restore.
Restore one or multiple indices from a snapshot

```bash
snapshot_name=<Snapshot name from previous step>
indices="<list of comma separated indices/index patterns>"

curl -k -u "${user}:${password}" -X POST "${es_url}/_snapshot/${snapshot_repo}/${snapshot_name}/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "'${indices}'"
}
'
```

Read the [API](https://www.elastic.co/guide/en/elasticsearch/reference/current/restore-snapshot-api.html#restore-snapshot-api-request-body) to see all parameters and their explanations.


### Start new cluster from snapshot

This process is very similar to the one described above, but there are a few extra steps to carry out.

Before you install elasticsearch you can preferably disable the initial index creation by setting

```bash
configurer.createIndices: false
```

in the values file for opendistro. This will make the restore process leaner.

Install the elasticsearch suite

```bash
./bin/ck8s ops helmfile sc -l app=opendistro apply
```

Wait for the the installation to complete.

After the installation, go back up to the **Restore** section to proceed with the restore.
If you want to restore all indices, use the following `indices` variable

```bash
indices="kubernetes-*,kubeaudit-*,other-*"
```

**Note**, this process assumes that you are using the same s3 bucket as your previous cluster.
If you aren't

- Register a new s3 snapshot repository to the old bucket as per https://www.elastic.co/guide/en/elasticsearch/plugins/7.9/repository-s3-usage.html#repository-s3-usage
- Use the newly registered snapshot repository in the restore process

