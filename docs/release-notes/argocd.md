# Release Notes


## Compliant Kubernetes Argo CD
<!-- BEGIN TOC -->
- [v2.9.5-ck8s1](#v295-ck8s1) - 2024-01-30
- [v2.7.14-ck8s1](#v2714-ck8s1) - 2023-10-31
- [v2.4.20-ck8s1](#v2420-ck8s1) - 2023-03-29
<!-- END TOC -->

### v2.9.5-ck8s1

Released 2024-01-30

#### Updated

- Updated ArgoCD to `v2.9.5`.


#### Changed

- Secret  `helm-secrets-private-keys` in the `argocd-system` namespace (used for storing encryption keys) now uses a different label-value than before. The label has to be: `argocd.argoproj.io/secret-type=helm-secrets`

#### Added

- Added networkpolicies for Argo CD components
- Added support for age encrypted helm secrets
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
