---
tags:
  - BSI IT-Grundschutz APP.4.4.A14
  - NIST SP 800-171 3.13.3
---
# Use Dedicated Nodes for Additional Services

- Status: accepted
- Deciders: arch meeting
- Date: 2022-03-03
- Updated: 2023-01-12

## Context and Problem Statement

We run additional services in the Workload Cluster, currently databases (PostgreSQL), in-memory caches (Redis), message queues (RabbitMQ) and distributed tracing (Jaeger).

On what Nodes should they run?

## Decision Drivers

- We want to deliver a stable and secure platform.

## Considered Options

- Spread additional services on application Nodes.
- Run additional services on dedicated Nodes.

## Decision Outcome

Chosen option: "run additional service on dedicated Nodes", because it improves the stability and security of the platform.

Specifically, use the following Node labels

```text
elastisys.io/node-type=postgresql
elastisys.io/node-type=redis
elastisys.io/node-type=rabbitmq
elastisys.io/node-type=jaegertracing
```

and taints:

```text
elastisys.io/node-type=postgresql:NoSchedule
elastisys.io/node-type=redis:NoSchedule
elastisys.io/node-type=rabbitmq:NoSchedule
elastisys.io/node-type=jaegertracing:NoSchedule
```

!!!important

    Dedicated Nodes still contain some Workload Cluster components for logging, monitoring, intrusion detection, etc., so not all their capacity is available to the service.

### Positive Consequences

- Performance is more predictable.
- Responsibility is more clearly separated, i.e., application Nodes vs. additional services Nodes.
- Security and stability of additional services is somewhat improved, e.g., SystemOOM due to an application won't impact PostgreSQL.

### Negative Consequences

- Forces additional services to be sized based on available Node sizes. While some commonality exists, Node sizes are specific to each infrastructure provider.
- Latency is somewhat increased. This is an issue mostly for Redis, as other services are a bit more latency tolerant.

## Recommendations to Platform Administrators

For better application performance and security, run system Deployments and StatefulSets -- such as Ingress Controllers, Prometheus, Velero, Gatekeeper and Starboard -- onto dedicated Nodes.

Specifically, use the following Node label:

```text
elastisys.io/node-type=elastisys
```

and taint:

```text
elastisys.io/node-type=elastisys:NoSchedule
```

Remember to also add tolerations and Node affinity to all affected Pods.

## Links

- [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
- [Well-Known Labels, Annotations and Taints](https://kubernetes.io/docs/reference/labels-annotations-taints/)
- [Kubespray `node_labels` and `node_taints`](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/ansible/vars.md#other-service-variables)
