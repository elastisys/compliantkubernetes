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
    - Identity Provider (IdP) choice and configuration. See [this blog post](https://elastisys.com/connect-your-idp-to-your-compliant-kubernetes-cluster/).
    - On-call Management Tool (OMT) choice and configuration

1. Prepare Ubuntu-based VMs:
    If you are using public clouds, you can create VMs using the scripts included in Kubespray:
    - For Azure, use [AzureRM scripts](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/azurerm).
    - For other clouds, use their respective [Terraform scripts](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform).

1. Create a git working folder to store Compliant Kubernetes configurations in a version-controlled manner. Run the following commands from the root of the config repo.

    !!! note
        The following steps are done from the root of the git repository you created for the cofigurations.

    !!! note
        You can choose names for your Management Cluster and workload cluster by changing the values for `SERVICE_CLUSTER` and `WORKLOAD_CLUSTERS` respectively.

    ```bash
    export CK8S_CONFIG_PATH=./
    export CK8S_ENVIRONMENT_NAME=<my-ck8s-cluster>
    export CK8S_CLOUD_PROVIDER=[exoscale|safespring|citycloud|elastx|aws|baremetal]
    export CK8S_FLAVOR=[dev|prod] # defaults to dev
    export CK8S_PGP_FP=<PGP-fingerprint> # retrieve with gpg --list-secret-keys
    SERVICE_CLUSTER="sc"
    WORKLOAD_CLUSTERS="wc"
    ```

1. Add the Elastisys Compliant Kubernetes Kubespray repo as `git submodule` to the configuration repo as follows:

    ```bash
    git submodule add  https://github.com/elastisys/compliantkubernetes-kubespray
    git submodule update --init --recursive

    ```

1. Add compliantkubernetes-apps as `git submodule` to the configuration repo and install pre-requisites as follows:

    ```bash
    https://github.com/elastisys/compliantkubernetes-apps.git
    cd compliantkubernetes-apps
    ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass --connection local --inventory 127.0.0.1, get-requirements.yaml
    ```

1. Create the domain name.
    You need to create a domain name to access the different services in your environment. You will need to set up the following DNS entries (replace `example.com` with your domain name).
    - Point these domains to the workload cluster ingress controller (this step is done during Compliant Kubernetes app installation):
        - `*.example.com`
    - Point these domains to the Management Cluster ingress controller (this step is done during Compliant Kubernetes app installation):
        - `*.ops.example.com`
        - `dex.example.com`
        - `grafana.example.com`
        - `harbor.example.com`
        - `opensearch.example.com`

    ???+note "If both service and workload clusters are in the same subnet"

        If both the service and workload clusters are in the same subnet, it would be great to configure the following domain names to the private IP addresses of Management Cluster's worker nodes. (Replace `example.com` with your domain name.)

        - `*.thanos.ops.example.com`
        - `*.opensearch.ops.example.com`

1. Create S3 credentials and add them to `.state/s3cfg.ini`.

1. Set up load balancer

    You need to set up two load balancers, one for the workload cluster and one for the Management Cluster.

1. Make sure you have [all necessary tools](getting-started.md).

## Deploying Compliant Kubernetes using Kubespray


???+note "How to change Default Kubernetes Subnet Address"

    If  the default IP block ranges used for Docker and Kubernetes are the same as the internal IP ranges used in the company, you can change the values  to resolve the conflict as follows. Note that you can use any valid private IP address range, the values below are put as an example.

    === "For Kubernetes"

        ``` markdown
        * For Management Cluster: Add `kube_service_addresses: 10.178.0.0/18` and `kube_pods_subnet: 10.178.120.0/18` in `${CK8S_CONFIG_PATH}/sc-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml` file.
        * For workload cluster:  Add `kube_service_addresses: 10.178.0.0/18` and `kube_pods_subnet: 10.178.120.0/18` in `${CK8S_CONFIG_PATH}/wc-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml` file.
        ```

    === "For Docker"

        ``` markdown
        * For Management Cluster: Added `docker_options: "--default-address-pool base=10.179.0.0/24,size=24"` in `${CK8S_CONFIG_PATH}/sc-config/group_vars/all/docker.yml` file.
        * For workload cluster:  Added `docker_options: "--default-address-pool base=10.179.4.0/24,size=24"` in `${CK8S_CONFIG_PATH}/wc-config/group_vars/all/docker.yml` file.
        ```

### Init Kubespray config in your config path.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "{WORKLOAD_CLUSTERS}"; do
compliantkubernetes-kubespray/ck8s-kubespray init $CLUSTER $CK8S_CLOUD_PROVIDER $CK8S_PGP_FP
done
```

### Configure OIDC

To configure OpenID access for Kubernetes API and other services, Dex should be configured with your identity provider. Check what Dex needs from [your identity provider](https://dexidp.io/docs/connectors/).

#### Configure OIDC endpoint

Set `kube_oidc_url` in `${CK8S_CONFIG_PATH}/sc-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml` and `${CK8S_CONFIG_PATH}/wc-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml` based on your cluster. For example, if your domain is `example.com` then kube_oidc_url is set as `kube_oidc_url: https://dex.example.com` in both files.

### Copy the VMs information to the inventery files

Add the host name, user and IP address of each VM that you prepared above in `${CK8S_CONFIG_PATH}/sc-config/inventory.ini`for Management Cluster and `${CK8S_CONFIG_PATH}/sc-config/inventory.ini` for workload cluster. Moreover, you also need to add the host names of the master nodes under `[kube_control_plane]`, etdc nodes under `[etcd]` and worker nodes under `[kube_node]`.

!!! note
    Make sure that the user has SSH access to the VMs.

### Run Kubespray to deploy the Kubernetes clusters

```bash
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS}; do
    compliantkubernetes-kubespray/bin/ck8s-kubespray apply $CLUSTER --flush-cache
done
```

!!! note
    The kubeconfig for wc `.state/kube_config_wc.yaml` will not be usable until you have installed dex in the Management Cluster (by deploying apps).

### Set up Rook

_Only for Infrastructure Providers that doesn't natively support storage kubernetes._

Run the following command to set up Rook.

```bash
 for CLUSTER in  sc wc; do
     sops --decrypt ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml > $CLUSTER.yaml
     export KUBECONFIG=$CLUSTER.yaml
     compliantkubernetes-kubespray/rook/deploy-rook.sh
 done
```

Please restart the operator pod, `rook-ceph-operator*`, if some pods stall in the initialization state as shown below:

```bash
rook-ceph     rook-ceph-crashcollector-minion-0-b75b9fc64-tv2vg    0/1     Init:0/2   0          24m
rook-ceph     rook-ceph-crashcollector-minion-1-5cfb88b66f-mggrh   0/1     Init:0/2   0          36m
rook-ceph     rook-ceph-crashcollector-minion-2-5c74ffffb6-jwk55   0/1     Init:0/2   0          14m
```

!!!important
    Pods in pending state usually indicate resource shortage. In such cases you need to use bigger instances.
<!--deploy-rook-stop-->

<!--test-rook-start-->
### Test Rook

To test Rook, proceed as follows:

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml 'kubectl --kubeconfig {} apply -f https://raw.githubusercontent.com/rook/rook/release-1.5/cluster/examples/kubernetes/ceph/csi/rbd/pvc.yaml';
done

for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml 'kubectl --kubeconfig {} get pvc';
done
```

You should see PVCs in `Bound` state. If you want to clean the previously created PVCs:

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml 'kubectl --kubeconfig {} delete pvc rbd-pvc';
done
```
## Deploying Compliant Kubernetes Apps

???+note "How to change local DNS IP if you change the default Kubebernetes subnet address"

    You need to change the default coreDNS default IP address in `common-config.yaml` file if  you change the default IP block  used for Kubernetes services above.  To get the coreDNS IP address, run the following commands.

    ```bash
    ${CK8S_CONFIG_PATH}/compliantkubernetes-apps/bin/ck8s ops kubectl sc get svc -n kube-system coredns
    ```
    Once you get the IP address edit `${CK8S_CONFIG_PATH}/scommon-config.yaml` file  and set  the value  to `global.clusterDns` field.


???+note "Configure the load balancer IP on the loopback interface for each worker node"
    The Kubernetes data planenodes (i.e., worker nodes) cannot connect to themselves with the IP address of the load balancer that fronts them. The easiest is to configure the load balancer's IP address on the loopback interface of each nodes. Create `/etc/netplan/20-eip-fix.yaml` file and add the following to it. `${loadblancer_ip_address}` should be replaced with the IP address of the load balancer for each cluster.

    ```yaml
    network:
    version: 2
    ethernets:
        "lo:0":
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

### Initialize the apps configuration

```bash
compliantkubernetes-apps/bin/ck8s init
```

This will initialise the configuration in the `${CK8S_CONFIG_PATH}` directory. Generating configuration files `common-config.yaml`, `sc-config.yaml` and `wc-config.yaml`, as well as secrets with randomly generated passwords in `secrets.yaml`. This will also generate read-only default configuration under the directory `defaults/` which can be used as a guide for available and suggested options.

### Configure the apps and secrets

The configuration files contain some predefined values. You may want to check and edit based on your current environment requirements. The configuration files that require editing are `${CK8S_CONFIG_PATH}/common-config.yaml`, `${CK8S_CONFIG_PATH}/sc-config.yaml`, `${CK8S_CONFIG_PATH}/wc-config.yaml` and `${CK8S_CONFIG_PATH}/secrets.yaml` and set the appropriate values for some of the configuration fields.
Note that, the latter is encrypted.

```bash
vim ${CK8S_CONFIG_PATH}/sc-config.yaml

vim ${CK8S_CONFIG_PATH}/wc-config.yaml

vim ${CK8S_CONFIG_PATH}/common-config.yaml
```

Edit the secrets.yaml file and add the credentials for:

- s3 - used for backup storage
- dex - connectors -- check [your indentiy provider](https://dexidp.io/docs/connectors/).
- On-call management tool configurations-- Check [supported on-call management tools](https://prometheus.io/docs/alerting/latest/configuration/)

```bash
sops ${CK8S_CONFIG_PATH}/secrets.yaml
```

!!! tip
    The default configuration for the Management Cluster and workload cluster are available in the directory `${CK8S_CONFIG_PATH}/defaults/` and can be used as a reference for available options.

!!! warning
    Do not modify the read-only default configurations files found in the directory `${CK8S_CONFIG_PATH}/defaults/`. Instead configure the cluster by modifying the regular files `${CK8S_CONFIG_PATH}/sc-config.yaml` and `${CK8S_CONFIG_PATH}/wc-config.yaml` as they will override the default options.

### Create S3 buckets

You can use the following command to create the required S3 buckets. The command uses `s3cmd` in the background and gets configuration and credentials for your S3 provider from the `~/.s3cfg` file.

```bash
compliantkubernetes-apps/bin/ck8s s3cmd create
```

### Install Compliant Kubernetes apps

This will set up apps, first in the Management Cluster and then in the workload cluster:

```bash
compliantkubernetes-apps/bin/ck8s apply sc
compliantkubernetes-apps/bin/ck8s apply wc
```

### Settling

!!! info
    Leave sufficient time for the system to settle, e.g., request TLS certificates from LetsEncrypt, perhaps as much as 20 minutes.

Check if all helm charts succeeded.

```bash
compliantkubernetes-apps/bin/ck8s ops helm wc list -A --all
```

You can check if the system settled as follows.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
 compliantkubernetes-apps/bin/ck8s ops kubectl $CLUSTER get --all-namespaces pods
done
```

Check the output of the command above. All Pods need to be `Running` or `Completed` status.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
  compliantkubernetes-apps/bin/ck8s ops kubectl $CLUSTER get --all-namespaces issuers,clusterissuers,certificates
done
```

Check the output of the command above.
All resources need to have the `Ready` column `True`.

### Testing

After completing the installation step you can test if the apps are properly installed and ready using the commands below.

Start with the Management Cluster:

```bash
compliantkubernetes-apps/bin/ck8s test sc
```

Then the workload clusters:

```bash
compliantkubernetes-apps/bin/ck8s test wc
```
