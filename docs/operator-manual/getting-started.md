# Compliant Kubernetes Setup and Installations on AWS

This document describes how to set up Compliant Kubernetes on AWS. The setup has two major parts: Kubernetes cluster setup and Compliant Kubernetes applications setup. The following sections present the necessary steps to set up both parts.

##  Kubernetes Cluster set up
In order to set up the kubernetes clusters, you need to clone the [Elastisys Compliant Kubernetes Kubespray](https://github.com/elastisys/compliantkubernetes-kubespray.git)  repo first.

```bash
git clone --recursive https://github.com/elastisys/compliantkubernetes-kubespray.git
# cd to the cloned repo
cd compliantkubernetes-kubespray
```
Once you download ck8s-cluster, please follow the steps below.
### Infrastructure setup using terraform

1. Setup Terraform Cloud.

   Add your Terraform Cloud authentication token in the ` ~/.terraformrc` file. Please refer [Terraform Cloud](https://learn.hashicorp.com/tutorials/terraform/cloud-sign-up#configure-access-for-the-terraform-cli) section for further information. Please also check the the [requirements](https://github.com/kubernetes-sigs/kubespray/tree/master/contrib/terraform/aws#kubernetes-on-aws-with-terraform) section for the specific Terraform version.

2. Update Terraform variables.

  You need to set your Terraform credentials and update the default  AWS cluster values.

  1. Setting  Terraform credentials.

    You can either export the variables for your AWS credentials or edit `kubespray/contrib/terraform/aws/credentials.tfvars`:

        ```bash
        cd kubespray/contrib/terraform/aws/
        cp credentials.tfvars.example credentials.tfvars
        export AWS_ACCESS_KEY_ID=<put your access-key>
        export AWS_SECRET_ACCESS_KEY=<put your secret-key>
        #please check the the link on how to create ssh key pair
        #https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html
        export AWS_SSH_KEY_NAME=<An SSH key set up on AWS>
        export AWS_DEFAULT_REGION=<put your aws region-name>
        ```
        Note: Pleased download the private key  when creating ssh key pair in AWS as it will be needed later.
  2. Customize your infrastructure.

    Edit `terraform.tfvars` and change the values according to your requirements. Since we need to create two different clusters (service and workload), you should  set `aws_cluster_name` to  `sc` when creating service cluster and `wc` when creating workload cluster.

    Below is an example configuration.
      ```
      #Global Vars
      aws_cluster_name = "sc|wc" #service cluster or workload cluster

      #VPC Vars
      aws_vpc_cidr_block       = "10.250.192.0/18"
      aws_cidr_subnets_private = ["10.250.192.0/20", "10.250.208.0/20"]
      aws_cidr_subnets_public  = ["10.250.224.0/20", "10.250.240.0/20"]

      #Bastion Host
      aws_bastion_size = "t2.medium"

      #Kubernetes Cluster

      aws_kube_master_num  = 3
      aws_kube_master_size = "t2.medium"

      aws_etcd_num  = 3
      aws_etcd_size = "t2.medium"

      aws_kube_worker_num  = 4
      aws_kube_worker_size = "t2.medium"

      #Settings AWS ELB

      aws_elb_api_port                = 6443
      k8s_secure_api_port             = 6443
      kube_insecure_apiserver_address = "0.0.0.0"

      default_tags = {
        #  Env = "devtest"
        #  Product = "kubernetes"
      }

      inventory_file = "../../../inventory/hosts"
      ```
  3. initialize and apply terraform.

    Once you are done with Terraform configuration, it is now time to create the cluster two clusters.
    ```bash
    terraform  init
    terraform apply -state-out=<sc|wc state path>
  ```

  Please make sure that you copy `../../../inventory/hosts` or use a different name before you create the second cluster. Otherwise, it will be overwritten. It  will be needed to deploy the kubernetes cluster later.

### Deploying sc|wc cluster with Kubespray.

With the infrastructure provisioned, we can now deploy both the  sc and wc Kubernetes clusters using kubespray. Before trying any of the steps, make sure you are in the repo's root folder.

1. Init the kubespray config in your config path.
  ```bash
  export CK8S_CONFIG_PATH=~/.ck8s/aws
  export CK8S_PGP_FP=<put your GPG-key here>
  #Use the AWS private key you downloaded above when you create SSH key pair.
  bin/ck8s-kubespray init sc default <AWS private-key>
  ```

  If you don't have a GPG key already, then you need to generate GPG key. This is because  secrets in Compliant Kubernetes are are encrypted using [SOPS](https://github.com/mozilla/sops). To generate your own PGP key, run the command below:
  ```bash
  gpg --full-generate-key
  ```
2. Copy the content of `../../../inventory/hosts` file (see step-3 under Terraform in case you use a different file) and paste it to `~/.ck8s/aws/inventory.ini`.
   The following shows a sample content for `~/.ck8s/aws/inventory.ini`.

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
  #please comment out lines with "---" in ~/.ck8s/aws/<sc|wc>-config/group_vars/all/all.yml and  ~/.ck8s/aws/<sc|wc>-config/group_vars/k8s-cluster/k8s-cluster.yml  as they may sometimes cause an error.
  ./bin/ck8s-kubespray apply <sc|wc>  --flush-cache
  ```
4. Done. You should now have a working kubernetes cluster. You should also have an encrypted kubeconfig at `~/.ck8s/aws/.state/kube_config_<sc|wc>.yaml` that you can use to access the cluster.

5. Accessing the clusters.
 Please copy the content of your  kubeconfig and save it, for example, in your working directory
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

Now the kubernetes clusters are up and running, we are ready to install the compliant kubernetes apps.

Once the cluster is ready, please follow the instructions below to install the compliant Kubernetes-apps. For more information about compliant kubernetes apps, please check the compliant kubernetes apps repo [here](https://github.com/elastisys/compliantkubernetes-apps).

1. Clone the compliant kubernetes apps repo.

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

  Point these domains to the workload cluster ingress controller:

  `*.example.com`

  `prometheus.ops.example.com`

  Point these domains to the service cluster ingress controller:

  `*.ops.example.com`

  `grafana.example.com`

  `harbor.example.com`

  `kibana.example.com`

  `dex.example.com`

  `notary.harbor.example.com`

5. Edit the kubeconfig files
 Two encrypted kubeconfig files were created when the  two kubernetes clusters(i.e, sc, wc) were created  above. The two files are  `~/.ck8s/aws/.state/kube_config_sc.yaml` for  `sc` cluster and `~/.ck8s/aws/.state/kube_config_wc.yaml` for `wc` cluster.  

  Please copy the URL of the load balancer from inventory file
 (i.e., ~/.ck8s/aws/<sc|wc>-config/inventory.ini) and
 paste this URL into the server parameter in kubeconfig. Do not overwrite the port (see the example presented above).
6. Initialization of Compliant Kubernetes apps.

    Run the following command to initialize the compliant kubernetes apps. Note that this will not overwrite existing values, but it will append to existing files.

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
        regionEndpoint: "set-me" #put the region endpoint, e.g., https://s3.us-west-1.amazonaws.com
     ```
   3. Changes in `~/.ck8s/aws/secrets.yaml`:

   ```
   objectStorage:
    s3:
        accessKey: "set-me" #put your s3 accesskey
        secretKey: "set-me" #put your s3 secretKey
   ```

6. Installing Compliant Kubernetes apps.

    This step assumes the ck8s-cluster setup above is up and running. To install the sc and wc clusters run the following commands.

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
