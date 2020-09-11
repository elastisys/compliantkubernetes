# Getting Started

As a user, you will need:

* [docker](https://docs.docker.com/get-docker/)
* [helm](https://helm.sh/docs/intro/install/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [oidc-login](https://github.com/int128/kubelogin); we suggest installing it via [krew](https://github.com/kubernetes-sigs/krew)

The easier is to request a demo environment from a [managed Compliant Kubernetes provider](https://compliantkubernetes.com). You should receive:

* URLs for Compliant Kubernetes UI components, such as the dashboard, container registry, logs, etc.
* A [kubeconfig](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) file for configuring kubectl access to the cluster.
* (Optionally) Static username and password. Normally, you should log in via a username and a password of your organizations identity provider.

If you want to setup your own Compliant Kubernetes installation, head to the [Operator Manual](operator-manual).
