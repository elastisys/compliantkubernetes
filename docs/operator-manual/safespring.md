# Compliant Kubernetes Deployment on Safespring

This document contains instructions on how to set up a Compliant Kubernetes environment (consisting of a service cluster and one or more workload clusters) on Safespring.

!!!note
    This guide is written for compliantkubernetes-apps [v0.13.0](https://github.com/elastisys/compliantkubernetes-apps/tree/v0.13.0)

TODO: The document is split into two parts:

- Cluster setup (setting up infrastructure and the Kubernetes clusters).
  We will be using the [Terraform module for Openstack that can be found in the Kubespray repository](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack).
  Please refer to it if you need more details about this part of the setup.

- Apps setup (including information about limitations)

Before starting, make sure you have [all necessary tools](getting-started.md). In addition to these general tools, you will also need:

- [Openstack credentials](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack#openstack-access-and-credentials) (either using `openrc` or the `clouds.yaml` configuration file) for setting up the infrastructure.

- For Safespring, you can get these by logging into the Safespring Openstack dashboard and download either the `clouds.yaml` or `OpenRC` file from the API Access page.

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

We recommend you to have at least three worker nodes with 4 cores and 8 GB memory each, and we recommend you to have at least 2 cores and 4 GB for your control plane nodes.

Below is example `cluster.tfvars` for a few select openstack providers.
The examples are copy-pastable, but you might want to change `cluster_name` and `network_name` (if neutron is used!).

=== "Safespring sto1 with public IPs assigned to VMs (no floating IP)"

    ``` hcl
    # your Kubernetes cluster name here
    cluster_name = "your-cluster-name"

    # image to use for bastion, masters, standalone etcd instances, and nodes
    image = "ubuntu-20.04"

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

    use_server_groups = true # Comment this out if you don't mind that the VMs are schedules on different physical machines
                             # Also, comment this out if you run into problems on Safespring because of shortage of physical machines
    ```
    
=== "Safespring sto1 with private IPs and floating IPs assigned to VMs"

For this to work, make sure that you can create networks and floating IPs on Safespring.
    
        ``` hcl
        # your Kubernetes cluster name here
        cluster_name = "your-cluster-name"
    
        # image to use for bastion, masters, standalone etcd instances, and nodes
        image = "ubuntu-20.04"
    
        # 0|1 bastion nodes
        number_of_bastions = 0
    
        use_neutron = 0
    
        # standalone etcds
        number_of_etcd = 0
    
        # masters
        number_of_k8s_masters = 1
        number_of_k8s_masters_no_etcd = 0
        number_of_k8s_masters_no_floating_ip = 0
        number_of_k8s_masters_no_floating_ip_no_etcd = 0
        flavor_k8s_master = "8a707999-0bce-4f2f-8243-b4253ba7c473"
    
        # nodes
        number_of_k8s_nodes = 3
        number_of_k8s_nodes_no_floating_ip = 0
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
        network_name = "private" # Change this if you would like a new network to be created
    
        use_server_groups = true # Comment this out if you don't mind that the VMs are schedules on different physical machines
                                 # Also, comment this out if you run into problems on Safespring because of shortage of physical machines
        ```

### Expose Openstack credentials to Terraform

Terraform will need access to Openstack credentials in order to create the infrastructure.
More details can be found [here](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack#openstack-access-and-credentials).

We will be using the declarative option with the `clouds.yaml` file.
Since this file can contain credentials for multiple environments, we specify the name of the one we want to use in the environment variable `OS_CLOUD`:

```bash
export OS_CLOUD=<name-of-openstack-cloud-environment>
```

If you use the `clouds.yaml` file copy it in the `compliantkubernetes-kubespray/kubespray/contrib/terraform/openstack/` and edit the file to add your password `password: your-safespring-openstack-password` in the `auth:` section.

Alternatively, using the `openrc` file:

`source /path/to/your/openrc/file`

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

For cloud provider integration, you have a few options [as described here](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/openstack.md#the-external-cloud-provider).
We will be going with the external cloud provider and simply source the Openstack credentials.
See below for how to modify the variables that need to be modified.

### Setting up Kubespray variables

In `${CK8S_CONFIG_PATH}/$CLUSTER-config/group_vars/k8s_cluster/ck8s-k8s-cluster-openstack.yaml`, the default variables should look like this:

```yaml
etcd_kubeadm_enabled: true

cloud_provider: external
external_cloud_provider: openstack
calico_mtu: 1480

external_openstack_cloud_controller_extra_args:
  # Must be different for every cluster in the same openstack project
  cluster-name: "set-me"

cinder_csi_enabled: true
persistent_volumes_enabled: true
expand_persistent_volumes: true
openstack_blockstorage_ignore_volume_az: true

storage_classes:
  - name: cinder-csi
    is_default: true
    parameters:
      allowVolumeExpansion: true
      availability: nova
```

`cluster-name` should be set to a name that is unique in the Openstack project you're deploying your clusters in. If you don't have any other clusters in the project, just make sure that the service cluster and workload clusters have different names.

Cinder CSI is enabled by default along with the configuration options to enable persistent volumes and the expansion of these volumes. It is also set to ignore the volume availability zone to allow volumes to attach to nodes in different or mismatching zones. The default works well with both CityCloud and SafeSpring.

If you want to set up LBaaS in your cluster, you can add the following config:

```yaml
external_openstack_lbaas_create_monitor: false
external_openstack_lbaas_monitor_delay: "1m"
external_openstack_lbaas_monitor_timeout: "30s"
external_openstack_lbaas_monitor_max_retries: "3"
external_openstack_lbaas_provider: octavia
external_openstack_lbaas_use_octavia: true
# external_openstack_lbaas_network_id: "Neutron network ID to create LBaaS VIP"
external_openstack_lbaas_subnet_id: "Neutron subnet ID to create LBaaS VIP"
external_openstack_lbaas_floating_network_id: "Neutron network ID to get floating IP from"
# external_openstack_lbaas_floating_subnet_id: "Neutron subnet ID to get floating IP from"
external_openstack_lbaas_method: "ROUND_ROBIN"
external_openstack_lbaas_manage_security_groups: false
external_openstack_lbaas_internal_lb: false
```

The `network_id` and `subnet_id` variables need to be set by you, depending on whether or not you used floating IP. `network_id` should match the `external_net` variable in your Terraform variables, whereas the `subnet_id` should match the subnet ID that Terraform outputs after it is applied.

Additionally, when you later set up `compliantkubernetes-apps` in your cluster, you should set `ingressNginx.controller.service.enabled` to `true` and `ingressNginx.controller.service.type` to `LoadBalancer` in both your `sc-config.yaml` and `wc-config.yaml`. Use the IP of the `ingress-nginx-controller` service in your cluster when you set up your DNS.

!!!note
    At this point if the cluster is running on Safespring and you are using `kubespray v2.17.0+` it is possible to create an application credential.
    Which will give the cluster its own set of credentials instead of using your own.

    To create a set of credentials use the following command:
    `openstack application credential create <name>`

    And set the following environment variables

    ```console
    export OS_APPLICATION_CREDENTIAL_NAME: <name>
    export OS_APPLICATION_CREDENTIAL_ID: <project_id>
    export OS_APPLICATION_CREDENTIAL_SECRET: <secret>
    ```

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

### Create the DNS Records

You will need to setup a number of DNS entries for traffic to be routed correctly.
Determine the public IP of one or more of the nodes in the service cluster.
Then point these domains to the services.

Since Safespring does not have a domain name service, use alternatives such as AWS Route53.

## Deploying Compliant Kubernetes Apps

{%
   include-markdown "common.md"
   start="<!--clone-apps-start-->"
   end="<!--clone-apps-stop-->"
   comments=false
%}

{%
   include-markdown "common.md"
   start="<!--init-apps-start-->"
   end="<!--init-apps-stop-->"
   comments=false
%}

{%
   include-markdown "common.md"
   start="<!--configure-apps-start-->"
   end="<!--configure-apps-stop-->"
   comments=false
%}

The following are the minimum change you should perform:

```yaml
# ${CK8S_CONFIG_PATH}/sc-config.yaml and ${CK8S_CONFIG_PATH}/wc-config.yaml
global:
  baseDomain: "set-me"  # set to $CK8S_ENVIRONMENT_NAME.$DOMAIN
  opsDomain: "set-me"  # set to ops.$CK8S_ENVIRONMENT_NAME.$DOMAIN
  issuer: letsencrypt-prod

objectStorage:
  type: "s3"
  s3:
    region: "set-me"  # Region for S3 buckets, e.g, west-1
    regionEndpoint: "set-me"  # e.g., https://s3.us-west-1.amazonaws.com

storageClasses:
  default:  cinder-csi
  nfs:
    enabled: false
  cinder:
    enabled: true
  local:
    enabled: false
  ebs:
    enabled: false

```

```yaml
# ${CK8S_CONFIG_PATH}/sc-config.yaml (in addition to the changes above)
ingressNginx:
    controller:
      service:
        type: "this-is-not-used"
        annotations: "this-is-not-used"

harbor:
  oidc:
    groupClaimName: "set-me" # set to group claim name used by OIDC provider

issuers:
  letsencrypt:
    prod:
      email: "set-me"  # set this to an email to receive LetsEncrypt notifications
    staging:
      email: "set-me"  # set this to an email to receive LetsEncrypt notifications
```

Edit ${CK8S_CONFIG_PATH}/secrets.yaml with sops

`sops ${CK8S_CONFIG_PATH}/secrets.yaml`

```yaml
# ${CK8S_CONFIG_PATH}/secrets.yaml
objectStorage:
  s3:
    accessKey: "set-me" # set to your s3 accesskey
    secretKey: "set-me" # set to your s3 secretKey
```

### Create S3 buckets

Create object storage buckets for backups and container registry storage (if desired).

For this you need to obtain access keys from Safespring to be able to create S3 buckets.

```
cd compliantkubernetes-apps
git checkout v0.17.0
AWS_ACCESS_KEY=set-me
AWS_ACCESS_SECRET_KEY=set-me
scripts/S3/generate-s3cfg.sh safespring ${AWS_ACCESS_KEY} ${AWS_ACCESS_SECRET_KEY} s3.sto2.safedc.net sto2 > ~/.s3cfg
scripts/S3/entry.sh create
```

{%
   include-markdown "common.md"
   start="<!--test-s3-buckets-start-->"
   end="<!--test-s3-buckets-stop-->"
   comments=false
%}

### Prepare for Compliant Kubernetes Apps

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

##### Edit the storage class manifests 

```
./bin/ck8s ops kubectl sc edit storageclass cinder-csi
./bin/ck8s ops kubectl wc edit storageclass cinder-csi
```

Set storageclass.kubernetes.io/is-default-class: "true"

### Install Compliant Kubernetes Apps!

Start with the service cluster:

```
ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${SERVICE_CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_sc.yaml
./bin/ck8s apply sc  # Respond "n" if you get a WARN
```

Then the workload clusters:

```
for CLUSTER in "${WORKLOAD_CLUSTERS[@]}"; do
    ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_wc.yaml
    ./bin/ck8s apply wc  # Respond "n" if you get a WARN
done
```

<!--settling-start-->
### Settling

!!!important
    Leave sufficient time for the system to settle, e.g., request TLS certificates from LetsEncrypt, perhaps as much as 20 minutes.

You can check if the system settled as follows:

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} get --all-namespaces pods'
done
```

Check the output of the command above. All Pods needs to be Running or Completed.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} get --all-namespaces issuers,clusterissuers,certificates'
done
```

Check the output of the command above.
All resources need to have the Ready column True.
<!--settling-stop-->

<!--testing-start-->
### Testing

After completing the installation step you can test if the apps are properly installed and ready using the commands below.

Start with the service cluster:

```bash
ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${SERVICE_CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_sc.yaml
./bin/ck8s test sc  # Respond "n" if you get a WARN
```

Then the workload clusters:

```bash
for CLUSTER in "${WORKLOAD_CLUSTERS[@]}"; do
    ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_wc.yaml
    ./bin/ck8s test wc  # Respond "n" if you get a WARN
done
```

Done.
Navigate to the endpoints, for example `grafana.$BASE_DOMAIN`, `kibana.$BASE_DOMAIN`, `harbor.$BASE_DOMAIN`, etc. to discover Compliant Kubernetes's features.
<!--testing-stop-->

<!--clean-apps-start-->
### Removing Compliant Kubernetes Apps from your cluster

To remove the applications added by compliant kubernetes you can use the two scripts `clean-sc.sh` and `clean-wc.sh`, they are located here in the [scripts folder](https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts).

They perform the following actions:

1. Delete the added helm charts
1. Delete the added namespaces
1. Delete any remaining PersistentVolumes
1. Delete the added CustomResourceDefinitions

Note: if user namespaces are managed by Compliant Kubernetes apps then they will also be deleted if you clean up the workload cluster.
<!--clean-apps-stop-->

## Remove the infrastructure

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
