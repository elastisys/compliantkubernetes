# Capacity Management

Our users trust us -- the Compliant Kubernetes administrators -- to keep applications up and secure.
Keeping the application up means that there is sufficient capacity in the environment, both for headroom -- in case the application suddenly gets popular -- and resilience to Node failure.
Keeping the application secure means having sufficient capacity in the environment to allow rolling Node restarts -- as required for keeping the base OS up-to-date and secure -- without causing downtime.

## Upscaling

### When?

!!!note
    TBD; implementation in progress.

Compliant Kubernetes triggers a P2 alert when any capacity dimension is predicted to exceed 66% within 3 days.

That was very information dense, so let's break it down.

* **Why a P2 alert?** P2 alerts are events that need to be dealt with within a business day. Capacity can be easily predicted and added in advance. Excess capacity is cheaper than frustrated administrators. There is no need to disturb anyone's sleep.
* **What capacity dimensions?** Sum of CPU requests to CPU allocatable, sum of memory request to memory allocatable, host disk, PersistentVolumeClaim used to size, and Rook/Ceph used to size. Note that Compliant Kubernetes can be configured to [require resource requests](/user-guide/safeguards/#avoid-downtime-with-resource-requests) for all Pods.
* **Why 66%?** Most Kubernetes clusters will feature 3 Nodes (see discussion below about too many Nodes). Hence, 1 extra Node means 66% capacity.
* **Why within 3 days?** This should ensure sufficient time to act on the capacity shortage, without ruining anyone's weekend.

### How?

[Add a new Node](/operator-manual/troubleshooting/#node-seems-really-not-fine-i-want-a-new-one) of the same type as the other Nodes in the cluster.
If the cluster has 6 Nodes, consider consolidating to 3 Nodes of twice-the-size -- both in number of CPUs and memory -- if the infrastructure cost is reduced.
If you are about to double the number of Nodes, get in touch with application developers to ensure their application is not misbehaving, before upscaling.

## Downscaling

We hope that the applications we host will only grow in popularity and that downscaling is never needed.
Nevertheless, application developer trust us to keep infrastructure costs down, if their application hasn't gone viral -- yet!

### When?

The capacity of the environment should be regularly reviewed.

### How?

If any capacity dimension -- as defined above -- was below 33% for at least 3 days, then remove one Node at a time, until capacity is above 33%.
Make sure to drain and cordon the Node before decommissioning it.
If you are about to go below 3 Nodes, consider replacing the Nodes with 6 Nodes of half-the-size before downscaling.
If you are about to half the number of Nodes, get in touch with application developers to ensure their application is not misbehaving, before downscaling.
