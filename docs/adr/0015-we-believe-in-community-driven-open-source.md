---
tags:
  - ISO 27001 A.17.1.1 Planning Information Security Continuity
---
# We believe in community-driven open source

- Status: accepted
- Deciders: Rob, Johan, Cristian (a.k.a., Product Management working group)
- Date: 2021-08-17

## Context and Problem Statement

We often get bombarded with questions like "Why don't you use X?" or "Why don't you build on top of Y?", sometimes preceded by "product/project X already has feature Y". Needless to say, this can cause a ["Simpsons Already Did It"](https://en.wikipedia.org/wiki/Simpsons_Already_Did_It) feeling.

This ADR clarifies one of the core values of the Welkin project, namely our belief in community-driven open source. The ADR is useful to clarify both to internal and external stakeholders the choices we make.

## Decision Drivers

- We do not want to depend on the interests of any single company, be it small or large.
- The Application Developers need to have a business continuity plan, see [ISO 27001, Annex A.17](https://www.isms.online/iso-27001/annex-a-17-information-security-aspects-of-business-continuity-management/). Therefore, we want to make it easy to "exit" Welkin and take over platform management.
- We want to use the best tools out there.

## Considered Options

- Prefer closed source solutions.
- Prefer single-company open source solutions.
- Prefer community-drive open source solutions.

## Decision Outcome

Chosen option: "prefer community-driven open source solutions".

### Positive Consequences

- We do not depend on the interests of any single company.
- The Application Developers do not depend on the interests of any single company.
- Business continuity is significantly simplified for the Application Developers.
- We have better chances at influencing projects in a direction that is useful to us and the Application Developers. The smaller the project, the easier to influence.

### Negative Consequences

- Sometimes we might need to give up "that cool new feature" until the community-driven open source solution catches up with their closed source or single-company open source alternative. Alternatively, we might need to put extra time and effort to develop "that cool new feature" ourselves.
- As they are not bound by vendor liability -- e.g., end-of-life promises -- community-driven projects present a greater risk of being abandoned. The smaller the project, the higher the risk.
