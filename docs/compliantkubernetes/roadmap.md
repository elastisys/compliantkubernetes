# Roadmap

## Support for pull-based CD that adhere to security safeguards

Compliant kubernetes can be integrated with many different CI/CD pipelines.
Pull-based solutions such as Argo and Flux by default require too extensive security privileges
and needs modified roles to be operated in a safe manner.

## Security hardening as code

Implementation of suggested [security safeguards](https://elastisys.io/compliantkubernetes/user-guide/safeguards/) through Open Policy Agent.


# Non-Goals

## Opinionated CI/CD

Compliant Kubernetes can be used with a wide range of CI/CD pipelines, including traditional push-style tools and pull-style solutions such as GitOps operators.
Compliant Kubernetes will not be opinionated and prescribe one specific CI/CD technology.
