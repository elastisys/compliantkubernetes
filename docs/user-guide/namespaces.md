---
description: How to work with namespaces in Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
tags:
- ISO 27001 A.12.1.4 Separation of Development, Testing & Operational Environments
- ISO 27001 A.14.2.5 Secure System Engineering Principles
---

# Namespaces

## HNC

[Hierarchical Namespace Controller](https://github.com/kubernetes-sigs/hierarchical-namespaces) (HNC) is included in Compliant Kubernetes. It allows the super application developer to manage namespaces as subnamespaces and delegates access automatically. From the perspective of Kubernetes these are regular namespaces, but these can be modified via a namespaced resource by the user. Building a good namespace structure will enable you to apply namespace-scoped RBAC resources to multiple namespaces at once.

## Namespace Management

Creating a subnamespace:
```bash
kubectl apply -f - <<EOF
apiVersion: hnc.x-k8s.io/v1alpha2
kind: SubnamespaceAnchor
metadata:
  name: <descendant-namespace>
  namespace: <parent-namespace>
EOF
```

Verify that it gets created:
```bash
kubectl get ns <descendant-namespace>
```

Verify that it gets configured:
```console
$ kubectl get subns -n <parent-namespace> <descendant-namespace> -o yaml
apiVersion: hnc.x-k8s.io/v1alpha2
kind: SubnamespaceAnchor
metadata:
	...
  name: <descendant-namespace>
  namespace: <parent-namespace>
...
status:
  status: Ok
```

If the status is `Ok` then the subnamespace is ready to go.

!!!tip
    HNC also comes with the [HNS `kubectl` plugin](https://github.com/kubernetes-sigs/hierarchical-namespaces/blob/master/docs/user-guide/how-to.md#prepare-to-use-hierarchical-namespaces-as-a-user).

    Using this plugin creating subnamespaces is as easy as:
    ```bash
    kubectl hns create -n <parent-namespace> <descendant-namespace>
    ```

    And provides more detailed information using:
    ```bash
    kubectl hns describe <namespace>

    kubectl hns tree <namespace>
    ```

## Resource Propagation

When a subnamespace is created all `Roles` and `RoleBindings` will propagate from the parent namespace to the descendant namespace to ensure that correct access is set. This is what lets you apply namespace-scoped RBAC resources to multiple namespaces at once.
Propagated copies cannot be modified, these types of resources cannot be created in a parent namespace if it conflicts with a resource in a descendant namespace.
To put an exception annotate the `Role` or `RoleBinding` with `propagate.hnc.x-k8s.io/none: "true"` to prevent if from being propagated at all.
Another option is to only propagate to selected descendant namespaces use `propagate.hnc.x-k8s.io/treeSelect: ...`, include descendant namespaces with `<descendant-namespace>` or exclude namespaces with `!<descendant-namespace>`.

!!!note
    In Compliant Kubernetes `v0.27.0` and later `NetworkPolicies` will also propagate from the parent namespace to the descendant namespace just like `Roles` and `Rolebindings`.

## Further Reading

* [HNC User Documentation](https://github.com/kubernetes-sigs/hierarchical-namespaces/tree/master/docs/user-guide)
* [Introducing HNC](https://kubernetes.io/blog/2020/08/14/introducing-hierarchical-namespaces/)
