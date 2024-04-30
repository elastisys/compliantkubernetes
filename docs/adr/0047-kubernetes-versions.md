# When to upgrade to new Kubernetes versions

- Status: Accepted
- Deciders: Architecture meeting
- Date: 2024-03-07

## Context and Problem Statement

With the addition of Cluster API we need to take decisions on when we want to release a new minor version of Kubernetes.
Cluster API is a fast moving project, and it would allow us to support new minor versions of Kubernetes almost directly after they've been released.
However immediately upgrading to a new minor version could potentially introduce bugs or regressions not yet found and patched upstream.

For Kubespray we have not needed to take the same decision, as we follow when Kubespray releases a new minor version, which then includes a new minor version of Kubernetes.
Kubespray is not as fast moving, and when it releases a new minor version it includes a new minor version of Kubernetes that is already a few patches in.
This makes the potential of it introducing bugs and regressions much smaller as they should have been found and patched upstream at that point.

But what should be our strategy be to upgrade Kubernetes with Cluster API?

## Decision Drivers <!-- optional -->

- We want to ensure the Kubernetes version is up to date
- We want to ensure the Kubernetes version is stable
- We want to reduce maintainer effort on keeping Cluster API and Kubespray equivalent.

## Considered Options

1.  Upgrade as soon as there is a new minor version
1.  Upgrade when Kubespray upgrades

## Decision Outcome

Chosen option: option 2, because we want to keep our Kubernetes installers in the same pace when it comes to new Kubernetes minor versions, and then we know that this version will be more tested and patched upstream.

### Positive Consequences <!-- optional -->

- Ensures our Kubernetes version is more stable
- Reduces our maintainer effort as we keep Cluster API and Kubespray equivalent.

### Negative Consequences <!-- optional -->

- Slower adoption of new versions in Cluster API
  - Mitigator 1: rework patch process to accelerate the release of new patch versions
  - Mitigator 2: keep main branch of Cluster API aligned with latest minor version

## Pros and Cons of the Options <!-- optional -->

### Option 1: _Upgrade as soon as there is a new minor version_

- Good, because Cluster API will be up to date
- Bad, because new minor Kubernetes versions may introduce bugs and regressions as it has not had the time to be tested by the community at large
- Bad, because we get a version skew between Cluster API and Kubespray

### Option 2 - _Upgrade when Kubespray upgrades_

- Bad, because Cluster API will not be fully up to date
  - Mitigator 1: rework patch process to accelerate the release of new patch versions
  - Mitigator 2: keep main branch of Cluster API aligned with latest minor version
- Good, because new minor Kubernetes versions will be more tested by the community at large
- Good, because we do not get a version skew between Cluster API and Kubespray
