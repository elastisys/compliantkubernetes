# Filter by cluster label then data source

- Status: accepted
- Deciders: arch meeting
- Date: 2021-01-27

Technical Story: <https://github.com/elastisys/compliantkubernetes-apps/issues/742>

## Context and Problem Statement

Compliant Kubernetes allows multiple Workload Clusters to be connected to a single Management Cluster.
This allows the metrics of multiple Workload Clusters to be inspected via the same dashboards.

How should we organise metrics to allow users and admins to select for which clusters they want to see metrics?

## Decision Drivers

- We want to be able to see metrics for a single cluster, for multiple cluster, and even for all clusters.
- We want to be able to reuse upstream dashboards, and [some are missing filters](https://github.com/prometheus-community/helm-charts/blob/main/charts/kube-prometheus-stack/templates/grafana/dashboards-1.14/alertmanager-overview.yaml) for the `cluster` variable.
- We want to stay flexible.

## Considered Options

- Use only the `cluster` label and expose a single data source.
- Expose multiple data sources and ignore the `cluster` label.
- Filter primarily by `cluster` label, but allow filtering by data source.
- Filter primarily by data source, but allow filtering by `cluster` label.

## Decision Outcome

Chosen option:
"Filter primarily by `cluster` label, but allow filtering by data source",
because it fulfills the all decision drivers with little complexity.

[Prom-label-enforcer](https://github.com/prometheus-community/prom-label-proxy) can be used to create multiple data sources from a single data store, discriminating by `cluster` label. To simplify Thanos configuration, we can also discriminate based on `tenant_id`, which will always contain the same value as `cluster`.

In general, we will aim to fix dashboards missing the `cluster` variable upstream. However, by also providing filtering based on data source, we facilitate our users to reuse their dashboards, which might not be cluster-aware.

### Positive Consequences

- We support both dashboards with `cluster` filter and without
- We can enforce metrics multi-tenancy, i.e., map Grafana users/orgs to datasources, to filter some metrics out.

### Negative Consequences

- [Minor] We need to configure data sources in `sc-config.yaml`
    - For example, if we forget to add the name of a Workload Cluster, the data source will be missing, but filtering based on `cluster` label is still possible.
- [Minor] Label enforcer uses a bit of resources.
    - However, we already saved a lot by migrating from InfluxDB to Thanos, so we can afford go back a bit.
