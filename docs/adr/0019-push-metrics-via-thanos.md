# Push Metrics via Thanos

* Status: accepted
* Deciders: arch meeting
* Date: 2022-01-20

## Context and Problem Statement

Currently, the service cluster exposes several end-points for workload clusters:

* Dex, for authentication;
* OpenSearch, for pushing logs (append-only);
* InfluxDB, for pusing metrics;
* Harbor, for pulling container images.

InfluxDB has served us really well over the years. However, as we enter a new era of growth, it no longer satisfies our needs. In particular:

* It is not community-driven (see [ADR-0015 We believe in community-driven open source](0015-we-believe-in-community-driven-open-source)).
* The open-source version cannot be run replicated, hence it is a single point of failure.
* It is rather capacity hungry, eating as much as 2 CPUs and 15 Gi in a standard package environment.
* It is unsuitable for long-term metrics storage, which we need -- among others -- for proper capacity management.

We decided to [migrate from InfluxDB to Thanos](https://github.com/elastisys/compliantkubernetes/commit/61ddf81430dc542cf0bed96708a90f3b63ff0ed2), which can both push and pull metrics.

Shall we push or pull metrics using Thanos?

## Decision Drivers

* We want to support multiple workload clusters.
* We want to untangle the life-cycle of the service cluster and workload cluster.
* The service cluster acts as a tamper-proof logging environment, hence it should be difficult to tamper with metrics from the workload cluster.

## Considered Options

1. Push metrics from workload cluster to service cluster.
1. Pull metrics from workload cluster to service cluster.

## Decision Outcome

We chose to push metrics from the workload cluster to the service cluster via
via [Thanos Receive](https://thanos.io/tip/components/receive.md/),
because it keeps the "direction" of metrics flow.
Hence, we keep support for multiple workload clusters without any changes.

At the time of this writing, pulling metrics via [Thanos sidecar](https://thanos.io/tip/thanos/quick-tutorial.md/#components) seems to be the preferred way to deploy Thanos. We will monitor the ecosystem and our needs, and -- if needed -- move to pulling metrics.

At any rate, even if we end up with Thanos Sidecar, migrating in two steps -- first from InfluxDB to Thanos Receive, then to Thanos Sidecar -- feels less risky.

### Positive Consequences

* All of `*.$opsDomain` can point to the service cluster workers -- optionally fronted by a load-balancer -- which considerably simplifies setup.
* Multiple workload clusters can push metrics to the service cluster, which paves the path to workload multi-tenancy.
* The service cluster can be set up first, followed by one-or-more workload clusters.
* Workload clusters become more "cattle"-ish.

### Negative Consequences

* Metrics are less protected than in a pull architecture. E.g., compromising the workload cluster can easier be used to mount an attack against long-term metrics storage.
