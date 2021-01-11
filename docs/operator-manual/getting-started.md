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

## Deploying sc|wc cluster with Kubespray.

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
          certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN5RENDQWJDZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJeE1ERXdPVEl5TURRek9Wb1hEVE14TURFd056SXlNRFF6T1Zvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTG1GCmxoZ0FuQzdwVTNMRjdIaGZvWWJwcmN1Vks5akNDYU9hTTZpME1KaEN3Mlk5M3NxZDZvUkpjL0hsaldYa0RHeVMKMFJLWWt3emZqb1I0bFExL1gvMyswQk5ISXQ3ZUk4aWFWalBLSDlpbGt0Rkx6TTFLYzBDYnJwdmdKQ3pTWXNUaApQNmRYYUlPbEFicEwwSEJ5YWJYU3UrYWNBb2J5MWovNnRWMkZIV2tqTFQvR2Fkd3pmUlZvb2h6SzRuOXljU3I0CjY0ZUVwZmNQYWx6WEI1YmpOZDN3eWJIaDhyd1pyZzhPTzNRYWZ1WnpUZFU0MXVsazRqczdRMENJSVd4RzRtbFgKOEZjMi9CU1FFU1JDd3FQRzllR0kxb2xLdUhqdkJvemk0SDVXRUJ2VFJLdG01dHhDbC9zMUJrZzFodUZLcnNaYwp4QXNMVURXUWY3WVVJZ09VekpVQ0F3RUFBYU1qTUNFd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFFb0EwOU9DTFoybkJ4NzYrUnNYcjNqcXJWcy8KNUM5dW0zZkpxMnpKbkVhVmxacmZRUG50RmYwRUJyMStISmsrMGxBSkZGNDZpb085dStGaXYyaThRRld3OEtidwpFeTR5cEhWSVBucisxbitsR1FpREpwMUdOeTFWcTU4SlQyckpiblMwajlFNWJDYitObGFDMTh5cnBLL3F6ZjdECk1xNzFPMUFjZkJwNnQ2YkpqUTc0amNjeTVnK2wwL2FMMkxkeGxlQWtUK3Q0OEhtcTFMbzhyNERac3h2ektESXoKZ3RWRUZUYzl2eXFpSVNSa0pkcnlVNmluVVF5eW1PSzZZbVBCQ0FLSngrNzJQRlpIcVMvbmVSL2tqQXc0WEJtagpQL3NnVjlULzNNZnY0UVFVM21mVXdjOURNZDNTM3Z1U2FiUFZSRVA1Q1JNb0NHaHVhb09KMHk4b2NPYz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
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
          client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM4akNDQWRxZ0F3SUJBZ0lJRXhUSms5V1lVWmt3RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TVRBeE1Ea3lNakEwTXpsYUZ3MHlNakF4TVRFd01UUXpNamhhTURReApGekFWQmdOVkJBb1REbk41YzNSbGJUcHRZWE4wWlhKek1Sa3dGd1lEVlFRREV4QnJkV0psY201bGRHVnpMV0ZrCmJXbHVNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTNuTmQrZFVYbkhzbXdadG8Kd3VSYzlIR252dEQ4V3BZS29mdGxhbG9LMWJrTDJzVGFrT0tVcnRiUVp0VU16YUJrdFpKN2kzVkJubEJZejJMbwppajRQSzh6aHBGU0syZzZJVG9XSmJYdnFycTIyRUtvUEt0Um1NYWl5TWhua0thZTBVdHlJaFVYb3FjVCtpZXlCCktDUWJ3VlV4SHFtY3graUtsY21KNWdIcU56VWt6VVJoTXkzdGZRVHR0QzcyUi9sN1d0a01iZmtyYVM2NUxwb1IKc0puR0NaVzY4QzRMTlUwY21pUTFLbWNkMTEvRGJRMHhGd3dlLzJJK1VSMUUwbGNoaEVjcUpJU2xYQ2h3NFplSQpqMzQvUWpWZ0dCMWVySTg0ZG91MmdxaDl6UnlJRllIdnVyN3VlRjYyT3JqMHhKL1pEcUE3UHJjSmxpRGtKZXV0CnVCZ05CUUlEQVFBQm95Y3dKVEFPQmdOVkhROEJBZjhFQkFNQ0JhQXdFd1lEVlIwbEJBd3dDZ1lJS3dZQkJRVUgKQXdJd0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFIeXBHRmF4MzVVekF5d0p1YjBmZTBHSVdFbFFkN2pGVDJZQgpBa2dtZEtFTVZGV1dSWERLcFRKeS9XSWplT1FZZVVMbTFpRnJZaGo5aEVZQUZUQVhBU1g0YXBnTVdleFA2OXJBCmFQSktMUDVDMGNqMGhqVXRETTFodk5FSWw5YzFiaDFkZ2lPZnlLU0ViUVJPMVA1Z2pQTSs0ditHRGxuWUVRc1AKTEF1UXRHVEdqcDNhY1h1VVBvQ3U4OXFsWklZZ1JiZWVRZFRKWG1wSHcxS2FibjMvTmtPTkNadEtkWGM4eXdSYwo3emxFMHBkS0tEWHlpeUFkMEd0MlN0QlNIQk9LOHlrSmhGWTNmeG9HZmNGYTFVMU5JcTVxa08zODRGM09vTUhlCmJrRERRbGRVZ2UyUWlQRllCWk44NmtaNVl4bURTc3JsWWtwWHhsRm55bXdvaGFkRm5JWT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
          client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcEFJQkFBS0NBUUVBM25OZCtkVVhuSHNtd1p0b3d1UmM5SEdudnREOFdwWUtvZnRsYWxvSzFia0wyc1RhCmtPS1VydGJRWnRVTXphQmt0Wko3aTNWQm5sQll6MkxvaWo0UEs4emhwRlNLMmc2SVRvV0piWHZxcnEyMkVLb1AKS3RSbU1haXlNaG5rS2FlMFV0eUloVVhvcWNUK2lleUJLQ1Fid1ZVeEhxbWN4K2lLbGNtSjVnSHFOelVrelVSaApNeTN0ZlFUdHRDNzJSL2w3V3RrTWJma3JhUzY1THBvUnNKbkdDWlc2OEM0TE5VMGNtaVExS21jZDExL0RiUTB4CkZ3d2UvMkkrVVIxRTBsY2hoRWNxSklTbFhDaHc0WmVJajM0L1FqVmdHQjFlckk4NGRvdTJncWg5elJ5SUZZSHYKdXI3dWVGNjJPcmoweEovWkRxQTdQcmNKbGlEa0pldXR1QmdOQlFJREFRQUJBb0lCQUdWbmE5aCtaalFFQTZmUQpJMUpzYlY5VkRDVzArTVNHanpSRitIWWhzN3kzalFyZUg5QmFLWE1HSTV3czFKaEwzSHpVMkpLN0VmMk1ITi8wCjg1SkpOZnMrZTBIQTlFYnd4dndjYlloR0s3WVRJK0syMHhFd0g2SFZoOTNFNWJpRFpYVThhTk53Q2Q2U0dZSmcKR0lSbTZXd1pYTG5na2NLalk4RmlUUVZYckNBYnROTVJ2Zm5BVVpQbzgrQ05ReUdBV2tRc3M4RDUzQ3ErUmRpQgpRUnU1S3IrSG5MN3F5bThEdk5pdFhJRzdsNjVVK1Exd3RpRFdHTzYwZFZoU285b0hDWjg1VC9yWFV2NEFOcDU0ClBSdGoyTlBWSkhaSXY5S0xuby9DM1lmTktLak8rM2grQThGOERNdWE4VzF1RTdKWEhrd0JNZE8xR2lyYnhBMFIKaW5US2FHVUNnWUVBNGNURzh6MTd2RFVDR2Z4dWlrMzhhem5lWWRNUG9MQThHWEE1SHhkWWlaMEx4YlBwV0ZsVwpiZEZ5N0grekFIR2MvRDUrcVJ2d3BjSGpzSy80elZLUkN4SXlBVDNuTjRyNHVvbzVoTkxwb2xZSk9tdENiVk1TCjUvTCtPTS91blpMZmFJTkhwVzRSeDdOdWF1cDlXaTczSGt5ZHlNVExGL1UyQmE5c1QyVXQzWDhDZ1lFQS9EeloKdWV1SDJaNDZhRm9icG9XdmRycmU2NldaNW1mdXF5c0lnb3FpT1pUbmtGSm4rWEd1TERqNGlLamFFRVUzOXdUdQpMclpvVEFnYkcrLzE2T014VlFwTGgxQXNvS203bG9LUW9ySUtmdEJPWXZMaExod3R6ZGRqZFJiUXFtTjFlc0FSCllTaE5idElhV2NxNUQrSHhOOWJMT0o1enV0c0t0Q2l4dFFGajMzc0NnWUVBbjUyOWdxOFBVZ3F3QjZzK2c2MkwKTGt2bGU0ZjYzb0o2bXdtS2VQN0thOUNLU0NaZ2JVUU1KT3dWc2pxK1ZTdjk3eUJIOEV0K29kSW9wZnhqak5ZNQpFWGkxdmNjRU4zS2JVMWJ5UDRQV0JoMkp2TEdrYnlKeWxXWm9jY1lnVDJ0Tlk5aWN5TXErNjA5aVcxaVpjeThOCkszRERoUFFOR2swVStvUUJzVWc1V3dVQ2dZRUFxWUVXNjNyZEV4L2lya2VIZDFNMVE3dDJuTEx2aGtkbnV2MHoKUGM1K0QrWUI2eG1GcDdwK1NsZUtwUU9iYnYybEMwbno2YzVJcm5kd0NFa3NYdkYyTUdpM3N0bnM4NWE4YWZ1Wgp5TXVPaEFQbCtWYXdmalVQanRsa2k4WG1PZXFXZ3dQWmFnb1VaeG1uL1psZTNjNS9OSUFTbHh6Y05zQ0dJK1dJCjdsTmQwMHNDZ1lCeUNZSnhzZDBmYytFc0dueC9GVWRrYXNtTGYzVWhuQWZ3Y2k5VWhqUndCb2NQNGVtUVl5NWIKTVlPN0k1TS9KTmlqWHViNWxtMExKN1Y1RjdTaHZsZHo1ZUhDSUpsYnFnVFBuQnlteFg2RnM0OENlQ2pZNEVhTQp2STN4bXBuMm5qYWxGVmV3N1REcXgyRXhLVWdnZFlic0ZnREdvMUhPUmFqemlJY1dNSEFaR0E9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
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

3. Initialization of Compliant Kubernetes apps.

    Run the following command to initialize the compliant kubernetes apps. Note that this will not overwrite existing values, but it will append to existing files.

    ```bash
    export CK8S_CONFIG_PATH=~/.ck8s/aws
    export CK8S_CLOUD_PROVIDER=aws
    export CK8S_ENVIRONMENT_NAME=<put Environment name>
    ./bin/ck8s init
    ```
    Three  files, `sc-config.yaml` and `wc-config.yaml`, and `secrets.yaml`, are generated in `~/.ck8s/aws/` directory.

    Edit the configuration files  `~/.ck8s/aws/sc-config.yaml`, `~/.ck8s/aws/wc-config.yaml` and `~/.ck8s/aws/secrets.yaml` and set the approriate values for some of the configuration fields, especially these fields whose values contain  `set-me`. Make sure also that the `objectStorage` values are set in `~/.ck8s/aws/sc-config.yaml`, `~/.ck8s/aws/wc-config.yaml` and `~/.ck8s/aws/secrets.yaml` according to your `objectStorage.type` (so `objectStorage.s3.*` if you are using S3 or `objectStorage.gcs.*` if you are using GCS.).

4. Installing Compliant Kubernetes apps.

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
