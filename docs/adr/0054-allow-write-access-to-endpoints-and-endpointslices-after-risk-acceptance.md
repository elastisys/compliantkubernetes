# Allow Application Developer write access to Endpoints and EndpointSlices after Proper Risk Acceptance

- Status: Accepted
- Deciders: Arch Meeting
- Date: 2024-02-08

## Context and Problem Statement

Our Platform strives to balance security with flexibility. In doing so, we frequently encounter trade-offs between ensuring robust security and maintaining full Platform functionality. The presence of low-risk vulnerabilities [CVE-2021-25740](https://github.com/kubernetes/kubernetes/issues/103675) related to Endpoints and EndpointSlices objects introduces several risks, primarily involving cross-namespace traffic that can bypass intended security controls.

This means that applications hosted in the Workload Cluster and running in one namespace could potentially interact with or access services in another namespace, thereby breaching the intended security isolation.

Should we allow Application Developers to create Endpoints and EndpointSlices objects on our Platform?

## Decision Drivers

- We want to maintain Platform security and stability.
- We want to avoid operational complexity.
- We want to best serve the Application Developers.
- We want to make the Platform Administrator life easier.

## Considered Options

1. Allow creation and editing of Endpoints and EndpointSlices by default.

1. Disallow creation and editing of Endpoints and EndpointSlices by default.

1. Never allow creation and editing of Endpoints and EndpointSlices.

1. Allow creation and editing of Endpoints and EndpointSlices, but only after Application Developer accepted the security risks.

## Decision Outcome

**Chosen Option:** Option 4: Allow creation and editing of Endpoints and EndpointSlices, but only after Application Developer accepted the security risks.

Opting for this option provides a balanced approach, allowing Platform flexibility while still emphasizing the importance of security through best practices and proactive risk management.

### Positive Consequences

- Allows Application Developers to maintain essential connections to external resources without breaking existing setups.
- Ensures that Application Developers have the freedom to configure their services according to their needs.
- Encourages Application Developers education, adherence to best practices, and proactive monitoring to mitigate potential risks.

### Negative Consequences

- The vulnerability remains, potentially exposing Application Developers to risk if misconfigured.
- Continuous effort is needed to ensure Application Developers are aware of the risks and follow best practices.

## Pros and Cons of the Options <!-- optional -->

### Option 1

- Good, because it allows Application Developers the flexibility to configure Endpoints and EndpointSlices as needed without requiring intervention from Platform Administrators.
- Good, because disabling Endpoints and EndpointSlices by default or tightening security to eliminate low-risk vulnerabilities would increase operational complexity for both Application Developers and Platform Administrators.
- Bad, because in multi-tenant environments, a single tenant's misconfiguration could expose vulnerabilities to others, leading to potential security breaches.
- Bad, because even low-risk vulnerabilities could become more exploitable in the future, especially if misconfigurations occur.

### Option 2

- Good, because strict security policies reduce the risk of attacks, particularly in multi-tenant environments where isolation and protection are crucial.
- Bad, because restricting access to external systems introduces significant operational challenges for Application Developers.
- Bad, because enforcing strict security policies could break existing Application Developers workflows, requiring significant reconfiguration.

### Option 3

- Good, because it eliminates the risk associated with Endpoints and EndpointSlices, ensuring that cross-namespace traffic and security breaches are not possible.
- Bad, because restricting access to external systems introduces significant operational challenges for Application Developers.
- Bad, because enforcing strict security policies could break existing Application Developers workflows, requiring significant reconfiguration.

### Option 4

- Good, because it offers a middle ground by allowing flexibility while ensuring Application Developers are aware of and accept the associated risks before creating and editing Endpoints and EndpointSlices.
- Bad, because it relies on Application Developers fully understanding and accepting the risks, which may not always be the case.

## Recommendation to Platform Administrators

If you enable this feature, then make sure Application Developers understand and accept the added stability and security risks. A message as follows could be used:

```text
Hello Team,

After careful discussion, we have decided that it is permissible to grant Application Developers the ability to create Endpoints and EndpointSlices objects, provided the following conditions are met:

(a) There is no other viable alternative for your use case;
(b) You understand and accept the security risks involved;

For (a), please confirm that you have explored all other potential options for your use case and found that using Endpoints or EndpointSlices is the only way forward. Refer to the Kubernetes documentation for possible alternatives: https://kubernetes.io/docs/concepts/services-networking/service/

For (b), please confirm that you are aware of the security implications and understand the consequences of this CVE: https://github.com/kubernetes/kubernetes/issues/103675.

To summarize, if you can confirm points (a) through (b), we will proceed with enabling the necessary permissions for creating Endpoints and EndpointSlices.

Regards,
Elastisys Managed Services Team
```

## Links

- [CVE-2021-25740](https://github.com/kubernetes/kubernetes/issues/103675)
- [ADR-0039](./0039-application-dev-permissions.md)
