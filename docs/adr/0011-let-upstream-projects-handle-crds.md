# Let upstream projects handle CRDs

* Status: accepted
* Deciders: Compliant Kubernetes Arch Meeting
* Date: 2021-04-29

Technical Story: [#446](https://github.com/elastisys/compliantkubernetes-apps/pull/446) [#369](https://github.com/elastisys/compliantkubernetes-apps/issues/369) [#391](https://github.com/elastisys/compliantkubernetes-apps/issues/391) [#402](https://github.com/elastisys/compliantkubernetes-apps/issues/402) [#436](https://github.com/elastisys/compliantkubernetes-apps/pull/436).

## Context and Problem Statement

CustomResourceDefinitions (CRDs) are tricky. They are essentially a mechanism to change the API of Kubernetes. Helm 2 had zero support for CRDs. Helm 3 has [support for installing CRDs](https://helm.sh/docs/topics/charts/#custom-resource-definitions-crds), but not upgrading them.

How should we handle CRDs?

## Decision Drivers

* CRDs add complexity and need to be treated specially.
* Generally need to “trim fat” and rely on upstream.

## Considered Options

* Install and upgrade CRDs as part of the bootstrap step, which is a Helm 2 legacy.
* Rely on whatever mechanism is proposed by upstream Helm Charts.

## Decision Outcome

Chosen option: "Rely on upstream", because it trims fat and reduces astonishment.

At installation, rely on upstream's approach to install CRDs (see below). At upgrade, propagate upstream migration steps in CK8s migration steps in each release notes. An [issue template](https://github.com/elastisys/compliantkubernetes-apps/pull/436) was created to ensure we won't forget.

Since we "vendor in" all Charts, CRDs can be discovered using:

```
grep -R 'kind: CustomResourceDefinition'
```

### Positive Consequences

* Less astonishing, compared to installing Chart "by hand".
* Less maintenance, i.e., there is only one source of truth for CRDs.

### Negative Consequences

* None really.

## Detailed Audit

A detailed audit was performed of all CRDs in Compliant Kubernetes on 2021-04-27.

As a summary, all projects encourage installing CRDs as part of standard `helm install`. Most projects encourage following manual migration steps to handle CRDs. Some projects handle CRD upgrades.

A detailed analysis is listed below:

### cert-manager

* Installation: The cert-manager Helm Chart includes the [`installCRDs`](https://github.com/jetstack/cert-manager/blob/master/deploy/charts/cert-manager/values.yaml#L42) value -- by default it is set to `false`. If set to `true`, then CRDs are automatically installed when installing cert-manager, albeit not using the CRDs mechanism provided by Helm.
* Upgrade: CRDs are supposed to be [upgraded manually](https://cert-manager.io/docs/installation/upgrading/#upgrading-with-helm).

### dex

Dex can be configured without CRDs. [ADR-0012](https://github.com/elastisys/compliantkubernetes/pull/134) argues for that approach.

### gatekeeper

* Installation: Gatekeeper installs CRDs using the [mechanism provided by Helm](https://github.com/open-policy-agent/gatekeeper/tree/master/charts/gatekeeper/crds).
* Upgrade: Gatekeeper wants you to either uninstall-install or run a [helm_migrate.sh](https://github.com/open-policy-agent/gatekeeper/tree/master/charts/gatekeeper#upgrade-chart).

### Prometheus (kube-prometheus-stack)

* Installation: kube-prometheus-stack installs CRDs using [standard Helm mechanism](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack/crds).
* Upgrade: kube-prometheus-stack expects you to [run manual upgrade steps](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack#from-14x-to-15x).

### Velero

* Installation: Velero install CRDs using [standard Helm mechanism](https://github.com/vmware-tanzu/helm-charts/tree/main/charts/velero/crds).
* Upgrade: Velero includes [magic to upgrade CRDs](https://github.com/vmware-tanzu/helm-charts/blob/main/charts/velero/templates/upgrade-crds/).
