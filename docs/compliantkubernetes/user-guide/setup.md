# Install Prerequisites

<!--user-demo-setup-start-->

As a user, you will need the following before you get started with Compliant Kubernetes:

* [docker](https://docs.docker.com/get-docker/)
* [helm](https://helm.sh/docs/intro/install/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [oidc-login](https://github.com/int128/kubelogin); we suggest installing it via [krew](https://github.com/kubernetes-sigs/krew)

The easier is to request a dev environment from a [managed Compliant Kubernetes provider](https://elastisys.com). You should receive:

* URLs for Compliant Kubernetes UI components, such as the dashboard, container registry, logs, etc.
* A [kubeconfig](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) file for configuring kubectl access to the cluster.
* (Optionally) Static username and password. Normally, you should log in via a username and a password of your organizations identity provider.

Make sure you configure your tools properly:

```
export KUBECONFIG=path/of/kubeconfig.yaml  # leave empty if you use the default of ~/.kube/config
export DOMAIN=  # the domain you received from the administrator
```

To verify if the required tools are installed and work as expected, type:

```bash
docker version
kubectl version  --client
helm version
# You should see the version number of installed tools and no errors.
```

To verify the received KUBECONFIG, type:

```bash
# Notice that you will be asked to complete browser-based single sign-on
kubectl get nodes
# You should see the Nodes of your Kubernetes cluster
```

To verify the received URLs, type:

```bash
curl --head https://dex.$DOMAIN/healthz
curl --include https://harbor.$DOMAIN/api/v2.0/health
curl --head https://grafana.$DOMAIN/healthz
curl --head https://kibana.$DOMAIN/api/status
# All commands above should return 'HTTP/2 200'
```

<!--user-demo-setup-end-->
