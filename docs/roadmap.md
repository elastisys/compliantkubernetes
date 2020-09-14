# Roadmap

## Light Compliant Kubernetes Renderings

Some users have requested a Compliant Kubernetes workload cluster, but with external container registry or logging solution. Compliant Kubernetes needs to be revised to facilitate this.

## Compliant Managed Services on top of Compliant Kubernetes

With improved support for stateful applications and operators in Kubernetes, it is now possible to offer managed services on top of Kubernetes. Said services should reduce compliance burden, hence building them on top of Compliant Kubernetes is natural. The following managed services are envisioned:

* Managed Container Registry (e.g., Harbor);
* Managed Database (e.g., MariaDB, MySQL, PostgreSQL);
* Managed Message Queues (e.g., NATS, Kafka);
* Managed Caches (e.g., Redis);
* Managed Logging (e.g., Elasticsearch).

## Multi-Region High-Availability

Some business continuity policies may require redundancy across regions. It should be able to run Compliant Kubernetes across regions of a cloud provider.

## Google Cloud Platform Support

Some users want to run Compliant Kubernetes both on-prem and on a public cloud provider, while getting the same "look and feel". Compliant Kubernetes should be ported to Google Cloud Platform, without relying on specific Google services (e.g., GKE, IAM, etc.).

## Multi-Tenancy

Right now, one service cluster is required for each workload cluster. In the future, we want to relax this requirement, so as to use a single service cluster for multiple workload clusters.

## Cloud-Agnostic Storage and Load Balancing

Some smaller cloud providers do not provide storage or load balancing that Kubernetes can build on. Compliant Kubernetes should offer its own, optional storage or load balancing if the underlying cloud provider does not have the required features.
