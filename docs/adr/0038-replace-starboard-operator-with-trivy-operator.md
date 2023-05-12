# Replace the starboard-operator with the trivy-operator

* Status: accepted
* Deciders: arch meeting
* Date: 2023-03-30

## Context and Problem Statement

The maintainers of Starboard [deprecated it](https://github.com/aquasecurity/starboard/discussions/1173) in favor of [Trivy Kubernetes](https://aquasecurity.github.io/trivy/v0.41/tutorials/kubernetes/cluster-scanning/) with [Trivy operator](https://github.com/aquasecurity/trivy-operator). They will no longer make any bigger changes to Starboard operator. They announced the change in march.

We currently use Starboard operator for scanning images with Trivy and for running the CIS Kubernetes benchmark with kubebench. Trivy operator has support for scanning images and running a version of the CIS Kubernetes benchmark.

Can or should we follow the evolution and replace starboard-operator with trivy-operator?

## Decision Drivers

* We want to maintain platform security and stability.
* We want to use the best tools out there.

## Considered Options

1. Do nothing
2. Move ahead and replace starboard-operator with trivy-operator

## Decision Outcome

Chosen option: 2 - Move ahead and replace starboard-operator with trivy-operator and include the CIS Kubernetes benchmark

### Positive Consequences

The main and the good reason for replacing starboard-operator with trivy-operator is that starboard-operator is getting replaces as stated above.

### Negative Consequences

I have no obvious reason not to do it other than that we may want to wait for a second before we do it as the current state of the chart is slightly unstable. For example:

https://github.com/aquasecurity/trivy-operator/discussions/1071

## Links

* [Trivy-operator dashboard!](https://raw.githubusercontent.com/dotdc/media/main/grafana-dashboards-kubernetes/k8s-addons-starboard-operator.png)
* [Hot to request Pass and Fail](https://github.com/aquasecurity/trivy-operator/blob/main/docs/tutorials/integrations/metrics.md#clustercompliancereport)
* [CIS Kubernetes benchmark](https://www.cisecurity.org/benchmark/kubernetes) goes under [ClusterComplianceReports](https://aquasecurity.github.io/trivy-operator/v0.12.1/docs/crds/clustercompliance-report/).
* [NSA, CISA Kubernetes Hardening Guidance v1.2](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
