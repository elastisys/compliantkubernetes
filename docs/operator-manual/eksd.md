# Compliant Kubernetes on EKS-D based clusters

This document contains instructions on how to install [Compliant Kubernetes](https://github.com/elastisys/compliantkubernetes-apps) on [AWS](https://aws.amazon.com/?nc2=h_lg) using [EKS-D](https://github.com/aws/eks-distro).

## Requirements

- An AWS account with billing enabled.
- A hosted zone in Route53.
- `yq v3.4.1` installed on you machine.
- `gpg2` installed on your machine with at least one key available.
- `kubectl` installed on your machine.

## Infrastructure and Kubernetes

### Get EKS-D

```ShellSession
git clone https://github.com/aws/eks-distro.git
cd eks-distro/development/kops
git checkout v1-19-eks-1
```
### Configure your AWS environment

Follow the instructions in [Getting Started with kOps on AWS](https://kops.sigs.k8s.io/getting_started/aws/#getting-started-with-kops-on-aws) up until you reach [Creating your first cluster](https://kops.sigs.k8s.io/getting_started/aws/#creating-your-first-cluster).
Unless you have very specific requirements you shouldn't need to take any action when it comes to the [DNS configuration](https://kops.sigs.k8s.io/getting_started/aws/#configure-dns).

If you followed the instructions you should have:

- An IAM user for kOps with the correct permissions.
- Set AWS credentials and any other AWS environment variables you require in your shell.
- An S3 bucket for storing the kOps cluster state.

### Create initial kOps cluster configurations

```ShellSession
export AWS_REGION=<region where you want the infrastructure to be created>
export KOPS_STATE_STORE=s3://<name of the bucket you created in previous step>

SERVICE_CLUSTER="<xyz, e.g. test-sc>.<your hosted zone in Route53, e.g. example.com>"
WORKLOAD_CLUSTER="<xyz, e.g. test-wc>.<your hosted zone in Route53, e.g. example.com>"

for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTER}; do
    export KOPS_CLUSTER_NAME=${CLUSTER}
    ./create_values_yaml.sh
    ./create_configuration.sh
done
```

### Modify kOps cluster configurations

```ShellSession
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTER}; do
echo '
---
- command: update
  path: spec.etcdClusters[0].manager
  value:
    env:
    - name: ETCD_LISTEN_METRICS_URLS
      value: http://0.0.0.0:8081
    - name: ETCD_METRICS
      value: basic

- command: update
  path: spec.networking
  value:
    calico:
      encapsulationMode: ipip

- command: update
  path: spec.metricsServer.enabled
  value:
    false

- command: update
  path: spec.kubeAPIServer
  value:
    image: public.ecr.aws/eks-distro/kubernetes/kube-apiserver:v1.19.6-eks-1-19-1
    auditLogMaxAge: 7
    auditLogMaxBackups: 1
    auditLogMaxSize: 100
    auditLogPath: /var/log/kubernetes/audit/kube-apiserver-audit.log
    auditPolicyFile: /srv/kubernetes/audit/policy-config.yaml
    enableAdmissionPlugins:
    - "PodSecurityPolicy"
    - "NamespaceLifecycle"
    - "LimitRanger"
    - "ServiceAccount"
    - "DefaultStorageClass"
    - "DefaultTolerationSeconds"
    - "MutatingAdmissionWebhook"
    - "ValidatingAdmissionWebhook"
    - "ResourceQuota"
    - "NodeRestriction"

- command: update
  path: spec.fileAssets
  value:
  - name: audit-policy-config
    path: /srv/kubernetes/audit/policy-config.yaml
    roles:
    - Master
    content: |
      apiVersion: audit.k8s.io/v1
      kind: Policy
      rules:
      - level: RequestResponse
        resources:
        - group: ""
          resources: ["pods"]
      - level: Metadata
        resources:
        - group: ""
          resources: ["pods/log", "pods/status"]
      - level: None
        resources:
        - group: ""
          resources: ["configmaps"]
          resourceNames: ["controller-leader"]
      - level: None
        users: ["system:kube-proxy"]
        verbs: ["watch"]
        resources:
        - group: "" # core API group
          resources: ["endpoints", "services"]
      - level: None
        userGroups: ["system:authenticated"]
        nonResourceURLs:
        - "/api*" # Wildcard matching.
        - "/version"
      - level: Request
        resources:
        - group: "" # core API group
          resources: ["configmaps"]
        namespaces: ["kube-system"]
      - level: Metadata
        resources:
        - group: "" # core API group
          resources: ["secrets", "configmaps"]
      - level: Request
        resources:
        - group: "" # core API group
        - group: "extensions" # Version of group should NOT be included.
      - level: Metadata
        omitStages:
          - "RequestReceived"
' | yq w -i -s - ${CLUSTER}/${CLUSTER}.yaml
done

# Configure OIDC flags for kube-apiserver.
for CLUSTER in ${WORKLOAD_CLUSTERS}; do
    yq w -i ${CLUSTER}/${CLUSTER}.yaml 'spec.kubeAPIServer.oidcIssuerURL' https://dex.${SERVICE_CLUSTER}
    yq w -i ${CLUSTER}/${CLUSTER}.yaml 'spec.kubeAPIServer.oidcUsernameClaim' email
    yq w -i ${CLUSTER}/${CLUSTER}.yaml 'spec.kubeAPIServer.oidcClientID' kubelogin
done

# Use bigger machines for service cluster worker nodes.
yq w -i -d2 ${SERVICE_CLUSTER}/${SERVICE_CLUSTER}.yaml 'spec.machineType' t3.large

# Update kOps cluster configurations in state bucket.
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTER}; do
    ./bin/kops-1-19 replace -f "./${CLUSTER}/${CLUSTER}.yaml"
done
```

### Create clusters
```ShellSession
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTER}; do
    export KOPS_CLUSTER_NAME=${CLUSTER}
    ./create_cluster.sh
done
```

The creation of the clusters might take anywhere from 5 minutes to 20 minutes.
You should run the `./cluster_wait.sh` script against all of your clusters as it creates a configmap needed by the `aws-iam-authenticator` pod, e.g.

```ShellSession
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTER}; do
    export KOPS_CLUSTER_NAME=${CLUSTER}
    kubectl config use-context ${CLUSTER}
    timeout 600 ./cluster_wait.sh
done
```

## Compliant Kubernetes Apps

### Get Compliant Kubernetes Apps
```ShellSession
git clone git@github.com:elastisys/compliantkubernetes-apps
cd compliantkubernetes-apps
git checkout v0.11.0
```

### Install requirements
```ShellSession
ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass --connection local --inventory 127.0.0.1, get-requirements.yaml
```

### Initialize configuration
```ShellSession
export CK8S_ENVIRONMENT_NAME=aws-eks-d
#export CK8S_FLAVOR=[dev|prod] # defaults to dev
export CK8S_CONFIG_PATH=~/.ck8s/aws-eks-d
export CK8S_CLOUD_PROVIDER=aws
export CK8S_PGP_FP=<your GPG key ID>  # retrieve with gpg --list-secret-keys
./bin/ck8s init
```

Three files, `sc-config.yaml` and `wc-config.yaml`, and `secrets.yaml`, were generated in the `${CK8S_CONFIG_PATH}` directory.

```ShellSession
ls -l ${CK8S_CONFIG_PATH}
```

### Edit configuration files
Edit the configuration files `sc-config.yaml`, `wc-config.yaml` and `secrets.yaml` and set the appropriate values for some of the configuration fields. Note that, the latter is encrypted.

```ShellSession
vim ${CK8S_CONFIG_PATH}/sc-config.yaml
vim ${CK8S_CONFIG_PATH}/wc-config.yaml
sops ${CK8S_CONFIG_PATH}/secrets.yaml
```

You should perform the following changes:

```ShellSession
# sc-config.yaml
global:
  baseDomain: "set-me"     # Set to ${SERVICE_CLUSTER}
  opsDomain: "set-me"      # Set to ops.${SERVICE_CLUSTER}
  issuer: letsencrypt-prod
  verifyTls: true
  clusterDNS: 100.64.0.10

storageClasses:
  default: kops-ssd-1-17
  nfs:
    enabled: false
  cinder:
    enabled: false
  local:
    enabled: false
  ebs:
    enabled: false

objectStorage:
  type: "s3"
  s3:
    region: "set-me"          # e.g. eu-north-1
    regionEndpoint: "set-me"  # e.g. https://s3.eu-north-1.amazonaws.com

issuers:
  letsencrypt:
    email: "set-me"  # Set to a valid email address
```

```ShellSession
# wc-config.yaml
global:
  baseDomain: "set-me"     # Set to ${WORKLOAD_CLUSTER}
  opsDomain: "set-me"      # Set to ops.${SERVICE_CLUSTER}
  issuer: letsencrypt-prod
  verifyTls: true
  clusterDNS: 100.64.0.10

storageClasses:
  default: kops-ssd-1-17
  nfs:
    enabled: false
  cinder:
    enabled: false
  local:
    enabled: false
  ebs:
    enabled: false

objectStorage:
  type: "s3"
  s3:
    region: "set-me"          # e.g. eu-north-1
    regionEndpoint: "set-me"  # e.g. https://s3.eu-north-1.amazonaws.com


opa:
  enabled: false # Does not work with k8s 1.19+

issuers:
  letsencrypt:
    email: "set-me"  # Set to a valid email address
```

```ShellSession
# secrets.yaml
objectStorage:
  s3:
    accessKey: "set-me" # Set to your AWS S3 accesskey
    secretKey: "set-me" # Set to your AWS S3 secretKey
```

### PSP and RBAC
Since we've enabled the PodSecurityPolicy admission plugin in the kube-apiserver we'll need to create some basic PSPs and RBAC rules that both you and Compliant Kubernetes Apps will need to run workloads.

```ShellSession
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTER}; do
kubectl config use-context ${CLUSTER}

# Install 'restricted' and 'privileged' podSecurityPolicies.
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/master/content/en/examples/policy/privileged-psp.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/master/content/en/examples/policy/restricted-psp.yaml

# Install RBAC so authenticated users are be able to use the 'restricted' psp.
echo '
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    addonmanager.kubernetes.io/mode: Reconcile
  name: psp:restricted
rules:
- apiGroups:
  - policy
  resourceNames:
  - restricted
  resources:
  - podsecuritypolicies
  verbs:
  - use

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: psp:any:restricted
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: psp:restricted
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:authenticated
' | kubectl apply -f -
done
```

### Create placeholder DNS records
To avoid negative caching and other surprises.
Create the following records using your favorite tool or you can use the [Import zone file](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating-import.html) feature in Route53:

```ShellSession
echo "
*.${SERVICE_CLUSTER}     60s A 203.0.113.123
*.${WORKLOAD_CLUSTER}    60s A 203.0.113.123
*.ops.${SERVICE_CLUSTER} 60s A 203.0.113.123
"
```

### Create S3 buckets
Depending on you configuration you may want to create S3 buckets.
Create the following buckets using your favorite tool or via the AWS console:

```ShellSession
# List bucket names.
{ yq r ${CK8S_CONFIG_PATH}/wc-config.yaml 'objectStorage.buckets.*';\
    yq r ${CK8S_CONFIG_PATH}/sc-config.yaml 'objectStorage.buckets.*'; } | sort | uniq

# Create buckets using the AWS CLI.
# Assumes that the same bucket is used for velero in both service and workload cluster.
for BUCKET in $(yq r ${CK8S_CONFIG_PATH}/sc-config.yaml 'objectStorage.buckets.*'); do
    aws s3api create-bucket\
        --bucket ${BUCKET} \
        --create-bucket-configuration LocationConstraint=${AWS_REGION}
done
```

### Prepare kubeconfigs
Compliant Kubernetes Apps demands that the kube contexts for the workload and service cluster are found in separate files encrypted with sops.

```ShellSession
kubectl config view --minify --flatten --context=${SERVICE_CLUSTER} > ${CK8S_CONFIG_PATH}/.state/kube_config_sc.yaml
sops -e -i --config ${CK8S_CONFIG_PATH}/.sops.yaml ${CK8S_CONFIG_PATH}/.state/kube_config_sc.yaml

kubectl config view --minify --flatten --context=${WORKLOAD_CLUSTER} > ${CK8S_CONFIG_PATH}/.state/kube_config_wc.yaml
sops -e -i --config ${CK8S_CONFIG_PATH}/.sops.yaml ${CK8S_CONFIG_PATH}/.state/kube_config_wc.yaml
```

### Install apps
You can install apps in parallel, although it is recommended to install the service cluster before the workload cluster.

```ShellSession
# Service cluster
./bin/ck8s apply sc # Respond "n" if you get a WARN

# Workload cluster
./bin/ck8s apply wc # Respond "n" if you get a WARN
```

Run the following to get metrics from etcd-manager
```ShellSession
# Service cluster
./bin/ck8s ops helmfile sc -l app=kube-prometheus-stack apply --skip-deps --set kubeEtcd.service.selector.k8s-app=etcd-manager-main --set kubeEtcd.service.targetPort=8081

# Workload cluster
./bin/ck8s ops helmfile wc -l app=kube-prometheus-stack apply --skip-deps --set kubeEtcd.service.selector.k8s-app=etcd-manager-main --set kubeEtcd.service.targetPort=8081
```

### Update DNS records
Now that we've installed all applications, the loadbalancer fronting the ingress controller should be ready.
Run the following commands and update the A records in Route53.

```ShellSession
sc_lb=$(./bin/ck8s ops kubectl sc -n ingress-nginx get svc ingress-nginx-controller -ojsonpath={.status.loadBalancer.ingress[0].hostname})
wc_lb=$(./bin/ck8s ops kubectl wc -n ingress-nginx get svc ingress-nginx-controller -ojsonpath={.status.loadBalancer.ingress[0].hostname})
sc_lb_ip=$(dig +short ${sc_lb} | head -1)
wc_lb_ip=$(dig +short ${wc_lb} | head -1)

echo "
*.${SERVICE_CLUSTER}     60s A ${sc_lb_ip}
*.${WORKLOAD_CLUSTER}    60s A ${wc_lb_ip}
*.ops.${SERVICE_CLUSTER} 60s A ${sc_lb_ip}
"
```

## Teardown

### Compliant Kubernetes Apps
This step is optional.
If this is not run you'll have to check and manually remove any leftover cloud resources like S3 buckets, ELBs, and EBS volumes.

```ShellSession
git checkout 6f2e386
timeout 180 ./scripts/clean-wc.sh
timeout 180 ./scripts/clean-sc.sh

# Delete buckets
for BUCKET in $(yq r ${CK8S_CONFIG_PATH}/sc-config.yaml 'objectStorage.buckets.*'); do
    aws s3 rb --force s3://${BUCKET}
done

# Delete config repo
rm -rf ${CK8S_CONFIG_PATH}
```

Remember to also remove the A records from Route53.

### Infrastructure and Kubernetes
Enter `eks-distro/development/kops` and run:

```ShellSession
# Destroy clusters and local cluster configurations.
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTER}; do
    export KOPS_CLUSTER_NAME=${CLUSTER}
    ./delete_cluster.sh
    rm -rf ${CLUSTER}
done
```

You'll have to manually remove the leftover kOps A records from Route53.

```ShellSession
# Get names of the A records to be removed.
for CLUSTER in ${SERVICE_CLUSTER} ${WORKLOAD_CLUSTER}; do
    echo kops-controller.internal.${CLUSTER}
done
```

Finally, you'll also need to remove the `${KOPS_STATE_STORE}` from S3 and the IAM user that you used for this guide.
