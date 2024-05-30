---
description: Overview page for Application Developers in Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
---

# Application Developer Overview

We know software developers are busy people that want to get up and running as soon as possible!

Use the navigational bar to the side to jump to the section that interests you the most.

## Getting started quickly

Compliant Kubernetes is a Kubernetes distribution that consists of the best (community-driven) open source components in the cloud native space, configured for security and platform stability.
It does not contain any proprietary technology, and no vendor-specific tooling, such as command-line tools or abstractions that only work in this distribution.
To the greatest extent possible, all technology contained within the distribution is community-driven open source, as in, not under a single vendor's control or governance.
The distribution is itself open source, and is also designed and developed in a transparent manner (see our [Architectural Decision Records](../adr/index.md)).

{%
    include "./prepare.md"
    start="<!--prerequisites-start-->"
    end="<!--prerequisites-end-->"
    %}

### Endpoint access

{%
    include "./prepare.md"
    start="<!--endpoint-access-start-->"
    end="<!--endpoint-access-end-->"
%}

<!--
## Component overview

TODO https://github.com/elastisys/compliantkubernetes/issues/836

-->

## Finding more information

If you are not familiar with Kubernetes since before, following our three-step process is a good idea, which includes a demo application for you to deploy and understand the entire process of containerizing an application and how to deploy it.

1. The [first step](prepare.md) is about making necessary preparations such as installing prerequisite software on your laptop.
1. The [second step](deploy.md) is about deploying your software.
1. The [third step](operate.md) is about how you continuously operate the software.

It may be a good idea to **follow along** in all of these, even if you have worked with similar systems before.

If you are familiar with similar systems, a common next step for Application Developers that are already used to Kubernetes is to read up on the [safeguards that Compliant Kubernetes ships with](safeguards/index.md).
You may also wish to use the "Go Deeper" link in the site's navigational bar to find more information about specific topics, such as:

- how to set up [log-based](log-based-alerts.md) or [metric-based](alerts.md) alerts,
- configure [long-term retention of logs](long-term-log-retention.md), or
- how to [use a user-friendly Kubernetes UI](kubernetes-ui.md) as an alternative or complement to the `kubectl` command line tool.
