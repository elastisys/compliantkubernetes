# Kubernetes API

[](<!-- How does the kubeconfig of a Compliant Kubernetes cluster typically look? How does a user install/merge it with their existing kubeconfig? -->)

To access the Kubernetes APIs in Compliant Kubernetes, you will need at least one [kubeconfig](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/) file.
Compliant Kubernetes comes with three kinds of kubeconfig files:

* Service cluster administrator access
* Workload cluster administrator access
* User access

For user workload management, the User access kubeconfig file should be used.
This access is further described in the [User access](#user-access) section.

The service and workload cluster administrator kubeconfig files have full access to their respective clusters.
These kubeconfig files should only be used by the operators to install and maintain Compliant Kubernetes.
For more information on operating Compliant Kubernetes, see the [Operator Manual](../operator-manual/index.md).

## User access

[](<!-- What Kubernetes roles does a user have by default? What is allowed and what is disallowed? Why? -->)

The User access kubeconfig file provides individual access to the Kubernetes API through [dex](https://github.com/dexidp/dex).
Normally, you should authenticate using your organizations identity provider connected to dex, but it is also possible for operators to configure static usernames and passwords.

The authorization is done by the Kubernetes API based on [Kubernetes role-based access controls](https://kubernetes.io/docs/reference/access-authn-authz/rbac/), and a cluster operator has to grant you permission.
If you are authorized to log in to the cluster, you will have administrator access to the user workload namespaces by default.
In order to follow [the principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege), you as an user should only have sufficient access to manage resources required by your application.
User access to the Kubernetes API may need to be restricted from case to case to follow the principle of least privilege.
These access controls are configurable by the cluster operators.

## Usage guide

[](<!-- Please show step-by-step how to use kubectl, including auth flow via Dex and Terminal screenshots. -->)

This focuses on using the User access kubeconfig.
To use the operator kubeconfig files, see the [Operator Manual](../operator-manual/index.md).

### Using the kubeconfig file

The kubeconfig file can be used with `kubectl` by:

* Setting and exporting the `KUBECONFIG` environment variable:

  ```bash
  export KUBECONFIG=/path/to/kubeconfig
  kubectl get pods
  ```

* Merging the configuration with your existing kubeconfig file, see [Kubernetes documentation on merging kubeconfig files](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/#merging-kubeconfig-files).

### Authenticating to the Kubernetes API

Make sure you have installed the [oidc-login](https://github.com/int128/kubelogin) plugin (also known as kubelogin) in `kubectl`.
With the plugin installed, run a `kubectl` command and the plugin will launch a browser where you log in to the cluster.
Your credentials will then be used by the Kubernetes API to make sure you are authorized.
Once you have logged in through the browser, you are authenticated to the cluster.

## Further reading

[](<!-- Further reading: Dex, Kubernetes Tutorial, other relevant documentation -->)

* [dex on GitHub](https://github.com/dexidp/dex)
* [oidc-login/kubelogin on GitHub](https://github.com/int128/kubelogin)
* [Organizing Cluster Access Using kubeconfig Files
](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
