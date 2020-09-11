# Concepts

This page introduces terminology used in the Compliant Kubernetes project. We assume that you are familiar with [Kubernetes concepts](https://kubernetes.io/docs/concepts/).

* **Control**: "Points" in an organization that need a clear policy in order to comply with regulation.
* **Regulation**: Law or contractual requirements that an organization is required to follow to be allowed to operate.
* **Operator**: A person or automation process (i.e., CI/CD pipeline) that creates, destoys, updates or otherwise maintains a Compliant Kubernetes installation.
* **Service cluster**: Kubernetes cluster that hosts monitoring, logging and technical vulnerability management components. These components are separated from the workload cluster to give an extra layer of security, as is required by some regulations.
* **Workload cluster**: Kubernetes cluster hosting the application that exposes end-user -- front-office or back-office -- functionality.
* **User**: A person or an automation process (i.e., CI/CD pipeline) that interacts with Compliant Kubernetes for the purpose of running and monitoring an application hosted by Compliant Kubernetes.
