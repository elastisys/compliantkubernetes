# Use one Subscription per Customer on Azure

* Status: Accepted
* Deciders: PA and P.O
* Date: 2023-03-19

## Context and Problem Statement

Compliant Kubernetes can be run on Azure now and so, we explored different strategies for resource isolation within Azure to best serve multiple customers. The options considered included isolation at the resource group level versus adopting a per subscription per customer approach.

Should we consider the per Subscription-per-Customer Model for managing Azure resources under one tenant?

## Decision Drivers

* We want to maintain Platform security and stability.
* We want to find a solution which is scalable and minimises Platform Administrator burden.
* We want to make the Platform Administrator life easier.
* We want to have simplified billing and invoices.

## Considered Options

1. Isolation at the Subscription Level

   - `Good`, because subscriptions provide clear separation for billing and invoice purposes considering Azure invoices are prepared based on the Subscription ID, making it easier to track and manage costs per customer.
   - `Good`, because Azure typically operates with one tenant per organisation, closely tied to the Active Directory (AD) or Azure AD. Utilising multiple subscriptions under one tenant provides a coherent organisational structure, enhancing management and governance.
   - `Good`, because Role-Based Access Control (RBAC) settings are easier to manage at the subscription level, offering straightforward governance and security controls for each customer.
   - `Good`, because Azure imposes certain limits at the subscription level; having separate subscriptions helps in managing these limits more effectively.
   - `Good`, because virtual networks are scoped to a subscription, simplifying network management and isolation between customers.
   - `Bad`, because setting up network communication between subscriptions will require additional work than within a single subscription.

2. Isolation at the Resource Group Level

   - `Good` because resource groups allow for organising resources more flexibly within a single subscription, facilitating easier management of resources.
   - `Good` because managing subscriptions can reduce the complexity and overhead associated with subscription management, permissions, and billing setups.
   - `Good` because setting up network communication between resource groups will be less complex as compared with across the subscriptions.
   - `Bad`, because while Azure Cost Management can track costs by resource group, billing separation is not as straightforward as with subscriptions, potentially complicating cost allocation and invoicing for different customers.
   - `Bad`, because fine-grained access control is more challenging to implement and manage effectively at the resource group level compared to subscription-level controls.
   - `Bad`, because the resource groups share the same subscription limits, there's a risk of hitting these limits, which could impact scalability and performance.

## Decision Outcome

Chosen option:

Isolation at the Subscription level i.e Subscription-per-Customer Model because, as an organization, we wanted to ensure complete isolation for billing, invoices, resources, and compliance, while maintaining the flexibility to communicate and share resources across subscriptions as necessary.

### Positive Consequences

* We maintain Platform security and resource isolation.
* We don't increase the operational complexity.
* We have stricter access controls and limit the scope of potential security breaches.
* We have simplified billing and invoices.
* We avoid potential resource contention issues.

### Negative Consequences

* Managing multiple subscriptions can increase the administrative workload.
* Network communication across tenant requires advanced networking setups, like virtual network peering, etc
