{%
   include-markdown "common.md"
   start="<!--out-of-date-start-->"
   end="<!--out-of-date-stop-->"
   comments=false
%}

# Compliant Kubernetes Deployment on GCP

This document contains instructions on how to set up a Compliant Kubernetes environment (consisting of a service cluster and one or more workload clusters) on GCP. The document is split into two parts:

- Cluster setup (Setting up infrastructure and the Kubernetes clusters)
- Apps setup (including information about limitations)

Before starting, make sure you have [all necessary tools](getting-started.md). In addition to these general tools, you will also need:

- A GCP project
- A [JSON keyfile](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for [running Terraform](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started#adding-credentials).
- SSH key that you will use to access GCP, which you have [added to the metadata in your GCP project](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys).
- (Optional) Another JSON keyfile for the [GCP Persistent Disk CSI Driver](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/gcp-pd-csi.md). It is possible (but not recommended) to reuse the same JSON keyfile as you use for Terraform.

!!!note
    This guide is written for compliantkubernetes-apps [v0.13.0](https://github.com/elastisys/compliantkubernetes-apps/tree/v0.13.0)

## Initial setup

Choose names for your service cluster and workload cluster(s):

```bash
SERVICE_CLUSTER="testsc"
WORKLOAD_CLUSTERS=( "testwc0" )
```

## Cluster setup

1. Clone the [compliantkubernetes-kubespray](https://github.com/elastisys/compliantkubernetes-kubespray) repository:
```bash
git clone --recursive https://github.com/elastisys/compliantkubernetes-kubespray
cd compliantkubernetes-kubespray
```
For all commands in the cluster setup part of this guide, your working directory is assumed to be the root directory of this repository.
2. In `config/gcp/group_vars/all/ck8s-gcp.yml`, set the value of `gcp_pd_csi_sa_cred_file` to the path of your JSON keyfile for GCP Persistent Disk CSI Driver.
3. Modify `kubespray/contrib/terraform/gcp/tfvars.json` in the following way:
    - Set `gcp_project_id` to the ID of your GCP project.
    - Set `keyfile_location` to the location of your JSON keyfile. This will be used as credentials for accessing the GCP API when running Terraform.
    - Set `ssh_pub_key` to the path of your public SSH key.
    - In `ssh_whitelist`, `api_server_whitelist` and `nodeport_whitelist`, add IP address(es) that you want to be able to access the cluster.
4. Set up the nodes by performing the following steps:
    1. Make copies of the Terraform variables, one for each cluster:
    ```bash
    pushd kubespray/contrib/terraform/gcp
    for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
      cp tfvars.json $CLUSTER-tfvars.json
    done
    popd
    ```
    2. Set up the nodes with Terraform. If desired, first modify `"machines"` in `kubespray/contrib/terraform/gcp/$CLUSTER-tfvars.json` to add/remove nodes, change node sizes, etc. (For setting up compliantkubernetes-apps in the service cluster, one `n1-standard-8` worker and one `n1-standard-4` worker is enough.)
    ```bash
    pushd kubespray/contrib/terraform/gcp
    for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
        terraform init
        terraform apply -var-file $CLUSTER-tfvars.json -auto-approve -state $CLUSTER.tfstate -var prefix=$CLUSTER
    done
    popd
    ```
    Save the outputs from `apply`. (Alternatively, get them later by running `terraform output -state $CLUSTER.tfstate` in the folder with the state file)

    3. Generate inventory file:
    ```bash
    pushd kubespray/contrib/terraform/gcp
    for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
        ./generate-inventory.sh $CLUSTER.tfstate > $CLUSTER-inventory.ini
    done
    popd
    ```
    4. Initialize the config:
    ```bash
    export CK8S_CONFIG_PATH=~/.ck8s/<environment-name>
    ./bin/ck8s-kubespray init $CLUSTER gcp <path to SSH key> [<SOPS fingerprint>]
    ```
    * `path to SSH key` should point to your private SSH key. It will be copied into your config path and encrypted with SOPS, the original file left as it were.
    * `SOPS fingerprint` is the gpg fingerprint that will be used for SOPS encryption. You need to set this or the environment variable `CK8S_PGP_FP` the first time SOPS is used in your specified config path.
    5. Copy the inventory files:
    ```bash
    pushd kubespray/contrib/terraform/gcp
    for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTERS[@]}; do
        mv $CLUSTER-inventory.ini $CK8S_CONFIG_PATH/$CLUSTER-config/inventory.ini
    done
    popd
    ```
    6. Run kubespray to set up the kubernetes cluster:
        ```bash
        ./bin/ck8s-kubespray apply $CLUSTER
        ```
    7. In your config path, open `.state/kube_config_$CLUSTER.yaml` with SOPS and change `clusters.cluster.server` to the `control_plane_lb_ip_address` you got from `terraform apply`.

## Apps setup

The following instructions were made for release v0.13.0 of compliantkubernetes-apps. There may be discrepancies with newer versions.

### Limitations

Note that there are a few limitations when using compliantkubernetes-apps on GCP at the moment, due to lack of support for certain features:

- Backup retention for InfluxDB is disabled due to it only being supported with S3 as object storage. If you want to circumvent this, consider using S3 as object storage or deploying [Minio](https://docs.min.io/docs/minio-gateway-for-gcs.html) as a gateway.
- Fluentd does not work due to a missing output plugin. If you want to circumvent this, consider using S3 as object storage or deploying [Minio](https://docs.min.io/docs/minio-gateway-for-gcs.html) as a gateway. Alternatively, Fluentd can be disabled in the compliantkubernetes-apps configuration, which has the consequence of no logs being saved from the service cluster.

For information on how to modify the configuration to use S3 as object storage, refer to the administrator manual for [AWS](aws.md) or [Exoscale](exoscale.md), in the section for apps configuration.

### Setup

1. Set up your DNS entries on a provider of your choice, using the `ingress_controller_lb_ip_address` from `terraform apply` as your loadbalancer IPs. You need the following entries:
    ```bash
    *.ops.<environment_name>.$DOMAIN            A <service_cluster_lb_ip>
    grafana.<environment_name>.$DOMAIN          A <service_cluster_lb_ip>
    harbor.<environment_name>.$DOMAIN           A <service_cluster_lb_ip>
    kibana.<environment_name>.$DOMAIN           A <service_cluster_lb_ip>
    dex.<environment_name>.$DOMAIN              A <service_cluster_lb_ip>
    notary.harbor.<environment_name>.$DOMAIN    A <service_cluster_lb_ip>
    ```

    Optionally, if alertmanager is enabled in the workload cluster, create the following DNS record:

    ```bash
    *.<environment_name>.$DOMAIN    A <workload_cluster_lb_ip>
    ```

2. In `compliantkubernetes-apps`, run:
    ```bash
    export CK8S_ENVIRONMENT_NAME=<environment-name>
    export CK8S_CLOUD_PROVIDER=baremetal
    ./bin/ck8s init
    ```

3. You will need to modify `secrets.yaml`, `sc-config.yaml` and `wc-config.yaml` in your config path.

    - `secrets.yaml`
        - Uncomment `objectStorage.gcs.keyfileData` and paste the contents of your JSON keyfile as the value.
    - `sc-config.yaml` AND `wc-config.yaml`
        - Set `global.baseDomain` to `<environment-name>.<dns-domain>` and `global.opsDomain` to `ops.<environment-name>.<dns-domain>`.
        - Set `global.issuer` to `letsencrypt-prod`.
        - Set `storageClasses.default` to `csi-gce-pd`. Also set all `storageClasses.*.enabled` to `false`.
        - Set `objectStorage.type` to `"gcs"`.
        - Uncomment `objectStorage.gcs.project` and set it to the name of your GCP project.
    - `sc-config.yaml`
        - Set `influxDB.backupRetention.enabled` to `false`.
        - Set `ingressNginx.controller.service.type` to `this-is-not-used`
        - Set `ingressNginx.controller.service.annotations` to `this-is-not-used`
        - Set `harbor.oidc.groupClaimName` to  `set-me`
        - Set `issuers.letsencrypt.prod.email` and `issuers.letsencrypt.staging.email` to email addresses of choice.

4. Create buckets for storage on GCP (found under "Storage"). The names must match the bucket names found in your `sc-config.yaml` and `wc-config.yaml` in the config path.
5. Set the default storageclass by running the following command:
    ```bash
    bin/ck8s ops kubectl sc "patch storageclass csi-gce-pd -p '{\"metadata\": {\"annotations\":{\"storageclass.kubernetes.io/is-default-class\":\"true\"}}}'"
    bin/ck8s ops kubectl wc "patch storageclass csi-gce-pd -p '{\"metadata\": {\"annotations\":{\"storageclass.kubernetes.io/is-default-class\":\"true\"}}}'"
    ```
6. Apply the apps:
    ```bash
    bin/ck8s apply sc
    bin/ck8s apply wc
    ```

Done. You should now have a functioning Compliant Kubernetes environment.
