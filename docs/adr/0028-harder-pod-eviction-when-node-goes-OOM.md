# Harder Pod eviction when nodes are going OOM

- Status: accepted
- Deciders: arch meeting
- Date: 2022-12-08

## Context and Problem Statement

We had several incidents where nodes are going OOM and become unresponsive when too many pods are being scheduled on them. This also leads to pods getting evicted, and this applies to our pods that are responsible for the platform security and compliance.
Should we enable kubelet hard eviction so as to behold the vital components?

## Decision Drivers

- We want to ensure platform security and stability.
- We want to make it hard for Application Developers to break the platform via trivial mistakes.
- We want to make sure that the critical components are not evicted when nodes are overcommitted.

## Considered Options

- Enable kubelet hard eviction.
- Adjust OOM score so that kernel does not OOM critical Pods
- Setup priority class for all our apps
- Do not make any changes and reinforce the responsibility to the customer for not overloading the nodes.

## Decision Outcome

Chosen options: `Enable kubelet hard eviction` & `Setup priority class for all our apps` .

The option `Adjust OOM score so that kernel does not OOM critical Pods` is not viable as it can be used only if we set requests=limits on all our pods (see [here](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/#node-out-of-memory-behavior) and [here](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/#create-a-pod-that-gets-assigned-a-qos-class-of-guaranteed)), and this will not allow us to benefit from the burstable capabilities of Kubernetes and have a static allocation of resources which locks the resources on the nodes even if they are not used most of the time. This reduces the available resources for the Application Developer on the nodes.

### Positive Consequences

- Security and stability of the platform is somewhat improved.

### Negative Consequences

- Application Developer pods will be stuck in pending until resources are available and this might make the Application Developer feel that their pods are less important.
- [kubectl may not observe pressure right away](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/#kubelet-may-not-observe-memory-pressure-right-away)

## Recommendation to Platform Administrators

Test multiple configurations using kubelet hard eviction, priority classes and other option to obtain the desired behaviour where the nodes do not become unresponsive and our components are not getting evicted when the node is overcommitted by the Application Developer.
