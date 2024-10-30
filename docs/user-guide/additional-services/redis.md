---
search:
  boost: 2
---
# Redis™

!!! elastisys "For Elastisys Managed Services Customers"

    You can order Managed Ephemeral Redis™ by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/). Here are the highlights:

    * **Business continuity**: Replicated across three dedicated Nodes.
    * **Disaster recovery**: none -- we recommend against using Redis as a primary database.
    * **Monitoring, security patching and incident management**: included.

    For more information, please read [ToS Appendix 3 Managed Additional Service Specification](https://elastisys.com/legal/terms-of-service/#appendix-3-managed-additional-service-specification-managed-services-only).

<figure>
    <img alt="Redis Deployment Model" src="../img/redis.drawio.svg" >
    <figcaption>
        <strong>Redis on Welkin Deployment Model</strong>
        <br>
        This help you build a mental model on how to access Redis as an Application Developer and how to connect your application to Redis.
    </figcaption>
</figure>

This page will help you succeed in connecting your application to a low-latency in-memory cache Redis which meets your security and compliance requirements.

!!!important "Important: Access Control with NetworkPolicies"

    Please note the follow information about [Redis access control](https://redis.io/topics/security/) from the upstream documentation:

    > Redis is designed to be accessed by trusted clients inside trusted environments.

    Redis access is protected by [NetworkPolicies](../safeguards/enforce-networkpolicies.md). To allow your applications access to a Redis cluster the Pods need to be labeled with `elastisys.io/redis-<cluster_name>-access: allow`.

!!!important "Important: No Disaster Recovery"

    We do not recommend using Redis as primary database. Redis should be used to store:

    * Cached data: If this is lost, this data can be quickly retrieved from the primary database, such as the PostgreSQL cluster.
    * Session state: If this is lost, the user experience might be impacted -- e.g., the user needs to re-login -- but no data should be lost.

!!!important "Important: Sentinel support"

    We recommend a highly available setup with at minimum three instances. The Redis client library that you use in your application needs to support [Redis Sentinel](https://redis.io/topics/sentinel/). Notice that clients with Sentinel support need [extra steps to discover the Redis primary](https://redis.io/docs/latest/develop/reference/sentinel-clients/).

## Install Prerequisites

Before continuing, make sure you have access to the Kubernetes API, as describe [here](../prepare.md).

Make sure to install the Redis client on your workstation. On Ubuntu, this can be achieved as follows:

```bash
sudo apt install redis-tools
```

## Getting Access

Your administrator will set up a ConfigMap inside Welkin, which contains all information you need to access your Redis cluster.
The ConfigMap has the following shape:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: $CONFIG_MAP
  namespace: $NAMESPACE
data:
  # REDIS_CLUSTER_NAME is the name of the Redis Cluster. You need to know the name to label your Pods correctly for network access.
  REDIS_CLUSTER_NAME: $REDIS_CLUSTER_NAME

  # REDIS_SENTINEL_HOST represents a cluster-scoped Redis Sentinel host, which only makes sense inside the Kubernetes cluster.
  # E.g., rfs-redis-cluster.redis-system
  REDIS_SENTINEL_HOST: $REDIS_SENTINEL_HOST

  # REDIS_SENTINEL_PORT represents a cluster-scoped Redis Sentinel port, which only makes sense inside the Kubernetes cluster.
  # E.g., 26379
  REDIS_SENTINEL_PORT: "$REDIS_SENTINEL_PORT"
```

To extract this information, proceed as follows:

```bash
export CONFIG_MAP=            # Get this from your administrator
export NAMESPACE=         # Get this from your administrator

export REDIS_SENTINEL_HOST=$(kubectl -n $NAMESPACE get configmap $CONFIG_MAP -o 'jsonpath={.data.REDIS_SENTINEL_HOST}')
export REDIS_SENTINEL_PORT=$(kubectl -n $NAMESPACE get configmap $CONFIG_MAP -o 'jsonpath={.data.REDIS_SENTINEL_PORT}')
```

!!!important

    At the time of this writing, we do not recommend to use a Redis cluster in a multi-tenant fashion. One Redis cluster should have only one purpose.

## Create a ConfigMap

First, check that you are on the right Welkin cluster, in the right **application** namespace:

```bash
kubectl get nodes
kubectl config view --minify --output 'jsonpath={..namespace}'; echo
```

Now, create a Kubernetes ConfigMap in your application namespace to store the Redis Sentinel connection parameters:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
    name: app-redis-config
data:
    REDIS_SENTINEL_HOST: $REDIS_SENTINEL_HOST
    REDIS_SENTINEL_PORT: "$REDIS_SENTINEL_PORT"
EOF
```

## Allow your Pods to communicate with the Redis cluster

The Redis cluster is protected by Network Policies. Add the following label to your Pods: `elastisys.io/redis-<cluster_name>-access: allow`

`cluster_name` can be retrieved from the ConfigMap provided by your administrator:

```bash
kubectl -n $NAMESPACE get configmap $CONFIG_MAP -o 'jsonpath={.data.REDIS_CLUSTER_NAME}'
```

## Expose Redis Connection Parameters to Your Application

To expose the Redis cluster to your application, follow one of the following upstream documentation:

- [Create a Pod that has access to the ConfigMap data through a Volume](https://kubernetes.io/docs/concepts/configuration/configmap/#using-configmaps-as-files-from-a-pod)
- [Define container environment variables using ConfigMap data](https://kubernetes.io/docs/concepts/configuration/configmap/#configmaps-and-pods)

!!!important

    Make sure to use a Redis client library with Sentinel support. For example:

    * [Django-Redis Client that supports Sentinel Cluster HA](https://github.com/danigosa/django-redis-sentinel-redux#how-to-use-it)
        If the linked code example doesn't work, try `LOCATION: redis://mymaster/db`.

    If your library doesn't support sentinel you could use this project - [Redis sentinel proxy](https://github.com/anubhavmishra/redis-sentinel-proxy)
        Note that the default configuration in this repository will not ensure HA for redis.
        For this you'll either need to use multiple replicas or use it as a sidecar for your applications.

## Follow the Go-Live Checklist

You should be all set.
Before going into production, don't forget to go through the [go-live checklist](../go-live.md).

## CK8S Redis Release Notes

Check out the [release notes](../../release-notes/redis.md) for the Redis cluster that runs in Welkin environments!

## Best Practices Recommended

- **Eviction Policy**: Choose the [eviction policy](https://redis.io/docs/reference/eviction/) that works for your application. The `default` eviction policy for our Managed Redis is `allkeys-lru`, which means any key can be evicted under memory pressure irrespective of whether the key is expired or not. It will keep the most recently used keys and remove the least recently used (LRU) key.
  !!!Note

      Since this is a server setting, it cannot be set by the user itself, but needs to be set by the administrators. Please send a support ticket with the values you would like to set.

- **Set TTL**: If possible, take the advantage of expiring keys, such as temporary OAuth authentication keys. When you set the key, set it with some expiration and Redis will clean up for you. Refer to [TTL](https://redis.io/commands/ttl/)
- **Avoid expensive or blocking operations**: Since Redis command processing is single-threaded, operations like the [KEYS](https://redis.io/commands/keys/) command are expensive and should be avoided. You can avoid `KEYS` by using [SCAN](https://redis.io/commands/scan/) to reduce CPU spikes.
- **Monitor memory usage**: Monitor the usage in Grafana dashboard to ensure that you don't run out of memory and have the chance to scale your cache before seeing issues.
- **Manage idle connection**: The number of connections to Redis increases if connections are not properly terminated. This can lead to bad performance. Therefore, we recommend to setting `timeout` which allows you to set the number of seconds before idle client connections are automatically terminated.
  The default `timeout` for our Managed Redis is set to `0`, which means the idle clients do not timeout and remain connected until the client issues the termination.
  !!!Note

      Since this is a server setting, it cannot be set by the user itself, but needs to be set by the administrators. Please send a support ticket with the values you would like to set.

- **Cache-hit ratio**: You should regularly monitor your `cache-hit` ratio so that you know what percentage of key lookups are successfully returned by keys in your Redis instance.
  `info stats` command provides `keyspace_hits` & `keyspace_misses` metric data to further calculate cache hit ratio for a running Redis instance.

## Further Reading

- [Redis Sentinel](https://redis.io/topics/sentinel/)
- [Sentinel client spec](https://redis.io/docs/latest/develop/reference/sentinel-clients/)
- [Redis Commands](https://redis.io/commands/)
- [Kubernetes ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)
