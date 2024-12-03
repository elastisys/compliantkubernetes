# Use Standard Kubeconfig Mechanisms

- Status: accepted
- Deciders: Architecture Meeting
- Date: 2021-02-02

## Context and Problem Statement

To increase adoption of Welkin, we were asked to observe the [Principle of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment). Currently, Welkin's handing of kubeconfig is astonishing. Most tools in the ecosystem use the standard `KUBECONFIG` environment variable and kubeconfig context implemented in the client-go library. These tools leave it up to the user to set `KUBECONFIG` or use the default `~/.kube/config`. Similarly, there is a default kubeconfig context which can be overwritten via command-line. Tools that get cluster credentials generate a context related to the name of the cluster.

Tools that behave as such include:

- `gcloud container clusters get-credentials`
- `az aks get-credentials`
- `kops`
- `helmfile`
- `helm`
- `kubectl`
- `fluxctl`

## Decision Drivers

- Welkin needs to observe the Principle of Least Astonishment.
- Welkin needs to be compatible with various "underlying" vanilla Kubernetes tools.
- Welkin needs to be usable with various tools "on top".

## Considered Options

- Current solution, i.e., scripts wrapping kubeconfigs in sops which then execute "fixed" commands, like `helmfile`, `helm` and `kubectl`.
- "Lighter" scripts wrapping and unwrapping kubeconfig, allowing administrators to run `helmfile`, `helm` and `kubectl` as the administrator sees fit.
- Use standard kubeconfig mechanism.

## Decision Outcome

We chose using standard kubeconfig mechanism, because it improves integration both with tools "below" Welkin and "on top" of Welkin.

Tools that produce Kubernetes contexts are expected to use an approach similar to `kubectl config set-cluster`, `set-credentials` and `set-context`. The name of the cluster, user and context should be derived from the name of the cluster.

Tools that consume Kubernetes contexts are expected to use an approach similar to `kubectl`, `helm` or `helmfile` (see links below).

## Links

- [Organizing Cluster Access Using kubeconfig Files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
- [`kubectx` / `kubens`](https://github.com/ahmetb/kubectx)
