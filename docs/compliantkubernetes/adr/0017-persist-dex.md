# Persist Dex

* Status: accepted
* Deciders: Compliant Kubernetes Architecture Meeting
* Date: 2021-11-16

Technical Story: [Enable Dex persistence](https://github.com/elastisys/compliantkubernetes-apps/issues/680)

## Context and Problem Statement

> Dex requires persisting state to perform various tasks such as track refresh tokens, preventing replays, and rotating keys.

What persistence option should we use?

## Decision Drivers

* CRDs add complexity
* Storage adds complexity
* We want to frequently reboot Nodes for security patching
* We want to deliver excellent user experience

## Considered Options

* Use ["memory" storage](https://github.com/dexidp/helm-charts/tree/master/charts/dex#minimal-configuration)
* Use [CRD-based storage](https://dexidp.io/docs/storage/#kubernetes-custom-resource-definitions-crds)

## Decision Outcome

Chosen option: "use CRD-based storage", because it improves user experience when Nodes are rebooted.

With "memory" storage, Dex loses the OpenID keys when restarted, which leads to the user being forced to eventually re-login. Worst off, this forced re-login happens unexpectedly from the user's perspective, when the Kubernetes apiserver chooses to refresh the OpenID keys.

Here is the experiment to illustrate the issue:

```console
$ curl https://dex.$DOMAIN/.well-known/openid-configuration > before-openid-configuration.json
$ curl https://dex.$DOMAIN/keys > before-keys.json

$ kubectl delete pods -n dex -l app.kubernetes.io/instance=dex

$ curl https://dex.$DOMAIN/.well-known/openid-configuration > after-openid-configuration.json
$ curl https://dex.$DOMAIN/keys > after-keys.json

$ diff -y before-openid-configuration.json after-openid-configuration.json
[empty output, no differences]

$ diff -y before-keys.json after-keys.json
[all keys are replaced]
```

### Positive Consequences

* Nodes which host Dex can be rebooted for security patching
* User experience is optimized

### Negative Consequences

* Dex will have a more permissions in the Service Cluster (see [`rbac.yaml`](https://github.com/dexidp/helm-charts/blob/dex-0.6.3/charts/dex/templates/rbac.yaml))
* We will need to closely monitor migration steps for Dex
