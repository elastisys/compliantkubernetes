# Enforce TTL on Jobs

- Status: accepted
- Deciders: arch meeting
- Date: 2023-03-30

## Context and Problem Statement

Lingering finished Jobs are annoying, put unnecessary pressure on the API server, and causes bloat metrics.
I fail to see any point of having the possibility of keeping Jobs in Kubernetes around forever.
Others agree with me and since k8s 1.23 TTL on Jobs entered a stable API state.

So, should we enforce the usage of TTL on Jobs?

## Decision Drivers

- We want to maintain platform security and stability.
- We want to find a solution which is scalable and minimizes MSE burden.
- We want to best serve the Application Developers.
- We want to make the Platform Administrator life easier.

## Considered Options

1. Do nothing
1. Enforce TTL via Gatekeeper, aka reject if not set in Job spec.
1. Enforce TTL via Gatekeeper mutation, aka update Job spec if not set.
1. Enforce TTL via Gatekeeper mutation, aka update Job spec if not set. and lower the value if set too high.

## Decision Outcome

Chosen option: 3 - "Enforce TTL via Gatekeeper mutation, aka update Job spec if not set.
We decided for a default Job TTL of 7 days, as this is a good compromise between being able to inspect the Pod -- e.g., check exit status and logs -- and not keeping Pods for too long.

### Positive Consequences

- Application Developers don't need to worry about setting any value
- We don't have to worry about setting any value for our jobs (assuming we will run Gatekeeper in SC, in the meantime we can just update our Job specs in Apps)
- There won't be any lingering Jobs in Kubernetes (assuming that no bad finalizers are set)
- TTL of Jobs will be visible in out IO site and possibly stated in our ToS

### Negative Consequences

- Some Application Developers might not agree with our set TTL (not likely though IMO)
