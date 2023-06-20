<!--deploy-rook-start-->
### Deploy Rook

To deploy Rook, please go to the `compliantkubernetes-kubespray` repo root directory and run the following.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops --decrypt ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml > $CLUSTER.yaml
    export KUBECONFIG=$CLUSTER.yaml
    ./rook/deploy-rook.sh
    shred -zu $CLUSTER.yaml
done
```

Please restart the operator pod, `rook-ceph-operator*`, if some pods stalls in initialization state as shown below:

```console
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

You should see PVCs in Bound state. If you want to clean the previously created PVCs:

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml 'kubectl --kubeconfig {} delete pvc rbd-pvc';
done
```
<!--test-rook-stop-->

<!--clone-apps-start-->
Now that the Kubernetes clusters are up and running, we are ready to install the Compliant Kubernetes apps.

### Clone `compliantkubernetes-apps` and Install Pre-requisites

If you haven't done so already, clone the `compliantkubernetes-apps` repo and install pre-requisites.

```bash
git clone https://github.com/elastisys/compliantkubernetes-apps.git
cd compliantkubernetes-apps
ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass --connection local --inventory 127.0.0.1, get-requirements.yaml
```
<!--clone-apps-stop-->

<!--init-apps-start-->
### Initialize the apps configuration

```bash
export CK8S_ENVIRONMENT_NAME=my-environment-name
#export CK8S_FLAVOR=[dev|prod] # defaults to dev
export CK8S_CONFIG_PATH=~/.ck8s/my-cluster-path
export CK8S_CLOUD_PROVIDER=# [exoscale|safespring|citycloud|aws|baremetal]
export CK8S_PGP_FP=<your GPG key fingerprint>  # retrieve with gpg --list-secret-keys

./bin/ck8s init
```

This will initialise the configuration in the `${CK8S_CONFIG_PATH}` directory. Generating configuration files `sc-config.yaml` and `wc-config.yaml`, as well as secrets with randomly generated passwords in `secrets.yaml`. This will also generate read-only default configuration under the directory `defaults/` which can be used as a guide for available and suggested options.

```bash
ls -l $CK8S_CONFIG_PATH
```

<!--init-apps-stop-->

<!--configure-apps-start-->
### Configure the apps

Edit the configuration files `${CK8S_CONFIG_PATH}/sc-config.yaml`, `${CK8S_CONFIG_PATH}/wc-config.yaml` and `${CK8S_CONFIG_PATH}/secrets.yaml` and set the appropriate values for some of the configuration fields.
Note that, the latter is encrypted.

```bash
vim ${CK8S_CONFIG_PATH}/sc-config.yaml
vim ${CK8S_CONFIG_PATH}/wc-config.yaml
sops ${CK8S_CONFIG_PATH}/secrets.yaml
```

!!!tip
    The default configuration for the management cluster and workload cluster are available in the directory `${CK8S_CONFIG_PATH}/defaults/` and can be used as a reference for available options.

!!!warning
    Do not modify the read-only default configurations files found in the directory `${CK8S_CONFIG_PATH}/defaults/`. Instead configure the cluster by modifying the regular files `${CK8S_CONFIG_PATH}/sc-config.yaml` and `${CK8S_CONFIG_PATH}/wc-config.yaml` as they will override the default options.

<!--configure-apps-stop-->

<!--install-apps-start-->
### Install Compliant Kubernetes apps

Start with the management cluster:

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
<!--install-apps-stop-->

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

Start with the management cluster:

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

To remove the applications added by Compliant Kubernetes you can use the two scripts `clean-sc.sh` and `clean-wc.sh`, they are located here in the [scripts folder](https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts).

They perform the following actions:

1. Delete the added helm charts
1. Delete the added namespaces
1. Delete any remaining PersistentVolumes
1. Delete the added CustomResourceDefinitions

Note: if user namespaces are managed by Compliant Kubernetes apps then they will also be deleted if you clean up the workload cluster.
<!--clean-apps-stop-->

<!--create-s3-buckets-start-->
### Create S3 buckets

You can use the following script to create required S3 buckets.
The script uses `s3cmd` in the background and gets configuration and credentials for your S3 provider from `${HOME}/.s3cfg` file.

```bash
# Use your default s3cmd config file: ${HOME}/.s3cfg
scripts/S3/entry.sh create
```

!!!important

    You should not use your own credentials for S3.
    Rather create a new set of credentials with write-only access, when supported by the object storage provider ([check a feature matrix](disaster-recovery.md#feature-matrix)).

<!--create-s3-buckets-stop-->

<!--test-s3-buckets-start-->
### Test S3

To ensure that you have configured S3 correctly, run the following snippet:

```bash
(
    access_key=$(sops exec-file ${CK8S_CONFIG_PATH}/secrets.yaml 'yq r {} "objectStorage.s3.accessKey"')
    secret_key=$(sops exec-file ${CK8S_CONFIG_PATH}/secrets.yaml 'yq r {} "objectStorage.s3.secretKey"')
    sc_config=$(yq m ${CK8S_CONFIG_PATH}/defaults/sc-config.yaml ${CK8S_CONFIG_PATH}/sc-config.yaml -a overwrite -x)
    region=$(echo ${sc_config} | yq r - 'objectStorage.s3.region')
    host=$(echo ${sc_config} | yq r -  'objectStorage.s3.regionEndpoint')

    for bucket in $(echo ${sc_config} | yq r -  'objectStorage.buckets.*'); do
        s3cmd --access_key=${access_key} --secret_key=${secret_key} \
            --region=${region} --host=${host} \
            ls s3://${bucket} > /dev/null
        [ ${?} = 0 ] && echo "Bucket ${bucket} exists!"
    done
)
```
<!--test-s3-buckets-stop-->

<!--out-of-date-start-->
!!!bug "This page is out of date"
    We are currently working on internal documentation to streamline
    Compliant Kubernetes onboarding for selected Infrastructure Providers. Until
    those documents are ready, and until we have capacity to make parts of
    that documentation public, this page is out-of-date.

    Nevertheless, parts of it are useful. Use at your own risk and don't expect things to work smoothly.
<!--out-of-date-end-->
