# Use local-volume-provisioner for Managed Services that requires high-speed disks.

* Status: accepted
* Deciders: arch meeting
* Date: 2022-11-10

## Context and Problem Statement

After performing several storage load testing and PostgreSQL load testing and benchmarking we have discovered that the local storage is significantly faster than network storage.
We have one use case where the disk have proven to be too slow for a PostgreSQL database and the performance was not as expected.
How should we expose local storage to Managed Services?

## Decision Drivers

* We want to best serve the application developer needs.
* We want to offer fast performant Managed Services.
* We want to find a solution which is scalable and minimizes administrator burden.
* We want to find a future-proof solution, which exposes local disks to any application.

## Considered Options

* Use the fastest network storage with dedicated IOPS.
* Use local storage with [local-volume-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner).
* Use local storage with [local-path-provisioner](https://github.com/rancher/local-path-provisioner)
* Use [hostPath](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath)
* Use [local](https://kubernetes.io/docs/concepts/storage/volumes/#local)

## Decision Outcome

Chosen option: Use local storage with local-volume-provisioner and move the code within the kubespray repo.

### Positive Consequences

* Services using the local storage are performing better.
* We are able to provide a PostgreSQL service that meet the high performance requirements.

### Negative Consequences

* Scaling the storage becomes harder as it will involve replacing the nodes.
* We are limited by the size of the volumes that are available within the cloud provider offering.

## Recommendation to Operators

When using the local-volume-provisioner please create dedicated partitions and make sure to reserve enough space for the boot partition. Failing to do so can lead to entire disc to become full and the node will become unresponsive and crash.

## Links

* [local-volume-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/tree/v2.5.0)
* [local-path-provisioner](https://github.com/rancher/local-path-provisioner)
* [hostPath](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath)
* [local](https://kubernetes.io/docs/concepts/storage/volumes/#local)
