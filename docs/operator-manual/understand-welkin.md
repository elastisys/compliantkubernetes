# Understand Welkin

This page gives you a basic understanding of Welkin from the point-of-view of the Platform Administrator.
For a basic understanding of Welkin from the point-of-view of the Application Developers, head to [Application Developer Overview](../user-guide/index.md).

## Welkin Architecture

To begin with, you should familiarize yourself with [Welkin's architecture](../architecture.md).
It describes what components are part of Welkin and what component talks to which other components.
It allows you to create a mental model and reason about complex failure modes, such as "a buffer overflow in Fluentd may be caused by OpenSearch lacking sufficient capacity to ingest all logs".

In particular, notice that:

- Welkin is composed of at least two Kubernetes clusters:
    - at least one Workload Cluster: this hosts the application(s) of the Application Developer; and
    - one Service Cluster: this provides several [Service Endpoints](../glossary.md#service-endpoint) to the Application Developers, in particular around authentication and observability.
- Welkin is composed of two layers:
    - The Kubernetes-lifecycle layer sets up rather vanilla Kubernetes Clusters with some security defaults. This layer is implemented either via Kubespray or Cluster API.
    - The Welkin Apps layer augments the two Kubernetes Clusters with projects around security and observability. This layer has a single implementation.

## Kubespray vs Cluster API

Although Welkin tries to be a platform which is as portable as possible, the two implementations of the Kubernetes-lifecycle layer differ quite a bit.
As a Platform Administrator, you need to be aware of these differences.

Welkin recommends using the Cluster API implementation when setting up a new Environment.
Cluster API offers features such as Cluster autoscaling, Node self-healing and faster Kubernetes upgrades.
On the downside, it requires a mature Cluster API provider.
Not all infrastructure providers have a mature Cluster API provider.

Therefore, Welkin Environments can also be set up using Kubespray.
Kubespray runs on pretty much any infrastructure you throw at it.
However, it lacks support for Cluster autoscaling and Kubernetes upgrades are slower (albeit reliable).

For both Cluster API and Kubespray, the infrastructure provider might come with its own limitations, such as lack of load-balancers and/or of block storage which integrate with Kubernetes.
The [provider audit](provider-audit.md) is a systematic way to discover and understand these differences, so as to configure Welkin properly.

## Configuration Repository

Welkin abides to the configuration-as-code and infrastructure-as-code principles.
In essence, all Welkin configuration is stored in text files (most frequently YAML).
Welkin expects you to stores these files in a git repository, which is why we refer to Welkin configuration as configuration repository.

A typical configuration repository when using [Welkin Kubespray](https://github.com/elastisys/compliantkubernetes-kubespray) looks as follows:

```console
my-welkin-environment
|-- adminlog
|   `-- changes
|   `-- incidents
|   `-- maintenance
|-- backups
|-- common-config.yaml
|-- compliantkubernetes-apps
|-- compliantkubernetes-kubespray
|-- defaults
|   |-- common-config.yaml
|   |-- sc-config.yaml
|   `-- wc-config.yaml
|-- README.md
|-- sc-config
|   |-- group_vars
|   |   |-- all
|   |   |   |-- ck8s-kubespray-general.yaml
|   |   |   `-- ck8s-ssh-keys.yaml
|   |   |-- etcd
|   |   |   `-- ck8s-etcd.yaml
|   |   `-- k8s_cluster
|   |       |-- ck8s-k8s-cluster-default.yaml
|   |       `-- ck8s-k8s-cluster.yaml
|   `-- inventory.ini
|-- sc-config.yaml
|-- secrets.yaml
|-- .sops.yaml
|-- .state
|   |-- kube_config_sc.yaml
|   |-- kube_config_wc.yaml
|   `-- s3cfg.ini
|-- wc-config
|   |-- group_vars
|   |   |-- all
|   |   |   |-- ck8s-kubespray-general.yaml
|   |   |   `-- ck8s-ssh-keys.yaml
|   |   |-- etcd
|   |   |   `-- ck8s-etcd.yaml
|   |   `-- k8s_cluster
|   |       |-- ck8s-k8s-cluster-default.yaml
|   |       `-- ck8s-k8s-cluster.yaml
|   `-- inventory.ini
`-- wc-config.yaml
```

Let us dive into the role of each of these files in the order you would commonly look at them:

- `README.md` is a human description of the environment.
This file is optional and ignored by Welkin.
We recommend describing here the propose of the Environment, what kind of applications it hosts, what infrastructure provider it runs on and any noteworthy deviations.
- `adminlogs` is a folder where you can put text files (Markdown) describing operations you performed against this environment.
This folder is optional and ignored by Welkin.
We recommend having separate folders for changes, incidents and maintenance.
- `.sops.yaml` contains [sops](https://github.com/getsops/sops) configuration, used by Welkin to encrypt secrets.
Welkin makes sure to decrypt secrets when it needs them.

The Welkin Kubespray layer initializes and reads the following configuration files and folders:

- `sc-config` and `wc-config` store configuration for the Service Cluster and Workload Cluster, respectively.
These folders are consumed by Ansible, which is part of this layer.
If `group_vars`, `all` and `inventory.ini` look new to you, we recommend you learn more about Ansible.

The Welkin Apps layer initializes and reads the following configuration files and folders:

- `backups` is a folder in which Welkin stores copies of previous configurations.
See this as a convenience, given that all configuration is already in git.
- `defaults` is a folder which contains the default `common-config.yaml`, `sc-config.yaml` and `wc-config.yaml` for the infrastructure provider and flavor you chose when you initialized the configuration repository using Welkin.
Do not change these files, as they may be overridden by Welkin.
Instead, override configuration values with the files described below.
- `common-config.yaml` contains override configuration common to both the Service Cluster and the Workload Cluster.
- `wc-config.yaml` and `sc-config.yaml` contains override configuration specific to the Service Cluster and the Workload Cluster, respectively.
- `secrets.yaml` contains secrets, both for the Workload Cluster and Service Cluster.
This file is encrypted using the information in `.sops.yaml`.
You should only edit this file using sops to make sure secrets never end up in plain text in the configuration repository.

Except for `init` sub-commands and configuration migration steps, the files above are only consumed by Welkin.
They only take as input explicit choices that you made and describe how an Environment should be.

The following files and folders are stored by Welkin in the configuration repository and contain information from an Environment:

- `.state` is a folder which contains the "state", i.e., files produced by Welkin needed to access an Environment during daily operations, in particular kubeconfig and S3 object storage access.
If needed, these files will be encrypted with sops.
In Welkin, kubeconfigs generally don't contain credentials, only pointer to OpenID configuration, hence are usually not encrypted.

To make sure your whole team knows exactly which version of Welkin an Environment runs, it is common practice to add the source code, in the example above `compliantkubernetes-apps` and `compliantkubernetes-kubespray`, as git submodules.
An alternative is to pack all Welkin source code in a Docker image.

## What does it mean to use Welkin as a Platform Administrator on a daily basis?

You must specify a configuration repository in the environment variable `CK8S_CONFIG_PATH`.
Then you can interact with Welkin via commands such as `ck8s` and `ck8s-kubespray` provided in the source code.
A typical usage of these commands is describe later in this guide.
