# Use bats for testing bash wrappers

- Status: accepted
- Deciders: Compliant Kubernetes Architecture Meeting
- Date: 2021-06-03

## Context and Problem Statement

We write wrapper scripts for simpler and consistent operations.
How should we test these scripts?

## Decision Drivers

- We want to use the best tools out there.
- We want to reduce tools sprawl, i.e., the collective cost (e.g., training) of adding a new tool should outweigh the collective benefit of the new tool.
- We want to make contributions inviting.

## Considered Options

- Do not test bash scripts. (We write perfect scripts 100% of the time, right? :smile:)
- Use `alias` for mocking, `diff` and `test` for assertions.
- Use [bats](https://github.com/bats-core/bats-core)

## Decision Outcome

Chosen option: "bats", because the benefit of using a standard and rather light tool outweighs the cost of collective training on the new tool.

### Positive Consequences

- We use a pretty standard tool for testing in the bash universe.
- We do not risk re-inventing the while by writing our own wrappers around `alias`, `diff` and `test`.

### Negative Consequences

- We need to learn another tool, fortunately, it seems pretty light.

## Other Considerations

Be very mindful about **not** overusing bash. Generally bash should only be used for things that you would do in the terminal, but got tired of copy-pasting, like:

- Running commands
- Copying files
- Setting environment variables
- Minor path translations

For more advanced functionality prefer upstreaming into Ansible roles/libraries, Helm Charts, upstream source code, etc.
