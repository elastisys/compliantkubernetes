# Roadmap

## Light Compliant Kubernetes Renderings

Some users have requested a Compliant Kubernetes workload cluster, but with external container registry or logging solution. Compliant Kubernetes needs to be revised to facilitate this.

## Multi-Region High-Availability

Some business continuity policies may require redundancy across regions. It should be able to run Compliant Kubernetes across regions of a cloud provider.

## More generic Multi-Tenancy

Right now, one service cluster can support multiple workload clusters, as long as they all use the same identity provider and reside in the same cloud provider. 
In the future, we want to relax these requirements for more flexible multi-tenancy scenarios.

## Support to run on top of multiple Kubernetes distributions, included managed services. 

Compliant Kubernetes can be configured on top of Kubernetes clusters created with kubespray or similar tools.
It could be possible to run Compliant Kubernetes on top of managed Kubernetes services such as GKE, as well as distributions such as OpenShift.

## Out of the box service mesh support

Compliant Kubernetes can be used with service meshes such as Istio and LinkerD, but does not come with a preconfigured service mesh installer as of now. 

## Compliant Managed Services on top of Compliant Kubernetes

With improved support for stateful applications and operators in Kubernetes, it is now possible to offer managed services on top of Kubernetes. Said services should reduce compliance burden, hence building them on top of Compliant Kubernetes is natural. The following managed services are envisioned for cloud providers
who use Compliant Kubernetes:

* Managed Container Registry (e.g., Harbor);
* Managed Database (e.g., MariaDB, MySQL, PostgreSQL);
* Managed Message Queues (e.g., NATS, Kafka);
* Managed Caches (e.g., Redis);
* Managed Logging (e.g., Elasticsearch).

# Non-Goals

## CI/CD

Compliant Kubernetes can be used with a wide range of CI/CD pipelines, including traditional push-style tools and pull-style solutions such as GitOps operators. 
Compliant Kubernetes will not be opinionated and prescribe a certain CI/CD technology. 
