# Compliant Kubernetes Deployment on Azure

This document contains instructions on how to setup a service cluster and a workload cluster in Azure.  The following are the main tasks addressed in this document:

1. Infrastructure setup for two clusters: one service and one workload cluster
2. Deploying Compliant Kubernetes on top of the two clusters.
3. Creating DNS Records
4. Deploying Rook Storage Orchestration Service
5. Deploying Compliant Kubernetes apps

Before starting, make sure you have [all necessary tools](getting-started.md).

## Setup

Choose names for your service cluster and workload clusters, as well as the DNS domain to expose the services inside the service cluster:

```bash
SERVICE_CLUSTER="sc-test"
WORKLOAD_CLUSTERS=( "wc-test0" )
BASE_DOMAIN="example.com"
```

## Infrastructure Setup using AzureRM

We suggest to set up Kubernetes clusters using kubespray. If you haven't done so already, clone the Elastisys Compliant Kubernetes Kubespray repo as follows:

```bash
git clone --recursive https://github.com/elastisys/compliantkubernetes-kubespray
cd compliantkubernetes-kubespray
```

### Install azure-cli

If you haven't done so already, please install and configure [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).

### Login with azure-cli.

```bash
az login
```

### Customize your infrastructure

Create a configuration for the service and the workload clusters:

```bash
pushd kubespray/contrib/azurerm/
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    az group create -g $CLUSTER -l northeurope
    mkdir -p $CLUSTER/inventory
done
popd
```

!!!note
    Please specify the value for the `ssh_public_keys` variable in `kubespray/contrib/azurerm/group_vars/all`. It must be your SSH public key to access your Azure virtual machines.  Besides, the value for the `cluster_name` variable must be globally unique due to some restrictions in Azure. Make sure that `$SERVICE_CLUSTER` and `$WORKLOAD_CLUSTERS` are unique.

Review and, if needed, adjust the files in `kubespray/contrib/azurerm/group_vars/all` accordingly.

### Generate and apply the templates

```bash
pushd kubespray/contrib/azurerm/
tmp=""
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
   cat group_vars/all \
   | sed \
       -e "s@^cluster_name:.*@cluster_name: \"$CLUSTER\"@" \
   > group_vars/all1
   cat group_vars/all1 > group_vars/all
   rm group_vars/all1
   if [ -z $tmp ]
   then
           sed -i "s/{{ playbook_dir }}/{{ playbook_dir }}\/$CLUSTER/g"  roles/generate-templates/tasks/main.yml

           ansible-playbook generate-templates.yml

           az deployment group create --template-file ./$CLUSTER/.generated/network.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/storage.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/availability-sets.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/bastion.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/masters.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/minions.json -g $CLUSTER
   else
           sed -i "s/{{ playbook_dir }}\/$tmp/{{ playbook_dir }}\/$CLUSTER/g"  roles/generate-templates/tasks/main.yml

           ansible-playbook generate-templates.yml

           az deployment group create --template-file ./$CLUSTER/.generated/network.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/storage.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/availability-sets.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/bastion.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/masters.json -g $CLUSTER
           az deployment group create --template-file ./$CLUSTER/.generated/minions.json -g $CLUSTER
   fi
   tmp=$CLUSTER
 done
 sed -i "s/{{ playbook_dir }}\/$tmp/{{ playbook_dir }}/g"  roles/generate-templates/tasks/main.yml
 sed -i "s/{{ playbook_dir }}\/$tmp/{{ playbook_dir }}/g"  roles/generate-inventory_2/tasks/main.yml
 sed -i "s/{{ playbook_dir }}\/$tmp/{{ playbook_dir }}/g"  roles/generate-inventory/tasks/main.yml
popd
```

### Generating an inventory for kubespray

```bash
pushd kubespray/contrib/azurerm/
tmp=""
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
 if [ -z $tmp ]
   then
         sed -i "s/{{ playbook_dir }}/{{ playbook_dir }}\/$CLUSTER/g"  roles/generate-inventory_2/tasks/main.yml
         sed -i "s/{{ playbook_dir }}/{{ playbook_dir }}\/$CLUSTER/g"  roles/generate-inventory/tasks/main.yml
         ./generate-inventory.sh $CLUSTER

   else
           sed -i "s/{{ playbook_dir }}\/$tmp/{{ playbook_dir }}\/$CLUSTER/g"  roles/generate-inventory_2/tasks/main.yml
           sed -i "s/{{ playbook_dir }}\/$tmp/{{ playbook_dir }}\/$CLUSTER/g"  roles/generate-inventory/tasks/main.yml
           ./generate-inventory.sh $CLUSTER
    fi
    tmp=$CLUSTER
done
sed -i "s/{{ playbook_dir }}\/$tmp/{{ playbook_dir }}/g"  roles/generate-inventory_2/tasks/main.yml
sed -i "s/{{ playbook_dir }}\/$tmp/{{ playbook_dir }}/g"  roles/generate-inventory/tasks/main.yml
popd
```

