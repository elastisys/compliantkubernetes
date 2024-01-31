# Release Notes


## Compliant Kubernetes Argo CD
<!-- BEGIN TOC -->
- [v2.9.5-ck8s1](#v295-ck8s1) - 2024-01-30
- [v2.7.14-ck8s1](#v2714-ck8s1) - 2023-10-31
- [v2.4.20-ck8s1](#v2420-ck8s1) - 2023-03-29
<!-- END TOC -->

### v2.9.5-ck8s1

Released 2024-01-30

#### Updated:

- Updated ArgoCD to `v2.9.5`.

<!-- -->
> [!IMPORTANT]
> **Platform Administrator Notice(s)**
> - Application Developers can with these change choose to either use `age` or `gpg` encryption to use with their Helm secrets, as long as an Platform Administrator configures ArgoCD with the correct `helmSecrets.type` for them.
> - Customer access to the Argo CD GUI is now configured through `customerAdminGroups`, `customerDevGroups` and/or `customerAdminUsers`.
<!-- -->
> [!NOTE]
> **Application Developer Notice(s)**
> - Application Developers now have to give Secret  `helm-secrets-private-keys` in the `argocd-system` namespace (used for storing encryption keys) a different label-value than before. The label has to be: `argocd.argoproj.io/secret-type=helm-secrets`The label for Secrets named `repo-*` remains the same, i.e.: `argocd.argoproj.io/secret-type=repository`.
> - Fixes so that Application Developers have correct permissions for getting and editing argo notifications configmap in the argocd-system namespace.

#### Added

- Added networkpolicy generator chart, rules and policies
- Added templating for supporting age
- Added vals as a secret backend

### v2.7.14-ck8s1

Released 2023-10-31

#### Updated:

- Updated ArgoCD to `v2.7.14`.

#### Added

- Added support for using ArgoCD declaratively
- Added support for managing secrets via helm-secrets through ArgoCD
- Added support for managing secrets via sealed secrets through ArgoCD

### v2.4.20-ck8s1

Released 2023-03-29

First release of Argo CD with version `2.4.20`!
