# Compliant Kubernetes Setup and Installations on AWS

This document describes how to setup compliant kubernetes in Amazon AWS. The setup has two major parts: Compliant Kubernetes Cluster and Compliant Kubernetes applications. The following sections present the necessary steps to setup  both the compliant Kubernetes Cluster and applications.

## Compliant Kubernetes Cluster configurations and installations
In order to set-up the compliant kubernetes cluster, you need to clone [ck8s-cluster](https://github.com/elastisys/ck8s-cluster.git)  repo first.

```bash
git clone  https://github.com/elastisys/ck8s-cluster.git
```
Once you download ck8s-cluster, please follow the steps below.
1. Installation of prerequisites.

   Make sure that you have all the [prerequisite](https://github.com/elastisys/ck8s-cluster/blob/master/README.md#requirements) tools in your system in advance.

2. Setup Terraform Cloud.

   Add your Terraform Cloud authentication token in the ` ~/.terraformrc` file. Please refer [Terraform Cloud](https://github.com/elastisys/ck8s-cluster/blob/master/README.md#terraform-cloud) section for further information. Please also check the the [requirements](https://github.com/elastisys/ck8s-cluster/blob/master/README.md#requirements) section for the specific Terraform version.

3. Generate PGP key.

  You need to generate GPG key as secrets in compliant kubernetes are are encrypted using [SOPS](https://github.com/mozilla/sops). To generate your own PGP key, run the command below:
  ```bash
  gpg --full-generate-key

  ```

4. Build CK8S-Cluster cli.

    We now have  all the prerequisites in place, it is time to build the cli for the compliant kubernetes cluster, `ck8s-cluster`. In order to build the ck8s-cluster cli please run  the following command:

    ```bash
    make build
    ```
    Once you build the cli, the built file can be found under `~/dist/` directory. Please rename the file to `ck8s`, as we will be using this name from this onward.

5. Upload and Register CK8S Base Image to AWS.

  Upload the latest ck8s base image to AWS. You can find the latest base image in  [ck8s-base-vm](https://github.com/elastisys/ck8s-base-vm) repo. You can also build the base image by your self following the instructions [here](https://github.com/elastisys/ck8s-base-vm#building-the-image).

  Once you upload and register the ck8s base image to AWS, please take a note of `AMI ID` of the image. It will be required later.

6. CK8S-Cluster Initialization.

  CK8S-Cluster initialization generates initial configuration files. In order to perform initialization you need to provide config path( i.e.,`CK8S_CONFIG_PATH`), your GPG-key (i.e., `CK8S_PGP_FP`), environment name, and cloud provider (i.e., `aws` in our case). Please refer [quick start](https://github.com/elastisys/ck8s-cluster/blob/master/README.md#quickstart) for details. The following bash code snippet shows ck8s-cluster initializtion with  config path `~/.ck8s/aws`, environment name `test1` and `aws` as a cloud provider.
  ```bash
  export CK8S_CONFIG_PATH=~/.ck8s/aws
  export CK8S_PGP_FP=<put your GPG-key here>
  #test1 is environment name
  #aws is cloud provider
  dist/ck8s init test1 aws
```
  Once you execute the above command, some config files and directories are generated under `~/.ck8s/aws` directory. You can see the list of files created:

  ```bash
  ls ~/.ck8s/aws
  #the folloging are the files generated during init
  backend_config.hcl  config.yaml  secrets.yaml  ssh  tfvars.json
  ```
  We need to edit some of the files to make the configurations ready for the next step. The minimum requirement is that we need to edit `~/.ck8s/aws/tfvars.json` to add our IP address in the whitelists and `AMI ID`, `~/.ck8s/aws/secrets.yaml` to add our credentials to the sops encrypted file , `~/.ck8s/aws/config.yaml` to add oidc issuer url  and `~/.ck8s/aws/backend_config.hcl` to add organization for Terraform cloud.

  The following snippet shows a list of whitelisted IP addresses in `~/.ck8s/aws/tfvars.json`.
  ```
  "public_ingress_cidr_whitelist":
   ["10.56.165.112/32",
  "10.36.15.132/32"],

  "api_server_whitelist":
  ["10.56.165.112/32",
  "10.36.15.132/32"],

  "nodeport_whitelist":
  ["10.56.165.112/32",
  "10.36.15.132/32"],
  ```
  Please also replace the values of all `image.name` instances in  `~/.ck8s/aws/tfvars.json`. The following snippet shows adding AMI ID `ami-0188237ecf1a71032`  for node master-0 in the service cluster.
  ```
  "machines_sc": {
    "master-0": {
      "node_type": "master",
      "size": "t3.small",
      "image": {
        "name":   "ami-0188237ecf1a71032"
      },
      "provider_settings": null
    }
    ```
  Edit `~/.ck8s/aws/secrets.yaml`  and provide your credintials. to edit the file:
  ```bash
  sops ~/.ck8s/aws/secrets.yaml
  ```
  Please edit  `~/.ck8s/aws/config.yaml` and `~/.ck8s/aws/backend_config.hcl` files  and add oidc issuer url and organization name used in Terraform Cloud, respectively.

7. Creating ck8s Cluster.

  We need to create two ck8s clusters:  service Cluster,`sc` and workload cluster, `wc`. Run the following commands to create the ck8s clusters:
  ```bash
  dist/ck8s apply --cluster sc
  dist/ck8s apply --cluster wc
  ```
  The cluster should now be up and running. You can verify this with:

  ```bash
  dist/ck8s status --cluster sc
  dist/ck8s status --cluster wc
  ```

## Compliant Kubernetes Applications' Configurations and Installations on AWS

Now the ck8s-cluster is up and runing, we are ready to install the compliant kubernetes apps.

Note that for some reason if your IP address changes, you need to add the new IP address in the whitelist under `~/.ck8s/aws/tfvars.json` file and run the following commands again.

```bash
dist/ck8s apply --cluster sc
dist/ck8s apply --cluster wc
```
Once the cluster is ready, please follow the following steps to install the compliant Kubernetes-apps. For more information about compliant kubernetes apps, please check the compliant kubernetes apps repo [here](https://github.com/elastisys/compliantkubernetes-apps).

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
    ./bin/ck8s init
    ```
    Two more files, `sc-config.yaml` and `wc-config.yaml`, are generated in `~/.ck8s/aws/` directory.

    Edit the configuration files  `~/.ck8s/aws/sc-config.yaml`, `~/.ck8s/aws/wc-config.yaml` and `~/.ck8s/aws/secrets.yaml` and set the approriate values for some of the configuration fields, especially these fields whose values contain  `set-me`. Make sure also that the `objectStorage` values are set in `~/.ck8s/aws/sc-config.yaml`, `~/.ck8s/aws/wc-config.yaml` and `~/.ck8s/aws/secrets.yaml` according to your `objectStorage.type` (so `objectStorage.s3.*` if you are using s3 or `objectStorage.gcs.*` if you are using gcs.).

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
