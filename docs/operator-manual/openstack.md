# Compliant Kubernetes on Openstack

This document contains instructions on how to set up a Compliant Kubernetes environment (consisting of a service cluster and one or more workload clusters) on Openstack.

!!!note
    This guide is written for compliantkubernetes-apps [v0.13.0](https://github.com/elastisys/compliantkubernetes-apps/tree/v0.13.0)

TODO: The document is split into two parts:

- Cluster setup (setting up infrastructure and the Kubernetes clusters).
  We will be using the [Terraform module for Openstack that can be found in the Kubespray repository](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack).
  Please refer to it if you need more details about this part of the setup.

- Apps setup (including information about limitations)

Before starting, make sure you have [all necessary tools](getting-started.md). In addition to these general tools, you will also need:

- [Openstack credentials](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack#openstack-access-and-credentials) (either using `openrc` or the `clouds.yaml` configuration file) for setting up the infrastructure.

!!!note
    Although recommended OpenStack authentication method is `clouds.yaml` it is more convenient to use the `openrc` method with compliant kubernetes as it works both with kubespray and terraform. If you are using the `clouds.yaml` method, at the moment, kubespray will still expect you to set a few environment variables.

## Initialize configuration folder

Choose names for your service cluster and workload cluster(s):

```bash
SERVICE_CLUSTER="testsc"
WORKLOAD_CLUSTERS=( "testwc0" "testwc1" )
```

Start by initializing a Compliant Kubernetes environment using Compliant Kubernetes Kubespray.
All of this is done from the root of the `compliantkubernetes-kubespray` repository.

```bash
export CK8S_CONFIG_PATH=~/.ck8s/<environment-name>
export SOPS_FP=<PGP-fingerprint>

for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  ./bin/ck8s-kubespray init "${CLUSTER}" openstack "${SOPS_FP}"
done
```

## Infrastructure setup using Terraform

Configure Terraform by creating a `cluster.tfvars` file for each cluster.
The available options can be seen in `kubespray/contrib/terraform/openstack/variables.tf`.
There is a sample file that can be copied to get something to start from.

```bash
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
  cp kubespray/contrib/terraform/openstack/sample-inventory/cluster.tfvars "${CK8S_CONFIG_PATH}/${CLUSTER}-config/cluster.tfvars"
done
```

!!!note
    You really *must* edit the values in these files.
    There is no way to set sane defaults for what flavor to use, what availability zones or networks are available across providers.
    In the section below some guidance and samples are provided but remember that they might be useless to you depending on your needs and setup.

### Infrastructure guidance

We recommend you to have at least three worker nodes with 4 cores and 8 GB memory each, and we recommend you to have at least 2 cores and 4 GB for your master nodes.

Below is example `cluster.tfvars` for a few select openstack providers.
The examples are copy-pastable, but you might want to change `cluster_name` and `network_name` (if neutron is used!).

=== "Citycloud Kna1"

    ``` hcl
    # your Kubernetes cluster name here
    cluster_name = "your-cluster-name"

    # image to use for bastion, masters, standalone etcd instances, and nodes
    image = "Ubuntu 20.04 Focal Fossa 20200423"

    # 0|1 bastion nodes
    number_of_bastions = 0

    # standalone etcds
    number_of_etcd = 0

    # masters
    number_of_k8s_masters = 1
    number_of_k8s_masters_no_etcd = 0
    number_of_k8s_masters_no_floating_ip = 0
    number_of_k8s_masters_no_floating_ip_no_etcd = 0
    flavor_k8s_master = "96c7903e-32f0-421d-b6a2-a45c97b15665"

    # nodes
    number_of_k8s_nodes = 3
    number_of_k8s_nodes_no_floating_ip = 0
    flavor_k8s_node = "572a3b2e-6329-4053-b872-aecb1e70d8a6"

    # networking
    # ssh access to nodes
    k8s_allowed_remote_ips = ["0.0.0.0/0"]
    worker_allowed_ports = [
      { # Node ports
        "protocol"         = "tcp"
        "port_range_min"   = 30000
        "port_range_max"   = 32767
        "remote_ip_prefix" = "0.0.0.0/0"
      },
      { # HTTP
        "protocol"         = "tcp"
        "port_range_min"   = 80
        "port_range_max"   = 80
        "remote_ip_prefix" = "0.0.0.0/0"
      },
      { # HTTPS
        "protocol"         = "tcp"
        "port_range_min"   = 443
        "port_range_max"   = 443
        "remote_ip_prefix" = "0.0.0.0/0"
      }
    ]
    network_name = "name-of-your-network"
    external_net = "fba95253-5543-4078-b793-e2de58c31378"
    floatingip_pool = "ext-net"
    use_access_ip = 0
    ```

=== "Safespring sto1 (old)"

    ``` hcl
    # your Kubernetes cluster name here
    cluster_name = "your-cluster-name"

    # list of availability zones available in your OpenStack cluster
    az_list = ["se-east-1"]
    az_list_node = ["se-east-1"]

    # image to use for bastion, masters, standalone etcd instances, and nodes
    image = "ubuntu-20.40-server-cloudimg-amd64-20200423"

    # 0|1 bastion nodes
    number_of_bastions = 0

    # standalone etcds
    number_of_etcd = 0

    # masters
    number_of_k8s_masters = 1
    number_of_k8s_masters_no_etcd = 0
    number_of_k8s_masters_no_floating_ip = 0
    number_of_k8s_masters_no_floating_ip_no_etcd = 0
    flavor_k8s_master = "9d82d1ee-ca29-4928-a868-d56e224b92a1"

    # nodes
    number_of_k8s_nodes = 3
    number_of_k8s_nodes_no_floating_ip = 0
    flavor_k8s_node = "16d11558-62fe-4bce-b8de-f49a077dc881"

    # networking
    # ssh access to nodes
    k8s_allowed_remote_ips = ["0.0.0.0/0"]
    worker_allowed_ports = [
      { # Node ports
        "protocol"         = "tcp"
        "port_range_min"   = 30000
        "port_range_max"   = 32767
        "remote_ip_prefix" = "0.0.0.0/0"
      },
      { # HTTP
        "protocol"         = "tcp"
        "port_range_min"   = 80
        "port_range_max"   = 80
        "remote_ip_prefix" = "0.0.0.0/0"
      },
      { # HTTPS
        "protocol"         = "tcp"
        "port_range_min"   = 443
        "port_range_max"   = 443
        "remote_ip_prefix" = "0.0.0.0/0"
      }
    ]
    network_name = "your-network-name"
    external_net = "71b10496-2617-47ae-abbc-36239f0863bb"
    floatingip_pool = "public-v4"
    use_access_ip = 0
    dns_nameservers = ["8.8.8.8", "1.1.1.1"]
    ```

=== "Safespring sto1 (new)"

    ``` hcl
    # your Kubernetes cluster name here
    cluster_name = "your-cluster-name"

    # image to use for bastion, masters, standalone etcd instances, and nodes
    image = "ubuntu-20.04-server-cloudimg-amd64-20201102"

    # 0|1 bastion nodes
    number_of_bastions = 0

    use_neutron = 0

    # standalone etcds
    number_of_etcd = 0

    # masters
    number_of_k8s_masters = 0
    number_of_k8s_masters_no_etcd = 0
    number_of_k8s_masters_no_floating_ip = 1
    number_of_k8s_masters_no_floating_ip_no_etcd = 0
    flavor_k8s_master = "8a707999-0bce-4f2f-8243-b4253ba7c473"

    # nodes
    number_of_k8s_nodes = 0
    number_of_k8s_nodes_no_floating_ip = 3
    flavor_k8s_node = "5b40af67-9d11-45ed-a44f-e876766160a5"

    # networking
    # ssh access to nodes
    k8s_allowed_remote_ips = ["0.0.0.0/0"]
    worker_allowed_ports = [
      { # Node ports
        "protocol"         = "tcp"
        "port_range_min"   = 30000
        "port_range_max"   = 32767
        "remote_ip_prefix" = "0.0.0.0/0"
      },
      { # HTTP
        "protocol"         = "tcp"
        "port_range_min"   = 80
        "port_range_max"   = 80
        "remote_ip_prefix" = "0.0.0.0/0"
      },
      { # HTTPS
        "protocol"         = "tcp"
        "port_range_min"   = 443
        "port_range_max"   = 443
        "remote_ip_prefix" = "0.0.0.0/0"
      }
    ]
    external_net = "b19680b3-c00e-40f0-ad77-4448e81ae226"
    use_access_ip = 1
    network_name = "public"
    ```

### Expose Openstack credentials to Terraform

Terraform will need access to Openstack credentials in order to create the infrastructure.
More details can be found [here](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack#openstack-access-and-credentials).
We will be using the declarative option with the `clouds.yaml` file.
Since this file can contain credentials for multiple environments, we specify the name of the one we want to use in the environment variable `OS_CLOUD`:

```bash
export OS_CLOUD=<name-of-openstack-cloud-environment>
```

### Initialize and apply Terraform

```bash
MODULE_PATH="$(pwd)/kubespray/contrib/terraform/openstack"

pushd "${MODULE_PATH}"
for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  terraform init
  terraform apply -var-file="${CK8S_CONFIG_PATH}/${CLUSTER}-config/cluster.tfvars" -state="${CK8S_CONFIG_PATH}/${CLUSTER}-config/terraform.tfstate"
done
popd
```

!!!warning
    The above will not work well if you are using a bastion host.
    This is due to [some hard coded paths](https://github.com/kubernetes-sigs/kubespray/blob/master/contrib/terraform/openstack/modules/compute/main.tf#L207).
    To work around it, you may link the `kubespray/contrib` folder to the correct relative path, or make sure your `CK8S_CONFIG_PATH` is already at a proper place relative to the same.

## Install Kubernetes using Kubespray

Before we can run Kubespray, we will need to go through the relevant variables.
Additionally we will need to expose some credentials so that Kubespray can set up cloud provider integration.

You will need to change at least one value: `kube_oidc_url` in `group_vars/k8s_cluster/ck8s-k8s_cluster.yaml`, normally this should be set to `https://dex.BASE_DOMAIN`.

!!!note
    If you have `use_access_ip = 0` in `cluster.tfvars`, you should add the public ip address of the master nodes to the variable `supplementary_addresses_in_ssl_keys = ["<master-0-ip-address>",...]` somewhere under `group_vars/`.

For cloud provider integration, you have a few options [as described here](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/openstack.md#the-in-tree-cloud-provider).
We will be going with the in-tree cloud provider and simply source the Openstack credentials.
This doesn't require any changes to the variables as set up using this guide.

### Run Kubespray

Copy the script for generating dynamic ansible inventories:

```bash
for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  cp kubespray/contrib/terraform/terraform.py "${CK8S_CONFIG_PATH}/${CLUSTER}-config/inventory.ini"
  chmod +x "${CK8S_CONFIG_PATH}/${CLUSTER}-config/inventory.ini"
done
```

Now it is time to run the Kubespray playbook!

```bash
for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  ./bin/ck8s-kubespray apply "${CLUSTER}"
done
```

### Test access to the Kubernetes API

You should now have an encrypted kubeconfig file for each cluster under `$CK8S_CONFIG_PATH/.state`.
Check that they work like this:

```bash
for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  sops exec-file "${CK8S_CONFIG_PATH}/.state/kube_config_${CLUSTER}.yaml" "kubectl --kubeconfig {} cluster-info"
done
```

The output should be similar to this.

```
Kubernetes control plane is running at https://<public-ip>:6443

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
Kubernetes control plane is running at https://<public-ip>:6443

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## Prepare for Compliant Kubernetes Apps

To make the kubeconfig files work with Compliant Kubernetes Apps, you will need to rename or copy them, since Compliant Kubernetes Apps currently only support clusters named `sc` and `wc`.
If you have multiple workload clusters, you can make this work by setting `CK8S_CONFIG_PATH` to each `$CK8S_CONFIG_PATH/$CLUSTER-config` in turn.
I.e. `CK8S_CONFIG_PATH` will be different for compliantkubernetes-kubespray and compliantkubernetes-apps.

```
# In compliantkubernetes-kubespray
CK8S_CONFIG_PATH=~/.ck8s/<environment-name>
# In compliantkubernetes-apps (one config path per workload cluster)
CK8S_CONFIG_PATH=~/.ck8s/<environment-name>/<prefix>-config
```

Copy the kubeconfig files to a path that Apps can find.

**Option 1** - A single workload cluster:

```bash
cp "${CK8S_CONFIG_PATH}/.state/kube_config_${SERVICE_CLUSTER}.yaml" "${CK8S_CONFIG_PATH}/.state/kube_config_sc.yaml"
cp "${CK8S_CONFIG_PATH}/.state/kube_config_${WORKLOAD_CLUSTERS[@]}.yaml" "${CK8S_CONFIG_PATH}/.state/kube_config_wc.yaml"
```

You can now use the same `CK8S_CONFIG_PATH` for Apps as for compliantkubernetes-kubespray.

**Option 2** - A multiple workload cluster:

```bash
mkdir -p "${CK8S_CONFIG_PATH}/${SERVICE_CLUSTER}-config/.state"
cp "${CK8S_CONFIG_PATH}/.state/kube_config_${SERVICE_CLUSTER}.yaml" "${CK8S_CONFIG_PATH}/${SERVICE_CLUSTER}-config/.state/kube_config_sc.yaml"
for CLUSTER in "${WORKLOAD_CLUSTERS[@]}"; do
  mkdir -p "${CK8S_CONFIG_PATH}/${CLUSTER}-config/.state"
  cp "${CK8S_CONFIG_PATH}/.state/kube_config_${CLUSTERS}.yaml" "${CK8S_CONFIG_PATH}/${CLUSTER}-config/.state/kube_config_wc.yaml"
done
```

You will then need to set `CK8S_CONFIG_PATH` to each `$CLUSTER-config` folder in turn, in order to install Apps on the service cluster and workload clusters.

With this you should be ready to install Compliant Kubernetes Apps on top of the clusters.
This will be similar to any other cloud provider.
Suggested next steps are:

1. Configure DNS using your favorite DNS provider.
2. Create object storage buckets for backups and container registry storage (if desired).
3. Install Compliant Kubernetes Apps!
   See for example [this guide](../exoscale) for more details.

## Cleanup

If you installed Compliant Kubernetes Apps, start by [cleaning it up](../clean-up).
Make sure you remove all PersistentVolumes and Services with `type=LoadBalancer`.
These objects may create cloud resources that are not managed by Terraform, and therefore would not be removed when we destroy the infrastructure.

Destroy the infrastructure using Terraform, the same way you created it:

```bash
MODULE_PATH="$(pwd)/kubespray/contrib/terraform/openstack"

pushd "${MODULE_PATH}"
for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  terraform init
  terraform destroy -var-file="${CK8S_CONFIG_PATH}/${CLUSTER}-config/cluster.tfvars" -state="${CK8S_CONFIG_PATH}/${CLUSTER}-config/terraform.tfstate"
done
popd
```

Don't forget to remove any DNS records and object storage buckets that you may have created.
