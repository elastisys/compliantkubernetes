# Configure Alerts in On-call Management Tool (e.g., Opsgenie)

- Status: accepted
- Deciders: Welkin Architecture Meeting
- Date: 2021-06-03

Technical Story: See "Investigate how to systematically work with alerts"

## Context and Problem Statement

Alerts are some noteworthy IT event, like a Node becoming un-ready, login failure or a disk getting full.
Terminology differs across tooling and organizations, but one generally cares about:

- P1 (critical) alerts, which require immediate human attention -- the person on-call needs to be notified immediately -- and;
- P2 (high) alerts which require human attention with 24 hours -- the person on-call needs to be notified next morning;
- P3 (moderate) alerts which do not require immediate human attention, but should be regularly reviewed.

Other priorities (e.g., P4 and below) are generally used for informational purposes.

Dealing with alerts correctly entails prioritizing them (e.g., P1, P2, P3), deciding if someone should be notified, who should be notified, how they should be notified (e.g., SMS or email) and when.
"Who", "how" and "when" should include escalation, if the previous notification was not acknowledged within a pre-configured time interval, then the same person if notified via a different channel or a new person is notified.

Under-alerting -- e.g., notifying an on-call person too late -- may lead to Service Level Agreement (SLA) violations and a general feeling of administrator anxiety: "Is everything okay, or is alerting not working?".
Over-alerting -- e.g., notifying a person too often about low-priority alerts -- leads to alert fatigue and "crying wolf" where even important alerts are eventually ignored.
Hence, configuring the right level of alerting -- in particular notifications -- is extremely important both for SLA fulfillment and a happy on-call team.

Where should alerting be configured, so as to quickly converge to the optimal alerting level?

## Decision Drivers

- Allow to quickly silence, un-silence and re-prioritize alerts.
- Allow arbitrary flexibility, e.g., who should be notified, when should notification happen, when should escalation happen, for what cluster and namespaces should notification happen, etc.
- Leverage existing tools and processes.

## Considered Options

- Configure alerting in Welkin, specifically Alertmanager.
- Configure alerting in an On-call Management Tool (OMT), e.g., Opsgenie, PagerDuty.

## Decision Outcome

Chosen option: Welkin “over-alerts”, i.e., forwards all alerts and all relevant information to an On-Call Management Tool (OMT, e.g., Opsgenie).
Configuration of alerts happens in the OMT.

### Positive Consequences

- Clear separation of concerns.
- Alerting does not require per-customer configuration of Welkin.
- Leverages existing tools and processes.
- We do not need to implement complex alert filtering in Welkin, e.g., silence alerts during maintenance windows, silence alerts during Swedish holidays, etc.

### Negative Consequences

- Does not capture alerting know-how in Welkin.
- Migration to a new OMT means all alerting configuration needs to be migrated to the new tool. Fortunately, this can be done incrementally.

## Recommendations to Platform Administrators

- Platform Administrators should familiarize themselves with the capabilities of OMT, e.g., OpsGenie. This should be first done using a web UI, since that improves discoverability of such capabilities.
- When alerting configuration becomes too complex and/or repetitive, Platform Administrators should employ a configuration management tools, such as Terraform, to configure the OMT.

## Links

- [Opsgenie documentation](https://docs.opsgenie.com/)
- [Alertmanager documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Terraform Opsgenie provider](https://registry.terraform.io/providers/opsgenie/opsgenie/latest/docs)
- [Pulumni Opsgenie module](https://www.pulumi.com/registry/packages/opsgenie/api-docs/)
