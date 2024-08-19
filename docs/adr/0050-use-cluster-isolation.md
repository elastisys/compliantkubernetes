# Use Cluster Isolation to separate the application and its traces from its logs and metrics

- Status: accepted
- Deciders: Product Team
- Date: 2024-08-16

## Context and Problem Statement

Let us introduce the context of this ADR.
First, we look at the regulatory and information security landscape.
Second, we look at the technological landscape.
Finally, we merge these two discussions to devise the problem statement.

### Regulatory and Information Security Landscape

The [NIS2 Directive](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive) came into force 2023 and will affect how platforms hosting software critical to society are secured.
Article 21 lists 10 cybersecurity risk-management measures which all essential and important entities will need to implement.

This ADR focuses on the following two measures, reproduced below verbatim from the NIS2 Directive:

> - (e) security in network and information systems acquisition, development and maintenance, including vulnerability handling and disclosure;
> - (i) human resources security, access control policies and asset management.

The most common way to implement these measures is using a concept called **Security Zone**.
A Security Zone is a logical grouping of IT systems with similar needs of protection.
For example, one Security Zone hosts [mission-critical applications](https://en.wikipedia.org/wiki/Mission_critical), whereas another Security Zone hosts non-mission-critical applications.

Each Security Zone has a separate network, either isolated physically (OSI layer 1) or logically (OSI layer 2, e.g., [VLAN](https://en.wikipedia.org/wiki/VLAN)).
The Internet itself can be conceptualized as a Security Zone with the lowest protection class.
Network traffic can only travel between Security Zones through firewalls.
Usually, connections are only allowed from Security Zones with higher protection class to those with lower.
As an additional measures, applications and protocols are designed to ensure that:

- A compromise of information availability and integrity of a Security Zone with lower protection class does not affect a Security Zone with a higher protection class.
For example, updates from the Internet need to pass through a manual review and validation process on a non-active production environment before being applied to the active production environment.
- Confidential information is not leaked from a Security Zone with higher protection class into one with lower protection class.
For example, application logs required for diagnostics may traverse from a higher to lower class. This, of course, entails that adequate requirements are set on the application development process, such as, logs should contain not confidential information.
However, application traces, given that they may contain function call parameters and hence pose a higher risk of leaking confidential information, should remain in the Security Zone with the higher protection class.

Besides network isolation, Security Zones with higher protection class may be accessed only by staff with a given security clearance.
For example, the Security Zone in the highest protection class may be accessed only by staff who cleared the [Swedish SÄPO Security Clearance](https://sakerhetspolisen.se/ovriga-sidor/other-languages/english-engelska/what-we-do/protective-security.html) or the [German SÜG](https://de.wikipedia.org/wiki/Sicherheits%C3%BCberpr%C3%BCfungsgesetz).
In contrast, Security Zones in a lower protection class may be accessed by the staff of suppliers, application developers, platform support staff, etc.

### Technological Landscape

Somewhat simplified, a containerized platform, such as Compliant Kubernetes, hosts the application stack and observability stack.
The [three pillars of observability](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/ch04.html) are metrics, logs and traces.
Metrics and logs are rather "explicit" in nature, i.e., the application developer usually add code to their application to explicitly decide what metrics and what log lines the application produces.
Traces are rather "implicit" in nature, i.e., the application developer [includes a library in their application and some code snippet](https://opentelemetry.io/docs/zero-code/python/example/), which automatically produces traces of all function calls and returns, including invoked parameters.

The application and observability stack may be separated through various levels of isolation: labels, namespace isolation, Node isolation and Cluster isolation.
See [Levels of Isolation](../user-guide/how-many-environments.md#levels-of-isolation) for a description of each isolation level and what kind of isolation they achieve.

## Problem Statement

Given the regulatory and information security landscape above, what level of isolation should Compliant Kubernetes employ between the application stack and observability stack?

## Decision Drivers

- We want to make it easy to protect code which runs in Security Zones with higher protection class, even if that means a reduction in productivity.
- We want to protect code which runs in Security Zones with lower protection class, but a reduction in productivity should be minimized.
- We want to avoid "Cluster sprawl" which increases maintenance burden.

## Considered Options

1. Use Namespace isolation between application and observability stack.
    - Good, because it avoids Cluster sprawl.
    - Bad, because Security Zones are only enforced using NetworkPolicies, which is usually insufficient for high-security organizations.
1. Use Node isolation between application and observability stack.
    - Good, because it avoids Cluster sprawl.
    - Good, because each Node may run in a different Security Zone.
    - Bad, because Kubernetes and its CNI tends to assume non-restricted communication between Nodes. The resulting firewall rules might look very generous and hard to audit.
    - Bad, because the Kubernetes control plane is shared between Security Zones, which violates the spirit of zoning.
1. Use Cluster isolation between application and observability stack.
    - Good, because each Cluster can run in a different Security Zone.
    - Good, because the application and observability stack can be in different Security Zones.
    - Bad, because traces end up in the same Security Zone as logs and metrics.
1. Use Cluster isolation between application and observability stack. Host the application and its traces in one Cluster, while the other Cluster hosts logs and metrics.
    - Good, because it avoid Cluster sprawl, i.e., only two Cluster, instead of the minimum of one.
    - Good, because it follows the Security Zone model.
1. Use Cluster isolation with one Cluster for each of application, traces, logs and metrics.
    - Neutral, because, compared to the option above, it does allow more Security Zones. However, many Security Zones are likely to be of the same protection class, hence, the benefits in terms of security does not outweigh the cost.
    - Bad, because it leads to Cluster sprawl.

## Decision Outcome

Chosen option: "Option 4: Host the application and its traces in one Cluster, while the other Cluster hosts logs and metrics", because it provides the right tradeoff between number of Security Zones and Cluster sprawl.

![Illustration of Option 4](img/0050-use-cluster-isolation.drawio.svg)

## Other Considerations

### Glossary used in Compliant Kubernetes

Compliant Kubernetes uses the following glossary:

- The Cluster hosting the application and traces is called the [Workload Cluster](../glossary.md#workload-cluster).
- The Cluster hosting logs and metrics is called the [Management Cluster](../glossary.md#management-cluster).

The pair of Cluster form a Compliant Kubernetes [Environment](../glossary.md#environment).

### Automated Platform Updates via Tekton

If the Workload Cluster is in a Security Zone with a high protection class, then we recommend against using auto-updates with Tekton.
Prefer running the migration scripts manually for added human supervision.
See [ADR-0035 Run Tekton on Management Cluster](0035-run-tekton-on-service-cluster.md).

### Cluster API

If the Workload Cluster is in a Security Zone with a higher protection class than the Management Cluster, then the Workload Cluster should run its own Cluster API controller.
This goes against [ADR-0033 Run Cluster API controllers on Management Cluster](0033-run-cluster-api-controllers-on-service-cluster.md).

## Links

- [NIS2 Directive](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive)
- [Proposal for an implementation of the NIS2 Directive in Sweden](https://www.regeringen.se/contentassets/1e56bf5cad214fc78eb80d91c11cccb6/nya-regler-om-cybersakerhet-sou-202418.pdf)
- [This is the NIS2 Directive from the Swedish Civil Contingencies Agency](https://www.msb.se/sv/amnesomraden/informationssakerhet-cybersakerhet-och-sakra-kommunikationer/krav-och-regler-inom-informationssakerhet-och-cybersakerhet/nis-direktivet/det-har-ar-nis2-direktivet/)
- [NIS2 in Germany](https://www.openkritis.de/eu/eu-nis-2-germany.html)
