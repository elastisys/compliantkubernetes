---
tags:
  - NIS2 Minimum Requirement (b) Incident Handling
---
# Troubleshooting for Platform Administrators

{%
    include "./common.md"
    start="<!--for-sme-customers-start-->"
    end="<!--for-sme-customers-end-->"
%}

Help! Something is wrong with my Welkin cluster. Fear no more, this guide will help you make sense.

This guide assumes that:

- You have [pre-requisites](getting-started.md) installed.
- Your environment variables, in particular `CK8S_CONFIG_PATH` is set, and `CLUSTER` set to either `sc` or `wc`.
- Your configuration folder is available.
- `compliantkubernetes-apps` and `compliantkubernetes-kubespray` is available.

!!!important

    `./bin/ck8s` references the `compliantkubernetes-apps` CLI
    `./bin/ck8s-kubespray` references the `compliantkubernetes-kubespray` CLI

!!!important

    For some of the Ansible commands below, you might require root privileges. To run commands as a privileged user with Ansible, use the `--become, -b` flag.

    Example:
    `ansible -i inventory.ini -b all -m ping`

## I have no clue where to start

If you get lost, start checking from the "physical layer" and up.

### Are the Nodes still accessible via SSH?

```bash
ansible -i ${CK8S_CONFIG_PATH}/${CLUSTER}-config/inventory.ini all -m ping
```

### Are the Nodes "doing fine"?

