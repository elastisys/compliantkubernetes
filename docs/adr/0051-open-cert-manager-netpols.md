# Open cert-manager Network Policies

- Status: accepted
- Deciders: Product Team
- Date: 2024-08-22

## Context and Problem Statement

Certificates is a critical component of any web-based application, as it asserts trust and security for the End User.

Setting up certificates require a few fundamental things which is different depending on if the issuer is using DNS-01 challenges or HTTP-01 challenges:

For DNS-01 challenges one needs:

- The issuer must be configured with correct credentials for the DNS provider.
    - Application developer responsibility
- The Network Policy must be configured to allow cert-manager controller access to the DNS provider, for both API and DNS.
    - Platform administrator responsibility

For HTTP-01 challenges one needs:

- The certificate domain must point towards the Ingress-controller of the cluster.
    - Application developer responsibility.
- The Network Policy must be configured to allow cert-manager controller access to the Ingress-controller of the cluster, and the Ingress-controller access to the cert-manager resolver.
    - Platform administrator responsibility.

This means that there is a shared responsibility.
For DNS-01 challenges this may cause complete failure of certificate issuing if platform administrators are not updated on the issuer application developers are using.
And for HTTP-01 challenges this may cause frequent alerts if certificates are misconfigured regarding packets blocked by Network Policies which may hide potentially critical issues.

The certificates setup by application developers should be application developers full responsibility to keep correctly configured and valid.
However the platform does not currently provide the best experience for application developers to take that responsibility.

Therefore we must consider opening up the Network Policy for cert-manager more to ensure that application developers have the best chance to manage certificates, and minimise the potential of the platform hindering it.

## Decision Drivers <!-- optional -->

- We want to maintain platform security and stability
- We want to find a solution that is scalable and minimises platform administrator burden
- We want to find a solution that is the least astonishing and that best serves application developers
- We want to make it easier to understand faults within the platform

## Considered Options

1. Open egress by default from cert-manager to `0.0.0.0:53/tcp` and `0.0.0.0:53/udp` to ensure any DNS providers should just work for DNS-01 challenges.
1. Open egress by default from cert-manager to `0.0.0.0:80/tcp` to ensure cert-manager can perform self-checks to identify invalid HTTP-01 challenges.
1. Do not open additional egress from cert-manager.

## Decision Outcome

Chosen option: option 1 and option 2.

### Positive Consequences <!-- optional -->

- It give the application developer better experience when setting up issuers and certificates.
    - It should just work for application developers to setup DNS-01 issuers.
    - It should giver clearer responses for application developers to why certificates cannot be issued.
- It gives the platform administrator better experience when monitoring environments.
    - It minimises the role of the platform administrator to ensure certificates can be issued.
    - It minimises the risk of critical alerts for cert-manager being shadowed by misconfigured certificates.

### Negative Consequences <!-- optional -->

- The Network Policy for cert-manager will be more permissive.
    - This would add unrestricted egress on `:80/tcp`, `:53/tcp`, and `:53/udp`.
    - This is somewhat offset by the fact that cert-manager is normally configured by default to allow egress to `0.0.0.0:443/tcp` to connect to Let's Encrypt as they by choice do not provide list of IP addresses to allowlist.

## Pros and Cons of the Options <!-- optional -->

### Option 1

- Good because it ensure that any DNS provider for DNS-01 challenges should just work.
- Good because it gives application developers more independence.
- Bad, because it opens up cert-manager to talk to any DNS server.

### Option 2

- Good because it ensure that cert-manager can identify invalid HTTP-01 challenges.
- Good because it gives application developers more independence.
- Bad, because it opens up cert-manager to talk to any HTTP server.

### Option 3

- Good, because it ensure that cert-manager runs with the most limited Network Policies.
- Bad, because application developers cannot configure DNS-01 and HTTP-01 challenges as they want.
- Bad, because it can cause constant Network Policy alerts that shadows larger problems.
- Bad, because it can lead to certificates in risk of expiry due to missed errors.
