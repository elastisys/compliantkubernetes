# Cluster API

!!!note

    Our packaging of Cluster API is being rolled out and is not available in all environments.
    Most Elastisys Managed Service customers are using a version of this platform that is based on Kubespray.
    Elastisys will eventually migrate everyone to Cluster API.
    There is no exact schedule for this migration yet, more information will be provided later.
    If you have any questions then contact our support.

This document aims to show what changes to expect as an Application Developer using Compliant Kubernetes when running on Cluster API instead of Kubespray.

## What is Cluster API

[Cluster API](https://Cluster-api.sigs.k8s.io/) is a project that provides declarative APIs and tools to provision, upgrade and operate Kubernetes Clusters.
It works using Kubernetes objects that describe the state (Cluster) you want and operators that try to reconcile the actual state to the desired state.
This means it's very similar to how one normally works with `Pods` and other resources in Kubernetes, e.g. one can use a `MachineDeployment` to provision Kubernetes Nodes (`Machines`) in a similar way that one can use `Deployments` to provision `Pods`.

Application Developers don't need a full understanding of Cluster API.
In fact, Application Developers will not interact directly with Cluster API at all.
However, Compliant Kubernetes running with Cluster API has a few implications, which Application Developers need to be aware of.
These are described below.

## Node replacement

Cluster API will often replace Nodes instead of modifying them as part of different operations, such as upgrading the Kubernetes version or resizing a Node.
This means that you should not expect individual Kubernetes Nodes to stay in the Cluster.

Node **names and IP addresses** _**will**_ change as the Nodes are replaced.

However, you can rely on the new replacement Nodes to be functionally equivalent to the old ones:

- Any attached storage to application Pods will (as per usual Kubernetes behavior) move to the new Nodes.
- Replacement Nodes will have the same size and any predefined labels.

For Clusters that are spread out across zones you can also rely on the new Nodes being spread out across zones in the same way.

## Egress traffic source IP

Kubernetes Nodes provisioned with Cluster API will by default only have a private IP address.
This means that egress traffic will use Network Address Translation (NAT) via the Infrastructure Provider, similar to how home networks behind a router work.
In turn, this removes the possibility to allowlist traffic from specific Kubernetes Nodes in external services based on the source IP that the external service will see.
Depending on the underlying Cloud Infrastructure Provider and their features, we cannot guarantee that the IP the external services sees is stable over time.
Also depending on underlying cloud infrastructure, the IP might not be exclusive for your Compliant Kubernetes environment, so traffic from that IP could originate from other servers that are not related to your environment.

!!!note

    Elastisys will look into the possibility of getting a stable egress IP for Application Developers that really need it.

All Ingress traffic will go through load balancers and there will not be any major differences for the Ingress traffic.

## Cluster autoscaling

The [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/clusterapi/README.md) will scale up a Cluster if there are Pods in the Pending state (refer to the [Kubernetes documentation on Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)) that cannot currently be scheduled because of a lack of resources with the current set of Nodes.
This means that the scaling is based on resource **requests** on Pods, not the actual current CPU/memory utilization.
In turn, this means the autoscaler cannot prevent Nodes from running out of CPU or memory if the resource requests are not close to the actual usage: to benefit the most from autoscaling, you need to set resource requests as correctly as possible.
The autoscaler will scale down a Cluster if there are unneeded nodes for more than 10 minutes.
A node is unneeded if it has less than cpu and memory requests less that 50% of its capacity and all pods running there can be moved to other nodes (refer to [this documentation](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#how-does-scale-down-work) for more information)

Cluster autoscaling will not be needed for everyone and might not be available on all Infrastructure Providers, contact your Platform Administrator to see if it could be possible to enable for you.
