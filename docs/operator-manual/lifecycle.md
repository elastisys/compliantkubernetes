# Multitenancy with ck8s-cluster

This document contains sample instructions on how to setup one service cluster together with multiple workload clusters. As stated, the instructions below are just samples, you need update them according to your situation and requirements. You will find more details on the commands executed in the cluster and apps repos. The sample instructions are shown for the exoscale cloud provider and the [exoscale cli](https://github.com/exoscale/cli/releases/tag/v1.21.0) is used to manage DNS. If you are using any other cloud provider use their corresponding tool for managing DNS.

The following repositores and commits have been tested:
- [ck8s-cluster](https://github.com/elastisys/ck8s-cluster/tree/324ac074a337b99b83a464ce0189ed2c0f267e19)
- [compliantkubernetes-apps](https://github.com/elastisys/compliantkubernetes-apps/tree/5b584dd568c39fea1630de48405679fb93b2c6bd)

The cluster setup will be as follows
- `mtt-0` will be the the repository from where the service cluster will be installed.
- `mtt-{1,2}` will be repositories from where we'll install workload clusters.

Simply do a _search and replace_ if you want to name your clusters something else.
`mtt` - simply stands for _multi-tenancy-test_.

### Infrastructure and kubernetes
1. Set some variables

    ```bash
    domain=<your_domain>
    pgp_fp=<your_pgp_fp>
    config_path=<path_to_store_config_repos>
    ```

1. Init repos

    ```bash
    ./dist/ck8s_linux_amd64 init mtt-0 exoscale --flavor dev --pgp-fp ${pgp_fp} --config-path ${config_path}/mtt-0
    ./dist/ck8s_linux_amd64 init mtt-1 exoscale --flavor dev --pgp-fp ${pgp_fp} --config-path ${config_path}/mtt-1
    ./dist/ck8s_linux_amd64 init mtt-2 exoscale --flavor dev --pgp-fp ${pgp_fp} --config-path ${config_path}/mtt-2
    ```

2. For each repo edit the configuration files

3. Create infrastructure and install kubernetes for the clusters

    ```bash
    ./dist/ck8s_linux_amd64 apply --cluster sc --config-path ${config_path}/mtt-0
    ./dist/ck8s_linux_amd64 apply --cluster wc --config-path ${config_path}/mtt-1
    ./dist/ck8s_linux_amd64 apply --cluster wc --config-path ${config_path}/mtt-2
    ```

3. Get the ip address of the cluster's loadbalancer

    ```bash
    mtt_0_lb_ip=$(./dist/ck8s_linux_amd64 internal terraform output --cluster sc --config-path ${config_path}/mtt-0 | jq -r '.sc_ingress_controller_lb_ip_address.value')
    mtt_1_lb_ip=$(./dist/ck8s_linux_amd64 internal terraform output --cluster wc --config-path ${config_path}/mtt-1 | jq -r '.wc_ingress_controller_lb_ip_address.value')
    mtt_2_lb_ip=$(./dist/ck8s_linux_amd64 internal terraform output --cluster wc --config-path ${config_path}/mtt-2 | jq -r '.wc_ingress_controller_lb_ip_address.value')
    ```

4. Create DNS records

    ```bash
    exo dns add A ${domain} -a ${mtt_0_lb_ip} -n *.ops.mtt-0
    exo dns add A ${domain} -a ${mtt_0_lb_ip} -n *.mtt-0
    exo dns add A ${domain} -a ${mtt_1_lb_ip} -n *.mtt-1
    exo dns add A ${domain} -a ${mtt_2_lb_ip} -n *.mtt-2
    ```

### Apps
1. Init config

    ```bash
    export CK8S_CLOUD_PROVIDER=exoscale

    export CK8S_ENVIRONMENT_NAME=mtt-0
    export CK8S_CONFIG_PATH=${config_path}/mtt-0
    ./bin/ck8s init

    export CK8S_ENVIRONMENT_NAME=mtt-1
    export CK8S_CONFIG_PATH=${config_path}/mtt-1
    ./bin/ck8s init

    export CK8S_ENVIRONMENT_NAME=mtt-2
    export CK8S_CONFIG_PATH=${config_path}/mtt-2
    ./bin/ck8s init
    ```

2. Edit
  - `secrets.yaml` for all clusters
  - `sc-config.yaml` for the service cluster
  - `wc-config.yaml` for all workload clusters
  You should use the same value for `opsDomain` in all clusters.

3. Install applications

    ```
    export CK8S_CONFIG_PATH=${config_path}/mtt-0
    ./bin/ck8s apply sc

    export CK8S_CONFIG_PATH=${config_path}/mtt-1
    ./bin/ck8s apply wc

    export CK8S_CONFIG_PATH=${config_path}/mtt-2
    ./bin/ck8s apply wc
    ```

### Teardown

```bash
# Tear down infra and k8s
./dist/ck8s_linux_amd64 destroy --cluster sc --config-path ${config_path}/mtt-0 --kubernetes-cleanup=false
./dist/ck8s_linux_amd64 destroy --cluster wc --config-path ${config_path}/mtt-1 --kubernetes-cleanup=false
./dist/ck8s_linux_amd64 destroy --cluster wc --config-path ${config_path}/mtt-2 --kubernetes-cleanup=false

# Remove dns records
exo dns remove ${domain} *.ops.mtt-0
exo dns remove ${domain} *.mtt-0
exo dns remove ${domain} *.mtt-1
exo dns remove ${domain} *.mtt-2
```

## Notes

- OIDC and kubelogin were not tested.
- Ingress of workload clusters were not tested, but are expected to work without issues.
- Blackbox exporter isn't able to check the kube-apiserver in any of the workload clusters.

