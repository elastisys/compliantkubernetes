# Cloud Provider Audit

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.12.4.4 Clock Synchronization
    * A.15 Supplier Relationships

Compliant Kubernetes is designed to build upon the security and compliance of the underlying cloud provider.
If you cannot trust the underlying provider with controls such as physical security to the servers, safe disposal of hard drives, access control to infrastructure control plane, then no technical measure will help you achieve your security and compliance goals.
Trying to take preventive measures in Compliant Kubernetes -- i.e., at the platform level -- is inefficient at best and downright dangerous at worst.
Failing to due your due diligence will end up in [security theatre](https://en.wikipedia.org/wiki/Security_theater), putting your reputation at risk.

This page will help you do your due diligence and ensure you choose a cloud provider that provides a solid foundation for Compliant Kubernetes.

## Overview

The remainder of this page contains open questions that you should ask your cloud provider. Notice the following:

* Make sure you ask open questions and note down the answers. Burden of proof lies with the provider that they do an excellent job with protecting data.
* Ask all questions, then evaluate the provider's suitability. It is unlikely that you'll find the perfect provider, but you'll likely find one that is sufficient for your present and future needs.
* The least expected the answer, the more "digging" is needed.
* "You" represents the cloud provider and "I" represents the Compliant Kubernetes administrator.

## Technical Capability Questionnaire

1. Availability Zones:
    1. Where are your data centers located?
    1. How are they presented, i.e., single API vs. multiple independent APIs?
1. Services:
    1. What services do you offer? (e.g., VMs, object storage)
    1. Are all your services available in all zones?
1. Identity and Access Management (IAM):
    1. Do you offer IAM?
    1. How can I create roles? Via an API? Via a UI? Via a Terraform provider?
    1. What services can I configure role-based access control for?
    1. Can IAM be configured via API? Can IAM be configured via Terraform?
1. Infrastructure aaS:
    1. Which IaaS engine do you use? (e.g., OpenStack, VMware, proprietary)
    1. Do you have a Terraform provider for your API?
    1. Do you have pre-uploaded Ubuntu images? Which?
        1. Do these images have [AutomaticSecurityUpdates by default](https://help.ubuntu.com/community/AutomaticSecurityUpdates)?
        1. Do these images have [NTP enabled by default](https://ubuntu.com/server/docs/network-ntp)?
    1. Do you have a Kubernetes integration for your IaaS?
        1. Can I use a [cloud-controller](https://kubernetes.io/docs/concepts/architecture/cloud-controller/) for automatic discovery of Nodes and labeling Nodes with the right Zone?

1. Storage capabilities:
    1. Do you offer Object Storage as a Service (OSaaS)?
        1. Can I use the object storage via an S3-compatible API?
        1. Can I create buckets via API?
        1. Can I create bucket credentials via API?
        1. Do you have a Terraform provider for your API?
        1. In which zones?
        1. Do you have immutable storage or object lock?
        1. Is OSaaS stretched across zones?
        1. Is object storage replicated across zones?
    1. Do you offer Block storage as a Service (BLaaS)?
        1. Which API (OpenStack, VMware)?
        1. In which zones?
        1. Can I use a [Container Storage Interface (CSI) driver](https://kubernetes-csi.github.io/docs/drivers.html) for automatic creating of PersistentVolumes?
        1. Is BSaaS stretched across zones?
        1. Is block storage replicated across zones?
    1. Do you offer encryption-at-rest?
        1. Encrypted object storage: Do you offer this by default?
        1. Encrypted block storage: Do you offer this by default?
        1. Encrypted boot discs: Do you offer this by default?

1. Networking capabilities:
    1. Can the VMs be set up on a private network? Do you have a Terraform provider for your API?
        1. Is your private network stretched across zones?
        1. Do you trust the network between your data centers?
    1. Firewall aaS
        1. Are Firewall aaS available?
        1. What API? (e.g., OpenStack, VMware)
        1. Do you have a Terraform provider for your API?
    1. Do you offer Load Balancer aaS (LBaaS)?
        1. Can I create a LB via API?
        1. Do you have a Terraform provider for your API?
        1. Can I use a [cloud-controller](https://kubernetes.io/docs/concepts/architecture/cloud-controller/) for automatic creation of [external LoadBalancers](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/)?
        1. Can I set up a LB across zones? Via API?
    1. Do you offer IPv6 support? By default?
    1. Do you offer DNS as a Service? Which API?

## Organizational capabilities

1. What regulations are your existing customers subject to? (e.g., GDPR, public sector regulations, some ISO 27001 profile)
1. Can you show us your ISO-27001 certification?
    1. Which profile?
    1. Which organization made the audit?
    1. Can we get a copy of the [Statement of Applicability (SoA)](https://www.isms.online/iso-27001/iso27001-statement-applicability-simplified/)?
1. Who is overall responsible with compliance in your organization?
1. How do you implement regulatory and contractual requirements?
1. How is a new requirement discovered?
    1. What is the journey that a requirement takes from discovery, to updating policies, to training employees, to implementation, to evidence of implementation?
1. How is physical security handled?
1. How do you handle incidents and deviations?
    1. What response times / time to resolution do you offer?
    1. What are your actual response times / time to resolution?
1. What is your change management process?
1. How do you handle technical vulnerabilities?
1. How do you handle capacity management?
1. In case of a breach, how long until you notify your customers?
1. What SLA do you offer?
    1. What uptime do you offer?
    1. What is your measured uptime?
    1. Do you have a public status page?
1. How do you handle access control?
1. Does your operation team have individual accounts? How do you handle team member onboarding / offboarding?
1. How do you communicate credentials to your customers?
1. Do you have audit logs?
    1. How long do you store audit logs? Who has access to them? How are they protected against disclosure and tampering?
1. How do you handle business continuity?
    1. How often do you test fail-over? How did the last test go?
1. How do you handle disaster recovery?
    1. How often do you test disaster recovery? How did the last test go?

## Legal issues

1. Do you fully operate under EU jurisdiction?
1. Is your ownership fully under EU jurisdiction?
1. Are your suppliers fully under EU jurisdiction?
    1. Even the web fonts and analytics code on your front-page?
1. Do you have a DPO?
    1. Is this an internal employee or outsourced?

## Collaboration

1. How can we collaborate with your on-call team?
    1. What collaboration channels do you offer? (e.g., Slack, Teams, phone, service desk)
    1. What response times can we expect?
    1. Is your on-call team available 24/7?
1. Are you open to having quarterly operations (engineering) retrospectives? Our engineering team wants to keep a close loop with vendors and regularly discuss what went well, what can be improved, and devise a concrete action plan.
1. Are you open to having quarterly roadmap discussions?
