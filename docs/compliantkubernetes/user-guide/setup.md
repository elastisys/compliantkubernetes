# Install Prerequisites

<!--user-demo-setup-start-->

As a user, you will need the following before you get started with Compliant Kubernetes:

<!--prerequisite-software-start-->
Required software:

* [oidc-login](https://github.com/int128/kubelogin), which helps you log into your Kubernetes cluster via OpenID Connect integration with your Identity Provider of choice

Your cluster management software of choice, of which you can choose either or both:

* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/), a command-line tool to help manage your Kubernetes resources
* [Lens](https://k8slens.dev/), a graphical user interface to help manage your Kubernetes resources (see also our [dedicated page on Lens integration](kubernetes-ui.md))

Optional, but very useful, tools for developers and DevOps engineers:

* [docker](https://docs.docker.com/get-docker/), if you want to build (Docker) container images locally
* [helm](https://helm.sh/docs/intro/install/), if you want to manage your application with the Helm package manager
<!--prerequisite-software-end-->

## Verify Your Prerequisite Software and its Configuration

The easiest way to get started is to request a working installation from a [managed Compliant Kubernetes provider](https://elastisys.com). This means you will receive:


<!--bill-of-materials-service-start-->
* URLs for the Elastisys Compliant Kubernetes UI components: OpenSearch Dashboards, Grafana, and Harbor;
* a [kubeconfig](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) file for configuring `kubectl` or Lens access to the underlying Kubernetes cluster; and
* (optionally and rarely) a static username and password. Note that normally, you should log in via a username and a password of your organization's Identity Provider, such as LDAP, Active Directory, or Google Workspaces account.
<!--bill-of-materials-service-end-->

Make sure you have configured your tools properly:

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
curl --head https://harbor.$DOMAIN/healthz
curl --head https://grafana.$DOMAIN/healthz
curl --head https://opensearch.$DOMAIN/api/status
curl --insecure --head https://app.$DOMAIN/healthz  # WC Ingress Controller
# All commands above should return 'HTTP/2 200'
```

<!--user-demo-setup-end-->
