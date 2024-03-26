# ArgoCD with dynamic HNC namespaces

- Status: accepted
- Deciders: product owner, DX, GoTo
- Date: 2023-05-23

## Context and Problem Statement

Argo CD cannot create HNC namespaces and deploy services into them.
Our current Argo offering is a namespaced installation where a CronJob patches the cluster [secret](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters) with the list of managed Namespaces every minute.
An issue occurs when an Application Developer tries to create an Application which also includes a Namespace.
As the new **not yet created/patched to the cluster secret** namespace is not managed, Argo CD fails at the comparison stage.

Currently, upstream ArgoCD is unaware of HNC resources, and does not give subnamespaces the needed precedence, read more [here](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/#how-does-it-work).
The cluster secret that takes a list of managed namespaces, does not take a regular expression, so it is hard for Application Developers to create namespaces as part of an Application.

So, do we want to let Application Developer create and delete subnamespaces dynamically via Argo CD?
If yes, how?

## Decision Drivers <!-- optional -->

- We want to maintain platform security and stability.
- We want to find a solution which is scalable and minimizes Platform Administrator burden.
- We want to best serve our Application Developers.
- We want to make the operator life easier.

## Considered Options

1.  Wait for the Argo Project to integrate better with HNC and ask customers to only create subnamespaces manually until this is fixed upstream.

    - Good, because we are inline with how upstream Argo is built.
    - Bad, because this will not give customers a smooth GitOps experience.
    - Bad, because it makes it hard to use ApplicationSets to dynamically create Applications on new namespaces.

1.  Use OPA to restrict operations on our namespaces and give customers the ability to create/delete namespaces?

    - Bad, because giving Application developers access to create/delete namespaces has been a no-go since the beginning of Compliant Kubernetes for various security reasons.
    - Bad, because building OPA policies to restrict operations on namespaces, would takes away from how community does things and makes it hard for us to pivot to new big changes in the future.

1.  To deploy all the Applications into one big namespace.

    - Bad, because proposing developers to deploy different versions of their components within the same namespace goes against the goal of achieving separation and isolation through namespaces.

1.  Sync Waves and Phases.

    - We investigated this, but found that sync waves are not a solution in this case, as the reconciliation is failing at the comparison stage which happens before sync waves are executed.

1.  Test to see if ArgoCD accepts regex in cluster secret.

    - We investigated this, but found that the secret does not accept wildcards or regex. See the open issue [here](https://github.com/argoproj/argo-cd/issues/10054#issue-1310861246).

1.  Setup Argo CD cluster-wide installation.

    - Bad, because cluster-wide installation would give Argo a lot of permissions and right now, there is no good solution to stop Argo from deploying applications into our system namespaces such as falco, gatekeeper-system, etc., assuming that one needs to use a wildcard as destinations in ArgoCD projects.
    - Bad, because even if Argo CD is installed cluster-wide, When ArgoCD syncs by kind, it does not prioritize subnamespaces first. See [here](https://github.com/argoproj/gitops-engine/blob/bc9ce5764fa306f58cf59199a94f6c968c775a2d/pkg/sync/sync_tasks.go#L27-L66).
    - Bad, because this would also require us to build a lot of OPA policies and later makes it hard to pivot to new ways.

## Decision Outcome

The decision is to let the Argo CD project adopt practices around HNC. Until then:

- Application Developers need to create subnamespaces manually and deploy applications into it.
- Application Developers cannot template the namespace as a value in their manifests.
