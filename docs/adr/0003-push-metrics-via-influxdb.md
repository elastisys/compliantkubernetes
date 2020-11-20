# Push Metrics via InfluxDB

* Status: accepted
* Deciders: Johan, Cristian, Viktor, Emil, Olle, Fredrik
* Date: 2020-11-19

## Context and Problem Statement

We want to support workload multi-tenancy, i.e., one service cluster -- hosting the tamper-proof logging environment -- and multiple workload clusters. Currently, the service cluster exposes two end-points for workload clusters:

* Dex, for authentication;
* Elastisearch, for pushing logs (append-only).

Currently, the service cluster pulls metrics from the workload cluster. This makes it difficult to have multiple workload clusters connected to the same service cluster.

## Decision Drivers

* We want to support workload multi-tenancy.
* We want to untangle the life-cycle of the service cluster and workload cluster.
* The service cluster acts as a tamper-proof logging environment, hence it should be difficult to tamper with metrics from the workload cluster.

## Considered Options

1. Service cluster exposes InfluxDB; workload cluster pushes metrics into InfluxDB.
2. Migrate from InfluxDB to [Thanos](https://thanos.io/)
3. Migrate from InfluxDB to [Cortex](https://github.com/cortexproject/cortex)

## Decision Outcome

We chose to push metrics from the workload cluster to the service cluster via InfluxDB, because it involves the least amount of effort and is sufficient for the current use-cases that we want to support. InfluxDB supports a writer role, which makes overwriting metrics difficult -- unfortunately, not impossible.

### Positive Consequences

* All of `*.$opsDomain` can point to the service cluster workers -- optionally fronted by a load-balancer -- which considerably simplifies setup.
* Multiple workload clusters can push metrics to the service cluster, which paves the path to workload multi-tenancy.
* The service cluster can be set up first, followed by one-or-more workload clusters.
* Workload clusters become more "cattle"-ish.

### Negative Consequences

* Existing Compliant Kubernetes clusters will need some manual migration steps, in particular changing the `prometheus.$opsDomain` DNS entry.
* The service cluster exposes yet another endpoint, which should only be available to workload clusters and not the Internet. HTTP authentication (over HTTPS) feels sufficient for now, but we need a follow-up decision on how to add another layer of protection to these endpoints.
* The workload clusters will have to properly label their metrics.
* Although not easy, metrics can be overwritten from the workload cluster. We will improve on this when (a) demand for closing this risk increases, (b) we re-evaluate long-term metrics storage.

## Pros and Cons of the Options

Both Thanos and Cortex seems worthy projects to replace InfluxDB. At the time of this writing, they were both having CNCF Incubating status. The two projects feature a healthy collaboration and are likely to merge in the future.

However, right now, migrating away from InfluxDB feels like it adds more cost than benefits. We will reevaluate this decision when InfluxDB is no longer sufficient for our needs.
