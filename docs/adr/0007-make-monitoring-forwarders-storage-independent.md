# Make Monitoring Forwarders Storage Independent

* Status: accepted
* Deciders: Axel, Cristian, Fredrik, Johan, Olle, Viktor
* Date: 2021-02-09

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
* We want to have self-healing and avoid manual actions after failure.
* We want to be able to find the root cause of an incident quickly.
* We want to run as many components non-root as possible and tightly integrate with [securityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods).

## Considered Options

* Use underlying storage provider for increased buffering resilience ([current approach](https://github.com/elastisys/compliantkubernetes-apps/blob/v0.9.0/helmfile/values/kube-prometheus-stack-wc.yaml.gotmpl#L100)).
* Use [Local Persistent Volumes](https://kubernetes.io/blog/2018/04/13/local-persistent-volumes-beta/).
* Use [emptyDir](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir) volumes.
* Use [hostPath](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath) volumes.

## Decision Outcome

Chosen option: emptyDir for Prometheus as forwarder, because it allows monitoring of the storage system in some cases (e.g. Rook) and can redeploy automatically after node failure. It also keeps the complexity down without much risk of data loss.

Fluentd as forwarder is deployed via DaemonSet. Both, emptyDir and hostPath can be used.

### Positive Consequences

* We can monitor the storage system.
* Failure of the storage system does not affect monitoring forwarder.
* Forwarder can be easier deployed "fresh".

### Negative Consequences

* Buffered monitoring information is lost if node is lost.
* emptyDir can cause disk pressure. This can be handled by alerting on low disk space.

## Pros and Cons of the Options

### Use underlying storage provider

* Good, because the forwarder can be restarted on any node.
* Good, because the buffer can be large.
* Good, because no buffered monitoring information is lost if a node goes down.
* Good, because buffered monitoring information is preserved if the forwarder is redeployed.
* Bad, because non-node-local storage is generally slower. Note, however, that at least SafeSpring and CityCloud use a central Ceph storage cluster for the VM's boot disk, which wipes out node-local's storage advantage.)
* Bad, because the forwarder will fail if storage provider goes down. This is especially problematic for Exoscale, bare-metal and BYO-VMs.
* Bad, because the forwarder cannot monitor the storage provider (circular dependency).
* Bad, because setting right ownership requires init containers or [alpha features](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods).

### Use Local Persistent Volumes

* Bad, because the forwarder cannot be restarted on any node without manual action: "if a node becomes unhealthy, then the local volume becomes inaccessible by the pod. The pod using this volume is unable to run.".
* Bad, because the amount of forwarding depends on the node's local disk size.
* Bad, because buffered monitoring information is lost if the forwarder's node goes down.
* Good, because buffered monitoring information is preserved if the forwarder is redeployed.
* Good, because node-local storage is generally faster.
* Good, because the forwarder will survive failure of storage provider.
* Good, because the forwarder can monitor the storage provider (no circular dependency).
* Bad, because local persistent storage requires an additional configuration step.
* Bad, because setting right ownership requires init containers or [alpha features](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods).

### Use emptyDir

* Good, because the forwarder can be restarted on any node without manual action.
* Bad, because the amount of forwarding depends on the node's local disk size.
* Bad, because buffered monitoring information is lost if the forwarder's node goes down.
* Bad, because buffered monitoring information is lost if the forwarder is (not carefully enough) redeployed.
* Good, because node-local storage is generally faster.
* Good, because the forwarder will survive failure of storage provider.
* Good, because the forwarder can monitor the storage provider (no circular dependency).
* Good, because works out of the box.
* Good, because it integrates nicely with `securityContext`.

### Use hostPath

Similar to Local Persistent Volumes, but

* Worse, because if the forwarder is redeployed on a new node, buffering information may appear/disappear.
* Better, because it requires no extra storage provider configuration.

## Links

* [Prometheus Operator Storage](https://github.com/prometheus-operator/prometheus-operator/blob/master/Documentation/user-guides/storage.md)
