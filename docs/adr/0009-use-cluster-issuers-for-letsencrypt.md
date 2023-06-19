# Use ClusterIssuers for LetsEncrypt

* Status: accepted
* Deciders: Cristian, Lennart
* Date: 2021-02-26

Technical Story: [Make apps less fragile](https://github.com/elastisys/compliantkubernetes-apps/issues/300)

## Context and Problem Statement

Data protection regulations require encrypting network traffic over public networks, e.g., via HTTPS. This requires provisioning and rotating TLS certificates. To automate this task, we use the [cert-manager](https://cert-manager.io/), which automates provisioning and rotation of TLS certificates from [Let's Encrypt](https://letsencrypt.org/).

There are two ways to configure Let's Encrypt as an issuers for cert-manager: [Issuer and ClusterIssuer](https://cert-manager.io/docs/concepts/issuer/). The former is namespaced, whereas the latter is cluster-wide. Should we use Issuer or ClusterIssuer?

## Decision Drivers

* We want to make compliantkubernetes-apps less fragile, and LetsEncrypt ratelimiting is a cause of fragility.
* We want to make it easy for users to get started with Compliant Kubernetes in a "secure by default" manner.
* We want to have a clear separation between user and administrator resources, responsibilities and privileges.
* We want to keep the option open for "light" renderings, i.e., a single Kubernetes clusters that hosts both service cluster and workload cluster components.

## Considered Options

* Use one Issuer per namespace; users need to install their own Issuers in the workload clusters.
* Use ClusterIssuer in service cluster; let users install Issuers in the workload clusters as required.
* Use ClusterIssuer in both service cluster and workload cluster(s).

## Decision Outcome

Chosen option: "Use ClusterIssuers in the service cluster; optionally enable ClusterIssuers in the workload cluster(s)", because it reduces fragility, clarifies responsibilities, makes it easy to get started securely.

Each cluster is configured with an optional ClusterIssuer called `letsencrypt-prod` for LetsEncrypt production and `letsencrypt-staging` for LetsEncrypt staging. The email address for the ClusterIssuers is configured by the administrator.

## Recommendations to Platform Administrators

### Direct LetsEncrypt emails to a "logging" mailbox

Although LetsEncrypt does not require an email address, cert-managers seems to require all ClusterIssuers/Issuers to be configured with a syntactically valid email address. Said email address will receive notifications when certificates are close to expiry. Given that Compliant Kubernetes comes with [Cryptography](../ciso-guide/cryptography.md) dashboards, these emails do not seem useful. **Hence, ClusterIssuer emails should be directed to an address that has "logging" but not "alerting" status.**

### Separate registered domains

LetsEncrypt production has a rate limit of [50 certificates per week per registered domain](https://letsencrypt.org/docs/rate-limits/). For example, if `awesome-website.workload-cluster.environment.elastisys.se` points to the workload cluster's Ingress controller, then an excessive creation and destruction of Ingress resources may trigger rate limiting for all of `elastisys.se`.

It is therefore advisable to:

* Use separate registered domains for development and production environments.
* Use separate registered domains for workload cluster(s) and the service cluster, or restrict which Ingress resources can be created by the user.

Note that, the rate limiting risk exists with both Issuers and ClusterIssuers and was not introduced by this ADR.
