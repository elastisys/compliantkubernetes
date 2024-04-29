# Software Bill of Materials (SBOM)

!!!abstract "TL;DR"
    Our attention is directed at assessing each top-level component and ensuring that they fulfill our security and business continuity goals.

    If you are interested in how Elastisys does vulnerability management, please consult [ToS 3.6 Vulnerability Management](https://elastisys.com/legal/terms-of-service/#36-vulnerability-management).

This page explains our philosophy around SBOMs and where you can find the Compliant Kubernetes SBOM.

## What is an SBOM?

As described on Wikipedia:

> A software bill of materials (SBOM) declares the inventory of components used to build a software artifact such as a software application.
> It is analogous to a list of ingredients on food packaging: where you might consult a label to avoid foods that may cause allergies, SBOMs can help organizations or persons avoid consumption of software that could harm them.

## Why is an SBOM important?

If used correctly, an SBOM can avoid the following major risks:

- supply-chain attacks;
- breach of business continuity;
- technical vulnerabilities; and
- copyright violation.

An SBOM is probably the first step to comply with the proposed [EU Cyber Resilience Act](https://digital-strategy.ec.europa.eu/en/library/cyber-resilience-act).

## Our SBOM Philosophy

There is an [ocean of tools](https://spdx.dev/use/tools/open-source-tools/) capable to generate a SBOM in a machine-readable format like [SPDX](https://spdx.dev/).
Unfortunately, these tools create a lot of data, but not so much insight that is easy to grasp.
In fact, the value of an SBOM doesn't come from **generating** it.
Instead, the value of an SBOM comes from **assessing** the suitability of each component in the inventory to the [product's mission and vision](../mission-and-vision.md).

Compliant Kubernetes prefers [community-driven open-source components](../adr/0015-we-believe-in-community-driven-open-source.md) from reputable stewards, like the [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io/).
The CNCF already puts a lot of time into:

- assessing the [maturity and health](https://github.com/cncf/toc/blob/main/operations/project-health-review.md) of CNCF projects;
- making sure that components are [licensed under Apache 2.0 or equivalent](https://github.com/cncf/foundation/blob/main/allowed-third-party-license-policy.md);
- performing regular [security audits](https://www.cncf.io/blog/2022/08/08/improving-cncf-security-posture-with-independent-security-audits/).

Our reputable stewards and vendors have similar initiatives.

Therefore, our SBOM builds upon the due diligence of software vendors and stewards.
Our SBOM stops at the project level and does not go down into details such as the countless Go and NodeJS libraries they use.

Our attention is directed at assessing each top-level component and ensuring that they fulfill our security and business continuity goals.

## SBOM

Given the above, we publish our SBOM within the scope of the [Compliant Kubernetes layer](../architecture.md#level-3-individual-components) for each version of Compliant Kubernetes at <https://github.com/elastisys/compliantkubernetes-apps/blob/main/docs/sbom.md>.

If desired, we can share internal documents on how we assessed the suitability of each component.
