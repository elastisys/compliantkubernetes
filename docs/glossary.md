# Glossary

!!!important
    Harmonization of documentation with this glossary is underway. (See [#609](https://github.com/elastisys/compliantkubernetes/issues/609))

> There are only two hard things in Computer Science: cache invalidation and naming things.
>
> — Phil Karlton

This page introduces terminology used in the Compliant Kubernetes project.
We borrow terminology from:

* [Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/);
* [The Cluster API Book: Concepts](https://cluster-api.sigs.k8s.io/user/concepts.html).

You may want to familiarize yourself with that terminology first.

When naming things, we stick to [Inclusive Naming](https://inclusivenaming.org/).

<!--
NOTE to contributors:

- Please keep this list sorted.

TEMPLATE:

## TERM

DEFINITION

Usage notes:

* Do NOT use ...

See also:

* link 1
-->

## Application Developer

A person who writes an application that runs in a Kubernetes cluster.

Usage notes:

* It's okay to use "dev" or "developer", if it's clear from the context that we refer to an Application Developer.
* If you need more precision, use:
    * "Application Developers who are Grafana administrators" (see [Grafana Roles](https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/))
    * "Application Developers who are Harbor system administrators" (see [Harbor Managing Users](https://goharbor.io/docs/2.8.0/administration/managing-users/))
    * "Application Developers who are Kubernetes admins" (see [Kubernetes user-facing roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles))
    * "Application Developers with Kubernetes edit permissions" (see [Kubernetes user-facing roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles))
* Do NOT use "Super Application Developer", "user-admin", "user-view", etc.

See also:

* [Application Developer on Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/?all=true#term-application-developer)
* [Certified Kubernetes Application Developer (CKAD)](https://www.cncf.io/certification/ckad/)

## Cluster

Can refer to a [Kubernetes Cluster](#kubernetes-cluster), a PostgreSQL cluster, a Redis cluster, a RabbitMQ cluster, an OpenSearch Cluster, etc.

Usage notes:

* If it's not clear from the context what kind of Cluster you refer to, please spell it out. E.g., "The PostgreSQL Cluster runs inside the Workload Cluster." instead of "The Cluster runs inside the Workload Cluster."

See also:

* [Architecture Diagram Level 2: Clusters](architecture.md#level-2-clusters)
* [Cluster on Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/?all=true#term-cluster)
* [PostgreSQL Database Cluster](https://www.postgresql.org/docs/current/creating-cluster.html)
* [Redis Cluster](https://redis.io/docs/management/scaling/)
* [RabbitMQ Clustering Guide](https://www.rabbitmq.com/clustering.html)

## Contributor

Someone who makes Compliant Kubernetes better by providing code, documentation, feedback. Contributors make their work visible by raising issues and creating pull requests.

See also:

* [Contributor Guide](contributor-guide/index.md)

## Customer

Someone who benefits from Compliant Kubernetes via a commercial agreement.

Usage notes:

* Do NOT use "Customer" to refer figuratively to [Application Developer](#application-developer).
    Although we are big fans of a customer-driven mindset, there are several way to deliver Compliant Kubernetes commercially. Hence, this usage of the word "Customer" is confusing.
* Do NOT use "Customer" to refer figuratively to [End user](#end-user).
    Although we are big fans of a customer-driven mindset, there are several way to deliver Compliant Kubernetes commercially. Hence, this usage of the word "Customer" is confusing.
* Do NOT use "Data Controller", "Data Processor" or "Data Sub-processor". Determining which entity fulfills these GDPR concepts is usually done via a Data Protection Agreement (DPA). See EDPB [Guidelines 07/2020 on the concepts of controller and processor in the GDPR](https://edpb.europa.eu/system/files/2021-07/eppb_guidelines_202007_controllerprocessor_final_en.pdf).

See also:

* [Customer on Wikipedia](https://en.wikipedia.org/wiki/Customer).

## End User

Ultimate user of the Application deployed on top of Kubernetes.

Usage notes:

* Spell "End User" when used as noun, "end-user" when used as adjective. E.g., "good end-user experience" versus "good experience to the End User".
* Do NOT use "Application User" to refer to the [End User](#end-user).
* Platform Services, like Grafana, Harbor and OpenSearch, are meant for [Application Developers](#application-developer) and not End Users.

See also:

* [End user on Wikipedia](https://en.wikipedia.org/wiki/End_user)

## Environment

One instance of a Compliant Kubernetes deployment. One Environment is compose of two [Kubernetes Clusters](#kubernetes-cluster), the [Management Cluster](#management-cluster) and [Workload Cluster](#workload-cluster).

Usage notes:

* Make sure to distinguish between Environment and Cluster.

## Kubernetes Cluster

A set of worker machines, called nodes, that run containerized applications. Every cluster has at least one worker node.

Usage notes:

* Prefer [Workload Cluster](#workload-cluster) or [Management Cluster](#management-cluster) to avoid confusion.

See also:

* [Architecture Diagram Level 2: Clusters](architecture.md#level-2-clusters)
* [Cluster on Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/?all=true#term-cluster)

## Identity Provider

An Identity Provider (IdP) is a system that offers user authentication as a service. Examples include [Keycloak](https://www.keycloak.org/), [Azure Active Directory](https://azure.microsoft.com/en-us/products/active-directory), [Google Identity](https://developers.google.com/identity/openid-connect/openid-connect#setredirecturi) and [jumpcloud](https://jumpcloud.com/).

Usage notes:

* Do NOT use "Authentication Provider"

See also:

* [Identity provider on Wikipedia](https://en.wikipedia.org/wiki/Identity_provider)

## Infrastructure Provider

A supplier of Virtual or Bare-metal Machines, networks, load balancers, block storage and object storage.

Usage notes:

* Do NOT use "Data Processor" or "Data Sub-processor". Determining which entity fulfills these GDPR concepts is usually done via a Data Protection Agreement (DPA). See EDPB [Guidelines 07/2020 on the concepts of controller and processor in the GDPR](https://edpb.europa.eu/system/files/2021-07/eppb_guidelines_202007_controllerprocessor_final_en.pdf).

See also:

* [Architecture Diagram Level 1: System Context](architecture.md#level-1-system-context)
* [Infrastructure provider on The Cluster API Book](https://cluster-api.sigs.k8s.io/user/concepts.html#infrastructure-provider)

Usage notes:

* Do NOT use "Cloud Provider", as this is easily confused with "Platform-as-a-Service Cloud Provider".

## Management Cluster

A Kubernetes cluster hosting some platform components.

Usage notes:

* Do NOT use "Service Cluster". That terms is poorly recognized and hereby deprecated.
* `SC` and `sc` may be used to preserve backwards compatibility.

See also:

* [Management Cluster on The Cluster API Book](https://cluster-api.sigs.k8s.io/user/concepts.html#management-cluster)
* [Architecture Diagram Level 2: Clusters](architecture.md#level-2-clusters)

## Maintainer

"Those [contributors](#contributors) who lead an open source project." [Elastisys](https://elastisys.com) is Maintainer of Compliant Kubernetes.

Usage notes:

* Do NOT use "Creators" nor "Community Leaders".

See also:

* [Open source maintainers on Linux Foundation](https://www.linuxfoundation.org/blog/open-source-maintainers-what-they-need-and-how-to-support-them)

## Platform Administrator

The people who operate Compliant Kubernetes and Additional Platform Services.

Usage notes:

* Do NOT use "Operator" to refer to "Platform Administrator". Such usage is confusing due to the [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).
* It's okay to use "admin" or "administrator", if it's clear from the context that we refer to the Platform Administrator.

See also:

* [Certified Kubernetes Administrator (CKA)](https://www.cncf.io/certification/cka/)

## Service Endpoint

Interface exposed via the network for accessing Compliant Kubernetes functionality. Endpoints include Harbor, OpenSearch, Grafana, Dex and the [Workload Cluster](#workload-cluster) Kubernetes API.

Usage notes:

* Do NOT use "Webportals" or "Service Access Points".

See also:

* [API on Wikipedia](https://en.wikipedia.org/wiki/API)

## Workload Cluster

A Kubernetes cluster hosting the Application which is used by the [End User](#end-user).

See also:

* [Workload Cluster on The Cluster API Book](https://cluster-api.sigs.k8s.io/user/concepts.html#workload-cluster)
* [Architecture Diagram Level 2: Clusters](architecture.md#level-2-clusters)
