# Run csi-cinder-controllerplugin on the Elastisys nodes

* Status: accepted
* Deciders: arch meeting
* Date: 2023-01-26

## Context and Problem Statement

We use the Cinder CSI Driver to manage the lifecycle of OpenStack Cinder Volumes. Currently the csi-cinder-controllerplugin is running on arbitrary nodes.
Where should we run the csi-cinder-controllerplugin?

## Decision Drivers

* We want to deliver a stable and secure platform.
* Want want to keep application Nodes "light", so the application team knows what capacity is available for their application.

## Considered Options

* Run the csi-cinder-controllerplugin on arbitrary Nodes.
* Run the csi-cinder-controllerplugin on Elastisys Nodes.

## Decision Outcome

Chosen option: "Run the csi-cinder-controllerplugin on Elastisys Nodes",  because it improves the stability and security of the platform and makes the application nodes "light"

### Positive Consequences

* The application Nodes infrastructure footprint is lower.
* Security and stability of additional services is somewhat improved, e.g., SystemOOM due to an application won't impact the csi-cinder-controllerplugin.

### Negative Consequences

* We need to change the code to be able to make csi-cinder-controllerplugin run on the Elastisys Nodes.

## Recommendations to Platform Administrators

Specifically, use the following Node labels

```
elastisys.io/node-type=elastisys
```

and taint:

```
elastisys.io/node-type=elastisys:NoSchedule
```

Remember to also add tolerations and Node affinity to all affected Pods.

## Links

* [Taints and Tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
* [Well-Known Labels, Annotations and Taints](https://kubernetes.io/docs/reference/labels-annotations-taints/)
* [Kubespray `node_labels` and `node_taints`](https://github.com/kubernetes-sigs/kubespray/blob/master/docs/vars.md#other-service-variables)
