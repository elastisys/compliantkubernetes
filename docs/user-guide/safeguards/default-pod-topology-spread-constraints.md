---
tags:
- ISO 27001 A.17.2.1 Availability of information processing facilities
---
<!--
Note to contributors: Aim for the following format.

* Title: Highlight benefit to Application Developer
* Context
* Problem
* Solution
* Error
* Resolution
-->

# Default Pod Topology Spread Constraints

!!!important
    * This safeguard is enabled by default as since [Compliant Kubernetes Kubespray v2.23.0-ck8s2](../../release-notes/kubespray.md#v2230-ck8s2).

## Problem

A healthy security posture requires you to ensure your application tolerates failures.
This involves two things:

1. Running your application replicated with at least two Pods. Specifically, this implies that your Deployment has `.spec.replicas` of at least 2.
2. Ensuring that the Pods are spread across failure domains. The latter was usually achieved by setting correct `topologySpreadConstraints`.

In Compliant Kubernetes, dealing with (1) above is still the Application Developer's responsibility.

However, with Compliant Kubernetes, you don't need to deal with (2).

## Solution

Compliant Kubernetes comes with strong cluster-level default `topologySpreadConstraints`.

### Single-Zone Clusters

If your Cluster is hosted on a single zone, then your administrator will have configured the following default `topologySpreadConstraints`:

```yaml
- maxSkew: 1
  topologyKey: kubernetes.io/hostname
  whenUnsatisfiable: ScheduleAnyway
```

This means that the Kubernetes scheduler will try to spread Pods of the same Deployment across Nodes.
If this is not possible, it will still try to run the Pod on any Node.

This implies that your application is more likely to tolerate a Node going down.

### Multi-Zone Clusters

If your Cluster is hosted on at least three zones in the same region, then your administrator will have configured the following default `topologySpreadConstraints`:

```yaml
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: ScheduleAnyway
```

This means that the Kubernetes scheduler will try to spread Pods of the same Deployment across zones.
If this is not possible, it will still try to run the Pod on any zone.

This implies that your application is more likely to tolerate a zone going down.

## What if I need to customize my `topologySpreadConstraints`?

Simply override this in your application Helm Chart.
The [user demo](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L84) provides an example on how to achieve this.

## Further Reading

* [Cluster-level default constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/#cluster-level-default-constraints)
