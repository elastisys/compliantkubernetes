# User Guide Overview

<embed src="../img/user-guide.svg" alt="Overview of User Roles and Stories" width="100%" />

This guide is for users who manage application on top of Compliant Kubernetes.

A user can be described via the following user stories:

* As a Continuous Delivery (CD) pipeline I want to push changes to the Compliant Kubernetes cluster, so that the new version of the application is running.
* As an application developer, I want to inspect how my application is running, so that I can take better development decisions.

!!!note
    We suggest application developers to only perform changes to a production Compliant Kubernetes cluster via a Continuous Delivery Pipeline. This method, also known as GitOps, provides an audit log, review and testing of system changes for "free". This significantly facilitates complying with change management policies.
