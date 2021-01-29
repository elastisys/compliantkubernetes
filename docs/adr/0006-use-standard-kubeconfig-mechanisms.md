# Use Standard KUBECONFIG Mechanisms

* Status: proposed
* Deciders: TBD
* Date: 2021-01-28

## Context and Problem Statement

To increase adoption of Compliant Kubernetes, we were asked to observe the [Principle of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment). Currently, Compliant Kubernetes's handing of KUBECONFIG is astonishing. Most tools in the ecosystem use the standard `KUBECONFIG` environment variable and kubecontext implemented in the client-go library.

These tools leave it up to the user to set `KUBECONFIG` or use the default `~/.kube/config`. Similarly, there is a default kubecontext which can be overwritten via command-line. Tools that get cluster credentials generate a context related to the name of the cluster.

Tools that behave as such include:

* `gcloud container clusters get-credentials`
* `az aks get-credentials`
* `kops`
* `helm`
* `kubectl`
* `fluxctl`

## Decision Drivers <!-- optional -->

* [driver 1, e.g., a force, facing concern, …]
* [driver 2, e.g., a force, facing concern, …]
* … <!-- numbers of drivers can vary -->

## Considered Options

* [option 1]
* [option 2]
* [option 3]
* … <!-- numbers of options can vary -->

## Decision Outcome

Chosen option: "[option 1]", because [justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force force | … | comes out best (see below)].

### Positive Consequences <!-- optional -->

* [e.g., improvement of quality attribute satisfaction, follow-up decisions required, …]
* …

### Negative Consequences <!-- optional -->

* [e.g., compromising quality attribute, follow-up decisions required, …]
* …

## Pros and Cons of the Options <!-- optional -->

### [option 1]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

### [option 2]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

### [option 3]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

## Links <!-- optional -->

* [Link type] [Link to ADR] <!-- example: Refined by [ADR-0005](0005-example.md) -->
* … <!-- numbers of links can vary -->
