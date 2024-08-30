# Run Tekton on Management Cluster

- Status: accepted
- Deciders: Cluster API management and Tekton meeting
- Date: 2023-03-15

## Context and Problem Statement

With Tekton we need to decide where to run it, as it will need considerable permissions in the target cluster to be able to manage it.

So, where should we run Tekton?

## Decision Drivers <!-- optional -->

- We want to ease the maintenance and management process
- We want to maintain good security posture
- We want to be able to tolerate faults

## Considered Options

- Tekton on Management Cluster
- Tekton on each cluster

## Decision Outcome

Chosen option "Tekton on Management Cluster", because it will follow nicely together with the decision for Cluster API controller and management hierarchy. No credentials have to be stored in the Workload Cluster, and management can be done centralised.

### Positive Consequences <!-- optional -->

- Requires single instance of Tekton per environment
- Requires less maintenance and management efforts
- Tekton should be unaffected if the Workload Cluster is subjected to faults or a bad change and should be able to keep managing the Workload Cluster and perform rollback as needed.

### Negative Consequences <!-- optional -->

- Possibility that Tekton itself goes into a bad state by applying a bad change
    - This should however only impact the Management Cluster

## Pros and Cons of the Options <!-- optional -->

### Tekton on Management Cluster

- Good, single instance to setup and manage
- Good, centralised management of all clusters
- Good, environment can be managed as a group or individually if needed
- Good, Tekton itself should be unaffected if it applies a bad change to the Workload Cluster and will be available to perform rollback
- Bad, Tekton itself can potentially go into a bad state if it applies a bad change to the Management Cluster
- Good, no need for high privilege credentials in Workload Cluster
- Bad, aggregating high privilege credentials in Management Cluster
- Good, limited access to Management Cluster

### Tekton on each cluster

- Bad, multiple instances to setup and manage
- Bad, individual management of each cluster
- Good, each cluster individually impacted by failures
- Bad, Tekton itself can potentially go into a bad state if it applies a bad change to the cluster
- Bad, need for high privilege credentials in Workload Cluster
- Good, no aggregation of high privilege credentials in Management Cluster
- Bad, wider access to Workload Cluster
