# Roadmap

## GPU support

Support for GPU nodes in Compliant Kubernetes Workload Clusters, subject to GPU availability on supported Infrastructure Providers.

## Secrets management service

Convenient solution to manage secrets for Compliant Kubernetes Application Developers, such as SOPS or Sealed Secrets.

## SAML support

Support for SAML based Identity Providers (IDPs) as a complement to currently supported OpenID format.

## ArgoCD configation that adhere to security safeguards

Locked down security profile for ArgoCD that adheres to Compliant Kubernetes security practices.
By default, pull-based CD solutions such as ArgoCD (and Flux, for that matter) require too extensive security privileges.

## Additional dashboards

User experience for Compliant Kubernetes operators, Application Developers, and CISOs will be continuously improved,
including addition of single pane of glass dashboards that give overviews of all relevant services.

# Non-Goals

## Opinionated CI/CD

Compliant Kubernetes can be used with a wide range of CI/CD pipelines, including traditional push-style tools and pull-style solutions such as GitOps operators.
Compliant Kubernetes will not dictate the use of one specific CI/CD technology.
