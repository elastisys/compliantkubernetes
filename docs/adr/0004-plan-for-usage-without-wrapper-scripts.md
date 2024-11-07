# Plan for Usage without Wrapper Scripts

- Status: accepted
- Deciders: Architecture Meeting
- Date: 2020-11-24

## Context and Problem Statement

We frequently write wrapper scripts. They bring the following value:

1. They bind together several tools and make them work together as a whole, e.g., `sops` and `kubectl`.
1. They encode domain knowledge and standard operating procedures, e.g., how to add a node, how a cluster should look like, where to find configuration files.
1. They enforce best practices, e.g., encrypt secrets consumed or produced by tools.

Unfortunately, wrapper scripts can also bring disadvantages:

1. They make usages that are deviating from the "good way" difficult.
1. They risk adding opacity and raise the adoption barrier. People used to the underlying tools may find it difficult to follow how those tools are invoked.
1. They add overhead when adding new features or supporting new use-cases.
1. They raise the learning curve, i.e., newcomers need to learn the wrapper scripts in addition to the underlying tools. Completely abstracting away the underlying tools is unlikely, due to the [Law of Leaky Abstractions](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/).

## Decision Drivers

- We want to make operations simple, predictable, resilient to human error and scalable.
- We want to have some predictability in how an environment is set up.
- We want to make Welkin flexible and agile.

## Considered Options

- On one extreme, we can enforce wrapper scripts as the only way forward. This would require significant investment, as these scripts would need to be very powerful and well documented.
- On the other extreme, we completely "ban" wrapper scripts.

## Decision Outcome

We have chosen to keep wrapper scripts in general. However, they need to be written in a way that ensures that our artefacts (e.g., Terraform scripts, Ansible roles, Helmfiles and Helm Charts) are usable without wrapper scripts. Wrapper scripts should also be simple enough so they can be inspected and useful commands can be copy-pasted out. This ensures that said scripts do not need to be "too" powerful and "too" well documented, but at the same time they do brings the sought after value.

This decision applies for new wrapper scripts. We will not rework old wrapper scripts.

### Positive Consequences

- Platform Administrators can encode standard operating procedures and scale ways of working.
- Our professional services team can easily reuse artefacts for new use-cases, without significant development effort.
- Newcomers will (hopefully) find the right trade-off of barriers, depending on whether they are looking for flexibility or predictability.

### Negative Consequences

- There will be a constant temptation to do things outside wrapper scripts, which will complicated knowledge sharing, operations and support. When this becomes a significant issue, we will need to draft clear guidelines on what should belong in a wrapper scripts and what not.
