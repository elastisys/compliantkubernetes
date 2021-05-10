# Troubleshooting Tools

Help! Something is wrong with my Compliant Kubernetes cluster. Fear no more, this guide will help you make sense.

This guide assumes that:

* You have [pre-requisites](operator-manual/getting-started/) installed.
* Your environment variables, in particular `CK8S_CONFIG_PATH` is set.
* Your config folder (e.g. [for OpenStack](/operator-manual/openstack/#initialize-configuration-folder)) is available.
* `compliantkubernetes-apps` and `compliantkubernetes-kubespray` is available.

## I have no clue where to start

If you get lost, start checking from the "physical layer" and up.

### Are the Nodes still accessible via SSH?

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ansible -i $CK8S_CONFIG_PATH/inventory/$CLUSTER/inventory.ini all -m ping
done
```

### Are the Nodes "doing fine"?

Dmesg should not display unexpected messages:

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ansible -i $CK8S_CONFIG_PATH/inventory/$CLUSTER/inventory.ini all -m shell -a 'echo; hostname; dmesg | tail -n 10'
done
```

Uptime should show high uptime (e.g., days) and low load (e.g., less than 3):

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ansible -i $CK8S_CONFIG_PATH/inventory/$CLUSTER/inventory.ini all -m shell -a 'echo; hostname; uptime'
done
```

Any process that uses too much CPU?

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ansible -i $CK8S_CONFIG_PATH/inventory/$CLUSTER/inventory.ini all -m shell -a 'echo; hostname; ps -Ao user,uid,comm,pid,pcpu,tty --sort=-pcpu | head -n 6'
done
```

Is there enough disk space? All writeable file-systems should have at least 30% free.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ansible -i $CK8S_CONFIG_PATH/inventory/$CLUSTER/inventory.ini all -m shell -a 'echo; hostname; df -h'
done
```

Is there enough available memory? There should be at least a few GB of available memory.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ansible -i $CK8S_CONFIG_PATH/inventory/$CLUSTER/inventory.ini all -m shell -a 'echo; hostname; cat /proc/meminfo | grep Available'
done
```

Can Nodes access the Internet?

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    ansible -i $CK8S_CONFIG_PATH/inventory/$CLUSTER/inventory.ini all -m shell -a 'echo; hostname; curl --silent  https://checkip.amazonaws.com'
done
```

### Are the Kubernetes clusters doing fine?

Are the Nodes reporting in on Kubernetes? All Kubernetes Nodes, both control-plane and workers, should be `Ready`:

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} get nodes'
done
```

If Rook is installed, is Rook doing fine?

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} -n rook-ceph apply -f ./compliantkubernetes-kubespray/rook/toolbox-deploy.yaml'
done

for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    CEPH_TOOLS_POD=$(
        sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
            'kubectl --kubeconfig {} -n rook-ceph get pod -l "app=rook-ceph-tools" -o name')
    echo $CEPH_TOOLS_POD
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} -n rook-ceph exec '$CEPH_TOOLS_POD' -- ceph status'
done
```

Are all Pod fine? Pods should be `Running` or `Completed`, and fully `Ready` (e.g., `1/1` or `6/6`)?

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} get --all-namespaces pods'
done
```

Are all Deployments fine? Deployments should show all Pods Ready, Up-to-date and Available (e.g., `2/2 2 2`).

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} get --all-namespaces deployments'
done
```

Are all DaemonSets fine? DaemonSets should show as many Pods Desired, Current, Ready and Up-to-date, as Desired.

```bash
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    sops exec-file ${CK8S_CONFIG_PATH}/.state/kube_config_$CLUSTER.yaml \
        'kubectl --kubeconfig {} get --all-namespaces ds'
done
```
