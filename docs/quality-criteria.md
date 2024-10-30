---
tags:
  - ISO 27001 A.14.2.9 System Acceptance Testing
---

# Quality Criteria

Welkin provides a stable and secure platform for containerized applications.
To achieve this, quality assurance is an integral part of development.
When we say "quality", we really refer to the following quality criteria.

Feature can be delivered ...

- ... at scale

    - Feature has good developer-facing documentation. The documentation includes:
        - the [happy path](https://en.wikipedia.org/wiki/Happy_path);
        - a running example based on the [user demo](https://github.com/elastisys/compliantkubernetes/tree/main/user-demo), if applicable;
        - limitations, if applicable;
        - further reading.
    - Feature is self-serviced
    - Feature is well-understood and aligned in marketing, sales, product and operations
    - Feature is clearly covered by ToS
    - Feature is implemented using a stable upstream API
    - Feature is used by at least 2 Application Developers
    - Feature generates a manageable number of service tickets, whether questions or change orders
    - Feature has well understood packaging and pricing
    - Feature can be billed easily
    - Feature integrates well with application developer observability (alerting, logging, metrics)
    - Feature integrates well with application developer authentication

- ... without ruining admin's life

    - At least 2 admins have required training
    - Feature has good admin-facing documentation (2nd day ops, all processes in place and documented, etc.)
    - Feature triggers a manageable number of P1 alerts
    - Feature triggers a manageable number of P2 alerts
    - Feature has good upstream support
    - All information security risks related to feature have been identified
    - (In case of a new supplier) Supplier collaborates directly with Elastisys admins
    - Feature is covered by QA
    - Feature is sufficiently redundant to be able to operate in degraded state upon faults
    - Feature integrates well with Ops observability (alerting, logging, metrics)

- ... without compromising our security posture

    - Feature has good and well-understood access control towards Application Developer
    - Feature does not expose platform to additional risk (needs escalated privilegies that were not analyzed, etc.)
    - Feature has good and well-understood security patching
    - Feature has good and well-understood upgrades
    - Feature has good and well-understood business continuity, i.e., high availability or self-healing
    - Feature has good and well-understood disaster recovery
    - Feature does not impair ability to upgrade underlying infrastructure and base OS
    - (In case of a new supplier) Supplier provides sufficient security for our needs
    - Feature has good and well understood way of measuring SLA fulfillment

These criteria should be taken as a direction, not a "task list".
For some features, some of these criteria won't apply.
For other features, we might accept that some of these criteria cannot be fully satisfied.
It is the role of our Quality Assurance Engineer (QAE) to decide how to apply these criteria to each feature.

## Quality Assurance (QA)

Each release of Welkin is quality assured.
Some, but not all, of the quality assurance steps are public.
Please find them linked below:

- [Welkin Kubespray Release Checklist](https://github.com/elastisys/compliantkubernetes-kubespray/blob/main/.github/ISSUE_TEMPLATE/release.md)
- [Welkin Apps Release Checklist](https://github.com/elastisys/compliantkubernetes-apps/blob/main/.github/ISSUE_TEMPLATE/release.md)
