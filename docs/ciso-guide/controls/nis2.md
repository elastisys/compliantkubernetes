---
title: NIS2 Overview
description: Overview of what the Network and Information Security Directive 2 (NIS2) is and how it relates to Compliant Kubernetes
---

<!-- markdownlint-disable-file single-h1 -->

# Network and Information Security Directive 2 (NIS2)

{%
   include-markdown './_common.include'
   start='<!--legal-disclaimer-start-->'
   end='<!--legal-disclaimer-end-->'
%}

The [NIS2 Directive](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive){:target="\_blank"} stands as a comprehensive EU-wide cybersecurity legislation, aimed at elevating the overall state of cybersecurity across the European Union.
Imposing legal measures, it serves to fortify the digital landscape in the region.

Initiated in 2016, the EU's cybersecurity regulations underwent a substantial transformation with the enactment of the NIS2 Directive in 2023.
This update was imperative to adapt to the expanding realm of digitization and the continuously evolving cybersecurity threats.
The directive's enhancements extend the applicability of cybersecurity regulations to novel sectors and entities, thereby enhancing the resilience and response capabilities of public and private bodies, competent authorities, and the entire EU.

The NIS2 Directive, officially titled the Directive on measures for a high common level of cybersecurity across the Union, imposes legal requisites to augment cybersecurity throughout the EU.
Its key provisions encompass ensuring the preparedness of Member States, mandating the establishment of essential capabilities like a Computer Security Incident Response Team (CSIRT) and a competent national network and information systems (NIS) authority.
Furthermore, it promotes cooperation among Member States through the establishment of a Cooperation Group, fostering strategic collaboration and information exchange.

The directive seeks to instill a culture of security across critical sectors vital for the economy and society, heavily reliant on information and communication technologies (ICTs).
These sectors include energy, transport, water, banking, financial market infrastructures, healthcare, and digital infrastructure.

To uphold the directive's objectives, businesses identified by Member States as operators of essential services in the specified sectors must implement suitable security measures and promptly report significant incidents to relevant national authorities.
Similarly, key digital service providers, such as search engines, cloud computing services, and online marketplaces, are obligated to adhere to the security and notification requirements outlined in the directive.

The NIS2 Directive shares a strong connection with two additional initiatives: the Critical Entities Resilience (CER) Directive and the Regulation for Digital Operational Resilience in the Financial Sector, commonly known as the Digital Operational Resilience Act (DORA).

## Which sectors are covered by the NIS2 Directive?

A lot more sectors than in the previous iteration.
Society has become more digital, and as a result, more vulnerable to cyberattacks.
It is clear that many use-cases where Compliant Kubernetes has been successfully used in the past are in scope for NIS2, including sectors of high criticality, healthcare, banking and the financial market, and general public administration.

The [official FAQ](https://digital-strategy.ec.europa.eu/en/faqs/directive-measures-high-common-level-cybersecurity-across-union-nis2-directive-faqs){:target="\_blank"} lists the sectors in scope as follows:

> Sectors of high criticality: energy (electricity, district heating and cooling, oil, gas and hydrogen); transport (air, rail, water and road); banking; financial market infrastructures; health including manufacture of pharmaceutical products including vaccines; drinking water; waste water; digital infrastructure (internet exchange points; DNS service providers; TLD name registries; cloud computing service providers; data centre service providers; content delivery networks; trust service providers; providers of public electronic communications networks and publicly available electronic communications services); ICT service management (managed service providers and managed security service providers), public administration and space.
>
> Other critical sectors: postal and courier services; waste management; chemicals; food; manufacturing of medical devices, computers and electronics, machinery and equipment, motor vehicles, trailers and semi-trailers and other transport equipment; digital providers (online market places, online search engines, and social networking service platforms) and research organisations.

## How does the NIS2 Directive relate to Compliant Kubernetes?

NIS2 Article 21(2) lists 10 so-called minimum requirements.
These minimum requirements need to be translated into policies for your organization, which can then be technically implemented.
Below is a list of pages, which help you translate such policies into implementation on top of Compliant Kubernetes.
Note that, some requirements, such as "basic cyber hygiene practices and cybersecurity training" are out-of-scope for Compliant Kubernetes, hence absent from the list below.

[TAGS]

## Country- and Sector-Specific Requirements

Please see the following pages, also linked in the side bar, for country- and sector-specific rules on top of the NIS2 minimum requirements.
Note that these rules were enacted under NIS1, as NIS2 still needs to be implemented in some EU Member States:

- [KRITIS](kritis.md) (Germany)
- [BSI IT Grundschutz](bsi-it-grundschutz.md) (Germany)
- [MSBFS 2018:8](msbfs-20188.md) (Sweden)