The inventory files for for cluster will be created under `*/inventory/`. Besides, two `loadBalancer_vars.yaml` files will be created, one for each cluster.

You may also want to check the Azure portal if the infrastructure was created correctly. The figure below shows for `wc-test0`.

![Kubespray Azure for wc-test0](../img/kubespray-azure-wc-sample.png)

## Deploying vanilla Kubernetes clusters using Kubespray

With the infrastructure provisioned, we can now deploy Kubernetes using kubespray. First, change to the `compliantkubernetes-kubespray` root directory.

```bash
cd ..
```

### Init the Kubespray config in your config path.

```bash

export CK8S_CONFIG_PATH=~/.ck8s/azure
export CK8S_PGP_FP=<your GPG key fingerprint>  # retrieve with gpg --list-secret-keys

for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ./bin/ck8s-kubespray init $CLUSTER default $CK8S_PGP_FP
done
```

### Copy the generated inventory files in the right location

```bash
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
  #add calico to the inventory file
  cat kubespray/contrib/azurerm/$CLUSTER/inventory/inventory.j2 \
        | sed  '/\[k8s-cluster:children\]/i \[calico-rr\]' \
        > $CK8S_CONFIG_PATH/$CLUSTER-config/inventory.ini
echo "calico-rr" >> $CK8S_CONFIG_PATH/$CLUSTER-config/inventory.ini $CK8S_CONFIG_PATH/$CLUSTER-config/inventory.ini
    #add ansible_user ubuntu   (note that this assumes you have set admin_username in azurerm/group_vars/all to ubuntu)
    echo -e 'ansible_user: ubuntu' >> $CK8S_CONFIG_PATH/$CLUSTER-config/group_vars/k8s-cluster/ck8s-k8s-cluster.yaml

    #get the  IP address of the loadbalancer (to be added in kubadmin certSANs list which will be used for kubectl)
    ip=$(grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' kubespray/contrib/azurerm/$CLUSTER/loadbalancer_vars.yml)
    echo 'supplementary_addresses_in_ssl_keys: ["'$ip'"]' >> $CK8S_CONFIG_PATH/$CLUSTER-config/group_vars/k8s-cluster/ck8s-k8s-cluster.yaml
    echo -e 'nameservers:\n  - 1.1.1.1' >> $CK8S_CONFIG_PATH/$CLUSTER-config/group_vars/k8s-cluster/ck8s-k8s-cluster.yaml
    echo 'resolvconf_mode: host_resolvconf' >> $CK8S_CONFIG_PATH/$CLUSTER-config/group_vars/k8s-cluster/ck8s-k8s-cluster.yaml

done
```

### Run kubespray to deploy the Kubernetes clusters

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ./bin/ck8s-kubespray apply $CLUSTER --flush-cache
done
```

This may take up to 30 minutes per cluster.

Please increase the value for timeout, e.g `timeout=30`, in `kubespray/ansible.cfg` if you face the following issue while running step-3.

```
TASK [bootstrap-os : Fetch /etc/os-release] **************************************************************************************************************************************************************************************
fatal: [minion-0]: FAILED! => {"msg": "Timeout (12s) waiting for privilege escalation prompt: "}
fatal: [minion-1]: FAILED! => {"msg": "Timeout (12s) waiting for privilege escalation prompt: "}
fatal: [minion-2]: FAILED! => {"msg": "Timeout (12s) waiting for privilege escalation prompt: "}
fatal: [master-0]: FAILED! => {"msg": "Timeout (12s) waiting for privilege escalation prompt: "}
```

### Correct the Kubernetes API IP addresses

Get the public IP address of the loadbalancer:

```bash
grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' kubespray/contrib/azurerm/$CLUSTER/loadbalancer_vars.yml
```

Locate the encrypted kubeconfigs `kube_config_*.yaml` and edit them using sops. Copy the IP shown above into `kube_config_*.yaml`. Do not overwrite the port.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml
done
```

### Test access to the clusters as follows:

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} get nodes'
done
```

### Deploy Rook

To deploy Rook, please go to the `compliantkubernetes-kubespray` repo root directory and run the following.

```bash
pushd rook
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops --decrypt ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml > $CLUSTER.yaml
    export KUBECONFIG=$CLUSTER.yaml
    ./deploy-rook.sh
    shred -zu $CLUSTER.yaml
done
popd
```
Please restart the operator pod, `rook-ceph-operator*`, if some pods stalls in initialization state as shown below:
```
rook-ceph     rook-ceph-crashcollector-minion-0-b75b9fc64-tv2vg    0/1     Init:0/2   0          24m
rook-ceph     rook-ceph-crashcollector-minion-1-5cfb88b66f-mggrh   0/1     Init:0/2   0          36m
rook-ceph     rook-ceph-crashcollector-minion-2-5c74ffffb6-jwk55   0/1     Init:0/2   0          14m
```

Note: pods in pending state usually indicate resource shortage. In such cases you need to use bigger instances.

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

You should see PVCs in Bound state. If you want to clean the previously created PVCs:

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml 'kubectl --kubeconfig {} delete pvc rbd-pvc';
done
```

