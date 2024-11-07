# Welkin to consist of both public and private open source

- Status: Accepted
- Deciders: Management Team
- Date: 2024-11-07

## Context and Problem Statement

Elastisys Welkin consists of open source software, and indeed, most of Welkin itself is also public:

- the [Kubespray-based installer](https://github.com/elastisys/compliantkubernetes-kubespray);
- the [documentation](https://github.com/elastisys/welkin) (accessible also as a web site); and
- the [core application components](https://github.com/elastisys/compliantkubernetes-apps) themselves.

Some parts, however, have never been public open source, such as:

- the so-called Additional Managed Services (e.g. PostgreSQL);
- the Cluster API-based installer; and
- the internal tools and documentation Elastisys needs to operate the managed service on public clouds.

This ADR is about those components that are not publicly available. The ones that already are public will stay public.

For context, it is important to note the difference between public and private vs. closed or open source:

- **Public and open source**: Code is publicly available for anyone to view, use, modify, and distribute. This is a very common distribution model for open source software, such as Linux or Kubernetes.
- **Public but closed source**: Software is accessible to the public but with proprietary code that can't be modified. This is the standard for typical proprietary software.
- **Private and open source**: Code is made available under an open source license to a restricted set of authorized users or organizations.
- **Private and closed source**: Code and access to the software is restricted to only specific users, with no modification allowed.

Should the additional components of Welkin's source code be open or closed source, and should distribution thereof be public or private?

## Decision Drivers

- Elastisys wants to protect Welkin users' open source freedom
- Elastisys wants to offer product support customers good value for their money, and incentivise these to keep paying Elastisys, not only for support but also for access to future Welkin development, security patches, etc.
- Product support customers should have ability to adapt Welkin if needed
- Elastisys was founded on a bedrock on knowledge sharing and openness, and wants that to be reflected in the products and services it develops
- Elastisys needs to protect its intellectual property

## Considered Options

1. Offer everything as public open source.
1. Keep the core open and public, other parts as private and open.
1. Keep the core open and public, other parts as private and proprietary (open core model).

## Decision Outcome

Option 2: Keep the core open and public, other parts as private and open.

This gives a balanced approach where those that pay for features that are needed in e.g. enterprise settings or for advanced on-premise use can have access to up to date open source code for as long as their engagement with Elastisys is ongoing.

Once a company stops paying for up to date open source access and product support, they can still keep the code as it was when they had access to it, but do not get further updates, and Elastisys is also not under obligation to keep QA processes ongoing to ensure that future versions of Welkin are compatible with any special solutions developed as part of a past customer engagement.

### Positive Consequences

- Good, because Welkin can stay true to its open source commitment, and thus also preserves user freedoms.
- Good, because customers of product support get exactly what they pay for: access to the open source powering the best security-focused Kubernetes distribution in the world, possible to modify to their liking, and with upstream fixes by Elastisys for the duration of the contract period.
- Good, because with a clear distinction between what is public and private open source, we are clear that everything is open source – what differs is only whether it is distributed in private or public.
- Good, because Elastisys protects its intellectual property around what is needed to operate a Kubernetes platform service at scale on several underlying cloud infrastructure platforms.

### Negative Consequences

- Bad, because a public open source distribution is easier to show every single detail about, as all details are laid out in public anyway.
- Bad, because there may be a general perception that "open source" loosely means _public_ open source, and that it should all be available on e.g. GitHub.
- Bad, because there is no way for community contributions.
