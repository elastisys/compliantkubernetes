# Roadmap

## Unattended upgrades

Support for fully unattended upgrades of Compliant Kubernetes, to allow off-hour upgrades, etc.

## Support for pull-based CD that adhere to security safeguards

Compliant kubernetes can be integrated with many different CI/CD pipelines.
Pull-based solutions such as Argo and Flux by default require too extensive security privileges
and needs modified roles to be operated in a safe manner.

## Multi-provider stretched clusters

Compliant kubernetes can stretch several data centers. We plan to extend this support to be able to
stretch clusters across all supported cloud providers and thus improve geo-resilience.

## Migration of logging stack to OpenSearch

We will migrate the current logging stack to OpenSearch. This will stabilize the logging interface and
make log-based alerting generally available in Compliant Kubernetes.

## Security hardening as code

Implementation of suggested [security safeguards](https://elastisys.io/compliantkubernetes/user-guide/safeguards/) through Open Policy Agent.



# Non-Goals

## Opinionated CI/CD

Compliant Kubernetes can be used with a wide range of CI/CD pipelines, including traditional push-style tools and pull-style solutions such as GitOps operators.
Compliant Kubernetes will not be opinionated and prescribe one specific CI/CD technology.