`dmesg` should not display unexpected messages. [OOM](https://en.wikipedia.org/wiki/Out_of_memory) will show up here.

```bash
ansible -i ${CK8S_CONFIG_PATH}/${CLUSTER}-config/inventory.ini all -m shell -a 'echo; hostname; dmesg | tail -n 10'
```

Uptime should show high uptime (e.g., days) and low load (e.g., less than 3):

```bash
ansible -i $CK8S_CONFIG_PATH/${CLUSTER}-config/inventory.ini all -m shell -a 'echo; hostname; uptime'
```

Any process that uses too much CPU?

```bash
ansible -i $CK8S_CONFIG_PATH/${CLUSTER}-config/inventory.ini all -m shell -a 'echo; hostname; ps -Ao user,uid,comm,pid,pcpu,tty --sort=-pcpu | head -n 6'
```

Is there enough disk space? All writeable file-systems should have at least 30% free.

```bash
ansible -i $CK8S_CONFIG_PATH/${CLUSTER}-config/inventory.ini all -m shell -a 'echo; hostname; df -h'
```

Is there enough available memory? There should be at least a few GB of available memory.

```bash
ansible -i $CK8S_CONFIG_PATH/${CLUSTER}-config/inventory.ini all -m shell -a 'echo; hostname; cat /proc/meminfo | grep Available'
```

Can Nodes access the Internet?

```bash
ansible -i $CK8S_CONFIG_PATH/${CLUSTER}-config/inventory.ini all -m shell -a 'echo; hostname; curl --silent  https://checkip.amazonaws.com'
```

Are the Nodes having the proper time? You should see `System clock synchronized: yes` and `NTP service: active`.

```bash
ansible -i $CK8S_CONFIG_PATH/${CLUSTER}-config/inventory.ini all -m shell -a 'echo; timedatectl status'
```

### Is the base OS doing fine?

We generally run the latest [Ubuntu LTS](https://ubuntu.com/blog/what-is-an-ubuntu-lts-release), at the time of this writing Ubuntu 20.04 LTS.

You can confirm this by doing:

```bash
ansible -i $CK8S_CONFIG_PATH/${CLUSTER}-config/inventory.ini all -m shell -a 'cat /etc/lsb-release'
```

Are systemd units running fine? You should see `running` and not `degraded`.

```bash
ansible -i $CK8S_CONFIG_PATH/${CLUSTER}-config/inventory.ini all -m shell -a 'systemctl is-system-running'
```

### Are the Kubernetes clusters doing fine?

Are the Nodes reporting in on Kubernetes? All Kubernetes Nodes, both control-plane and workers, should be `Ready`:

```bash
./bin/ck8s ops kubectl $CLUSTER get nodes
```

### Is Rook doing fine?

If Rook is installed, is Rook doing fine? You should see `HEALTH_OK`.

```bash
export CK8S_KUBESPRAY_PATH=/path/to/compliantkubernetes-kubespray

./bin/ck8s ops kubectl $CLUSTER -n rook-ceph apply -f $CK8S_KUBESPRAY_PATH/rook/toolbox-deploy.yaml
```

Once the Pod is Ready run:

```bash
./bin/ck8s ops kubectl $CLUSTER -n rook-ceph exec deploy/rook-ceph-tools -- ceph status
```

### Are Kubernetes Pods doing fine?

Pods should be `Running` or `Completed`, and fully `Ready` (e.g., `1/1` or `6/6`)?

```bash
./bin/ck8s ops kubectl $CLUSTER get --all-namespaces pods
```

Are all Deployments fine? Deployments should show all Pods Ready, Up-to-date and Available (e.g., `2/2 2 2`).

```bash
./bin/ck8s ops kubectl $CLUSTER get --all-namespaces deployments
```

Are all DaemonSets fine? DaemonSets should show as many Pods Desired, Current, Ready and Up-to-date, as Desired.

```bash
./bin/ck8s ops kubectl $CLUSTER get --all-namespaces ds
```

### Are Helm Releases fine?

All Releases should be `deployed`.

```bash
./bin/ck8s ops helm $CLUSTER list --all --all-namespaces
```

### Is cert-manager doing fine?

Are (Cluster)Issuers fine? All Resources should be `READY=True` or `valid`.

```bash
./bin/ck8s ops kubectl $CLUSTER get clusterissuers,issuers,certificates,orders,challenges --all-namespaces
```

## Where do I find the Nodes public and private IP?

```bash
find . -name inventory.ini
```

or

```bash
ansible-inventory -i ${CK8S_CONFIG_PATH}/${CLUSTER}-config/inventory.ini --list all
```

`ansible_host` is usually the public IP, while `ip` is usually the private IP.

## Node cannot be accessed via SSH

!!!important

    Make sure it is "not you". Are you well connected to the VPN? Is this the only Node which lost SSH access?

!!!important

    If you are using Rook, it is usually set up with replication 2, which means it can tolerate **one** restarting Node. Make sure that, either Rook is healthy or that you are really sure you are restarting the right Node.

Try connecting to the unhealthy Node via a different Node and internal IP:

```bash
UNHEALTHY_NODE=172.0.10.205  # You lost access to this one
JUMP_NODE=89.145.xxx.yyy  # You have access to this one

ssh -J ubuntu@$JUMP_NODE ubuntu@$UNHEALTHY_NODE
```

Try rebooting the Node via Infrastructure Provider specific CLI:

```bash
UNHEALTHY_NODE=cksc-worker-2

# Example for ExoScale
exo vm reboot --force $UNHEALTHY_NODE
```

If using Rook make sure its health goes back to `HEALTH_OK`.

## A Node has incorrect time

Incorrect time on a Node can have sever consequences with replication and monitoring.
In fact, if you follow ISO 27001, [A.12.4.4 Clock Synchronisation](https://www.isms.online/iso-27001/annex-a-12-operations-security/) requires you to ensure clocks are synchronized.

These days, Linux distributions should come out-of-the-box with [timesyncd](https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html) for time synchronization via NTP.

To figure out what is wrong, SSH into the target Node and try the following:

```bash
sudo systemctl status systemd-timesyncd
sudo journalctl --unit systemd-timesyncd
sudo timedatectl status
sudo timedatectl timesync-status
sudo timedatectl show-timesync
```

Possible causes include incorrect NTP server settings, or NTP being blocked by firewall.
For reminder, NTP works over UDP port 123.

## Node seems not fine

!!!important

    If you are using Rook, it is usually set up with replication 2, which means it can tolerate **one** restarting Node. Make sure that, either Rook is healthy or that you are really sure you are restarting the right Node.

Try rebooting the Node:

```bash
UNHEALTHY_NODE=89.145.xxx.yyy

ssh ubuntu@$UNHEALTHY_NODE sudo reboot
```

If using Rook make sure its health goes back to `HEALTH_OK`.

## Node seems really not fine. I want a new one

Is it 2AM? Do not replace Nodes, instead simply add a new one. You might run out of capacity, you might lose redundancy, you might replace the wrong Node. Prefer to add a Node and see if that solves the problem.

## Okay, I want to add a new Node

Prefer this option if you "quickly" need to add CPU, memory or storage (i.e., Rook) capacity.

First, check for infrastructure drift, as shown [here](#how-do-i-check-if-infrastructure-drifted-due-to-manual-intervention).

Depending on your provider:
If the infrastructure is not managed by Terraform you can skip to step 3:

1. Add a new Node by editing the `*.tfvars`.
1. Re-apply Terraform.
1. Add the new node to the `inventory.ini` (skip this step if the cluster is using a dynamic inventory).
1. Re-apply Kubespray only for the new node.

    ```bash
    cd [welkin-kubespray-root-dir]

    CLUSTER=[sc | wc]

    ./bin/ck8s-kubespray run-playbook $CLUSTER facts.yml
    ./bin/ck8s-kubespray run-playbook $CLUSTER scale.yml -b --limit=[new_node_name]
    ```

1. Add SSH keys to the new node if necessary

    ```bash
    ./bin/ck8s-kubespray apply-ssh $CLUSTER --limit=[new_node_name]
    ```

1. Update Network Policies

    ```bash
    cd [welkin-apps-root-dir]

    ./bin/ck8s update-ips sc update
    ./bin/ck8s update-ips wc update

    ./bin/ck8s ops helmfile sc -l app=common-np -i apply
    ./bin/ck8s ops helmfile wc -l app=common-np -i apply

    ./bin/ck8s ops helmfile sc -l app=service-cluster-np -i apply
    # or
    ./bin/ck8s ops helmfile wc -l app=workload-cluster-np -i apply
    ```

    Check that the new Node joined the cluster, as shown [here](#are-the-kubernetes-clusters-doing-fine).

## A systemd unit failed

SSH into the Node. Check which systemd unit is failing:

```bash
systemctl --failed
```

Gather more information:

```bash
FAILED_UNIT=fwupd-refresh.service

systemctl status $FAILED_UNIT
journalctl --unit $FAILED_UNIT
```

## Rook seems not fine

Please check the following upstream documents:

- [Rook Common Issues](https://github.com/rook/rook/blob/master/Documentation/Troubleshooting/common-issues.md)
- [Ceph Common Issues](https://github.com/rook/rook/blob/master/Documentation/Troubleshooting/ceph-common-issues.md)

## Pod seems not fine

Make sure you are on the **right** cluster:

```bash
echo $CK8S_CONFIG_PATH
echo $CLUSTER
```

Find the name of the Pod which is not fine:

```bash
./bin/ck8s ops kubectl $CLUSTER get pod -A

# Copy-paste the Pod and Pod namespace below
UNHEALTHY_POD=prometheus-kube-prometheus-stack-prometheus-0
UNHEALTHY_POD_NAMESPACE=monitoring
```

Gather some "evidence" for later diagnostics, when the heat is over:

```bash
./bin/ck8s ops kubectl $CLUSTER describe pod -n $UNHEALTHY_POD_NAMESPACE $UNHEALTHY_POD
./bin/ck8s ops kubectl $CLUSTER logs -n $UNHEALTHY_POD_NAMESPACE $UNHEALTHY_POD
```

Try to kill and check if the underlying Deployment, StatefulSet or DaemonSet will restart it:

```bash
./bin/ck8s ops kubectl $CLUSTER delete pod -n $UNHEALTHY_POD_NAMESPACE $UNHEALTHY_POD
./bin/ck8s ops kubectl $CLUSTER get pod -A --watch
```

## Helm Release is `failed`

Make sure you are on the **right** cluster:

```bash
echo $CK8S_CONFIG_PATH
echo $CLUSTER
```

Find the failed Release:

```bash
./bin/ck8s ops helm $CLUSTER ls --all-namespaces --all

FAILED_RELEASE=user-rbac
FAILED_RELEASE_NAMESPACE=kube-system
```

Just to make sure, do a drift check, as shown [here](#how-do-i-check-if-apps-drifted-due-to-manual-intervention).

Remove the failed Release:

```bash
./bin/ck8s ops helm $CLUSTER uninstall -n $FAILED_RELEASE_NAMESPACE $FAILED_RELEASE
```

Re-apply `apps` according to documentation.

## cert-manager is not fine

Follow cert-manager's troubleshooting, specifically:

- [Troubleshooting](https://cert-manager.io/docs/troubleshooting/)
- [Troubleshooting Issuing ACME Certificates](https://cert-manager.io/docs/troubleshooting/acme/)

### Failed to perform self check: no such host

If with `kubectl describe challenges -A` you get an error similar to below:

```error
Waiting for HTTP-01 challenge propagation: failed to perform self check
    GET request ''http://url/.well-known/acme-challenge/xVfDZoLlqs4tad2qOiCT4sjChNRausd5iNpbWuGm5ls'':
    Get "http://url/.well-known/acme-challenge/xVfDZoLlqs4tad2qOiCT4sjChNRausd5iNpbWuGm5ls":
    dial tcp: lookup opensearch.domain on 10.177.0.3:53: no such host'
```

Then you might have a DNS issue inside your cluster. Make sure that `global.clusterDns` in `common-config.yaml` is set to the CoreDNS Service IP returned by `kubectl get svc -n kube-system coredns`.

### Failed to perform self check: connection timed out

If with `kubectl describe challenges -A` you get an error similar to below:

```error
Reason: Waiting for http-01 challenge propagation: failed to perform self check GET request 'http://abc.com/.well-known/acme-challenge/Oej8tloD2wuHNBWS6eVhSKmGkZNfjLRemPmpJoHOPkA': Get "http://abc.com/.well-known/acme-challenge/Oej8tloD2wuHNBWS6eVhSKmGkZNfjLRemPmpJoHOPkA": dial tcp 18.192.17.98:80: connect: connection timed out
```

Then your Kubernetes data plane Nodes cannot connect to themselves with the IP address of the load-balancer that fronts them. The easiest is to configure the load-balancer's IP address on the loopback interface of each Nodes. (See example [here](https://github.com/kubernetes-sigs/kubespray/blob/release-2.18/contrib/terraform/exoscale/modules/kubernetes-cluster/templates/cloud-init.tmpl#L29).)

## How do I check if infrastructure drifted due to manual intervention?

Go to the docs of the Infrastructure Provider and run Terraform `plan` instead of `apply`. For Exoscale, it looks as follows:

```bash
TF_SCRIPTS_DIR=$(readlink -f compliantkubernetes-kubespray/kubespray/contrib/terraform/exoscale)
pushd ${TF_SCRIPTS_DIR}
export TF_VAR_inventory_file=${CK8S_CONFIG_PATH}/${CLUSTER}-config/inventory.ini
terraform init
terraform plan \
    -var-file=${CK8S_CONFIG_PATH}/${CLUSTER}-config/cluster.tfvars \
    -state=${CK8S_CONFIG_PATH}/${CLUSTER}-config/terraform.tfstate
popd
```

## How do I check if the Kubespray setup drifted due to manual intervention?

At the time of this writing, this cannot be done, but [efforts are underway](https://github.com/cristiklein/kubespray/tree/make-check-work).

## How do I check if `apps` drifted due to manual intervention?

```bash
# For Management Cluster
./bin/ck8s ops helmfile sc diff  # Respond "n" if you get WARN
```

```bash
# For the Workload Clusters
./bin/ck8s ops helmfile wc diff  # Respond "n" if you get WARN
```

## Velero backup stuck in progress

Velero is known to get stuck `InProgress` when doing backups

```bash
velero backup get

NAME                                 STATUS             ERRORS   WARNINGS   CREATED                          EXPIRES   STORAGE LOCATION   SELECTOR
velero-daily-backup-20211005143248   InProgress         0        0          2021-10-05 14:32:48 +0200 CEST   29d       default            !nobackup
```

First try to delete the backup

```bash
./velero backup delete velero-daily-backup-20211005143248
```

Then kill all the pods under the velero namespace

```bash
./bin/ck8s ops kubectl wc delete pods -n velero --all
```

Check that the backup is gone

```bash
velero backup get

NAME                                 STATUS             ERRORS   WARNINGS   CREATED                          EXPIRES   STORAGE LOCATION   SELECTOR

```

Recreate the backup from a schedule

```bash
velero backup create --from-schedule velero-daily-backup
```

## How do I use `kubectl` and `helm` directly?

This guide makes heavy use of the `compliantkubernetes-apps` CLI to access and control Welkin clusters. However, you can use `kubectl` and `helm` directly, by exporting a `KUBECONFIG` like so:

```bash
export KUBECONFIG=${CK8S_CONFIG_PATH}/.state/kube_config_${CLUSTER}.yaml

kubectl get pods -A

helm list -A
```
