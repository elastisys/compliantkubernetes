# ISA/IEC 62443

There are several standards and frameworks whose goal is to improve the security of Industrial Control Systems (ICS).
One of these is ISA/IEC 62443, whose purpose is to improve the availability, integrity and confidentiality of ICS.

This page is aimed at system owners and explains how Welkin fulfills the foundational requirements of ISA/IEC 62443.

## FR 1: Identification and Authentication Control

All Welkin Service Endpoints are exposed via HTTPS and require OpenID-based authentication with an [Identity Provider (IdP)](../user-guide/prepare-idp.md).
Provided that your IdP is configured securely, this means that Welkin can only be accessed via individual usernames and passwords.

You may further protect Welkin Service Endpoints as follows:

- Configure your IdP with Multi-Factor Authentication (MFA): This removes the risk of an attacker gaining access to ICS via a compromised password.
- Configure IP allowlisting: This adds one more layer of protection in that an attacker must first gain access to an internal network before mounting an attack.
- Run Welkin in an [air-gapped network](../operator-manual/air-gapped.md): This means that platform administrators and application developers need on-site presence to gain access to Service Endpoints.

## FR 2: Use Control

All Welkin Service Endpoints provide for access control and leave an audit log.

When it comes to access control, Welkin enforces a strong distinguishing between:

- Application Developers, who are [limited to administering their application](../user-guide/demarcation.md); and
- Platform Administrators, who have more permissions, as required for platform maintenance and troubleshooting.

Furthermore, each Service Endpoint features [fine-grained access control](../user-guide/delegation.md).
For example the Kubernetes Endpoint implements Kubernetes Role-Based Access Control (RBAC).

[Audit logs](../ciso-guide/audit-logs.md) store information about who did what and when.
Combined with periodic [log reviews](../ciso-guide/log-review.md) they form a powerful tool to deter and detect unauthorized access.

## FR 3: System Integrity and FR 4: Data Confidentiality

The fine-grained access control described above is carefully configure to ensure system integrity and data confidentiality.
For example, Welkin technically prevents Application Developers to make any changes which may compromise the security of the platform.
This includes compromising or working around access control, logging, monitoring, backups, alerting, etc.

Furthermore, Welkin comes with various [safeguards](../user-guide/safeguards/index.md) to make it hard to Application Developers to do the wrong thing, like running containers as root.
This ensures both system integrity and data confidentiality, e.g., Application Developers cannot take over the operating system on a Node.

## FR 5: Restricted Data Flow (Microsegmentation)

Welkin restricts data flows at three levels:

- Infrastructure: Provided the infrastructure supports this, the servers composing Welkin should always be put on a private network, fronted by a load-balancer.
  The load-balancer should restrict communication to port 80 (TCP ACME) and 443 (HTTPS).
- Platform: Within the platform, most Welkin components have NetworkPolicies in place.
  NetworkPolicies are roughly equivalent to firewall in a containerized environment.
  This ensures that components can only communicate to one-another on an "as-needed" basis, and severely restricts the ability to exploit certain vulnerabilities, such as the infamous Log4j vulnerability.
- Application: Application Developers should ship their application with NetworkPolicies to restrict data flows, as described on the [Network Model](../user-guide/network-model.md) page.
  By default, Welkin [warns Application Developer if NetworkPolicies are missing](../user-guide/safeguards/enforce-networkpolicies.md).

## FR 6: Timely Response to Events (Incident Management)

Welkin issues alerts when the application or platform requires human attention.
Welkin comes with many built-in alerts to allow the Platform Administrator to start [troubleshooting](../operator-manual/troubleshooting.md) before an incident happens.

The Application Developer is empowered to configure alerts for their application either via [log-based alerting](../user-guide/log-based-alerts.md) or via [metrics](../user-guide/alerts.md).

## FR 7: Resource Availability

Welkin comes with a [go-live checklist](../user-guide/go-live.md) to ensure that the environment is provided with sufficient capacity even in case of Node (single server) or Zone (whole data-center) failure.

Furthermore, Welkin comes with [capacity-related alerts](../operator-manual/capacity-management.md) to alert the Platform Administrator days in advance when capacity needs to be added to the environment.

## Further Reading

- [MSB, Standard: ISA/IEC 62443](https://www.msb.se/siteassets/dokument/amnesomraden/informationssakerhet-cybersakerhet-och-sakra-kommunikationer/industriella-informations--och-styrsystem/faktablad-standard-isaiec-62443-.pdf)
- [Wikipedia, Operational technology](https://en.wikipedia.org/wiki/Operational_technology)
- [Wikipedia, Industrial control systems](https://en.wikipedia.org/wiki/Industrial_control_system)
