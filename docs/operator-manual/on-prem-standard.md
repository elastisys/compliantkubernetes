---
tags:
  - BSI IT-Grundschutz APP.4.4.A13
---

# Standard Template for on-prem Environment

This document contains instructions on how to set-up a new Compliant Kubernetes on-prem environment.

## Prerequisites

!!!important "Decision to be taken"

    Decisions regarding the following items should be made before venturing on deploying Compliant Kubernetes.

    - Overall architecture, i.e., VM sizes, load-balancer configuration, storage configuration, etc.
    - Identity Provider (IdP) choice and configuration. See [this page](../user-guide/prepare-idp.md).
    - On-call Management Tool (OMT) choice and configuration

1. Make sure you [install all prerequisites](getting-started.md) on your laptop.

1. Prepare Ubuntu-based VMs:
    If you are using public clouds, you can create VMs using the scripts included in Kubespray:

    - For Azure, use [AzureRM scripts](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/azurerm).
    - For other clouds, use their respective [Terraform scripts](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform).

1. Create a git working folder to store Compliant Kubernetes configurations in a version-controlled manner. Run the following commands from the root of the config repo.

    !!! note
    The following steps are done from the root of the git repository you created for the configurations.

    ```bash
    export CK8S_CONFIG_PATH=./
    export CK8S_ENVIRONMENT_NAME=<my-ck8s-cluster>
    export CK8S_CLOUD_PROVIDER=[exoscale|safespring|citycloud|elastx|aws|baremetal]
    export CK8S_FLAVOR=[dev|prod|air-gapped] # defaults to dev
    export CK8S_PGP_FP=<PGP-fingerprint> # retrieve with gpg --list-secret-keys
    export DOMAIN=example.com # your domain
    export CLUSTERS=( "sc" "wc" )
    ```

1. Add the Elastisys Compliant Kubernetes Kubespray repo as a `git submodule` to the configuration repo and install pre-requisites as follows:

    ```bash
    git submodule add https://github.com/elastisys/compliantkubernetes-kubespray.git
    git submodule update --init --recursive
    cd compliantkubernetes-kubespray
    pip3 install -r kubespray/requirements.txt  # this will install ansible
    ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass --connection local --inventory 127.0.0.1, get-requirements.yaml
    ```

1. Add the Compliant Kubernetes Apps repo as a `git submodule` to the configuration repo and install pre-requisites as follows:

    ```bash
    git submodule add https://github.com/elastisys/compliantkubernetes-apps.git
    cd compliantkubernetes-apps
    ./bin/ck8s install-requirements
    ```

1. Create the domain name.
    You need to create a domain name to access the different services in your environment. You will need to set up the following DNS entries.

    - Point these domains to the Workload Cluster Ingress Controller (this step is done during Compliant Kubernetes Apps installation):
      - `*.$DOMAIN`
    - Point these domains to the Management Cluster Ingress Controller (this step is done during Compliant Kubernetes Apps installation):
      - `*.ops.$DOMAIN`
      - `dex.$DOMAIN`
      - `grafana.$DOMAIN`
      - `harbor.$DOMAIN`
      - `opensearch.$DOMAIN`

    ???+note "If both Management and Workload Clusters are in the same subnet"

        If both the Management and Workload Clusters are in the same subnet, it would be great to configure the following domain names to the private IP addresses of Management Cluster's worker nodes.

        - `*.thanos.ops.$DOMAIN`
        - `*.opensearch.ops.$DOMAIN`

1. Create S3 credentials and add them to `.state/s3cfg.ini`.

1. Set up load balancer

    You need to set up two load balancers, one for the Workload Cluster and one for the Management Cluster.

1. Make sure you have [all necessary tools](getting-started.md).

## Deploying Compliant Kubernetes using Kubespray

