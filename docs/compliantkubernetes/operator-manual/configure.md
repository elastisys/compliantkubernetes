# Configure an Environment - Overview

Compliant Kubernetes is composed of two layers, the Kubernetes layer and the apps layer. Each is configured slightly differently.

## Kubernetes Layer

To find the configuration of the Kubernetes layer, please read the [upstream Kubespray](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/vars.md) documentation.
The default configuration of the Kubernetes layer is stored [here](https://github.com/elastisys/compliantkubernetes-kubespray/tree/main/config).

## Apps Layer

The configuration of the apps layer is documented as comments in the [default configuration files](https://github.com/elastisys/compliantkubernetes-apps/tree/main/config/config).
If you find a configuration key is insufficiently documented, please [open a PR](https://github.com/elastisys/compliantkubernetes-apps/pulls).
