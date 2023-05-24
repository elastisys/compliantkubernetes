# ArgoCD with dynamic hnc namespaces

* Status: accepted
* Deciders: product owner, DX, GoTo
* Date: 2023-05-23

## Context and Problem Statement

Argo CD cannot create HNC namespaces and deploy services into them.
Our current Argo offering is a namespaced installation where a cronjob patches the cluster [secret](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#clusters) with the list of managed namespaces every minute.
So, when a user tries to create an Application and if part of it is a namespace and service to be deployed into the namespace.
As the new **Not yet created/patched to the cluster secret** namespace is not managed, Argo CD fails at the comparison stage.

Currently, upstream ArgoCD is unaware of HNC resources, and does not give subnamespaces the needed precedence, read more [here](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/#how-does-it-work).
The cluster secret that takes a list of managed namespaces, does not take a regular expression, so it is hard for Application developers to create namespaces as part of an Application.

So, do we want to let customers create and delete subnamespaces dynamically via Argo CD?
If yes, how?

## Decision Drivers <!-- optional -->

- We want to maintain platform security and stability.
- We want to find a solution which is scalable and minimizes MSE burden.
- We want to best serve our customers.
- We want to make the operator life easier.

## Considered Options

* Wait for the Argo Project to integrate better with HNC and ask customers to only create subnamespaces manually until this is fixed upstream.

  1. Good, We are inline with how upstream Argo is built.
  1. Bad, This will not give customers a smooth gitops experience
  1. Bad, Makes it hard to use ApplicationSets to dynamically create Applications on new namespaces.

* Use OPA to restrict operations on our namespaces and give customers the ability to create/delete namespaces ?

  1. Giving Application developers access to create/delete namespaces has been a no-go since the beginning of compliantkubernetes for various security reasons.
  1. Building OPA policies to restrict operations on namespaces, would takes away from how community does things and makes it hard for us to pivot to new big changes in the future.

* To deploy all the Applications into one big namespace.

  1. Proposing developers to deploy different versions of their components within the same namespace goes against the goal of achieving separation and isolation through namespaces.

* Sync Waves and Phases

  1. Investigated this, found that sync waves are not a solution in this case, as the reconciliation is failing at the comparison stage which happens before sync waves are executed.

* Test to see if ArgoCD accepts regex in cluster secret

  1. Investigated this, found that the secret does not accept wildcards or regex. See the open issue [here](https://github.com/argoproj/argo-cd/issues/10054#issue-1310861246)

* Setup ArgoCD cluster-wide installation.

  1. Cluster wide installation would give Argo a lot of permissions and right now, there is no good solution to stop Argo from deploying applications into our system namespaces such as falco, gatekeeper-system etc, Assuming that one needs to use a wildcard as destinations in ArgoCD projects.

  1. Even if ArgoCD is installed clusterwide, When ArgoCD syncs by kind it does not prioritize subnamespaces first. See [here](https://github.com/argoproj/gitops-engine/blob/bc9ce5764fa306f58cf59199a94f6c968c775a2d/pkg/sync/sync_tasks.go#L27-L66)

  1. This would also require us to build a lot of OPA policies and later makes it hard to pivot to new ways.

## Decision Outcome

The Decision is to let the ArgoCD project adopt practices around HNC and until then,

- Customers need to create subnamespaces manually and deploy applications into it.
- Customers cannot template the namespace as a value in their manifests.