???+note "How to change Default Kubernetes Subnet Address"

    If  the default IP block ranges used for Docker and Kubernetes are the same as the internal IP ranges used in the company, you can change the values  to resolve the conflict as follows. Note that you can use any valid private IP address range, the values below are put as an example.

    === "For Kubernetes"

        ``` markdown
        * For Management Cluster: Add `kube_service_addresses: 10.178.0.0/18` and `kube_pods_subnet: 10.178.120.0/18` in `${CK8S_CONFIG_PATH}/sc-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml` file.
        * For Workload Cluster:  Add `kube_service_addresses: 10.178.0.0/18` and `kube_pods_subnet: 10.178.120.0/18` in `${CK8S_CONFIG_PATH}/wc-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml` file.
        ```

    === "For Docker"

        ``` markdown
        * For Management Cluster: Added `docker_options: "--default-address-pool base=10.179.0.0/24,size=24"` in `${CK8S_CONFIG_PATH}/sc-config/group_vars/all/docker.yml` file.
        * For Workload Cluster:  Added `docker_options: "--default-address-pool base=10.179.4.0/24,size=24"` in `${CK8S_CONFIG_PATH}/wc-config/group_vars/all/docker.yml` file.
        ```

### Init Kubespray config in your config path

```bash
for CLUSTER in ${CLUSTERS[@]}"; do
    compliantkubernetes-kubespray/ck8s-kubespray init $CLUSTER $CK8S_CLOUD_PROVIDER $CK8S_PGP_FP
done
```

### Configure OIDC

