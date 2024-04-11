SealedSecrets (self-managed)
===========

{%
   include-markdown './_common.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

{%
   include-markdown './_common-crds.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

This page will help you to install [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets), so that you are allowed to install the cluster-wide resources that are required by Sealed Secrets.

This guide is a complement to [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets/tree/v0.24.2) own documentation.

# Preparation

The self-managed cluster-wide resources feature adds specific Roles, ServiceAccounts, etc. for you.
This enables you to install and manage the resources that Sealed Secrets needs.
These pre-installed resources are propagated via HNC from your root Namespace ([recall the documentation of this feature](../namespaces.md)).

First create a new Namespace using HNC, using the snippet below.
If you do not know which root namespace you should use, ask your platform administrator.

```yaml
apiVersion: hnc.x-k8s.io/v1alpha2
kind: SubnamespaceAnchor
metadata:
  name: sealed-secrets
  namespace: <root namespace>
```

## Install Sealed Secrets

!!! Note "Supported versions"
    This installation guide has been tested with Sealed Secrets version [0.24.2](https://github.com/bitnami-labs/sealed-secrets/tree/release/v0.24.2) and Helm Chart version [2.13.1](https://github.com/bitnami-labs/sealed-secrets/tree/helm-v2.13.1/helm/sealed-secrets).

Sealed Secrets have a section in their documentation about installing Sealed Secrets into a [restricted environment](https://github.com/bitnami-labs/sealed-secrets/tree/v0.24.2#helm-chart-on-a-restricted-environment), where they give a `config.yaml` that defines what should be installed.

The following `config.yaml` is an example of what is required to install Sealed Secrets into Compliant Kubernetes.

```yaml
serviceAccount:
  create: true
  name: sealed-secrets
rbac:
  create: false
  clusterRole: false
## Add your namespace(s) here
additionalNamespaces: []
resources:
  requests:
    cpu: 150m
    memory: 256Mi
  limits:
    cpu: 150m
    memory: 256Mi
```

!!! important
    Add the namespaces that should support creation of SealedSecrets to the `additionalNamespaces` list. If this list is empty the SealedSecrets controller will output an error when attempting to create a SealedSecret as it attempts to get secrets at cluster level.

You are now ready to install Sealed Secrets

```console
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm upgrade --install sealed-secrets -n sealed-secrets --version 2.13.1 sealed-secrets/sealed-secrets -f config.yaml
```

!!! Note "Note about `kubeseal`"
    The Sealed Secrets cli tool `kubeseal` expects the controller to be installed in the namespace `kube-system`.
    However the controller is installed in the namespace `sealed-secrets`.
    As such you need to follow this [guide](https://github.com/bitnami-labs/sealed-secrets/tree/release/v0.24.2#how-to-use-kubeseal-if-the-controller-is-not-running-within-the-kube-system-namespace) to use `kubeseal`

## Further Reading

Please refer to the official documentation how to operate and use Sealed Secrets.

- [Documentation](https://github.com/bitnami-labs/sealed-secrets/tree/release/v0.24.2#usage)
- [Crypto](https://github.com/bitnami-labs/sealed-secrets/blob/release/v0.24.2/docs/developer/crypto.md)
- [SealedSecrets with Elastisys Managed Argo CD](../additional-services/argocd.md#with-sealedsecrets)
