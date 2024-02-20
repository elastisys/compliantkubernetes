---
tags:
- ISO 27001 A.12.1.4 Separation of Development, Testing & Operational Environments
- HIPAA S12 - Information Access Management - Isolating Healthcare Clearinghouse Functions - § 164.308(a)(4)(ii)(A)
- MSBFS 2020:7 3 kap. 1 §
- MSBFS 2020:7 3 kap. 2 §
- HSLF-FS 2016:40 3 kap. 10 § Upphandling och utveckling
- BSI IT-Grundschutz APP.4.4.A1
- BSI IT-Grundschutz APP.4.4.A15
- MDR Annex VI UDI-related
- NIST SP 800-171 3.4.4
---
!!! elastisys "For Elastisys Managed Services Customers"

    You can order a new Environment by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/).

    If you have multiple Environments, and one or more have been clearly designated to be non-production Environments, Elastisys will apply major and minor updates to your non-production Environment(s) at least five working days before applying said update to your production Environment(s).

    For more information, please read [ToS 3.5 Updates and Upgrades](https://elastisys.com/legal/terms-of-service/#35-updates-and-upgrades).

Compliant Kubernetes recommends setting up at least two separate environments: one for non-production use (e.g. development and testing) and one for production use.

---

# How Many Environments?

## Definitions

For the purpose of this document we use the following distinction:

**Application Deployment** - One instance of a customer's application. Commonly, multiple application deployments are used in the software development life cycles, such as: local, development, integration, testing, staging, and production.

**Environment** - One instance of a Compliant Kubernetes deployment. One Environment is composed of two Kubernetes Clusters, the Management Cluster and Workload Cluster.

## Levels of Isolation

Various levels of isolation between Application Deployments can be achieved while using Kubernetes:

- **Labels**: in which Application Deployments reside in the same Namespace and are separated "only" by e.g. Helm Releases or Argo CD Application labels. Network Policies can apply here, but e.g. Secrets will be accessible throughout the entire Namespace.
- **Namespace isolation**: in which Application Deployments share a Workload Cluster, but are separated logically using Namespaces. Network Policies work here, too, and Namespaces are a Kubernetes trust boundary when it comes to access to Secrets. Namespaces can also be used for resource quotas, for soft capacity allocation limitations.
- **Node isolation**: in which Application Deployments share an environment, but are deployed on different Nodes. On this level, both performance and security isolation is greater than in the previous, since the underlying virtual machines are separate. This is what Compliant Kubernetes does with additional services, such as PostgreSQL and RabbitMQ. Node isolation can be done both with and without Namespace isolation.
- **Cluster isolation**: in which Application Deployments share an Environment, but are deployed on separate Workload Clusters.
- **Separate Environments**: in which Application Deployments share nothing. This level of isolation is the highest, which implies total isolation for access control, credentials, network traffic, performance, and there are no shared platform components.

## Relevant Regulations

Many regulations require strict separation between testing and production Application Deployments.
In particular, production data should not be compromised, no matter what happens in testing Application Deployments.

Similarly, some regulations -- such as Medical Devices Regulation (MDR) -- require you to take a risk-based approach to changing the tech stack.
Depending on your risk assessment, this implies **verifying** changes in a non-production Application Deployment before going into production.

## Recommendations

Taking into account the relevant regulations, Compliant Kubernetes recommends setting up **at least two Environments**:

- non-production Environment hosting Application Deployments from development up to staging;
- production Environment hosting the production Application Deployment.

However, the exact number of Application Deployments and Environments will depend on your needs.
Please use the two figures below to reason about environments, trading developer productivity and data security:

![Ideal Developer Experience](img/environments/ideal-dx.svg)

![Ideal Promotion](img/environments/ideal-promotion.svg)
