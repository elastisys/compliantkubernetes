# Allow a Harbor robot account that can create other robot accounts with full privileges

* Status: accepted
* Deciders: arch meeting
* Date: 2022-11-17

## Context and Problem Statement

We offer UI access to Harbor with admin privileges.
Customer uses a Harbor operator that needs an admin robot account with privileges to create other robot accounts with full privileges.
Should we allow creation of a Harbor robot account which can create other Harbor robot accounts?

## Decision Drivers

* We want to deliver a platform that is easy to use and easy to automate.
* We want to ensure platform security and stability.
* We want to make it hard for customers to break the platform via trivial mistakes.

## Considered Options

* Do not allow Harbor robot account which can create Harbor robot accounts.
* Allow Harbor robot accounts which can create Harbor robot accounts

## Decision Outcome

Chosen option: "Allow Harbor robot accounts which can create Harbor robot accounts", because it does not provide additional privileges, but instead offers a more self-service platform.

### Positive Consequences

* Harbor is more flexible and easy to automate

### Negative Consequences

* Increases the chances that the customer can cripple the Harbor service.

## Recommendations to Operators

Make it clear in the ticket requesting this that the customer accepts the risk of "shooting themselves in the foot"
