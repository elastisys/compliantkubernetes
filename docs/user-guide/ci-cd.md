CI/CD Integration
=================

Compliant Kubernetes does not come with a [CI/CD](https://en.wikipedia.org/wiki/CI/CD) solution. Fortunately, it can be easily integrated with your existing CI/CD solution.

!!!important
    Access control is an extremely important topic for passing an audit for compliance with data privacy and data security regulations. For example, Swedish patient data law requires all persons to be identified with individual credentials and that logs should capture who did what.

    Therefore, Compliant Kubernetes has put significant thought into how to do proper access control. As a consequence, CI/CD solutions that require cluster-wide permissions and/or introduce their own notion of access control are highly discouraged. Make sure you thoroughly evaluate your CI/CD solution with your CISO before investing in it.

Background
----------

For the purpose of Compliant Kubernetes, one can distinguish between two "styles" of CI/CD: push-style and pull-style.

**Push-style CI/CD** -- like [GitLab CI](https://docs.gitlab.com/ee/ci/) or [GitHub Actions](https://docs.github.com/en/actions) -- means that a commit will trigger some commands on a CI/CD worker, which will push changes into the Compliant Kubernetes cluster. The CI/CD worker generally runs outside the Kubernetes cluster. Push-style CI/CD solutions should work out-of-the-box and require no special considerations for Compliant Kubernetes.


**Pull-styles CI/CD** -- like [ArgoCD](https://argo-cd.readthedocs.io/en/stable/) or [Flux](https://fluxcd.io/) -- means that a special controller is installed inside the cluster, which monitors a Git repository. When a change is detected the controller "pulls" changes into the cluster from the Git repository. The special controller often requires considerable permissions and introduces a new notion of access control, which is problematic from a compliance perspective. As shown below, some pull-style CI/CD solutions can be used with Compliant Kubernetes, others not.

Push-style CI/CD
----------------

Please follow [this tutorial](https://www.auroria.io/kubernetes-ci-cd-service-account-setup/) to create the relevant credentials. For improved access control, make sure the Role you create gets the least permissions possible. For example, if your application only consists of a Deployment, Service and Ingress, those should be the only resources available to the Role.

The user-token **must** be treated as a secret and injected into the CI/CD pipeline via a proper secrets handing feature, such as GitLab CI's [protected variable](https://docs.gitlab.com/ee/ci/variables/#add-a-cicd-variable-to-a-project) and GitHub Action's [secrets](https://docs.github.com/en/actions/reference/encrypted-secrets#using-encrypted-secrets-in-a-workflow).

ArgoCD
------

By default, ArgoCD installs a [ClusterRole with wide permissions](https://github.com/argoproj/argo-cd/blob/v2.1.0-rc3/manifests/install.yaml#L2668), which can be used to bypass Compliant Kubernetes's access control. Using it as-is might be non-compliant with various regulations.

Instead, edit the default ArgoCD manifest to create a very restricted Role that only operates in the target namespace.

Flux v1
-------

Flux v1 is [in maintenance mode](https://github.com/fluxcd/flux/issues/3320) and might become obsolete soon.

Flux v2
-------

Flux v2 brings is own notion of access control and requires [special considerations](https://github.com/fluxcd/flux2-multi-tenancy#enforce-tenant-isolation) to ensure it obey Compliant Kubernetes access control. Installing it can only be done by the operator of the Compliant Kubernetes cluster, after having made a thorough risk-reward analysis. At the time of this writing, due to these special considerations, we discourage Flux v2.
