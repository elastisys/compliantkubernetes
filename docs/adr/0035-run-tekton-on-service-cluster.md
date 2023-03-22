# Run Tekton on service cluster

* Status: accepted
* Deciders: Cluster API management and Tekton meeting
* Date: 2023-03-15

## Context and Problem Statement

With Tekton we need to decide where to run it, as it will need considerable permissions in the target cluster to be able to manage it.

So, where should we run Tekton?

## Decision Drivers <!-- optional -->

* We want to ease the maintenance and management process
* We want to maintain good security posture
* We want to be able to tolerate faults

## Considered Options

* Tekton on service cluster
* Tekton on each cluster

## Decision Outcome

Chosen option "Tekton on service cluster", because it will follow nicely together with the decision for Cluster API controller and management hierarchy. No credentials have to be stored in the workload cluster, and management can be done centralised.

### Positive Consequences <!-- optional -->

* Requires single instance of Tekton per environment
* Requires less maintenance and management efforts
* Tekton should be unaffected if the workload cluster is subjected to faults or a bad change and should be able to keep managing the workload cluster and perform rollback as needed.

### Negative Consequences <!-- optional -->

* Possibility that Tekton itself goes into a bad state by applying a bad change
  - This should however only impact the service cluster

## Pros and Cons of the Options <!-- optional -->

### Tekton on service cluster

* Good, single instance to setup and manage
* Good, centralised management of all clusters
* Good, environment can be managed as a group or individually if needed
* Good, Tekton itself should be unaffected if it applies a bad change to the workload cluster and will be available to perform rollback
* Bad, Tekton itself can potentially go into a bad state if it applies a bad change to the service cluster
* Good, no need for high privilege credentials in workload cluster
* Bad, aggregating high privilege credentials in service cluster
* Good, limited access to service cluster

### Tekton on each cluster

* Bad, multiple instances to setup and manage
* Bad, individual management of each cluster
* Good, each cluster individually impacted by failures
* Bad, Tekton itself can potentially go into a bad state if it applies a bad change to the cluster
* Bad, need for high privilege credentials in workload cluster
* Good, no aggregation of high privilege credentials in service cluster
* Bad, wider access to workload cluster
