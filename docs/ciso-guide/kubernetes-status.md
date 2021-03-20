# Kubernetes Status Dashboard

## Relevant Regulations

* [GDPR Article 32](https://gdpr-info.eu/art-32-gdpr/):

    > The ability to ensure the ongoing confidentiality, integrity, **availability and resilience** of processing systems and services; [highlights added]

## Mapping to ISO 27001 Controls

* [A.12.1.3 Capacity Management](https://www.isms.online/iso-27001/annex-a-12-operations-security/)

    > The use of resources must be monitored, tuned and projections made of future capacity requirements to ensure the required system performance to meet the business objectives.

## Compliant Kubernetes Status Dashboard

![Kubernetes Status Dashboard](img/kubernetes-status.png)

The Compliant Kubernetes Status Dashboard shows a quick overview of the status of your kubernetes cluster.
This includes:

* Unhealthy pods
* Unhealthy nodes
* Resource requested of the total resources in the cluster
* Pods with missing resource requests

This makes it easy to identify when your cluster is not working correctly and helps you identify configuration that isn't following best practise.
