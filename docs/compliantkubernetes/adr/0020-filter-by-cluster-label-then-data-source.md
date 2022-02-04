# Filter by cluster label then data source

* Status: accepted
* Deciders: arch meeting
* Date: 2021-01-27

Technical Story: https://github.com/elastisys/compliantkubernetes-apps/issues/742

## Context and Problem Statement

Compliant Kubernetes allows multiple workload clusters to be connected to a single service cluster.
This allows the metrics of multiple workload clusters to be inspected via the same dashboards.

How should we organise metrics to allow users and admins to select for which clusters they want to see metrics?

## Decision Drivers

* We want to be able to see metrics for a single cluster, for multiple cluster, and even for all clusters.
* We want to be able to reuse upstream dashboards, and some are missing filters for the `cluster` variable.
* We want to stay flexible.

## Considered Options

* Use only the `cluster` label and expose a single data source.
* Expose multiple data sources and ignore the `cluster` label.
* Filter primarily by `cluster` label, but allow filtering by data source.
* Filter primarily by data source, but allow filtering by `cluster` label.

## Decision Outcome

Chosen option:
"Filter primarily by `cluster` label, but allow filtering by data source",
because it fulfills the all decision drivers with little complexity.

[Prom-label-enforcer](https://github.com/prometheus-community/prom-label-proxy) can be used to create multiple data sources from a single data store, discriminating by `cluster` label.

### Positive Consequences

* We support both dashboards with `cluster` filter and without
* We can enforce metrics multi-tenancy, i.e., map Grafana users/orgs to datasources, to filter some metrics out.

### Negative Consequences

* [Minor] We need to configure data sources in `sc-config.yaml`
* [Minor] Label enforcer uses a bit of resources.


<!--

CK Pending questions:

- Why do we use `tenant_id` in the label enforcer? https://github.com/elastisys/compliantkubernetes-apps/blob/27f336afb8b3570f35516dfb859c453694d7949a/helmfile/values/grafana-label-enforcer.yaml.gotmpl#L4
- Which upstream dashboards don't support filtering by cluster label? https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack/templates/grafana/dashboards-1.14

-->
