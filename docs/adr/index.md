# Architectural Decision Log

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
* [ADR-0013](0013-configure-alerts-in-omt.md) - Configure Alerts in On-call Management Tool (e.g., Opsgenie)
* [ADR-0014](0014-use-bats-for-testing-bash-wrappers.md) - Use bats for testing bash wrappers

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
