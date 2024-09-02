# Release Notes

## Compliant Kubernetes Argo CD

<!-- BEGIN TOC -->

- [v2.12.0-ck8s1](#v2120-ck8s1) - 2024-09-02
- [v2.9.9-ck8s1](#v299-ck8s1) - 2024-03-20
- [v2.9.5-ck8s1](#v295-ck8s1) - 2024-01-30
- [v2.7.14-ck8s1](#v2714-ck8s1) - 2023-10-31
- [v2.4.20-ck8s1](#v2420-ck8s1) - 2023-03-29
<!-- END TOC -->

### v2.12.0-ck8s1

Released 2024-09-02

#### Improvement(s)

- Updated Argo CD to `v2.12.0`.

### v2.9.9-ck8s1

Released 2024-03-20

!!! danger "Security Notice(s)"

    - This upgrade mitigates the following high and medium security vulnerabilities:
      - [Denial of Service (DoS) Vulnerability Due to Unsafe Array Modification in Multi-threaded Environment](https://github.com/argoproj/argo-cd/security/advisories/GHSA-6v85-wr92-q4p7)
      - [Bypassing Rate Limit and Brute Force Protection Using Cache Overflow](https://github.com/argoproj/argo-cd/security/advisories/GHSA-2vgg-9h6w-m454)
      - [Bypassing Brute Force Protection via Application Crash and In-Memory Data Loss](https://github.com/argoproj/argo-cd/security/advisories/GHSA-x32m-mvfj-52xv)

#### Improvement(s)

- Patch ArgoCD to v2.9.9 - See security notice above.
- Allow application developers to delete and watch ArgoCD resources they create declaratively.

#### Other(s)

- Correct Network Policies for applicationset controller and repo server to allow ApplicationSets to be created.
- Correct Gatekeeper policies to allow ArgoCD secrets to be restored.

### v2.9.5-ck8s1

Released 2024-01-30

#### Updated

- Updated ArgoCD to `v2.9.5`.

#### Changed

- Secret `helm-secrets-private-keys` in the `argocd-system` namespace (used for storing encryption keys) now uses a different label-value than before. The label has to be: `argocd.argoproj.io/secret-type=helm-secrets`

#### Added

- Added NetworkPolicies for Argo CD components
- Added support for age encrypted helm secrets
- Added vals as a secret backend

### v2.7.14-ck8s1

Released 2023-10-31

#### Updated

- Updated ArgoCD to `v2.7.14`.

#### Added

- Added support for using ArgoCD declaratively
- Added support for managing secrets via helm-secrets through ArgoCD
- Added support for managing secrets via sealed secrets through ArgoCD

### v2.4.20-ck8s1

Released 2023-03-29

First release of Argo CD with version `2.4.20`!
