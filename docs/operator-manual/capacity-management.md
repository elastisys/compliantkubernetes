---
tags:
  - ISO 27001 A.12.1.3 Capacity Management
---

# Capacity Management

Our users trust us -- the Compliant Kubernetes administrators -- to keep applications up and secure.
Keeping the application up means that there is sufficient capacity in the environment, both for headroom -- in case the application suddenly gets popular -- and resilience to Node or Zone failure.
Keeping the application secure means having sufficient capacity in the environment to allow rolling Node restarts -- as required for keeping the base OS up-to-date and secure -- without causing downtime.

## Types of Failure

Compliant Kubernetes environments are set up to withstand either:

- a single Node failure per Node Group (Node resilient); or
- a single Zone failure (Zone resilient).

Node resilient environments are set up with enough resources allocated to withstand a single Node failure on a per Node Group basis (e.g., control-plane, worker). In other words, the environment should be able to withstand a control-plane Node and worker Node failing simultaneously.

Zone resilient environments are set up over three Zones. All components that have HA capabilities will be spread across all three Zones, such that the environment can withstand a complete Zone failure (e.g., Kubernetes Control Plane, Ceph Mon, Opensearch etc.).

## Defining Node Groups

Node Groups are meant to represent a logical grouping of Nodes, for example the worker Nodes in a Cluster. In practice, these Node Groups are defined by labeling all Nodes with the name of the Node Group that they belong to:

```bash
kubectl label node <node-name> elastisys.io/node-group=<node-group>
```

These labels are required for the monitoring and alerting described on this page to function.

## Upscaling

Compliant Kubernetes uses a combination of alerts for both individual Nodes as well as Node Groups, which are also monitored and visualized in a Grafana dashboard.

### When?

Compliant Kubernetes triggers a P1 alert when:

- The average CPU usage for a Node or Node Group, over one hour, is above 95%.
- The average memory usage for a Node or Node Group, over one hour, is above 85%.

- **Why a P1 alert?** P1 alerts are events that need immediate attention, which makes them suitable for scenarios with a higher usage threshold over a shorter timespan. If the alert is triggered for a single Node, the administrator can attempt to redistribute the workload more evenly across the Node Group. If the alert is triggered for a Node Group, that Node Group needs to be scaled up.

Compliant Kubernetes triggers a P2 alert when:

- The average CPU or memory usage for a Node Group, over 24 hours, is above 75%.

- **Why a P2 alert?** P2 alerts are events that need to be dealt with within a business day. This makes them suitable for scenarios with a lower usage threshold over a longer timespan, giving administrators enough time to take action. Excess capacity is cheaper than frustrated administrators. There is no need to disturb anyone's sleep.

### Metrics

- **Why memory and CPU usage?**
  - These are the resource metrics that are directly tied to the Nodes, and represent how much of the resource is actually used and how much is available. If usage gets close to 100% of capacity, it will start impacting applications.
  - That isn't to say that these are the only capacity metrics to take into account. Other metrics are useful too, but are often not cause for an immediate scale-up and instead require further investigation. These other metrics include:
    - CPU:
      - sum of (Kubernetes) CPU requests to CPU allocatable;
      - load average;
    - Memory:
      - sum of (Kubernetes) memory request to memory allocatable;
    - Storage:
      - host disk used to size;
      - PersistentVolumeClaim used to size;
      - Rook/Ceph OSD used to size;

!!!note

    Compliant Kubernetes can be configured to [require resource requests](../user-guide/safeguards/enforce-resources.md) for all Pods.

!!!important

    Nodes dedicated for data services, such as PostgreSQL, are excluded from Kubernetes requests to allocatable calculation.

### How?

[Add a new Node](../operator-manual/troubleshooting.md#node-seems-really-not-fine-i-want-a-new-one) of the same type as the other Nodes in the cluster.

If the cluster has 6 Nodes, consider consolidating to 3 Nodes of twice-the-size -- in number of CPUs or memory or both -- if the infrastructure cost is reduced.
Before doing this, get in touch with Application Developers to ensure they don't have Kubernetes scheduling constraints that would cause issues on the consolidated environment.

If you are about to double the number of Nodes, get in touch with Application Developers to ensure their application is not misbehaving, before upscaling.

## Downscaling

We hope that the applications we host will only grow in popularity and that downscaling is never needed.
Nevertheless, Application Developer trust us to keep infrastructure costs down, if their application hasn't gone viral -- yet!

### When?

The capacity of the environment should be regularly reviewed, for example, after a maintenance window.

!!!important

    Downscaling may put application uptime at risk. Therefore, be conservative when downscaling.

    Before downscaling you should:

    * Evaluate the capacity trends in last 3 to 6 months and take decision based on that. Notice that capacity usage may be smaller during weekends, at the beginning or end of the month, during vacation periods, etc.
    * Ask the user if the reduction in capacity usage is a real trend, and not just sporadic due to quiet periods or vacation periods. E.g., an EdTech app won't be used as intensively during school holidays.
    * Ask the user if they foresee any increase in capacity due to new app releases or new apps additions or something that will require more resources.

### How?

If a decision has been made to downscale, make sure to drain and cordon the Node before decommissioning it.

If you are about to go below 3 Nodes, consider replacing the Nodes with 6 Nodes of half-the-size before downscaling.
Before doing this, get in touch with Application Developers to ensure they don't have Kubernetes scheduling constraints that would cause issues on the consolidated environment.

If you are about to half the number of Nodes, get in touch with Application Developers to ensure their application is not misbehaving, before downscaling.

### Optimization

Removing capacity is more dangerous than having extra capacity, when it comes to application uptime.
Furthermore, we need to avoid oscillations: Removing capacity to only add it back a few days later is no fun for the administrator.
Therefore, downscaling should only be performed periodically, whereas upscaling should be performed as soon as predictions show it is needed.