## Deploying Compliant Kubernetes Apps

Now that the Kubernetes clusters are up and running, we are ready to install the Compliant Kubernetes apps.

### Clone `compliantkubernetes-apps` and Install Pre-requisites

If you haven't done so already, clone the `compliantkubernetes-apps` repo and install pre-requisites.

```bash
git clone https://github.com/elastisys/compliantkubernetes-apps.git
cd compliantkubernetes-apps
ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass --connection local --inventory 127.0.0.1, get-requirements.yaml
```

### Initialize the apps configuration

```bash
export CK8S_ENVIRONMENT_NAME=azure
#export CK8S_FLAVOR=[dev|prod] # defaults to dev
export CK8S_CONFIG_PATH=~/.ck8s/azure
export CK8S_CLOUD_PROVIDER=azure
export CK8S_PGP_FP=<your GPG key fingerprint>  # retrieve with gpg --list-secret-keys
./bin/ck8s init
```

Three files, `sc-config.yaml` and `wc-config.yaml`, and `secrets.yaml`, were generated in the `${CK8S_CONFIG_PATH}` directory.

```bash
ls -l $CK8S_CONFIG_PATH
```

### Configure the apps

Edit the configuration files `${CK8S_CONFIG_PATH}/sc-config.yaml`, `${CK8S_CONFIG_PATH}/wc-config.yaml` and `${CK8S_CONFIG_PATH}/secrets.yaml` and set the appropriate values for some of the configuration fields. Note that, the latter is encrypted.

```bash
vim ${CK8S_CONFIG_PATH}/sc-config.yaml
vim ${CK8S_CONFIG_PATH}/wc-config.yaml
sops ${CK8S_CONFIG_PATH}/secrets.yaml
```

The following are the minimum change you should perform:

```
# ${CK8S_CONFIG_PATH}/sc-config.yaml and ${CK8S_CONFIG_PATH}/wc-config.yaml
global:
  baseDomain: "set-me"  # set to <enovironment_name>.$DOMAIN
  opsDomain: "set-me"  # set to ops.<environment_name>.$DOMAIN
  issuer: letsencrypt-prod
objectStorage:
  type: "s3"
  s3:
    region: "set-me"  # Region for S3 buckets, e.g, west-1
    regionAddress: "set-me"  # Region address, e.g, s3.us-west-1.amazonaws.com
    regionEndpoint: "set-me"  # e.g., https://s3.us-west-1.amazonaws.com

storageClasses:
  default:  rook-ceph-block
  nfs:
    enabled: false
  cinder:
    enabled: false
  local:
    enabled: false
  ebs:
    enabled: false
```

```
# ${CK8S_CONFIG_PATH}/sc-config.yaml (in addition to the changes above)

elasticsearch:
  dataNode:
    storageClass: rook-ceph-block
```

```
# ${CK8S_CONFIG_PATH}/secrets.yaml
objectStorage:
  s3:
    accessKey: "set-me" #set to your s3 accesskey
    secretKey: "set-me" #set to your s3 secretKey
```

### Install Compliant Kubernetes apps

Start with the service cluster:

```bash
ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${SERVICE_CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_sc.yaml
./bin/ck8s apply sc  # Respond "n" if you get a WARN
```

Then the workload clusters:

```bash
for CLUSTER in "${WORKLOAD_CLUSTERS[@]}"; do
    ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_wc.yaml
    ./bin/ck8s apply wc  # Respond "n" if you get a WARN
done
```

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

Check the output of the command above. All resources need to have the Ready column True.

### Testing

After completing the installation step you can test if the apps are properly installed and ready using the commands below.

Start with the service cluster:

```bash
ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${SERVICE_CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_sc.yaml
./bin/ck8s test sc  # Respond "n" if you get a WARN
```

Then the workload clusters:

```
for CLUSTER in "${WORKLOAD_CLUSTERS[@]}"; do
    ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_wc.yaml
    ./bin/ck8s test wc  # Respond "n" if you get a WARN
done
```


Done. Navigate to the endpoints, for example `grafana.$BASE_DOMAIN`, `kibana.$BASE_DOMAIN`, `harbor.$BASE_DOMAIN`, etc. to discover Compliant Kubernetes's features.


## Teardown

To teardown the cluster, please go to the `compliantkubernetes-kubespray` repo root directory and run the following.

```bash
pushd kubespray/contrib/azurerm
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ansible-playbook generate-templates.yml
    az group deployment create -g "$CLUSTER" --template-file ./$CLUSTER/.generated/clear-rg.json --mode Complete
done
popd
```

## Further Reading

* [Elastisys Compliant Kubernetes Kubespray](https://github.com/elastisys/compliantkubernetes-kubespray/blob/main/README.md)
* [Compliant Kubernetes apps repo](https://github.com/elastisys/compliantkubernetes-apps)
* [Configurations option](https://github.com/elastisys/compliantkubernetes-apps#elastisys-compliant-kubernetes-apps)
