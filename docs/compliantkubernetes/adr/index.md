# Architectural Decision Log

## Mapping to ISO 27001 Controls

* A.14.1.1 "Information security requirements analysis and specification"

## What are architectural decisions?

Architectural decisions are high-level technical decisions that affect most stakeholders, in particular Compliant Kubernetes developers, administrators and users.
A non-exhaustive list of architectural decisions is as follows:

* adding or removing tools;
* adding or removing components;
* changing what component talks to what other component;
* major (in the [SemVer](https://semver.org/) sense) component upgrades.

Architectural decisions should be taken as directions to follow for future development and not issues to be fixed immediately.

## What triggers an architectural decision?

An architectural decision generally starts with one of the following:

* A new features was requested by product management.
* An improvement was requested by engineering management.
* A new risk was discovered, usually by the architect, but also by any stakeholder.
* A new technology was discovered, that may help with a new feature, an improvement or to mitigate a risk.

## How are architectural decisions captured?

Architectural decisions are captured via [Architectural Decision Records](#adrs) or the [tech radar](../developer-guide/tech-radar/).
Both are stored in Git, hence a decision log is also captured as part of the Git commit messages.

## How are architectural decisions taken?

Architectural decisions need to mitigate the following information security risks:

* a component might not fulfill advertised expectations;
* a component might be abandoned;
* a component might change direction and deviate from expectations;
* a component might require a lot of (initial or ongoing) training;
* a component might not take security seriously;
* a component might change its license, prohibiting its reuse or making its use expensive.

The Compliant Kubernetes architect is overall responsible for this risk.

## How are these risks mitigated?

Before taking in any new component to Compliant Kubernetes, we investigate and evaluate them. We prefer components that are:

* **community-driven open-source projects**, to reduce the risk of a component becoming abandoned, changing its license or changing direction in the interest of a single entity; as far as possible, we choose [CNCF projects](https://landscape.cncf.io/?project=hosted) (preferably graduated ones) or projects which are governed by at least 3 different entities;
* **projects with a good security track record**, to avoid unexpected security vulnerabilities or delays in fixing security vulnerabilities; as far as possible, we choose projects with a clear security disclosure process and a clear security announcement process;
* **projects that are popular**, both from a usage and contribution perspective; as far as possible, we choose projects featuring well-known users and many contributors;
* **projects that rely on technologies that our team is already trained on**, to reduce the risk of requiring a lot of (initial or ongoing) training; as far as possible, we choose projects that overlap with the projects already on our [tech radar](../developer-guide/tech-radar);
* **projects that are simple to install and manage**, to reduce required training and burden on administrators.

Often, it is not possible to fulfill the above criteria. In that case, we take the following mitigations:

* Architectural Decision Records include recommendations on training to be taken by administrators.
* Closed-source or "as-a-Service" alternatives are used, if they are easy to replace thanks to broad API compatibility or standardization.

These mitigations may be relaxed for components that are part of alpha or beta features, as these features -- and required components -- can be removed at our discretion.

## ADRs

This log lists the architectural decisions for Compliant Kubernetes.

<!-- adrlog -- Regenerate the content by using "adr-log -i". You can install it via "npm install -g adr-log" -->

* [ADR-0000](0000-use-markdown-architectural-decision-records.md) - Use Markdown Architectural Decision Records
* [ADR-0001](0001-use-rook-storage-orchestrator.md) - Use Rook for Storage Orchestrator
* [ADR-0002](0002-use-kubespray-for-cluster-lifecycle.md) - Use Kubespray for Cluster Life-cycle
* [ADR-0003](0003-push-metrics-via-influxdb.md) - Push Metrics via InfluxDB
* [ADR-0004](0004-plan-for-usage-without-wrapper-scripts.md) - Plan for Usage without Wrapper Scripts
* [ADR-0005](0005-use-individual-ssh-keys.md) - Use Individual SSH Keys
* [ADR-0006](0006-use-standard-kubeconfig-mechanisms.md) - Use Standard Kubeconfig Mechanisms
* [ADR-0007](0007-make-monitoring-forwarders-storage-independent.md) - Make Monitoring Forwarders Storage Independent
* [ADR-0008](0008-use-hostnetwork-or-loadbalancer-for-ingress.md) - Use HostNetwork or LoadBalancer for Ingress
* [ADR-0009](0009-use-cluster-issuers-for-letsencrypt.md) - Use ClusterIssuers for LetsEncrypt
* [ADR-0010](0010-run-managed-services-in-workload-cluster.md) - Run managed services in workload cluster
* [ADR-0011](0011-let-upstream-projects-handle-crds.md) - Let upstream projects handle CRDs
* [ADR-0012](0012-do-not-persist-dex.md) - [Superseded by [ADR-0017](0017-persist-dex.md)] Do not persist Dex
* [ADR-0013](0013-configure-alerts-in-omt.md) - Configure Alerts in On-call Management Tool (e.g., Opsgenie)
* [ADR-0014](0014-use-bats-for-testing-bash-wrappers.md) - Use bats for testing bash wrappers
* [ADR-0015](0015-we-believe-in-community-driven-open-source.md) - We believe in community-driven open source
* [ADR-0016](0016-gid-0-is-okey-but-not-by-default.md) - gid=0 is okay, but not by default
* [ADR-0017](0017-persist-dex.md) - Persist Dex

<!-- adrlogstop -->

For new ADRs, please use [template.md](template.md) as basis.
More information on MADR is available at <https://adr.github.io/madr/>.
General information about architectural decision records is available at <https://adr.github.io/>.

## Index Regeneration

Pre-requisites:

* Install [npm](https://www.npmjs.com/)
* Install [adr-log](https://github.com/adr/adr-log#install)
* Install [make](https://packages.ubuntu.com/search?keywords=make)

Run `make -C docs/adr`
