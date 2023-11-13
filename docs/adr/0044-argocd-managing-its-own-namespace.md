# ArgoCD is not allowed to manage its own namespace.

* Status: Accepted
* Deciders: Arch Meeting
* Date: 2023-10-12

## Context and Problem Statement

Currently, ArgoCD is setup in namespaced mode.
We give it a [list of Namespaces](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters) that ArgoCD should manage and a list of permissions that it has on those namespaces through ArgoCD's [inclusions](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#resource-exclusioninclusion) and Kubernetes RBAC to the service account to back this.
This service account has a larger set of permissions than a developer's most privileged accounts do.

If an Application Developer wants to deploy resources other than ArgoCD `apps`, `applicationSets`, and `appProjects` into the `argocd-system` namespace via ArgoCD itself, it will fail since `argocd-system` is not a managed namespace in ArgoCD.

Do we want to make `argocd-system` a managed namespace in our ArgoCD offering?

## Decision Drivers

* We want to maintain Platform security and stability.
* We want to find a solution which is scalable and minimizes Platform Administrator burden.
* We want to best serve the Application Developers.
* We want to make the Platform Administrator life easier.
* We want to avoid Infrastructure Provider dependent implementation sprawl.

## Considered Options

1. Yes, we make ArgoCD manage its own namespace.

2. No, we do not make ArgoCD manage its own namespace.

## Decision Outcome

Chosen option:

- No, we do not allow argocd to manage its own namespace.
    - ArgoCD, through an Application Developer's configuration, should not deploy standard Kubernetes resources (such as pods or secrets) directly into its own namespace. If there is a requirement for such deployments, it should be initiated through a service ticket, ensuring that it undergoes thorough security and stability assessments to prevent any compromises to the platform.

### Positive Consequences

- We get to keep ArgoCD secure.
- A malicious user cannot exploit a potential bug in ArgoCD to deploy resources into `argocd-system` namespace.
- An Application Developer will not be able to deploy a malicious pod and read secrets in `argocd-system` namespace.

### Negative Consequences

- An Application Developer may also not be able to deploy standard Kubernetes resources via ArgoCD into `argocd-system` namespaces.
    - This should not count as a negative consequence, because our current security stance is that Application Developers should not be supposed to deploy into the `argocd-system` Namespace at all.
