{%
   include-markdown "common.md"
   start="<!--out-of-date-start-->"
   end="<!--out-of-date-stop-->"
   comments=false
%}

# Compliant Kubernetes on Openstack

This document contains instructions on how to set up a Compliant Kubernetes environment (consisting of a service cluster and one or more workload clusters) on Openstack.

1. Infrastructure setup for two clusters: one service and one workload cluster
2. Deploying Compliant Kubernetes on top of the two clusters.
3. Creating DNS Records
4. Deploying Compliant Kubernetes apps

Before starting, make sure you have [all necessary tools](getting-started.md). In addition to these general tools, you will also need:
- [Openstack credentials](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack#openstack-access-and-credentials) (either using `openrc` or the `clouds.yaml` configuration file) for setting up the infrastructure.

!!!note
    Although recommended OpenStack authentication method is `clouds.yaml`, it is more convenient to use the `openrc` method with Compliant Kubernetes as it works both with Kubespray and Terraform. If you are using the `clouds.yaml` method, at the moment, Kubespray will still expect you to set a few environment variables.

!!!note
    This guide is written for compliantkubernetes-apps [v0.17.0](https://github.com/elastisys/compliantkubernetes-apps/tree/v0.17.0)

## Setup

Choose names for your service cluster and workload cluster(s):

```bash
SERVICE_CLUSTER="sc"
WORKLOAD_CLUSTERS=( "wc0" "wc1" )

export CK8S_CONFIG_PATH=~/.ck8s/<environment-name>
export SOPS_FP=<PGP-fingerprint> # retrieve with gpg --list-secret-keys
```

## Infrastructure setup using Terraform

Before trying any of the steps, clone the Elastisys Compliant Kubernetes Kubespray repo as follows:
```bash
git clone --recursive https://github.com/elastisys/compliantkubernetes-kubespray
```

### Expose Openstack credentials to Terraform

Terraform will need access to Openstack credentials in order to create the infrastructure.
More details can be found [here](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/openstack#openstack-access-and-credentials).
We will be using the declarative option with the `open.rc` file.

Expose Openstack credentials to Terraform
For authentication create or download, from your provider, the file openstack-rc and `source path/to/your/openstack-rc`. The file should contain the following variables:
```bash
export OS_USERNAME=
export OS_PASSWORD=
export OS_AUTH_URL=
export OS_USER_DOMAIN_NAME=
export OS_PROJECT_DOMAIN_NAME=
export OS_REGION_NAME=
export OS_PROJECT_NAME=
export OS_TENANT_NAME=
export OS_AUTH_VERSION=
export OS_IDENTITY_API_VERSION=
export OS_PROJECT_ID=
```

### Customize your infrastructure

Start by initializing a Compliant Kubernetes environment using Compliant Kubernetes Kubespray.
All of this is done from the root of the `compliantkubernetes-kubespray` repository.

```bash
for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  ./bin/ck8s-kubespray init "${CLUSTER}" openstack "${SOPS_FP}"
done
```

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

The minimum infrastructure sizing requirements are at least three worker nodes with 4 cores and 8 GB memory each, and we recommend you to have at least 2 cores and 4 GB for your control plane nodes.

!!!note
    A recommended production infrastructure sizing is available in the [architecture diagram](https://compliantkubernetes.io/img/ck8s-c4model-level3.svg).

Below is example `cluster.tfvars` for a few select openstack providers.
The examples are copy-pastable, but you might want to change `cluster_name` and `network_name` (if neutron is used!).

=== "Citycloud Fra1"

    ``` hcl
    # your Kubernetes cluster name here
    cluster_name = "your-cluster-name"

    # list of availability zones available in your OpenStack cluster
    #az_list = ["nova"]

    # SSH key to use for access to nodes
    public_key_path = "~/.ssh/id_rsa.pub"

    # image to use for bastion, masters, standalone etcd instances, and nodes
    image = "Ubuntu 20.04 Focal Fossa 20200423"

    # user on the node (ex. core on Container Linux, ubuntu on Ubuntu, etc.)
    ssh_user = "ubuntu"

    # 0|1 bastion nodes
    number_of_bastions = 0

    # standalone etcds
    number_of_etcd = 0

    # masters
    number_of_k8s_masters = 1

    number_of_k8s_masters_no_etcd = 0

    number_of_k8s_masters_no_floating_ip = 0

    number_of_k8s_masters_no_floating_ip_no_etcd = 0

    # Flavor depends on your openstack installation
    # you can get available flavor IDs through `openstack flavor list`
    flavor_k8s_master = "89afeed0-9e41-4091-af73-727298a5d959""

    # nodes
    number_of_k8s_nodes = 3

    number_of_k8s_nodes_no_floating_ip = 0

    # Flavor depends on your openstack installation
    # you can get available flavor IDs through `openstack flavor list`
    flavor_k8s_node = "ecd976c3-c71c-4096-b138-e4d964c0b27f"

    # networking
    # ssh access to nodes
    k8s_allowed_remote_ips = ["0.0.0.0/0"]

    # List of CIDR blocks allowed to initiate an API connection
    master_allowed_remote_ips = ["0.0.0.0/0"]

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

    # use `openstack network list` to list the available external networks
    network_name = "name-of-your-network"

    # UUID of the external network that will be routed to
    external_net = "your-external-network-uuid"
    floatingip_pool = "ext-net"

    # If 1, nodes with floating IPs will transmit internal cluster traffic via floating IPs; if 0 private IPs will be used instead. Default value is 1.
    use_access_ip = 0

    # Create and use openstack nova servergroups, default: false
    use_server_groups = true

    subnet_cidr = "172.16.0.0/24"
    ```


=== "Citycloud Kna1"

    ``` hcl
    # your Kubernetes cluster name here
    cluster_name = "your-cluster-name"

    # list of availability zones available in your OpenStack cluster
    #az_list = ["nova"]

    # SSH key to use for access to nodes
    public_key_path = "~/.ssh/id_rsa.pub"

    # image to use for bastion, masters, standalone etcd instances, and nodes
    image = "Ubuntu 20.04 Focal Fossa 20200423"

    # user on the node (ex. core on Container Linux, ubuntu on Ubuntu, etc.)
    ssh_user = "ubuntu"

    # 0|1 bastion nodes
    number_of_bastions = 0

    # standalone etcds
    number_of_etcd = 0

    # masters
    number_of_k8s_masters = 1

    number_of_k8s_masters_no_etcd = 0

    number_of_k8s_masters_no_floating_ip = 0

    number_of_k8s_masters_no_floating_ip_no_etcd = 0

    # Flavor depends on your openstack installation
    # you can get available flavor IDs through `openstack flavor list`
    flavor_k8s_master = "96c7903e-32f0-421d-b6a2-a45c97b15665"

    # nodes
    number_of_k8s_nodes = 3

    number_of_k8s_nodes_no_floating_ip = 0

    # Flavor depends on your openstack installation
    # you can get available flavor IDs through `openstack flavor list`
    flavor_k8s_node = "572a3b2e-6329-4053-b872-aecb1e70d8a6"

    # networking
    # ssh access to nodes
    k8s_allowed_remote_ips = ["0.0.0.0/0"]

    # List of CIDR blocks allowed to initiate an API connection
    master_allowed_remote_ips = ["0.0.0.0/0"]

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
    # use `openstack network list` to list the available external networks
    network_name = "name-of-your-network"

    # UUID of the external network that will be routed to
    external_net = "your-external-network-uuid"
    floatingip_pool = "ext-net"

    # If 1, nodes with floating IPs will transmit internal cluster traffic via floating IPs; if 0 private IPs will be used instead. Default value is 1.
    use_access_ip = 0

    # Create and use openstack nova servergroups, default: false
    use_server_groups = true

    subnet_cidr = "172.16.0.0/24"
    ```

=== "Safespring sto1"

    ``` hcl
    # your Kubernetes cluster name here
    cluster_name = "your-cluster-name"

    # SSH key to use for access to nodes
    public_key_path = "~/.ssh/id_rsa.pub"

    # image to use for bastion, masters, standalone etcd instances, and nodes
    image = "ubuntu-20.04"

    # user on the node (ex. core on Container Linux, ubuntu on Ubuntu, etc.)
    ssh_user = "ubuntu"

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

    # Flavor depends on your openstack installation
    # you can get available flavor IDs through `openstack flavor list`
    flavor_k8s_master = "8a707999-0bce-4f2f-8243-b4253ba7c473"

    # nodes
    number_of_k8s_nodes = 0

    number_of_k8s_nodes_no_floating_ip = 3

    # Flavor depends on your openstack installation
    # you can get available flavor IDs through `openstack flavor list`
    flavor_k8s_node = "5b40af67-9d11-45ed-a44f-e876766160a5"

    # networking
    # ssh access to nodes
    k8s_allowed_remote_ips = ["0.0.0.0/0"]

    # List of CIDR blocks allowed to initiate an API connection
    master_allowed_remote_ips = ["0.0.0.0/0"]

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

    # use `openstack network list` to list the available external networks
    network_name = "public"

    # UUID of the external network that will be routed to
    external_net = "your-external-network-uuid"

    # If 1, nodes with floating IPs will transmit internal cluster traffic via floating IPs; if 0 private IPs will be used instead. Default value is 1.
    use_access_ip = 1

    # Create and use openstack nova servergroups, default: false
    use_server_groups = true

    subnet_cidr = "172.16.0.0/24"
    ```

### Initialize and apply Terraform

```bash
MODULE_PATH="$(pwd)/kubespray/contrib/terraform/openstack"

for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  pushd "${MODULE_PATH}"
  terraform init
  terraform apply -var-file="${CK8S_CONFIG_PATH}/${CLUSTER}-config/cluster.tfvars" -state="${CK8S_CONFIG_PATH}/${CLUSTER}-config/terraform.tfstate"
  popd
done
```

!!!warning
    The above will not work well if you are using a bastion host.
    This is due to [some hard coded paths](https://github.com/kubernetes-sigs/kubespray/blob/master/contrib/terraform/openstack/modules/compute/main.tf#L207).
    This is fixed in kubespray [release-2.17](https://github.com/kubernetes-sigs/kubespray/tree/release-2.17).
    If you are using an older version of kubespray, you may link the `kubespray/contrib` folder to the correct relative path, or make sure your `CK8S_CONFIG_PATH` is already at a proper place relative to the same.

## Deploying Compliant Kubernetes using Kubespray

Before we can run Kubespray, we will need to go through the relevant variables.
Additionally we will need to expose some credentials so that Kubespray can set up cloud provider integration.

You will need to change at least one value: `kube_oidc_url` in `${CK8S_CONFIG_PATH}/${CLUSTER}-config/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml`, normally this should be set to `https://dex.BASE_DOMAIN`.

For cloud provider integration, you have a few options [as described here](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/openstack.md#the-external-cloud-provider).
We will be going with the external cloud provider and simply source the Openstack credentials.

### Setting up Kubespray variables

Below are some examples for `${CK8S_CONFIG_PATH}/${CLUSTER}-config/group_vars/k8s_cluster/ck8s-k8s-cluster-openstack.yaml` for a few selected openstack providers. The examples are copy-pastable, but you will have to change some of the values.

=== "Citycloud Fra1"

    ``` hcl
    etcd_kubeadm_enabled: true

    cloud_provider: external
    external_cloud_provider: openstack
    calico_mtu: 1480

    cinder_csi_enabled: true
    persistent_volumes_enabled: true
    expand_persistent_volumes: true
    openstack_blockstorage_ignore_volume_az: true

    ## Cinder CSI is enabled by default along with the configuration options to enable persistent volumes and the expansion of these volumes.
    ## It is also set to ignore the volume availability zone to allow volumes to attach to nodes in different or mismatching zones. The default works well with both CityCloud and SafeSpring.
    storage_classes:
      - name: cinder-csi
        is_default: true
        parameters:
          availability: nova
          allowVolumeExpansion: true
          ## openstack volume type list
          type: default_encrypted


    ## If you want to set up LBaaS in your cluster, you can add the following config:
    external_openstack_cloud_controller_extra_args:
      ## Must be different for every cluster in the same openstack project
      cluster-name: "<your-cluster-name>.cluster.local"

    ## use `openstack subnet list` to list the available subnets
    external_openstack_lbaas_subnet_id: "your-cluster-subnet-uuid"

    ## use `openstack network list` to list the available external networks
    external_openstack_lbaas_floating_network_id: "your-external-network-uuid"

    external_openstack_lbaas_method: "ROUND_ROBIN"
    external_openstack_lbaas_provider: "octavia"
    external_openstack_lbaas_use_octavia: true
    external_openstack_lbaas_create_monitor: true
    external_openstack_lbaas_monitor_delay: "1m"
    external_openstack_lbaas_monitor_timeout: "30s"
    external_openstack_lbaas_monitor_max_retries: "3"
    external_openstack_network_public_networks:
      - "ext-net"

    ## if you have use_access_ip = 0 in cluster.tfvars, you should add the public ip address of the master nodes to this variable
    supplementary_addresses_in_ssl_keys: ["master-ip-address1", "master-ip-address2", ...]
    ```
=== "Citycloud Kna1"

    ``` hcl
    etcd_kubeadm_enabled: true

    cloud_provider: external
    external_cloud_provider: openstack
    calico_mtu: 1480

    cinder_csi_enabled: true
    persistent_volumes_enabled: true
    expand_persistent_volumes: true
    openstack_blockstorage_ignore_volume_az: true

    storage_classes:
      - name: cinder-csi
        is_default: true
        parameters:
          availability: nova
          allowVolumeExpansion: true
          ## openstack volume type list
          type: ceph_hdd_encrypted

    external_openstack_cloud_controller_extra_args:
      ## Must be different for every cluster in the same openstack project
      cluster-name: "<your-cluster-name>.cluster.local"

    ## use `openstack subnet list` to list the available subnets
    external_openstack_lbaas_subnet_id: "your-cluster-subnet-uuid"

    ## use `openstack network list` to list the available external networks
    external_openstack_lbaas_floating_network_id: "your-external-network-uuid"

    external_openstack_lbaas_method: "ROUND_ROBIN"
    external_openstack_lbaas_provider: "octavia"
    external_openstack_lbaas_use_octavia: true
    external_openstack_lbaas_create_monitor: true
    external_openstack_lbaas_monitor_delay: "1m"
    external_openstack_lbaas_monitor_timeout: "30s"
    external_openstack_lbaas_monitor_max_retries: "3"
    external_openstack_network_public_networks:
      - "ext-net"

    ## if you have use_access_ip = 0 in cluster.tfvars, you should add the public ip address of the master nodes to this variable
    supplementary_addresses_in_ssl_keys: ["master-ip-address1", "master-ip-address2", ...]
    ```

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
  ./bin/ck8s-kubespray apply "${CLUSTER}" --flush-cache
done
```

### Correct the Kubernetes API IP addresses

Locate the encrypted kubeconfigs in `${CK8S_CONFIG_PATH}/.state/kube_config_*.yaml` and edit them using sops. Copy the public IP address of the load balancer (usually one of the masters public IP address) and replace the private IP address for the server field in `${CK8S_CONFIG_PATH}/.state/kube_config_*.yaml`.
```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml
done
```

### Test access to the clusters as follows

You should now have an encrypted kubeconfig file for each cluster under `$CK8S_CONFIG_PATH/.state`.
Check that they work like this:

```bash
for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  sops exec-file "${CK8S_CONFIG_PATH}/.state/kube_config_${CLUSTER}.yaml" \
    'kubectl --kubeconfig {} get nodes'
done
```

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

=== "Citycloud Fra1, Kna1"

    ``` hcl

    # ${CK8S_CONFIG_PATH}/sc-config.yaml and ${CK8S_CONFIG_PATH}/wc-config.yaml
    global:
      baseDomain: "set-me"  # set to $CK8S_ENVIRONMENT_NAME.$DOMAIN
      opsDomain: "set-me"  # set to ops.$CK8S_ENVIRONMENT_NAME.$DOMAIN
      issuer: letsencrypt-prod

    storageClasses:
      default: cinder-csi
      nfs:
        enabled: false
      cinder:
        enabled: false
      local:
        enabled: false
      ebs:
        enabled: false

    objectStorage:
      type: s3
      s3:
        region: "set-me" # Kna1 for Karlskrona/Sweden, Fra1 for Frankfurt/Germany
        regionEndpoint: "set-me" # https://s3-<region>.citycloud.com:8080 # kna1 or fra1

    # ${CK8S_CONFIG_PATH}/sc-config.yaml (in addition to the changes above)
    ingressNginx:
        controller:
          useHostPort: false
          service:
            service: enabled
            type: LoadBalancer
            annotations: ""

    harbor:
      persistence:
        # Valid options are "filesystem" (persistent volume), "swift", or "objectStorage" (matching global config)
        type: swift
        disableRedirect: true
        swift:
          identityApiVersion: 3
          authURL: https://<region>.citycloud.com:5000 # kna1 or fra1
          regionName: "set-me" # Kna1 for Karlskrona/Sweden, Fra1 for Frankfurt/Germany
          projectDomainName: "set-me"
          userDomainName: "set-me"
          projectName: "set-me"
          projectID: "set-me"
          tenantName: "set-me"
          authVersion: 3
      oidc:
        groupClaimName: "set-me" # set to group claim name used by OIDC provider
        adminGroupNmae: "set-me"

    issuers:
      letsencrypt:
        enabled: true
        prod:
          email: "set-me"  # set this to an email to receive LetsEncrypt notifications
        staging:
          email: "set-me"  # set this to an email to receive LetsEncrypt notifications


    # ${CK8S_CONFIG_PATH}/secrets.yaml
    objectStorage:
      s3:
        accessKey: "set-me" # set to your s3 accesskey
        secretKey: "set-me" # set to your s3 secretKey
    ```

### Create S3 buckets
You can use the following script to create required S3 buckets. The script uses s3cmd in the background and gets configuration and credentials for your S3 provider from `$CK8S_CONFIG_PATH/.state/s3cfg.ini` file.

=== "Citycloud Fra1, Kna1"

    ``` hcl

    # To get your s3 access and secret keys run:
     openstack --os-interface public ec2 credentials list
    # If you don't have any create them with:
     openstack --os-interface public ec2 credentials create

    # Use your default s3cmd config file: "$CK8S_CONFIG_PATH/.state/s3cfg.ini" that should contain:
    access_key =
    secret_key =
    host_base = s3-<region>.citycloud.com:8080
    host_bucket = s3-<region>.citycloud.com:8080
    signurl_use_https = True
    use_https = True

    ./scripts/S3/entry.sh --s3cfg "$CK8S_CONFIG_PATH/.state/s3cfg.ini" create
    ```

### DNS
If are using service loadbalancers on citycloud you must provision it before you can setup the DNS. You can do that by running the following:

```bash
# for the service cluster
bin/ck8s bootstrap sc

bin/ck8s ops helmfile sc -l app=common-psp-rbac -l app=service-cluster-psp-rbac apply

bin/ck8s ops helmfile sc -l app=kube-prometheus-stack apply

bin/ck8s ops helmfile sc -l app=ingress-nginx apply

bin/ck8s ops kubectl sc get svc -n ingress-nginx

# for the workload clusters
for CLUSTER in "${WORKLOAD_CLUSTERS[@]}"; do
    ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_wc.yaml

    bin/ck8s bootstrap wc

    bin/ck8s ops helmfile wc -l app=common-psp-rbac -l app=workload-cluster-psp-rbac apply

    bin/ck8s ops helmfile wc -l app=kube-prometheus-stack apply

    bin/ck8s ops helmfile wc -l app=ingress-nginx apply

    bin/ck8s ops kubectl wc get svc -n ingress-nginx

done
```

Now that we have the loadbalancer public IPs we can setup the DNS.

1. If you are using Exoscale as your DNS provider make sure that your have [Exoscale cli](https://github.com/exoscale/cli/releases) installed and you can follow [this guide](../exoscale) for more details.
2. If you are using AWS make sure you have [AWS cli](https://github.com/aws/aws-cli) installed and follow the below instructions:
```bash
vim ${CK8S_CONFIG_PATH}/dns.json

# add this lines
{
  "Comment": "Manage test cluster DNS records",
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "*.CK8S_ENVIRONMENT_NAME.DOMAIN",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{ "Value": "<wc_cluster_lb_ip>"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "*.ops.CK8S_ENVIRONMENT_NAME.DOMAIN",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{ "Value": "<sc_cluster_lb_ip>"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "grafana.CK8S_ENVIRONMENT_NAME.DOMAIN",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{ "Value": "<sc_cluster_lb_ip>"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "harbor.CK8S_ENVIRONMENT_NAME.DOMAIN",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{ "Value": "<sc_cluster_lb_ip>"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "notary.harbor.CK8S_ENVIRONMENT_NAME.DOMAIN",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{ "Value": "<sc_cluster_lb_ip>"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "kibana.CK8S_ENVIRONMENT_NAME.DOMAIN",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{ "Value": "<sc_cluster_lb_ip>"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "dex.CK8S_ENVIRONMENT_NAME.DOMAIN",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{ "Value": "<sc_cluster_lb_ip>"}]
      }
    }
  ]
}


# set your profile credentials
AWS_ACCESS_KEY_ID='my-access-key'
AWS_SECRET_ACCESS_KEY='my-secret-key'

aws --configure default ${AWS_ACCESS_KEY_ID} ${AWS_SECRET_ACCESS_KEY}
aws configure set region <region_name>

# get your hosted zone id
aws route53 list-hosted-zones

# apply the DNS changes
aws route53 change-resource-record-sets --hosted-zone-id <hosted_zone_id> --change-batch file://${CK8S_CONFIG_PATH}/dns.json
```

{%
   include-markdown "common.md"
   start="<!--install-apps-start-->"
   end="<!--install-apps-stop-->"
   comments=false
%}

{%
   include-markdown "common.md"
   start="<!--settling-start-->"
   end="<!--settling-stop-->"
   comments=false
%}

{%
   include-markdown "common.md"
   start="<!--testing-start-->"
   end="<!--testing-stop-->"
   comments=false
%}

## Teardown

{%
   include-markdown "common.md"
   start="<!--clean-apps-start-->"
   end="<!--clean-apps-stop-->"
   comments=false
%}

### Remove infrastructure

To teardown the infrastructure, please switch to the root directory of the Kubespray repo (see the Terraform section).
Make sure you remove all PersistentVolumes and Services with `type=LoadBalancer`.
These objects may create cloud resources that are not managed by Terraform, and therefore would not be removed when we destroy the infrastructure.

```bash
MODULE_PATH="$(pwd)/kubespray/contrib/terraform/openstack"

for CLUSTER in "${SERVICE_CLUSTER}" "${WORKLOAD_CLUSTERS[@]}"; do
  pushd "${MODULE_PATH}"
  terraform init
  terraform destroy -var-file="${CK8S_CONFIG_PATH}/${CLUSTER}-config/cluster.tfvars" -state="${CK8S_CONFIG_PATH}/${CLUSTER}-config/terraform.tfstate"
  popd
done

# Remove DNS records
```

Don't forget to remove any DNS records and object storage buckets that you may have created.
