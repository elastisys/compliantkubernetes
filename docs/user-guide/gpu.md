---
search:
  boost: 2
---

# Using GPU Workload in Welkin

!!! elastisys "For Elastisys Managed Services Customers"
    You can order a new Environment with GPU support by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/).
    Make sure to specify the need for GPU Nodes in "Additional information or comments".
    If you are unsure, get in touch with your account manager.

As the demand for AI, machine learning, and data science workloads grows, Kubernetes provides a flexible and scalable platform to manage these applications.
In this guide, we'll focus on how to use GPU in the Welkin platform.

> [!NOTE]
> Not all infrastructure providers have support for GPU.
> Check with the platform administrator to find out if your environment has support for GPU workload.

## Deployment

To use GPU resources in your cluster, you need to create a deployment that is using the resource `nvidia.com/gpu`.
Here's an example of how to configure GPU resources for a Pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vectoradd
spec:
  restartPolicy: OnFailure
  containers:
  - name: cuda-vectoradd
    image: "nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda11.7.1-ubuntu20.04"
    resources:
      limits:
        nvidia.com/gpu: 1
```

> [!NOTE]
> If your cluster is using the cluster autoscaling feature and there's currently not enough resources, the autoscaler will create one for you.
> It might take a couple of minutes for the new node to join the cluster and to install all the pre-requisites.

### Further Reading

- [Kubernetes Schedule GPU Documentation](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)
- [Kubernetes Cluster Autoscaler Documentation](https://kubernetes.io/docs/concepts/cluster-administration/cluster-autoscaling/)
- [Cluster Autoscaler FAQ](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md)
