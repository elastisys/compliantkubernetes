# Handle all CRDs with the standard Helm CRD management

- Status: Accepted
- Deciders: Arch Meeting
- Date: 2024-02-22

## Context and Problem Statement

How should we handle CRDs?

We previously decided on letting upstream projects handle CRDs in any way they please as to decrease our own maintenance efforts. This decision has since proved to be flawed, due to the way some upstream project has decided to handle CRDs.

Helm 3 has [support for installing CRDs](https://helm.sh/docs/topics/charts/#custom-resource-definitions-crds), but not upgrading them, but not all upstream projects use this way of installing CRDs. Instead they include the CRDs as regular resources in the chart, meaning that there is no way of deleting the installed chart release without also removing CRDs and any associated Custom Resource objects.

One example of an issue that this can cause is that both our Apps and Cluster API uses cert-manager to provision certificates. If one were to uninstall cert-manager using our Apps, they would lose required certificate resources that Cluster API needs for its cluster management. A reinstall of cert-manager with Apps would not reinstall these specific Cluster API certificates. This is an issue since we do not want Apps to mess with the underlying infrastructure layer, be it Kubespray or Cluster API.

## Decision Drivers <!-- optional -->

- We need to manage CRDs in a way that is consistent and that allows us to perform necessary actions in Apps without unintended effects on the environment.
- We want to maintain separation of concerns between the Kubespray / Cluster API layer and our Apps layer.

## Considered Options

- Option 1: Make cert-manager opt-in in Apps so that we can disable it for CAPI clusters, and let CAPI handle it.
- Option 2: Improve Apps handling of CRDs, avoiding removing CRDs when uninstalling / cleaning apps, using the way Helm 3 recommends.
- Option 3: Make use of CAPI Operator to handle missing certs.

## Decision Outcome

Chosen option: "Option 2". We decided to supersede [ADR-0011](0011-let-upstream-projects-handle-crds.md) and instead ensure that all charts handle CRDs in the way that Helm 3 recommends. This allows us to remove any app without risking it also deleting CRDs so that there is not risk of us accidentally deleting resources and losing data.

### Positive Consequences <!-- optional -->

- CRDs will be handled in the same way independent of which project / app it is created by.
- Decreases the risk of accidentally deleting Custom Resources and leaving environments in undefined states.

### Negative Consequences <!-- optional -->

- Will require increased maintenance and development efforts from us to properly handle CRDs for all apps.
