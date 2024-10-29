# Advanced Configuration

You have already been exposed to some of Welkin's configuration options while creating a cluster. If not, read [that section](on-prem-standard.md) first.

This section will outline some advanced configuration topics.

## Overview

Welkin is composed of two layers, the Kubernetes layer and the apps layer. Each is configured slightly differently.

## Kubernetes Layer

To find all configuration option of the Kubernetes layer, please read the [upstream Kubespray](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/ansible/vars.md) documentation.
Welkin overrides some of Kubespray's defaults, as shown [here](https://github.com/elastisys/compliantkubernetes-kubespray/tree/main/config).

## Apps Layer

The configuration of the apps layer is documented [here](schema/README.md).
