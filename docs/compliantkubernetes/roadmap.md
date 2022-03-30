---
description: Roadmap for the Elastisys Compliant Kubernetes project, the security-focused Kubernetes distribution.
---

# Roadmap

## Support for pull-based CD that adhere to security safeguards

Elastisys Compliant Kubernetes can be integrated with many different CI/CD pipelines.
Pull-based solutions such as Argo and Flux by default require too extensive security privileges
and needs modified roles to be operated in a safe manner. Investigation into suitable, and secure,
alternative solutions are underway.

## Security hardening as code

Implementation of suggested [security safeguards](https://elastisys.io/compliantkubernetes/user-guide/safeguards/) through Open Policy Agent.