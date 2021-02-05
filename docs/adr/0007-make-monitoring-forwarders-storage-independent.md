# Make Monitoring Forwarders Storage Independent

* Status: proposed
* Deciders: Cristian
* Date: 2021-02-05

## Context and Problem Statement

In the context of this ADR, **forwarders** refers to any components that are necessary to forward monitoring information -- specifically traces, metrics and logs -- to some monitoring database. As of February 2021, Compliant Kubernetes employs two projects as forwarders:

* [Prometheus](https://prometheus.io/) for metrics forwarding;
* [fluentd](https://www.fluentd.org/) for log forwarding.

Similarly, two projects are employed as monitoring databases:

* [InfluxDB](https://www.influxdata.com/) for metrics;
* [Elasticsearch](https://opendistro.github.io/for-elasticsearch/) for logs.

Overall, the monitoring system needs to be one order of magnitude more resilient than the monitored system. Forwarders improve the resilience of the monitoring system by providing buffering: In case the database is under maintenance or down, the buffer of the forwarders will ensure that no monitoring information is lost.
Hence, forwarders are subject to the following tensions:

* More buffering implies storage, which make the forwarders vulnerable to storage outages (e.g., disk full, CSI hiccups);
* Less buffering implies higher risk of losing monitoring information when the database is under maintenance or down.

## Decision Drivers

* We want a robust monitoring system.
* We want to monitor the storage system.
* We want VM-template-based rendering of the workload cluster, which implies no cloud native storage integration.
* We want to make it easier to "cleanup and start from a known good state".

## Considered Options

* Use underlying storage provider for increased buffering resilience ([current approach](https://github.com/elastisys/compliantkubernetes-apps/blob/v0.9.0/helmfile/values/kube-prometheus-stack-wc.yaml.gotmpl#L100)).
* Use [Local Persistent Volumes](https://kubernetes.io/blog/2018/04/13/local-persistent-volumes-beta/).
* Use [emptyDir](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir) volumes.
* Use [hostPath](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath) volumes.

## Decision Outcome

Chosen option: "[option 1]", because [justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force force | … | comes out best (see below)].

### Positive Consequences <!-- optional -->

* [e.g., improvement of quality attribute satisfaction, follow-up decisions required, …]
* …

### Negative Consequences <!-- optional -->

* [e.g., compromising quality attribute, follow-up decisions required, …]
* …

## Pros and Cons of the Options

### Use underlying storage provider

* ✅ Good, because the forwarder can run on any node.
* ✅ Good, because the buffer can be unlimited.
* ✅ Good, because no buffered monitoring information is lost if a node goes down.
* Bad, because non-node-local storage is generally slower.
* Bad, because forwarder will fail if storage provider goes down. This is especially problematic for Exoscale, bare-metal and BYO-VMs.

### Use Local Persistent Volumes

* Good, because it preserves the same mechanisms as PVCs, but storage is node local.
* Good, because the forwarder survives failure of the underlying stoorage.
* Good, because the forwarder can monitor the storage provider.
* Bad, because "[i]f a node becomes unhealthy, then the local volume becomes inaccessible by the pod. The pod using this volume is unable to run.".
* Bad, because the amount of forwarding depends on the node's local disk size.
* Bad, because local persistent storage requires an additional configuration step.

### Use emptyDir

* Good, because forwarder can run on any node.
* Good, because the forwarder survives failure of the underlying stoorage.
* Good, because the forwarder can monitor the storage provider.
* Bad, because the amount of forwarding depends on the node's local disk size.
* Bad, because

## Links

* [Prometheus Operator Storage](https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/user-guides/storage.md)
