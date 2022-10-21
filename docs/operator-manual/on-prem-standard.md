# Standard Template for on-prem Environment

This document contains instructions on how to set-up a new Compliant Kubernetes on-prem environment.

## Prerequisites

!!! Decision

    Decisions regarding the following items should be made before venturing on deploying Compliant Kubernetes.

    - Overall architecture, i.e., VM sizes, load-balancer configuration, storage configuration, etc.
    - Identity Provider (IdP) choice and configuration
    - On-call Management Tool (OMT) choice and configuration

1. Prepare Ubuntu-based VMs:
    If you are using public clouds, you can create VMs using the scripts included in Kubespray:
    - For Azure, use [AzureRM scripts](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/azurerm).
    - For other clouds, use their respective [Terraform scripts](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform).

1. Create a git working folder to store Compliant Kubernetes configurations in a version-controlled manner. Run the following commands from the root of the config repo.

    !!! note
        The following steps are done from the root of the git repository you created for the cofigurations.

    !!! note 
    
        You can choose names for your service cluster and workload cluster by changing the values for `SERVICE_CLUSTER` and `WORKLOAD_CLUSTERS` respectively.

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
    - Point these domains to the service cluster ingress controller (this step is done during Compliant Kubernetes app installation):
        - `*.ops.example.com`
        - `dex.example.com`
        - `grafana.example.com`
        - `harbor.example.com`
        - `opensearch.example.com`

    ???+ "If both service and workload clusters are in the same subnet"

        If both the service and workload clusters are in the same subnet, it would be greate to configure the following domain names to the private IP addresses of the respective services. (Replace `example.com` with your domain name.)

        - `*.thanos.ops.example.com`
        - `*.opensearch.ops.example.com`

1. Create S3 credentials and add them to `.state/s3cfg.ini`.

1. Set up load balancer

    You need to set up two load balancers, one for the workload cluster and one for the service cluster.

1. Make sure you have [all necessary tools](https://elastisys.io/compliantkubernetes/operator-manual/getting-started/).

## Deploying Compliant Kubernetes using Kubespray

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

Add the host name, user and IP address of each VM that you prepared above in `${CK8S_CONFIG_PATH}/sc-config/inventory.ini`for service cluster and `${CK8S_CONFIG_PATH}/sc-config/inventory.ini` for workload cluster. Moreover, you also need to add the host names of the master nodes under `[kube_control_plane]`, etdc nodes under `[etcd]` and worker nodes under `[kube_node]`.

  !!! note
    Make sure that the user has SSH access to the VMs.

### Run Kubespray to deploy the Kubernetes clusters

```bash
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS}; do
    compliantkubernetes-kubespray/bin/ck8s-kubespray apply $CLUSTER --flush-cache
done
```

!!! note
    The kubeconfig for wc `.state/kube_config_wc.yaml` will not be usable until you have installed dex in the service cluster (by deploying apps).

### Set up Rook

_Only for cloud providers that doesn't natively support storage kubernetes._

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
    The default configuration for the service cluster and workload cluster are available in the directory `${CK8S_CONFIG_PATH}/defaults/` and can be used as a reference for available options.

!!! warning
    Do not modify the read-only default configurations files found in the directory `${CK8S_CONFIG_PATH}/defaults/`. Instead configure the cluster by modifying the regular files `${CK8S_CONFIG_PATH}/sc-config.yaml` and `${CK8S_CONFIG_PATH}/wc-config.yaml` as they will override the default options.

### Create S3 buckets

You can use the following command to create the required S3 buckets. The command uses `s3cmd` in the background and gets configuration and credentials for your S3 provider from the `~/.s3cfg` file.

```bash
compliantkubernetes-apps/bin/ck8s s3cmd create
```

### Install Compliant Kubernetes apps

This will set up apps, first in the service cluster and then in the workload cluster:

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

Start with the service cluster:

```bash
compliantkubernetes-apps/bin/ck8s test sc
```

Then the workload clusters:

```bash
compliantkubernetes-apps/bin/ck8s test wc
```
