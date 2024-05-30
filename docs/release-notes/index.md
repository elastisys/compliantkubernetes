# Compliant Kubernetes Release Cycle

Compliant Kubernetes consists of several layers each with their own release cycles.

> [!IMPORTANT]
> Patch versions may be released at any time if Customer systems and Customer Data is at risk.
>
> For more details, see [ToS 3.6 Vulnerability Management](https://elastisys.com/legal/terms-of-service/#36-vulnerability-management).

## Compliant Kubernetes Apps

For the [apps layer](https://github.com/elastisys/compliantkubernetes-apps/), we aim to release 10 times per year.
This corresponds to approximately once a month except for Swedish holiday months, i.e., July and December.

## Compliant Kubernetes Kubespray

For the [Kubespray layer](https://github.com/elastisys/compliantkubernetes-kubespray/), we aim to release as soon as there is a new upstream release.

## Cluster API

For the Cluster API layer, we aim to release as soon as there is a new upstream release for either:

- [Cluster API Provider OpenStack](https://cluster-api-openstack.sigs.k8s.io/); and
- [Cluster API Provider Azure](https://capz.sigs.k8s.io/).
