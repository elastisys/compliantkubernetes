# Compliant Kubernetes Deployment on OVH Managed Kubernetes

This document contains instructions on how to setup a service cluster and a workload cluster in [OVH](https://www.ovh.com).
The following are the main tasks addressed in this document:

1. Setting up Compliant Kubernetes for OVH Managed Kubernetes
1. Deploying Compliant Kubernetes on top of two Kubernetes clusters.

The instructions below are just samples, you need to update them according to your requirements.

Before starting, make sure you have [all necessary tools](getting-started.md).

!!!note
    This guide is written for compliantkubernetes-apps [v0.13.0](https://github.com/elastisys/compliantkubernetes-apps/tree/v0.13.0)

## Setup

Create two Kubernetes clusters in OVH, follow [this guide](https://docs.ovh.com/gb/en/kubernetes/creating-a-cluster/).

!!!note "Sizing hint"
    For the service cluster you can start with creating 3 nodes of size `B2-7` and add a `B2-15` node.

    The workload cluster is fine with 3 `B2-7` nodes.

### Configure Compliant Kubernetes

Start by preparing your shell with some variables that will be used.

```ShellSession
REGION="waw" # Region for the cluster
ISSUER_MAIL="user@example.com" # Mail that will be used for the LetsEncrypt certificate issuer

export CK8S_CONFIG_PATH=~/.ck8s/my-ovh-cluster # Path for the configuration
export CK8S_ENVIRONMENT_NAME=my-ovh-cluster # Name of the environment
export CK8S_PGP_FP="FOOBAR1234567" # Fingerprint of your PGP key, retrieve with gpg --list-secret-keys
export CK8S_CLOUD_PROVIDER=baremetal # We don't have a OVH flavor, but baremetal is fine
export CK8S_FLAVOR=dev # Change to "prod" if it's a production cluster you're setting up

S3_ACCESS_KEY="foo" # Access key for S3, see https://docs.ovh.com/gb/en/public-cloud/getting_started_with_the_swift_S3_API/#create-ec2-credentials
S3_SECRET_KEY="bar" # Secret key for S3
```

Download the kubeconfig and set them up for Compliant Kubernetes by following these steps:

### Create the path where they're going to be stored

```ShellSession
mkdir -p "${CK8S_CONFIG_PATH}/.state"
```

### Download the kubeconfig from OVH for the service cluster and run:

```ShellSession
mv ~/Downloads/kubeconfig.yml "${CK8S_CONFIG_PATH}/.state/kube_config_sc.yaml"
sops --encrypt --in-place --pgp "${CK8S_PGP_FP}" "${CK8S_CONFIG_PATH}/.state/kube_config_sc.yaml"
```

### Download the kubeconfig from OVH for the workload cluster and run:

```ShellSession
mv ~/Downloads/kubeconfig.yml "${CK8S_CONFIG_PATH}/.state/kube_config_wc.yaml"
sops --encrypt --in-place --pgp "${CK8S_PGP_FP}" "${CK8S_CONFIG_PATH}/.state/kube_config_wc.yaml"
```

### Prepare DNS records

Set up DNS records in OVH.

Run this snippet and append it into "Change in text format" in your domain in OVH.

```ShellSession
IP="203.0.113.123"

cat <<EOF | envsubst
*.ops.${CK8S_ENVIRONMENT_NAME} 60 IN A ${IP}
*.${CK8S_ENVIRONMENT_NAME} 60 IN A ${IP}
grafana.${CK8S_ENVIRONMENT_NAME} 60 IN A ${IP}
harbor.${CK8S_ENVIRONMENT_NAME} 60 IN A ${IP}
kibana.${CK8S_ENVIRONMENT_NAME} 60 IN A ${IP}
dex.${CK8S_ENVIRONMENT_NAME} 60 IN A ${IP}
notary.harbor.${CK8S_ENVIRONMENT_NAME} 60 IN A ${IP}
EOF
```

Since we don't know the IP for the loadbalancer yet, you can set them to `203.0.113.123` _(TEST-NET-3)_.

Create required buckets that Compliant Kubernetes will use.

```ShellSession
cat <<EOF | sops --encrypt --pgp "${CK8S_PGP_FP}" --output-type ini --input-type ini /dev/stdin > s3cmd.ini
[default]
use_https   = True
host_base   = s3.${REGION}.cloud.ovh.net
host_bucket = s3.${REGION}.cloud.ovh.net
access_key  = ${S3_ACCESS_KEY}
secret_key  = ${S3_SECRET_KEY}
EOF

sops exec-file --no-fifo s3cfg.ini "s3cmd --config {} mb s3://${CK8S_ENVIRONMENT_NAME}-harbor"
sops exec-file --no-fifo s3cfg.ini "s3cmd --config {} mb s3://${CK8S_ENVIRONMENT_NAME}-velero"
sops exec-file --no-fifo s3cfg.ini "s3cmd --config {} mb s3://${CK8S_ENVIRONMENT_NAME}-es-backup"
sops exec-file --no-fifo s3cfg.ini "s3cmd --config {} mb s3://${CK8S_ENVIRONMENT_NAME}-influxdb"
sops exec-file --no-fifo s3cfg.ini "s3cmd --config {} mb s3://${CK8S_ENVIRONMENT_NAME}-sc-logs"
```

Download Compliant Kubernetes and checkout the latest version.

```ShellSession
git clone git@github.com:elastisys/compliantkubernetes-apps.git
cd compliantkubernetes-apps
git checkout v0.13.0
```

Initialize the config.

```ShellSession
bin/ck8s init
```

Update the service cluster configuration for OVH

```ShellSession
yq write --inplace sc-config.yaml global.baseDomain "${CK8S_ENVIRONMENT_NAME}.${DOMAIN}"
yq write --inplace sc-config.yaml global.opsDomain "ops.${CK8S_ENVIRONMENT_NAME}.${DOMAIN}"
yq write --inplace sc-config.yaml global.issuer "letsencrypt-prod"

yq write --inplace sc-config.yaml storageClasses.default "csi-cinder-high-speed"
yq write --inplace sc-config.yaml storageClasses.local.enabled "false"

yq write --inplace sc-config.yaml objectStorage.s3.region "${REGION}"
yq write --inplace sc-config.yaml objectStorage.s3.regionEndpoint "https://s3.${REGION}.cloud.ovh.net/"

yq write --inplace sc-config.yaml fluentd.forwarder.useRegionEndpoint "false"

yq write --inplace sc-config.yaml nfsProvisioner.server "not-used"

yq write --inplace sc-config.yaml ingressNginx.controller.useHostPort "false"
yq write --inplace sc-config.yaml ingressNginx.controller.service.enabled "true"
yq write --inplace sc-config.yaml ingressNginx.controller.service.type "LoadBalancer"
yq write --inplace sc-config.yaml ingressNginx.controller.service.annotations ""

yq write --inplace sc-config.yaml issuers.letsencrypt.prod.email "${ISSUER_MAIL}"
yq write --inplace sc-config.yaml issuers.letsencrypt.staging.email "${ISSUER_MAIL}"

yq write --inplace sc-config.yaml metricsServer.enabled "false"
```

Update the workload cluster configuration for OVH

```ShellSession
yq write --inplace wc-config.yaml global.baseDomain "${CK8S_ENVIRONMENT_NAME}.${DOMAIN}"
yq write --inplace wc-config.yaml global.opsDomain "ops.${CK8S_ENVIRONMENT_NAME}.${DOMAIN}"
yq write --inplace wc-config.yaml global.issuer "letsencrypt-prod"

yq write --inplace wc-config.yaml storageClasses.default "csi-cinder-high-speed"
yq write --inplace wc-config.yaml storageClasses.local.enabled "false"

yq write --inplace wc-config.yaml objectStorage.s3.region "${REGION}"
yq write --inplace wc-config.yaml objectStorage.s3.regionEndpoint "https://s3.${REGION}.cloud.ovh.net/"

yq write --inplace wc-config.yaml ingressNginx.controller.useHostPort "false"
yq write --inplace wc-config.yaml ingressNginx.controller.service.enabled "true"
yq write --inplace wc-config.yaml ingressNginx.controller.service.type "LoadBalancer"
yq write --inplace wc-config.yaml ingressNginx.controller.service.annotations ""

yq write --inplace wc-config.yaml issuers.letsencrypt.prod.email "${ISSUER_MAIL}"
yq write --inplace wc-config.yaml issuers.letsencrypt.staging.email "${ISSUER_MAIL}"

yq write --inplace wc-config.yaml metricsServer.enabled "false"
```

Set s3 credentials

```ShellSession
sops --set '["objectStorage"]["s3"]["accessKey"] "'"${S3_ACCESS_KEY}"'"' secrets.yaml
sops --set '["objectStorage"]["s3"]["secretKey"] "'"${S3_SECRET_KEY}"'"' secrets.yaml
```

### Deploy Compliant Kubernetes

Now you're ready to deploy Compliant Kubernetes.
When the apply command is done, fetch the external IP assigned to the loadbalancer service and update the DNS record to match this.

```ShellSession
bin/ck8s apply sc

bin/ck8s ops kubectl sc get svc -n ingress-nginx ingress-nginx-controller
```

Run this snippet and update the DNS records you added previously to match the external IP of the service cluster load balancer.

```ShellSession
IP="SERVICE_CLUSTER_LB_IP"

cat <<EOF | envsubst
*.ops.${CK8S_ENVIRONMENT_NAME} IN A ${IP}
grafana.${CK8S_ENVIRONMENT_NAME} IN A ${IP}
harbor.${CK8S_ENVIRONMENT_NAME} IN A ${IP}
kibana.${CK8S_ENVIRONMENT_NAME} IN A ${IP}
dex.${CK8S_ENVIRONMENT_NAME} IN A ${IP}
notary.harbor.${CK8S_ENVIRONMENT_NAME} IN A ${IP}
EOF
```

Next, do the same for the workload cluster.

```ShellSession
bin/ck8s apply wc

bin/ck8s ops kubectl wc get svc -n ingress-nginx ingress-nginx-controller
```

Run this snippet and update the DNS records you added previously to match the external IP of the workload cluster load balancer.

```ShellSession
IP="WORKLOAD_CLUSTER_LB_IP"

cat <<EOF | envsubst
*.${CK8S_ENVIRONMENT_NAME} IN A ${IP}
EOF
```

### Limitations

At the time of writing, there's some issues with velero and fluentd.

Workarounds for making this work until fix is out

### Add `s3_endpoint` to fluentd, _fixed with [this issue](https://github.com/elastisys/compliantkubernetes-apps/issues/282)_

To add this, you need to edit the config map fluentd uses.
Find the `<match **>` tag and add `s3_endpoint https://s3.REGION.cloud.ovh.net/`
Where `REGION` matches what region you're using (`waw` in the example).

After that, delete the fluentd pod to force it to reload the configuration.

```ShellSession
$ bin/ck8s ops kubectl sc edit cm -n fluentd fluentd-aggregator-configmap

    .
    .
    .
    <match **>
      @id output-s3
      @type s3

      aws_key_id "#{ENV['AWS_ACCESS_KEY_ID']}"
      aws_sec_key "#{ENV['AWS_ACCESS_SECRET_KEY']}"
      s3_endpoint https://s3.waw.cloud.ovh.net/ # <--- Add this line
      s3_region waw
    .
    .
$ bin/ck8s ops kubectl sc delete pod -n fluentd fluentd-0
```

### Update velero to use 1.3.0 instead of 1.2.0, _fixed with [this issue](https://github.com/elastisys/compliantkubernetes-apps/issues/289)_

For velero to work with OVH S3, velero needs to run with version `1.3.0`.

```ShellSession
bin/ck8s ops kubectl sc patch deployment -n velero velero -p '{"spec":{"template":{"spec":{"containers":[{"name":"velero","image":"velero/velero:v1.3.0"}]}}}}'
bin/ck8s ops kubectl sc patch daemonset -n velero restic -p '{"spec":{"template":{"spec":{"containers":[{"name":"velero","image":"velero/velero:v1.3.0"}]}}}}'

bin/ck8s ops kubectl wc patch deployment -n velero velero -p '{"spec":{"template":{"spec":{"containers":[{"name":"velero","image":"velero/velero:v1.3.0"}]}}}}'
bin/ck8s ops kubectl wc patch daemonset -n velero restic -p '{"spec":{"template":{"spec":{"containers":[{"name":"velero","image":"velero/velero:v1.3.0"}]}}}}'
```
