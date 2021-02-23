# Compliant Kubernetes Deployment on Azure

This document describes how to set up Compliant Kubernetes on Azure. The setup has two major parts:

1. Deploying at least two vanilla Kubernetes clusters
2. Deploying Compliant Kubernetes apps

Before starting, make sure you have [all necessary tools](getting-started.md).

## Setup

Choose names for your service cluster and workload clusters, as well as the DNS domain to expose the services inside the service cluster:

```bash
SERVICE_CLUSTER="sc-test"
WORKLOAD_CLUSTERS="sc-test0"
BASE_DOMAIN="example.com"
```

## Deploying vanilla Kubernetes clusters

We suggest to set up Kubernetes clusters using kubespray. If you haven't done so already, clone the Elastisys Compliant Kubernetes Kubespray repo as follows:

```bash
git clone --recursive https://github.com/elastisys/compliantkubernetes-kubespray
cd compliantkubernetes-kubespray
```

### Infrastructure Setup

1. Install azure-cli
  If you haven't done so already, please install and configure [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).

2. Login with azure-cli.
    ```bash
    az login
    ```
3. Customize your infrastructure.

    Create a configuration for the service cluster and the workload cluster:
    ```bash
    pushd kubespray/contrib/azurerm/
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTER; do
      az group create -g $CLUSTER -l northeurope
      mkdir $CLUSTER
      mkdir $CLUSTER/inventory
    done
    popd
    ```

    NOTE:  Please specify the value for the `ssh_public_keys` variable in `kubespray/contrib/azurerm/group_vars/all` and it must be your ssh public key to access your azure virtual machines.   Besides, the value for the `cluster_name` variable must be globally unique due to some restrictions in Azure. Make sure that `$SERVICE_CLUSTER` and `$SERVICE_CLUSTER` are unique.

    Review and, if needed, adjust the files in `kubespray/contrib/azurerm/group_vars/all` accordingly.

4. Generating and applying the templates.

    ```bash
    pushd kubespray/contrib/azurerm/
    tmp=""
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTER; do
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

5. Generating an inventory for kubespray.

    ```bash
    pushd kubespray/contrib/azurerm/
    tmp=""
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTER; do
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
    The inventory files for for cluster will be created under `$SERVICE_CLUSTER/inventory/` and `$WORKLOAD_CLUSTER/inventory/`. Besides, two`loadBalancer_vars.yaml` files will be created, one for each cluster.

    You may also want to check the Azure portal if the infrastructure was created correctly. The figure below shows for `wc-test0`.

    ![Kubespray Axure for wc-test0](../img/kubespray-azure-wc-sample.png)

### Deploying vanilla Kubernetes clusters using Kubespray.

With the infrastructure provisioned, we can now deploy both the sc and wc Kubernetes clusters using kubespray. Before trying any of the steps, make sure you are in the repo's root folder.

1. Init the Kubespray config in your config path.

    ```bash
    export CK8S_CONFIG_PATH=~/.ck8s/azure
    export CK8S_PGP_FP=<your GPG key ID>  # retrieve with gpg --list-secret-keys

    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTERS; do
      ./bin/ck8s-kubespray init $CLUSTER default ~/.ssh/id_rsa.pub
    done
    ```
2. Copy the inventories files generated above in the right place.

    ```bash
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTERS; do
        cp kubespray/contrib/azurerm/$CLUSTER/inventory/inventory.j2 $CK8S_CONFIG_PATH/$CLUSTER-config/inventory.ini
        #add ansible_user ubuntu   (note that this assumes you have set admin_username in azurerm/group_vars/all to ubuntu)
        echo -e 'ansible_user: ubuntu' >> $CK8S_CONFIG_PATH/$CLUSTER-config/group_vars/k8s-cluster/ck8s-k8s-cluster.yaml

        #get the  IP address of  master-0 (to be added in kubadmin certSANs list which will be used for kubectl)
        ip=$(grep -m 1  "master-0" $CK8S_CONFIG_PATH/$CLUSTER-config/inventory.ini | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | head -n 1)

        echo 'supplementary_addresses_in_ssl_keys: ["'$ip'"]' >> $CK8S_CONFIG_PATH/$CLUSTER-config/group_vars/k8s-cluster/ck8s-k8s-cluster.yaml

    done
    ```

3. Run kubespray to deploy the Kubernetes clusters.

Before you running kubespray please set all the [azure parameters](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/azure.md).
    ```bash
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTERS; do
        ./bin/ck8s-kubespray apply $CLUSTER --flush-cache
    done
    ```

    This may take up to 20 minutes.

    Please increase the value for timeout, e.g `timeout=30`, in `kubespray/ansible.cfg` if you face the following issue while running step-3.
    ```
    TASK [bootstrap-os : Fetch /etc/os-release] **************************************************************************************************************************************************************************************
    fatal: [minion-0]: FAILED! => {"msg": "Timeout (12s) waiting for privilege escalation prompt: "}
    fatal: [minion-1]: FAILED! => {"msg": "Timeout (12s) waiting for privilege escalation prompt: "}
    fatal: [minion-2]: FAILED! => {"msg": "Timeout (12s) waiting for privilege escalation prompt: "}
    fatal: [master-0]: FAILED! => {"msg": "Timeout (12s) waiting for privilege escalation prompt: "}
    ```

