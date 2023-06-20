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

- a single Node failure (Node resilient); or
- a single Zone failure (Zone resilient).

Zone resilient environments are set up over three Zones, two active and one arbiter. The arbiter only runs some control-plane components (e.g., Kubernetes Data Plane, Ceph Mon), whereas the active Zones run both control-plane and data-plane components (e.g., Ceph OSD, Kubernetes data plane Nodes).

## Upscaling

### When?

Compliant Kubernetes triggers a P2 alert when any capacity dimension is predicted to exceed 66% (for Node resilient) or 50% (for Zone resilient) within 3 days.

That was very information dense, so let's break it down.

* **Why a P2 alert?** P2 alerts are events that need to be dealt with within a business day. Capacity can be easily predicted and added in advance. Excess capacity is cheaper than frustrated administrators. There is no need to disturb anyone's sleep.
* **What capacity dimensions?**
    * CPU:
        * sum of (Kubernetes) CPU requests to CPU allocatable;
        * sum of CPU used to CPU allocatable;
        * load average: since this is not a percentage, scale up when above 3;
    * Memory:
        * sum of (Kubernetes) memory request to memory allocatable;
        * sum of memory [non-available](https://superuser.com/questions/980820/what-is-the-difference-between-memfree-and-memavailable-in-proc-meminfo) to memory total;
    * Storage:
        * host disk used to size;
        * PersistentVolumeClaim used to size;
        * Rook/Ceph OSD used to size;
* **Why 66% or 50%?** Most Node-resilient Kubernetes clusters will feature 3 Nodes (see discussion below about too many Nodes). Hence, 1 extra Node means 66% capacity. Zone-resilient environments need 50% extra capacity, so that each active Zone can take over the load of the other active Zone.
* **Why within 3 days?** This should ensure sufficient time to act on the capacity shortage, without ruining anyone's weekend.

!!!note
    Compliant Kubernetes can be configured to [require resource requests](../user-guide/safeguards/enforce-resources.md) for all Pods.

!!!important
    Nodes dedicated for data services, such as PostgreSQL, are excluded from Kubernetes requests to allocatable calculation.

### How?

[Add a new Node](../operator-manual/troubleshooting.md#node-seems-really-not-fine-i-want-a-new-one) of the same type as the other Nodes in the cluster.

If the cluster has 6 Nodes, consider consolidating to 3 Nodes of twice-the-size -- in number of CPUs or memory or both -- if the infrastructure cost is reduced.
Before doing this, get in touch with Application Developers to ensure they don't have Kubernetes scheduling constraints that would cause issues on the consolidated environment.

If you are about to double the number of Nodes, get in touch with Application Developers to ensure their application is not misbehaving, before upscaling.

### Optimization

If the cluster has at least 5 Nodes, consider reducing the watermark to 80% to reduce extra capacity.

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

If any capacity dimension -- as defined above -- was below 33% for at least 3 days, then remove one Node at a time, until capacity is above 33%.
Make sure to drain and cordon the Node before decommissioning it.

If you are about to go below 3 Nodes, consider replacing the Nodes with 6 Nodes of half-the-size before downscaling.
Before doing this, get in touch with Application Developers to ensure they don't have Kubernetes scheduling constraints that would  cause issues on the consolidated environment.

If you are about to half the number of Nodes, get in touch with Application Developers to ensure their application is not misbehaving, before downscaling.

### Optimization

Removing capacity is more dangerous than having extra capacity, when it comes to application uptime.
Furthermore, we need to avoid oscillations: Removing capacity to only add it back a few days later is no fun for the administrator.
Therefore, downscaling should only be performed periodically, whereas upscaling should be performed as soon as predictions show it is needed.
