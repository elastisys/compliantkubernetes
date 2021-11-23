# [Superseded by [ADR-0017](0017-persist-dex.md)] Do not persist Dex

* Status: superseded by [ADR-0017](0017-persist-dex.md)
* Deciders: Compliant Kubernetes Architecture Meeting
* Date: 2021-04-29

Technical Story: [Reduce Helmfile concurrency for improved predictability](https://github.com/elastisys/compliantkubernetes-apps/issues/402#issuecomment-827476433)

## Context and Problem Statement

> Dex requires persisting state to perform various tasks such as track refresh tokens, preventing replays, and rotating keys.

What persistence option should we use?

## Decision Drivers

* CRDs add complexity
* Storage adds complexity

## Considered Options

* Use ["memory" storage](https://github.com/dexidp/helm-charts/tree/master/charts/dex#minimal-configuration)
* Use [CRD-based storage](https://dexidp.io/docs/storage/#kubernetes-custom-resource-definitions-crds)

## Decision Outcome

Chosen option: "use memory", because it simplified operations with little negative impact.

### Positive Consequences

* Dex brings no additional CRDs, which simplified upgrades.
* Dex brings no state, which simplified upgrades.

### Negative Consequences

* The authentication flow is disrupted, if Dex is rebooted *exactly* during an authentication flow. There is no user impact if Dex is restarted after the [JWT](https://jwt.io/) was issued. Cristian tested this with `kubectl` and Grafana. Since we will only reboot Dex during maintenance windows, this is unlikely to be an issue in the foreseeable future.

## Other Considerations

If Dex becomes a bottleneck and needs replication, or if we want to avoid disrupting authentication flows during operations on Dex, we will have to revisit this ADR.