4. Correct the Kubernetes API IP addresses.

    Find one of the public IP addresses of the master nodes:

    ```bash
    grep -m 1  "master-0" $CK8S_CONFIG_PATH/*-config/inventory.ini | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | head -n 1
    ```

    Locate the encrypted kubeconfigs `kube_config_*.yaml` and edit them using sops. Copy the IP above from inventory files shown above into `kube_config_*.yaml`. Do not overwrite the port.

    ```bash
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTERS; do
        sops $CK8S_CONFIG_PATH/.state/kube_config_$CLUSTER.yaml
    done
    ```

5. Test access to the clusters as follows:

    ```bash
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTERS; do
        sops exec-file $CK8S_CONFIG_PATH/.state/kube_config_$CLUSTER.yaml \
            'kubectl --kubeconfig {} get nodes'
    done
    ```
Deploy Rook

To deploy Rook, please go to the `compliantkubernetes-kubespray` repo root directory and run the following.

  ```bash
  cd rook
  for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
     sops --decrypt ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml > $CLUSTER.yaml
     export KUBECONFIG=$CLUSTER.yaml
  ./deploy-rook.sh
  done
```
## Deploying Compliant Kubernetes Apps

Now that the Kubernetes clusters are up and running, we are ready to install the Compliant Kubernetes apps.

1. If you haven't done so already, clone the Compliant Kubernetes apps repo and install pre-requisites.

      ```bash
      git clone https://github.com/elastisys/compliantkubernetes-apps.git
      cd compliantkubernetes-apps
      ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass --connection local --inventory 127.0.0.1, get-requirements.yaml
      ```

2. Initialize the apps configuration.

    ```bash
    export CK8S_ENVIRONMENT_NAME=azure
    #export CK8S_FLAVOR=[dev|prod] # defaults to dev
    export CK8S_CONFIG_PATH=~/.ck8s/azure
    export CK8S_CLOUD_PROVIDER=azure
    export CK8S_PGP_FP=<your GPG key ID>  # retrieve with gpg --list-secret-keys
    ./bin/ck8s init
    ```

    Three  files, `sc-config.yaml` and `wc-config.yaml`, and `secrets.yaml`, were generated in the `$CK8S_CONFIG_PATH` directory.

    ```bash
    ls -l $CK8S_CONFIG_PATH
    ```

3. Configure the apps.

    Edit the configuration files `sc-config.yaml`, `wc-config.yaml` and `secrets.yaml` and set the approriate values for some of the configuration fields. Note that, the latter is encrypted.

    ```bash
    vim $CK8S_CONFIG_PATH/sc-config.yaml
    vim $CK8S_CONFIG_PATH/wc-config.yaml
    sops $CK8S_CONFIG_PATH/secrets.yaml
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
    # secrets.yaml
    objectStorage:
      s3:
        accessKey: "set-me" #put your s3 accesskey
        secretKey: "set-me" #put your s3 secretKey
    ```

4. Bootstrapping To deploy the Compliant Kubernetes apps, please go to the `compliantkubernetes-apps` repo root directory and run the following.

    ```
    export CK8S_CONFIG_PATH=~/.ck8s/azure
    for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
       ./bin/ck8s bootstrap $CLUSTER
    done
    ```

5. Installing Compliant Kubernetes apps. To deploy the Compliant Kubernetes apps, please go to the `compliantkubernetes-apps` repo root directory and run the following.

    ```bash
    for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
       ./bin/ck8s apps $CLUSTER
    done
    ```

6. Testing: After completing the installation step you can test if the apps are properly installed and ready using the commands below.

    ```
    for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
       ./bin/ck8s test $CLUSTER
    done
    ```
Done. Navigate to `grafana.$BASE_DOMAIN`, `kibana.$BASE_DOMAIN`, `harbor.$BASE_DOMAIN`, etc. to discover Compliant Kubernetes's features.

## Teardown
To teardown the cluster , please go to the `compliantkubernetes-kubespray` repo root directory and run the following.
```bash
pushd kubespray/contrib/azurerm
for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTERS;; do
  ansible-playbook generate-templates.yml
  az group deployment create -g "$CLUSTER" --template-file ./$CLUSTER/.generated/clear-rg.json --mode Complete
done
popd
```



## Further Reading

* [Compliant Kubernetes apps repo](https://github.com/elastisys/compliantkubernetes-apps)
* [Configurations option](https://github.com/elastisys/compliantkubernetes-apps#elastisys-compliant-kubernetes-apps)
