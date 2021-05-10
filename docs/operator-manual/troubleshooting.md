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
