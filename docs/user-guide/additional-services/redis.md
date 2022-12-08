Redis™
======

![Redis Deployment Model](img/redis.drawio.svg)

This page will help you succeed in connecting your application to a low-latency in-memory cache Redis which meets your security and compliance requirements.

## Provision a New Redis Cluster

Ask your service-specific administrator to install a Redis cluster inside your Compliant Kubernetes environment. The service-specific administrator will ensure the Redis cluster complies with your security requirements, including:

* **Business continuity**: We recommend a highly available setup with at minimum three instances. The Redis client library that you use in your application needs to support [Redis Sentinel](https://redis.io/topics/sentinel). Notice that clients with Sentinel support need [extra steps to discover the Redis primary](https://redis.io/topics/sentinel-clients).
* **Capacity management**: Your service-specific administrator will ensure Redis has enough capacity to meet your needs.
* **Incident management**: Your administrator will set up the necessary Probes, dashboards and alerts, to discover issues and resolve them, before they become a problem.

!!!important "Important: Improve Access Control with NetworkPolicies"
    Please note the follow information about [Redis access control](https://redis.io/topics/security) from the upstream documentation:

    > Redis is designed to be accessed by trusted clients inside trusted environments.

    For improved security, discuss with your service-specific administrator what Pods and/or Namespaces need access to the Redis cluster. They can then set up the necessary [NetworkPolicies](/compliantkubernetes/user-guide/safeguards/enforce-networkpolicies/).

!!!important "Important: No Disaster Recovery"

    We do not recommend using Redis as primary database. Redis should be used to store:

    * Cached data: If this is lost, this data can be quickly retrieved from the primary database, such as the PostgreSQL cluster.
    * Session state: If this is lost, the user experience might be impacted -- e.g., the user needs to re-login -- but no data should be lost.

Compliant Kubernetes recommends the [Spotahome operator](https://github.com/spotahome/redis-operator).

## Install Prerequisites

Before continuing, make sure you have access to the Kubernetes API, as describe [here](/compliantkubernetes/user-guide/setup/).

Make sure to install the Redis client on your workstation. On Ubuntu, this can be achieved as follows:

```bash
sudo apt install redis-tools
```

## Getting Access

Your administrator will set up a ConfigMap inside Compliant Kubernetes, which contains all information you need to access your Redis cluster.
The ConfigMap has the following shape:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: $CONFIG_MAP
  namespace: $NAMESPACE
data:
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

First, check that you are on the right Compliant Kubernetes cluster, in the right **application** namespace:

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

## Expose Redis Connection Parameters to Your Application

To expose the Redis cluster to your application, follow one of the following upstream documentation:

* [Create a Pod that has access to the ConfigMap data through a Volume](https://kubernetes.io/docs/concepts/configuration/configmap/#using-configmaps-as-files-from-a-pod)
* [Define container environment variables using ConfigMap data](https://kubernetes.io/docs/concepts/configuration/configmap/#configmaps-and-pods)

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

Check out the [release notes](../../release-notes/redis.md) for the Redis cluster that runs in Compliant Kubernetes environments!

## Further Reading

* [Redis Sentinel](https://redis.io/topics/sentinel)
* [Guidelines for Redis clients with support for Redis Sentinel](https://redis.io/topics/sentinel-clients)
* [Redis Commands](https://redis.io/commands)
* [Kubernetes ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap)
