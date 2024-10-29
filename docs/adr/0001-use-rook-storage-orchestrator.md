# Use Rook for Storage Orchestrator

- Status: accepted
- Deciders: Cristian Klein, Lars Larsson, Pradyumna Kashyap, Daniel Harr, Viktor Forsberg, Fredrik Liv
- Date: 2020-11-16

## Context and Problem Statement

Welkin has the vision to reduce the compliance burden on multiple clouds ("Multi-cloud. Open source. Compliant."). Many of the Infrastructure Providers we target do not have a storage provider or do not have a storage provider that integrates with Kubernetes. How should we support PersistentVolumeClaims in such cases?

## Decision Drivers

- Storage Orchestrator needs to be popular and well maintained, so that developer can focus on adding value on top of Kubernetes clusters.
- Storage Orchestrator needs to be easy to set up, easy to operate and battle-tested, so on-call administrators are not constantly woken up.
- Storage Orchestrator needs to have reasonable performance. (A local storage provider can deal with high-performance use-cases.)

## Considered Options

- [Rook](https://rook.io)
- [GlusterFS](https://www.gluster.org/)
- [Longhorn](https://longhorn.io/)
- NFS Storage Provider

## Decision Outcome

Chosen option: "Rook", because it is CNCF graduated, hence it is most likely to drive development and adoption long-term. Prady tested it and showed it was easy to use. It supports Ceph as a backend, making it battle-tested. It has reasonable performance.

### Positive Consequences

- We no longer need to worry about Infrastructure Provider without native storage.

### Negative Consequences

- We need to deprecate our NFS storage provider.
- Some manual steps are required to set up partitions for Rook. These will be automated when the burden justifies it.

## Pros and Cons of the Options <!-- optional -->

### Longhorn

- Good, because it is a CNCF project.
- Good, because it is well integrated with Kubernetes.
- Bad, because it is not the most mature CNCF project in the storage class.
- Bad, because it was not easy to set up.

### GlusterFS

- Good, because it is battle-tested.
- Bad, because it is not as well integrated with Kubernetes as other projects.
- Bad, because it is not a CNCF project (driven by Red Hat).

### NFS Storage Provider

- Good, because we used it before and we have experience.
- Bad, because it is a non-redundant, snowflake, brittle solution.