To configure OpenID access for Kubernetes API and other services, Dex should be configured with your identity provider (IdP). Check what Dex needs from [your identity provider](https://dexidp.io/docs/connectors/).

#### Configure OIDC endpoint

The Management Cluster is recommended to be configured with an external OIDC endpoint provided by the IdP of your choice. This can be configured in `${CK8S_CONFIG_PATH}/sc-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml` by setting the following variables:

- `kube_oidc_auth` should be set to true, this enables OIDC authentication for the api-server
- `kube_oidc_url` should be set to an OIDC endpoint from your IdP (e.g. for Google this would be `https://accounts.google.com`)
- `kube_oidc_client_id` should be retrieved from your IdP
- `kube_oidc_client_secret` should be retrieved from your IdP

To configure the Workload Cluster to use Dex running in the Management Cluster for authentication you will also need to configure the following in `${CK8S_CONFIG_PATH}/wc-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml`:

- `kube_oidc_auth` should be set to true, this enables OIDC authentication for the api-server
- `kube_oidc_url` should be set to `https://dex.$DOMAIN`
- `kube_oidc_client_id` should be set to `kubelogin`
- `kube_oidc_client_secret` should be set to a Dex client secret generated with the apps config, it can be found in `${CK8S_CONFIG_PATH}/secrets.yaml` under the key `dex.kubeloginClientSecret` after running `ck8s init` (see [instructions on deploying apps](#deploying-compliant-kubernetes-apps)).

To generate kubeconfigs that use OIDC for authentication, the following variables should be set in the config files for both clusters (both can't be true):

```yaml
create_oidc_kubeconfig: true
kubeconfig_localhost: false
```

For more information on managing OIDC kubeconfigs and RBAC, or on running without OIDC, [see the ck8s-Kubespray documentation](https://github.com/elastisys/compliantkubernetes-kubespray#kubeconfig).

### Copy the VMs information to the inventory files

Add the host name, user and IP address of each VM that you prepared above in `${CK8S_CONFIG_PATH}/sc-config/inventory.ini`for Management Cluster and `${CK8S_CONFIG_PATH}/sc-config/inventory.ini` for Workload Cluster. Moreover, you also need to add the host names of the master nodes under `[kube_control_plane]`, etcd nodes under `[etcd]` and worker nodes under `[kube_node]`.

!!! note

    Make sure that the user has SSH access to the VMs.

### Run Kubespray to deploy the Kubernetes clusters

```bash
for CLUSTER in "${CLUSTERS[@]}"; do
    compliantkubernetes-kubespray/bin/ck8s-kubespray apply $CLUSTER --flush-cache
done
```

!!! info

    The kubeconfig for wc `.state/kube_config_wc.yaml` will not be usable until you have installed dex in the Management Cluster (by [deploying apps](#deploying-compliant-kubernetes-apps)).

## Rook Block Storage

Normally, we want to use block storage solutions provided by the infra provider. However, this is not always available, especially for on-prem environments. In such cases we can partition separate volumes on nodes in the cluster for Rook-Ceph and use that as a block storage solution.

{%
    include "./common.md"
    start="<!--deploy-rook-start-->"
    end="<!--deploy-rook-stop-->"
%}

{%
    include "./common.md"
    start="<!--test-rook-start-->"
    end="<!--test-rook-stop-->"
%}

## Deploying Compliant Kubernetes Apps

???+note "How to change local DNS IP if you change the default Kubernetes subnet address"

    You need to change the default coreDNS default IP address in `common-config.yaml` file if  you change the default IP block  used for Kubernetes services above.  To get the coreDNS IP address, run the following commands.

    ```bash
    ${CK8S_CONFIG_PATH}/compliantkubernetes-apps/bin/ck8s ops kubectl sc get svc -n kube-system coredns
    ```
    Once you get the IP address edit `${CK8S_CONFIG_PATH}/common-config.yaml` file  and set  the value  to `global.clusterDns` field.

???+note "Configure the load balancer IP on the loopback interface for each worker node"

    The Kubernetes data plane nodes (i.e., worker nodes) cannot connect to themselves with the IP address of the load balancer that fronts them. The easiest is to configure the load balancer's IP address on the loopback interface of each nodes. Create `/etc/netplan/20-eip-fix.yaml` file and add the following to it. `${loadblancer_ip_address}` should be replaced with the IP address of the load balancer for each cluster.

    ```yaml
    network:
      version: 2
      ethernets:
        lo0:
          match:
            name: lo
          dhcp4: false
          addresses:
          - ${loadblancer_ip_address}/32
    ```
    After adding the above content, run the following command in each worker node:

    ```bash
    sudo netplan apply
    ```

{%
    include "./common.md"
    start="<!--init-apps-start-->"
    end="<!--init-apps-stop-->"
%}

{%
    include "./common.md"
    start="<!--configure-apps-start-->"
    end="<!--configure-apps-stop-->"
%}

{%
    include "./common.md"
    start="<!--create-s3-buckets-start-->"
    end="<!--create-s3-buckets-stop-->"
%}

{%
    include "./common.md"
    start="<!--install-apps-start-->"
    end="<!--install-apps-stop-->"
%}

{%
    include "./common.md"
    start="<!--settling-start-->"
    end="<!--settling-stop-->"
%}

{%
    include "./common.md"
    start="<!--testing-start-->"
    end="<!--testing-stop-->"
%}

### Operate

The following endpoints can be probed to ensure Compliant Kubernetes services are up and running:

```bash
curl --head https://dex.$DOMAIN/healthz
curl --head https://harbor.$DOMAIN/healthz
curl --head https://grafana.$DOMAIN/healthz
curl --head https://grafana.ops.$DOMAIN/healthz
curl --head app.$DOMAIN/healthz  # Pokes the WC Ingress Controller
curl --head app.ops.$DOMAIN/healthz  # Pokes the SC Ingress Controller
# All commands above should return 'HTTP/2 200'

curl --head -k https://kube-apiserver.$DOMAIN
curl --head https://notary.harbor.$DOMAIN
curl --head https://thanos-receiver.ops.$DOMAIN
curl --head https://opensearch.ops.$DOMAIN
curl --head https://opensearch.$DOMAIN/api/status
# The commands above should return 'HTTP/2 401'
```

!!! note

    Some of these subdomains can be overwritten in config (see example [here](https://github.com/elastisys/compliantkubernetes-apps/blob/v0.33.0/config/config/common-config.yaml#L260))
