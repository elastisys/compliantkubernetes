# Do Not Use Managed Kubernetes Services

- Status: Accepted
- Deciders: Product Team
- Date: 2024-09-26

## Context and Problem Statement

Some of our Infrastructure Providers offer managed Kubernetes services.
Customers of the self-managed service have already asked why, if they are going to manage the entire stack on a modern cloud (AWS in this case), they can't use the managed Kubernetes control plane to make things easier for them.
We know we have a lot of good reasons for why we don't (loss of fine-grained control, not equivalent offerings means a huge test matrix, etc.), and e.g. bare metal deployments would be impossible if we always assumed a managed Kubernetes Service existing underneath.
We need to provide solid reasoning toward, in particular, self-managed customers (managed service ones obviously shouldn't have to care how we do what we do).
Should we use cloud-managed Kubernetes services with Welkin?

## Decision Drivers

- We want to maintain Platform security and stability.
- We want to avoid operational and development complexity.
- We want to best serve Application Developers.
- We want to make the Platform Administrator life easier.

## Considered Options

- Yes
- No, do not use Managed Kubernetes services and always rely on Kubespray or a Cluster API provider for Kubernetes Cluster life-cycle management.

## Decision Outcome

Chosen option: 2 - No, and write an ADR to capture the reasons why.

### Positive Consequences

There are several advantages of using installer included in our open source project:

- Quality Assurance: When we release an upgraded platform version, you get a well-tested package of up-to-date versions of Kubernetes and other platform level components, which we confirmed that are compatible with each other.
- Regulatory Compliance: You get the Kubernetes cluster which is configured according to the relevant EU Regulations and Directives, Best Security Practices, Industry Specific Regulations applicable in Sweden, as documented here, e.g., we use ntp.se for time synchronization.
- Platform Portability: You can install the very same Kubernetes Platform on any Infrastructure Provider, either via a Cluster API provider or Kubespray. This means that a Welkin environment looks and feels the same, no matter if its hosted on Azure, EU cloud or on-prem. Customer Application can run as required within a specific geographical location or jurisdiction, with differences being hidden away by the platform.

### Negative Consequences

- This means we don't leverage reduced operational burden which comes with mature Kubernetes offerings, such as Azure Kubernetes Service (AKS). However, we see this as a price worth paying for a portable platform.
