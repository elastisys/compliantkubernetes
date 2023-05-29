---
tags:
- ISO 27001 A.12.1.4 Separation of Development, Testing & Operational Environments
- HIPAA S12 - Information Access Management - Isolating Healthcare Clearinghouse Functions - § 164.308(a)(4)(ii)(A)
- MSBFS 2020:7 3 kap. 1 §
- MSBFS 2020:7 3 kap. 2 §
- HSLF-FS 2016:40 3 kap. 10 § Upphandling och utveckling
- BSI IT-Grundschutz APP.4.4.A1
- BSI IT-Grundschutz APP.4.4.A15
---

Compliant Kubernetes recommends to setting up at least two separate environments: one for testing and one for production.

---

# How Many Environments?

Many regulations require strict separation between testing and production environments.
In particular, production data should not be compromised, no matter what happens in testing environments.
Therefore, Compliant Kubernetes recommends setting up **at least two environments**:

- staging;
- production.

However, the exact number of environments will depend on your needs.
Please use the two figures below to reason about environments, trading developer productivity and data security:

![Ideal Developer Experience](img/environments/ideal-dx.svg)

![Ideal Promotion](img/environments/ideal-promotion.svg)
