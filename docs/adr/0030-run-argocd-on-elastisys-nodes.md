# Run ArgoCD on the Elastisys nodes

* Status: accepted
* Deciders: arch meeting
* Date: 2023-01-26

## Context and Problem Statement

We run additional services in the workload cluster on dedicated nodes, currently databases (PostgreSQL), in-memory caches (Redis), message queues (RabbitMQ) and distributed tracing (Jaeger).
Where should we run ArgoCD?

## Decision Drivers

* We want to deliver a stable and secure platform.
* We want to deliver an affordable adittional managed service and avoid resource waste.
* ArgoCD has a small footprint, e.g., 200m CPU and 0.5GB RAM for one of our largest deployments.
* Want want to keep application Nodes "light", so the application team knows what capacity is available for their application.

## Considered Options

* Spread ArgoCD services on application Nodes.
* Run ArgoCD services on dedicated Nodes.
* Run ArgoCD services on Elastisys Nodes, and scale up the nodes.

## Decision Outcome

Chosen option: "Run ArgoCD services on Elastisys Nodes, and scale up the nodes.",  because it improves the stability and security of the platform, avoids resource waste and makes the ArgoCD service more affordable to the application developers.

Scale up the Elastisys Nodes to 4C8GB before installing managed ArgoCD.

### Positive Consequences

* The ArgoCD service infrastructure footprint is lower than when using dedicated nodes, due to less per-Node overhead (fluentd, Falco)..
* Security and stability of additional services is somewhat improved, e.g., SystemOOM due to an application won't impact ArgoCD

### Negative Consequences

* We need to scale up the Elastisys nodes to 4C8GB
* We are sharing the Elastisys nodes resources with the other Elastisys platform components, e.g., Ingress Controller.

## Recommendations to Platform Administrators

Specifically, use the following Node labels

```
elastisys.io/node-type=elastisys
```

and taint:

```
elastisys.io/node-type=elastisys:NoSchedule
```

Remember to also add tolerations and Node affinity to all affected Pods.

## Links

* [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
* [Well-Known Labels, Annotations and Taints](https://kubernetes.io/docs/reference/labels-annotations-taints/)
* [Kubespray `node_labels` and `node_taints`](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/vars.md#other-service-variables)
