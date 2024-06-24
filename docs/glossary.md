# Glossary

> There are only two hard things in Computer Science: cache invalidation and naming things.
>
> — Phil Karlton

This page introduces terminology used in the Compliant Kubernetes project.
We borrow terminology from:

- [Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/);
- [The Cluster API Book: Concepts](https://cluster-api.sigs.k8s.io/user/concepts.html).

You may want to familiarize yourself with that terminology first.

When naming things, we stick to [Inclusive Naming](https://inclusivenaming.org/).

Please capitalize these terms, i.e., treat them as [proper nouns](https://en.wikipedia.org/wiki/Proper_noun).

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

## Air-gapped Network

From [Wikipedia](<https://en.wikipedia.org/wiki/Air_gap_(networking)>):

> An [**air-gapped network**] is a network security measure employed on one or more computers to ensure that a secure computer network is physically isolated from unsecured networks, such as the public Internet or an unsecured local area network. It means a computer or network has no network interface controllers connected to other networks, with a physical or conceptual air gap, analogous to the air gap used in plumbing to maintain water quality.

Usage notes:

- Please avoid "air-gapped environment" to avoid confusion with [Environment](#environment).
- Please avoid synonymous expressions, like "disconnected network" or "offline environment".

See also:

- [Air gap (networking) on Wikipedia](<https://en.wikipedia.org/wiki/Air_gap_(networking)>)

## Application Developer

A person who writes an application that runs in a Kubernetes cluster.

Usage notes:

- It's okay to use "app dev", "dev" or "developer", if it's clear from the context that we refer to an Application Developer.
- If you need more precision, use:
    - "Application Developers who are Grafana administrators" (see [Grafana Roles](https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/))
    - "Application Developers who are Harbor system administrators" (see [Harbor Managing Users](https://goharbor.io/docs/2.8.0/administration/managing-users/))
    - "Application Developers who are Kubernetes admins" (see [Kubernetes user-facing roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles))
    - "Application Developers with Kubernetes edit permissions" (see [Kubernetes user-facing roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles))
- Do NOT use "Super Application Developer", "user-admin", "user-view", etc.

See also:

- [Application Developer on Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/?all=true#term-application-developer)
- [Certified Kubernetes Application Developer (CKAD)](https://www.cncf.io/certification/ckad/)

## Apps layer (or Compliant Kubernetes layer)

Denotes the Compliant Kubernetes components installed on top of a Kubernetes cluster.

Usage notes:

- This term is likely to be known and understood only by [Platform Administrators](#platform-administrator) and [Contributors](#contributor). Use only when addressing these two audiences.

See also:

- [Architecture Diagram Level 3: Individual Components](architecture.md#level-3-individual-components)
- [Apps layer source code](https://github.com/elastisys/compliantkubernetes-apps/)

## Cluster

Can refer to a [Kubernetes Cluster](#kubernetes-cluster), a PostgreSQL cluster, a Redis cluster, a RabbitMQ cluster, an OpenSearch Cluster, etc.

Usage notes:

- If it's not clear from the context what kind of Cluster you refer to, please spell it out. E.g., "The PostgreSQL Cluster runs inside the Workload Cluster." instead of "The Cluster runs inside the Workload Cluster."

See also:

- [Architecture Diagram Level 2: Clusters](architecture.md#level-2-clusters)
- [Cluster on Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/?all=true#term-cluster)
- [PostgreSQL Database Cluster](https://www.postgresql.org/docs/current/creating-cluster.html)
- [Redis Cluster](https://redis.io/docs/management/scaling/)
- [RabbitMQ Clustering Guide](https://www.rabbitmq.com/clustering.html)

## Contributor

Someone who makes Compliant Kubernetes better by providing code, documentation, feedback. Contributors make their work visible by raising issues and creating pull requests.

See also:

- [Contributor Guide](contributor-guide/index.md)

## Critical Entity

To quote the [EU Critical Entities Resilience (CER) Directive](https://eur-lex.europa.eu/eli/dir/2022/2557/oj#d1e32-193-1):

> Critical entities, as providers of essential services, play an indispensable role in the maintenance of vital societal functions or economic activities in the internal market in an increasingly interdependent Union economy.

In particular, they all need to take various measures related to physical and staff security.

However, there is no single clear definition for Critical Entities.
Instead, EU Member States must implement a process for identifying critical entities based on categories of entities published in EU CER Directive.

All entities identified as critical under CER are considered [essential entities](#essential-entity) under the [EU NIS2 Directive](https://eur-lex.europa.eu/eli/dir/2022/2555).

See also:

- [EU Critical Entities Resilience (CER) Directive: Categories of Entities](https://eur-lex.europa.eu/eli/dir/2022/2557/oj#d1e32-193-1)

## Customer

Someone who benefits from Compliant Kubernetes via a commercial agreement.

Usage notes:

- Do NOT use "Customer" to refer figuratively to [Application Developer](#application-developer).
  Although we are big fans of a customer-driven mindset, there are several way to deliver Compliant Kubernetes commercially. Hence, this usage of the word "Customer" is confusing.
- Do NOT use "Customer" to refer figuratively to [End User](#end-user).
  Although we are big fans of a customer-driven mindset, there are several way to deliver Compliant Kubernetes commercially. Hence, this usage of the word "Customer" is confusing.
- Do NOT use "Data Controller", "Data Processor" or "Data Sub-processor". Determining which entity fulfills these GDPR concepts is usually done via a Data Protection Agreement (DPA). See EDPB [Guidelines 07/2020 on the concepts of controller and processor in the GDPR](https://edpb.europa.eu/our-work-tools/documents/public-consultations/2020/guidelines-072020-concepts-controller-and_en).

See also:

- [Customer on Wikipedia](https://en.wikipedia.org/wiki/Customer).

## End User

Ultimate user of the Application deployed on top of Kubernetes.

Usage notes:

- Spell "End User" when used as noun, "end-user" when used as adjective. E.g., "good end-user experience" versus "good experience to the End User".
- Do NOT use "Application User" to refer to the [End User](#end-user).
- Platform Services, like Grafana, Harbor and OpenSearch, are meant for [Application Developers](#application-developer) and not End Users.

See also:

- [End User on Wikipedia](https://en.wikipedia.org/wiki/End_user)

## Environment

One instance of a Compliant Kubernetes deployment. One Environment is composed of two [Kubernetes Clusters](#kubernetes-cluster), the [Management Cluster](#management-cluster) and [Workload Cluster](#workload-cluster).

Usage notes:

- Make sure to distinguish between Environment and Cluster.

## Essential Entity

Essential Entities are organizations which are considered to provide essential services to society and have obligations according to the [EU NIS2 Directive](https://eur-lex.europa.eu/eli/dir/2022/2555/oj/).
In particular, they need to take certain measures related to information security and cybersecurity.

There is no clear definition for Essential Entities.
Instead, EU Member States must implement a process for identifying essential entities based on a list of sectors of high criticality published in NIS2.

This process is currently under development in most EU Member States.
As an example on how this process could look like, please refer to the NIS-era [MSBFS 2024:4 rule](https://www.msb.se/contentassets/b15833b9aaa0425ca0c898cc0a120c81/myndigheten-for-samhallsskydd-och-beredskaps-foreskrifter-om-anmalan-och-identifiering-av-leverantorer-av-samhallsviktiga-tjanster-2024-4-pdf.pdf).

Usage notes:

- The EU NIS2 Directive also introduces "important entities". These organizations have somewhat lower obligations under NIS2 and are subject to lower maximum fines.

See also:

- [EU NIS2 Directive: Sectors of High Criticality](https://eur-lex.europa.eu/eli/dir/2022/2555/oj#d1e32-143-1)
- [Swedish MSBFS 2024:4 Rules on identification of providers of essential services](https://www.msb.se/contentassets/b15833b9aaa0425ca0c898cc0a120c81/myndigheten-for-samhallsskydd-och-beredskaps-foreskrifter-om-anmalan-och-identifiering-av-leverantorer-av-samhallsviktiga-tjanster-2024-4-pdf.pdf)

## Kubernetes Cluster

A set of worker machines, called nodes, that run containerized applications. Every cluster has at least one worker node.

Usage notes:

- Prefer [Workload Cluster](#workload-cluster) or [Management Cluster](#management-cluster) to avoid confusion.

See also:

- [Architecture Diagram Level 2: Clusters](architecture.md#level-2-clusters)
- [Cluster on Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/?all=true#term-cluster)

## Identity Provider

An Identity Provider (IdP) is a system that offers user authentication as a service. Examples include:

- [Keycloak](https://www.keycloak.org/)
- [Microsoft Entra ID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id) previously known as Azure Active Directory
- [Google Identity](https://developers.google.com/identity/openid-connect/openid-connect#setredirecturi)
- [jumpcloud](https://jumpcloud.com/)

Usage notes:

- Do NOT use "Authentication Provider"
- [Dex](https://dexidp.io/) is a "Federated OpenID Connect Provider". Hence, it is okay to call it a "Federated Identity Provider".

See also:

- [Identity provider on Wikipedia](https://en.wikipedia.org/wiki/Identity_provider)

## Infrastructure Provider

A supplier of Virtual or Bare-metal Machines, networks, load balancers, block storage and object storage.

Usage notes:

- Do NOT use "Data Processor" or "Data Sub-processor". Determining which entity fulfills these GDPR concepts is usually done via a Data Protection Agreement (DPA). See EDPB [Guidelines 07/2020 on the concepts of controller and processor in the GDPR](https://edpb.europa.eu/our-work-tools/documents/public-consultations/2020/guidelines-072020-concepts-controller-and_en).
- Do NOT use "Cloud Provider", as this is easily confused with "Platform-as-a-Service Cloud Provider".

See also:

- [Architecture Diagram Level 1: System Context](architecture.md#level-1-system-context)
- [Infrastructure provider on The Cluster API Book](https://cluster-api.sigs.k8s.io/user/concepts.html#infrastructure-provider)

## Management Cluster

A Kubernetes cluster hosting some platform components.

Usage notes:

- Do NOT use "Service Cluster". That terms is poorly recognized and hereby deprecated.
- `SC` and `sc` may be used to preserve backwards compatibility. Acceptable usage includes code and command-line tools. Unacceptable usage include documentation.

See also:

- [Management Cluster on The Cluster API Book](https://cluster-api.sigs.k8s.io/user/concepts.html#management-cluster)
- [Architecture Diagram Level 2: Clusters](architecture.md#level-2-clusters)

## Maintainer

"Those [contributors](#contributor) who lead an open source project." [Elastisys](https://elastisys.com) is Maintainer of Compliant Kubernetes.

Usage notes:

- Do NOT use "Creators" nor "Community Leaders".

See also:

- [Open source Maintainers on Linux Foundation](https://www.linuxfoundation.org/blog/open-source-Maintainers-what-they-need-and-how-to-support-them)

## Personal Data Controller

Defined in [Art. 4 GDPR](https://gdpr.fan/a4) as:

> the natural or legal person, public authority, agency or other body which, alone or jointly with others, determines the purposes and means of the processing of personal data; where the purposes and means of such processing are determined by Union or Member State law, the controller or the specific criteria for its nomination may be provided for by Union or Member State law;

In brief, this is the organization which decides or influences what goes in the privacy policy.

Usage notes:

- "Controller" can also refer to the [Controller pattern](https://kubernetes.io/docs/concepts/architecture/controller/) in Kubernetes. Only use "controller" (without "personal data" or "Kubernetes") if the reader can understand from the context which one you refer to.

See also:

- [Art. 4 GDPR](https://gdpr.fan/a4)

## Personal Data Processor

Defined in [Art. 4 GDPR](https://gdpr.fan/a4) as:

> a natural or legal person, public authority, agency or other body which processes personal data on behalf of the controller;

In brief, this is the organization that receives instructions from the data controller and -- with few exceptions -- can only process personal data as instructed.

Usage notes:

- The GDPR **does not** define the concept of "sub-processor".
  However, the European Data Protection Board (EDPB) encourages using the term "sub-processor" to denote an organization which acts under the instructions of the processor.

See also:

- [Art. 4 GDPR](https://gdpr.fan/a4)
- [What is a sub-processor? Data Protection Guide for Small Business by the EDPB](https://www.edpb.europa.eu/sme-data-protection-guide/data-controller-data-processor_en#toc-5)

## Platform Administrator

The people who operate Compliant Kubernetes and Additional Platform Services.

Usage notes:

- Do NOT use "Operator" to refer to "Platform Administrator". Such usage is confusing due to the [Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).
- It's okay to use "admin" or "administrator", if it's clear from the context that we refer to the Platform Administrator.

See also:

- [Certified Kubernetes Administrator (CKA)](https://www.cncf.io/certification/cka/)

## Service Endpoint

Interface exposed via the network for accessing Compliant Kubernetes functionality. Endpoints include Harbor, OpenSearch, Grafana, Dex and the [Workload Cluster](#workload-cluster) Kubernetes API.

Usage notes:

- Do NOT use "Webportals" or "Service Access Points".

See also:

- [API on Wikipedia](https://en.wikipedia.org/wiki/API)

## Workload Cluster

A Kubernetes cluster hosting the Application which is used by the [End User](#end-user).

See also:

- [Workload Cluster on The Cluster API Book](https://cluster-api.sigs.k8s.io/user/concepts.html#workload-cluster)
- [Architecture Diagram Level 2: Clusters](architecture.md#level-2-clusters)
