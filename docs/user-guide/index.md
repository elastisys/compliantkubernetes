# User Guide Overview

<embed src="../img/user-guide.svg" alt="Overview of User Roles and Stories" width="100%" />

This guide is for users who manage application on top of Compliant Kubernetes.

A user can be described via the following user stories:

* As a Continuous Integration (CI) pipeline, I want to push new container images to the container registry.
* As a Continuous Delivery (CD) pipeline, I want to push changes to the Compliant Kubernetes cluster, so that the new version of the application is running.
* As an application developer, I want to inspect how my application is running, so that I can take better development decisions.
* As a super user, I want to configure Role-Based Access Control (RBAC) to delegate access to application developers.
* As a super user, I want to configure NetworkPolicies, so that applications running in the same Compliant Kubernetes cluster are well zoned.
* As a super user, I want to configure Policies (e.g., "do not use `latest` as a container tag), so as to avoid trivial mistakes.

!!!note
    We suggest application developers to only perform changes to a production Compliant Kubernetes cluster via a Continuous Delivery Pipeline. This method, also known as GitOps, provides an audit log, review and testing of system changes for "free". This significantly facilitates complying with change management policies.

## Running Example

To make the most out of Compliant Kubernetes, this documentation features a minimalistic NodeJS application. I allows to explore all Compliant Kubernetes benefits, including HTTPS Ingresses, logging, metrics and user alerts.

The application provides:

- some REST endpoints (`/`, `/users`);
- structured logging;
- metrics endpoint;
- Dockerfile;
- Helm Chart;
- ability to make it crash (`/crash`).

Furthermore, the application caters to a security-hardened environment, and additionally:

- runs as non-root.

If you are a newcomer to Compliant Kubernetes, we suggest you clone the user demo as follows:

```bash
git clone https://github.com/elastisys/compliantkubernetes/
cd compliantkubernetes/user-demo
```
