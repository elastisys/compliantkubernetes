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
