# Compliant Kubernetes Deployment on AWS

This document describes how to set up Compliant Kubernetes on AWS. The setup has two major parts:

1. Deploying at least two vanilla Kubernetes clusters
2. Deploying Compliant Kubernetes applications

Before starting, make sure you have [all necessary tools](getting-started.md).

## Setup

Choose names for your service cluster and workload clusters:

```bash
SERVICE_CLUSTER="testsc"
WORKLOAD_CLUSTERS="testwc0"
```

## Deploying vanilla Kubernetes clusters

We suggest to set up Kubernetes clusters using kubespray. If you haven't done so already, clone the Elastisys Compliant Kubernetes Kubespray repo as follows:

```bash
git clone --recursive https://github.com/elastisys/compliantkubernetes-kubespray
cd compliantkubernetes-kubespray
```

### Infrastructure Setup using Terraform

1. Optional: Setup Terraform Cloud.

    We suggest storing Terraform state in Terraform Cloud. To this end, add your Terraform Cloud authentication token in the ` ~/.terraformrc` file. Please refer [Terraform Cloud](https://learn.hashicorp.com/tutorials/terraform/cloud-sign-up#configure-access-for-the-terraform-cli) for further information. Please also check the the [requirements](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/aws#kubernetes-on-aws-with-terraform) section for the specific Terraform version.

2. Expose AWS credentials to Terraform.

    We suggest exposing AWS credentials to Terraform via environment variables, so they are not accidently left on the file-system:

    ```shell
    export TF_VAR_AWS_ACCESS_KEY_ID="www"
    export TF_VAR_AWS_SECRET_ACCESS_KEY="xxx"
    export TF_VAR_AWS_SSH_KEY_NAME="yyy"
    export TF_VAR_AWS_DEFAULT_REGION="zzz"
    ```

3. Customize your infrastructure.

    Create a configuration for the service cluster and the workload cluster:

    ```bash
    pushd kubespray
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTERS; do
        cat contrib/terraform/aws/terraform.tfvars \
        | sed \
            -e "s@^aws_cluster_name =.*@aws_cluster_name = \"$CLUSTER\"@" \
            -e "s@^inventory_file =.*@inventory_file = \"../../../inventory/hosts-$CLUSTER\"@" \
        > inventory/terraform-$CLUSTER.tfvars
    done
    popd
    ```

    Review and, if needed, adjust the files in `kubespray/inventory/`.

3. Initialize and Apply Terraform.

    ```bash
    pushd kubespray/contrib/terraform/aws
    terraform init
    for CLUSTER in $SERVICE_CLUSTER $WORKLOAD_CLUSTERS; do
        terraform apply \
            -var-file=../../../inventory/terraform-$CLUSTER.tfvars \
            -auto-approve \
            -state-out=../../../inventory/tfstate-$CLUSTER.tfstate
    done
    popd
    ```

### Deploying vanilla Kubernetes clusters using Kubespray.

With the infrastructure provisioned, we can now deploy both the sc and wc Kubernetes clusters using kubespray. Before trying any of the steps, make sure you are in the repo's root folder.

1. Init the kubespray config in your config path.

    ```bash
    export CK8S_CONFIG_PATH=~/.ck8s/aws
    export CK8S_PGP_FP=<put your GPG-key here>

    for CLUSTER in test-sc test-wc0; do
        ./bin/ck8s-kubespray init $CLUSTER default ~/.ssh/id_rsa.pub
    done
    ```


2. Copy the content of `../../../inventory/hosts-sc|wc` file (see step-3 under Terraform in case you use a different file) and paste it to `~/.ck8s/aws/sc|wc-config/inventory.ini`.
   The following shows a sample content for `~/.ck8s/aws/sc-config/inventory.ini`.

   ```bash
   [all]
    ip-10-250-203-132.us-west-1.compute.internal ansible_host=10.250.203.132
    ip-10-250-204-174.us-west-1.compute.internal ansible_host=10.250.204.174
    ip-10-250-209-206.us-west-1.compute.internal ansible_host=10.250.209.206
    ip-10-250-198-29.us-west-1.compute.internal ansible_host=10.250.198.29
    bastion ansible_host=3.101.23.107
    bastion ansible_host=3.101.61.191

    [bastion]
    bastion ansible_host=3.101.23.107
    bastion ansible_host=3.101.61.191

    [kube-master]
    ip-10-250-203-132.us-west-1.compute.internal

    [kube-node]
    ip-10-250-204-174.us-west-1.compute.internal
    ip-10-250-209-206.us-west-1.compute.internal

    [etcd]
    ip-10-250-198-29.us-west-1.compute.internal

    [k8s-cluster:children]
    kube-node
    kube-master
    etcd

    [k8s-cluster:vars]
    apiserver_loadbalancer_domain_name="kubernetes-elb-sc-569874712.us-west-1.elb.amazonaws.com"

    #don't forget to add the following as they won't be in the hosts file
    [all:vars]
    ansible_python_interpreter=/usr/bin/python3
    ansible_user=ubuntu
   ```

3. Run kubespray to set up the kubernetes cluster.

      ```
      ./bin/ck8s-kubespray apply <sc|wc>  --flush-cache
      ```
4. Done. You should now have a working kubernetes cluster. You should also have an encrypted kubeconfig at `~/.ck8s/aws/.state/kube_config_<sc|wc>.yaml` that you can use to access the cluster.

5. Accessing the clusters.
  Please copy the content of your kubeconfig and save it, for example, in your working directory.

     ```
     #open the encrypted kubeconfig for your cluster and copy the content
     sops ~/.ck8s/aws/.state/kube_config_<sc|wc>.yaml

     #paste the copied content and save it in your working directory
     #please copy the URL of the load balancer from inventory file
     #(i.e., ~/.ck8s/aws/<sc|wc>-config/inventory.ini) and
     #paste this URL into the server parameter in kubectl config. Do not overwrite the port.
     vi  <sc|wc>.yaml

     #accessing the cluster
     kubectl --kubconfig <sc|wc>.yaml get nodes
     ```
    The following snippet shows an example kubeconfig.
     ```
      apiVersion: v1
      clusters:
      -   cluster:
              certificate-authority-data: xxx
              server: https://kubernetes-elb-sc-569874712.us-west-1.elb.amazonaws.com:6443
          name: cluster.local
      contexts:
      -   context:
              cluster: cluster.local
              user: kubernetes-admin-cluster.local
          name: kubernetes-admin-cluster.local@cluster.local
      current-context: kubernetes-admin-cluster.local@cluster.local
      kind: Config
      preferences: {}
      users:
      -   name: kubernetes-admin-cluster.local
          user:
              client-certificate-data: xxx
              client-key-data: xxx
    ```



## Compliant Kubernetes Applications' Configurations and Installations on AWS

Now that the Kubernetes clusters are up and running, we are ready to install the Compliant Kubernetes applications.

Once the clusters are ready, please follow the instructions below to install the Compliant Kubernetes applications. For more information, please check the Compliant Kubernetes repo [here](https://github.com/elastisys/compliantkubernetes-apps).

1. Clone the Compliant Kubernetes apps repo.

      ```bash
      git clone https://github.com/elastisys/compliantkubernetes-apps.git
      ```
2. Installation of prerequisite tools.
  To install the prerequisites please run the command below (assumes you are under `compliantkubernetes-apps` directory.). For more information please check the requirements section [here](https://github.com/elastisys/compliantkubernetes-apps#requirements).

      ```bash
      ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass --connection local --inventory 127.0.0.1, get-requirements.yaml
      ```
3. Prepare all the required domains.
  You will need to set up the following DNS entries (replace example.com with your domain).

    Point these domains to the workload cluster load balancer fronting the Ingress controller:

      ```
        *.example.com
        prometheus.ops.example.com
      ```

    Point these domains to the service cluster load balancer fronting the Ingress controller:

      ```
      *.ops.example.com
      grafana.example.com
      harbor.example.com
      kibana.example.com
      dex.example.com
      notary.harbor.example.com
      ```

4. Edit the kubeconfig files
 Two encrypted kubeconfig files were created when the  two kubernetes clusters(i.e, sc, wc) were created  above. The two files are  `~/.ck8s/aws/.state/kube_config_sc.yaml` for  `sc` cluster and `~/.ck8s/aws/.state/kube_config_wc.yaml` for `wc` cluster.  

      Please copy the URL of the load balancer from inventory file
     (i.e., ~/.ck8s/aws/<sc|wc>-config/inventory.ini) and
     paste this URL into the server parameter in kubeconfig. Do not overwrite the port (see the example presented above).
5. Initialization of Compliant Kubernetes apps.
     Run the following command to initialize the Compliant Kubernetes apps. Note that this will not overwrite existing values, but it will append to existing files.

    ```bash
    export CK8S_ENVIRONMENT_NAME=aws
    #export CK8S_FLAVOR=[dev|prod] # defaults to dev
    export CK8S_CONFIG_PATH=~/.ck8s/aws
    export CK8S_CLOUD_PROVIDER=aws
    export CK8S_PGP_FP=<PGP-fingerprint>
    ./bin/ck8s init
    ```
    Three  files, `sc-config.yaml` and `wc-config.yaml`, and `secrets.yaml`, are generated in `~/.ck8s/aws/` directory.

    Edit the configuration files  `~/.ck8s/aws/sc-config.yaml`, `~/.ck8s/aws/wc-config.yaml` and `~/.ck8s/aws/secrets.yaml` and set the approriate values for some of the configuration fields. The following are the  minimum change you should to do.

      1. Changes in `~/.ck8s/aws/sc-config.yaml`:

           ```
           global:
            baseDomain: "set-me" #based on the above domain example this is set to example.com
            opsDomain: "set-me" #based on the above domain example this is set to ops.example.com

          objectStorage:
            type: "s3" # assumes that you are using s3
            s3:
              region: "set-me" #put the region, e.g, west-1
              regionAddress: "set-me" #put the region address, e.g, s3.us-west-1.amazonaws.com
              regionEndpoint: "set-me"#put the region endpoint, e.g., https://s3.us-west-1.amazonaws.com

          fluentd:
           useRegionEndpoint: "set-me" # set it to either true or false
           ```
       2. Changes in `~/.ck8s/aws/sc-config.yaml`:

             ```
           global:
            baseDomain: "set-me" #based on the above domain example this is set to example.com
            opsDomain: "set-me" #based on the above domain example this is set to ops.example.com

          objectStorage:
            type: "s3" # assumes that you are using s3
            s3:
              region: "set-me" #put the region, e.g, west-1
              regionAddress: "set-me" #put the region address, e.g, s3.us-west-1.amazonaws.com
              regionEndpoint: "set-me"#put the region endpoint, e.g., https://s3.us-west-1.amazonaws.com
           ```
       3. Changes in `~/.ck8s/aws/secrets.yaml`:

           ```
           objectStorage:
            s3:
                accessKey: "set-me" #put your s3 accesskey
                secretKey: "set-me" #put your s3 secretKey
           ```

6. Installing Compliant Kubernetes apps.
  Run the following commands:

    ```bash
    ./bin/ck8s apply sc
    ./bin/ck8s apply wc
    ```

    After completing the installation step you can test if the apps are properly installed and ready using the commands below.

    ```bash
    ./bin/ck8s test sc
    ./bin/ck8s test wc
    ```
 More detail configurations option can be found [here](https://github.com/elastisys/compliantkubernetes-apps#elastisys-compliant-kubernetes-apps).
