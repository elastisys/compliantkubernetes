# Run Cluster API controllers on Management Cluster

* Status: accepted
* Deciders: Cluster API management and Tekton meeting
* Date: 2023-03-15

## Context and Problem Statement

With Cluster API there multiple different ways to organise the management hierarchy that have different impacts on the environment in regard to cost, availability, security and ease of deployment and maintainability.

Where should we run the Cluster API controller?

## Decision Drivers <!-- optional -->

* We want to minimise the impact it has on resources
* We want to ease the deployment and maintenance process
* We want to be able to tolerate faults in management and workload clusters
* We want to maintain good security posture

## Considered Options

* Independent clusters
  - All clusters run the Cluster API controllers and all clusters manage themselves independently.
* Management Cluster
  - A new separate Management Cluster runs the Cluster API controllers and manages all clusters in the environment.
* Management Cluster
  - The Management Cluster runs the Cluster API controllers and manages all clusters in the environment.

## Decision Outcome

Chosen option: "Management Cluster", because it strikes the balance between security, as it has relatively good availability properties and no Kubernetes admin credentials have to be stored in the workload cluster, and maintainability, as clusters can be managed centralised.

### Positive Consequences <!-- optional -->

* Requires no additional resources
* Requires single instance of Cluster API controllers per environment
* Requires less deployment and maintenance efforts to manage
* Management Cluster already provides services to allow backups, monitoring, and logging
* Workload cluster will not have Kubernetes admin credentials

### Negative Consequences <!-- optional -->

* Cluster API controllers availability relies on Management Cluster
  - Main consideration is control plane, since Management Cluster has sufficient nodes for the controller to reschedule
  - Workload cluster will still function but it will lose auto heal and auto scaling functions
* Management Cluster will have Kubernetes admin credentials for the workload cluster

## Pros and Cons of the Options <!-- optional -->

### Independent cluster

* Good, no additional resource requirements
* Good, all clusters have required supporting services
* Good, all clusters are independently impacted by failures
* Good, all clusters are independently impacted by configuration mistakes, although...
* Bad, it is easier to do configuration mistakes
* Bad, it requires more effort to manage for each cluster
* Bad, all clusters have to be bootstrapped
* Bad, will contain Kubernetes admin credentials in workload cluster

### Management Cluster

* Bad, requires additional resources
* Bad, requires additional supporting services
* Bad, service and workload cluster lose management (auto healing and auto scaling) on Management Cluster failure, although...
* Good, service and workload cluster state can be backed up and restored
* Good, environment can be managed as a group or individually if needed, although...
* Bad, all cluster can be impacted by configuration mistakes, although...
* Good, it is harder for configuration mistakes
* Good, it requires less effort to manage each cluster
* Good, single cluster has to be bootstrapped
* Good, will not contain Kubernetes admin credentials in workload cluster

### Management Cluster

* Good, no additional resource requirements
* Good, Management Cluster has required supporting services
* Bad, workload cluster lose management (auto healing and auto scaling) on Management Cluster failure, although...
* Good, workload cluster state can be backed up and restored
* Good, environment can be managed as a group or individually if needed, although...
* Bad, all cluster can be impacted by configuration mistakes, although...
* Good, it is harder for configuration mistakes
* Good, it requires less effort to manage each cluster
* Good, single cluster has to be bootstrapped
* Good, will not contain Kubernetes admin credentials in workload cluster
