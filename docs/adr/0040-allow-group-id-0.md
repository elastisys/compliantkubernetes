# Allow running containers with primary and supplementary group id 0

- Status: accepted
- Deciders: arch meeting
- Date: 2023-04-19

## Context and Problem Statement

Kubernetes has removed PodSecurityPolicy admission in version v1.25.
The replacement, Pod Security admission, does not even in its most restricted profile limit what primary group id (uninx `gid`) or supplementary group id's (unix `groups`) containers are allowed to run with. In terms of `securityContext` the following fields are not restricted:

- `fsGroup`
- `runAsGroup`
- `supplementaryGroups`

With our current Kubernetes installer, Kubespray, the default `restricted` PodSecurityPolicy does not allow using id 0 for any of the `securityContext` fields listed above.

Should we with the introduction of Pod Security admission follow the new standard of allowing group id 0, or should we continue to restrict it through some 3rd party admission webhook?

## Decision Drivers

- We want to maintain platform security.
- For user expectations, we want to make it easy to start with Compliant Kubernetes.

## Considered Options

1.  Allow group id 0 by default - default behavior of PSA.
1.  Keep current behavior and only allow group id 0 upon request.

## Decision Outcome

Chosen option: 1 - "Allow group id 0 by default - default behavior of PSA".

### Positive Consequences

- We follow upstream Kubernetes restricted pod security standards.
  With PodSecurityPolicy we use the one provided by Kubespray which has changed over time from first allowing group id 0 to now in its latest iteration not allowing it.
- Application Developers can run their containers inspired by the OpenShift pattern for supporting arbitrary user IDs etc.

### Negative Consequences

- It can be argued that in the event of an container escape vulnerability, our security is slightly weakened. However, a non-root user with group 0 is still not a privileged user.
