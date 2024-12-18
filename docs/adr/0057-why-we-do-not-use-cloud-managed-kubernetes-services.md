# Do Not Use Managed Kubernetes Services

- Status: Accepted
- Deciders: Product Team
- Date: 2024-09-26

## Context and Problem Statement

Several of our Infrastructure Providers offer managed Kubernetes services. These services are designed to simplify the operational overhead of managing Kubernetes control planes. Customers of our self-managed service, especially those operating on modern cloud platforms like AWS, have expressed interest in leveraging these managed control planes to streamline their stack management.
This raises the question: should we consider integrating cloud-managed Kubernetes services into our Welkin stack?

## Decision Drivers

- We want to maintain Platform security and stability.
- We want to avoid operational and development complexity.
- We want to best serve Application Developers.
- We want to make the Platform Administrator life easier.
- We want to maintain fine-grained control over the Kubernetes stack
- We want to reduce the complexity of the testing matrix
- We want to keep platform portability

## Considered Options

- Yes
- No, we do not use Managed Kubernetes services because we want to reduce QA complexity and keep platform portability.

## Decision Outcome

Chosen option: 2 - No, we do not use Managed Kubernetes services because we want to reduce QA complexity and keep platform portability.

While managed Kubernetes services may seem appealing, adopting them introduces challenges that conflict with our operational and strategic goals. These include losing fine-grained control over the Kubernetes stack , dealing with non-equivalent service offerings across Infrastructure Providers (resulting in a complex and unmanageable test matrix), and the inability to support bare metal deployments.

### Positive Consequences

- Quality Assurance: When we release an upgraded platform version, you get a well-tested package of up-to-date versions of Kubernetes and other platform level components, which we confirmed that are compatible with each other.
- Regulatory Compliance: You get the Kubernetes cluster which is configured according to the relevant EU Regulations and Directives, Best Security Practices, Industry Specific Regulations applicable in Sweden, as documented here, e.g., we use ntp.se for time synchronization.
- Platform Portability: You can install the very same Kubernetes Platform on any Infrastructure Provider, either via a Cluster API provider or Kubespray. This means that a Welkin environment looks and feels the same, no matter if its hosted on Azure, EU cloud or on-prem. Customer Application can run as required within a specific geographical location or jurisdiction, with differences being hidden away by the platform.
- Need for Fine-Grained Control: The ability to maintain fine-grained control over the Kubernetes stack is a key requirement, which would be limited by using managed Kubernetes services.

### Negative Consequences

- This means we don't leverage reduced operational burden which comes with mature Kubernetes offerings, such as Azure Kubernetes Service (AKS). However, we see this as a price worth paying for a portable platform.
