# Application developer privilege elevation

- Status: accepted
- Deciders: Olle, Christian
- Date: 2023-04-11

## Context and Problem Statement

Kubernetes comes with a set of default ClusterRoles that are meant to be user-facing.
One such ClusterRole is `admin`.
It is meant to be granted on a per namespace basis, and it grants read and write permissions on _most_ of the default namespaced resources.
Welkin grants the `admin` ClusterRole in the appropriate namespaces to application developers.
The `admin` ClusterRole is elevated with additional privileges through the use of the ClusterRole aggregation feature.
Application developers are granted additional permissions for some cluster-wide resources through the use of extra ClusterRoles and clusterRoleBindings.

At times, application developers request access to additional resources not yet granted by Welkin, both concerning namespaced and cluster-scoped resources.
How should we manage such requests and when should the core permissions granted by Welkin be elevated?

## Decision Drivers

- We want to maintain a stable and secure platform.
- We want to adhere to our managed service customer needs.

## Considered Options

1. Never elevate privileges for application developers.
    - Application developer privileges are strictly tied to the running version of Welkin.
1. Elevate privileges on a case-by-case basis
    - Application developers can request additional privileges.
      The request can be accepted or rejected by the Platform administrators.
      If accepted, the elevated privileges should, if possible, be implemented into the core platform.

## Decision Outcome

- (2) Elevate privileges on a case-by-case basis

### Positive Consequences

- Application developer is happy if the Platform administrators accept the request.

### Negative Consequences

- Could potentially lead to feature sprawl unless the additional privileges are implemented into to the core platform.
