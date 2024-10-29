# Use Probe to Measure Uptime of Internal Welkin Services

- Status: accepted
- Deciders: Cristian, Lucian, Ravi
- Date: 2021-11-25

## Context and Problem Statement

We need to measure uptime for at least two reasons:

1. To serve as feedback on what needs to be improved next.
1. To demonstrate compliance with our SLAs.

How exactly should we measure uptime?

## Decision Drivers

- We want to reduce tools sprawl.
- We want to be mindful about capacity and infrastructure costs.
- We want to measure uptime as observed by a consumer -- i.e., application or user -- taking into account business continuity measures, such as redundancy, fail-over time, etc.

## Considered Options

- [Blackbox exporter](https://github.com/prometheus/blackbox_exporter)
- [kubelet prober metrics](https://stackoverflow.com/questions/62736899/how-to-set-up-an-alert-when-liveness-readiness-probe-fails-in-kubernetes)
- [Prometheus Operator Probe](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#probespec), which essentially wraps the Blackbox exporter in a `Probe` CustomResource.

## Decision Outcome

Chosen option: "use Probe for measuring uptime of internal Welkin services", because it measures uptime as observed by a consumer. Although this requires a bit of extra capacity for running Blackbox, the costs are worth the benefits.

Instead of configuring Blackbox directly, `Probe` is a cleaner abstraction provided by the Prometheus Operator.

The following is an example for a Probe:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: Probe
metadata:
  name: google-is-up
  labels:
    probe: google
    release: kube-prometheus-stack
spec:
  interval: 60s
  module: http_2xx
  prober:
    url: blackbox-prometheus-blackbox-exporter.monitoring.svc.cluster.local:9115
  targets:
    staticConfig:
      static:
        - https://www.google.com
```

This will generate a metric as follows: `probe_success{cluster="ckdemo-wc", instance="https://www.google.com", job="probe/demo1/google-is-up", namespace="demo1"}`.

### Positive Consequences

- We measure uptime as observed by a consumer.
- Increasing redundancy, reducing failure time, etc. will contribute positively to our uptime, as desired.

### Negative Consequences

- We don't currently run Blackbox in the Workload Cluster, so we'll need a bit of extra capacity.

## Recommendations to Platform Administrators

Blackbox should only be used for measuring uptime of internal services, i.e., those that are only exposed within the Kubernetes cluster. Examples include additional services, such as PostgreSQL, Redis and RabbitMQ.

For external endpoints -- specifically, Dex, Grafana, Kibana, Harbor and Ingress Controllers -- prefer using an external uptime service which integrates with an On-Call Management Tool, e.g., [Uptime Cloud Monitor Integration for Opsgenie](https://docs.opsgenie.com/v1.0/docs/copperegg-integration).

External uptime measurement should achieve the similar effect as the commands below:

```console
curl --head https://dex.$DOMAIN/healthz
curl --include https://harbor.$DOMAIN/api/v2.0/health
curl --head https://grafana.$DOMAIN/healthz
curl --head https://kibana.$DOMAIN/api/status

curl --head some-domain.$DOMAIN/healthz  # Pokes the WC Ingress Controller
```
