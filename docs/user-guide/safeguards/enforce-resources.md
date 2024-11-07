---
search:
  boost: 2
tags:
  - ISO 27001 A.12.1.3 Capacity Management
---

<!--
Note to contributors: Aim for the following format.

* Title: Highlight benefit to Application Developer
* Context
* Problem
* Solution
* Error
* Resolution
-->

# Avoid downtime with Resource Requests and Limits

!!!note

    This section helps you implement ISO 27001, specifically:

    - A.12.1.3 Capacity Management

!!!important

    This safeguard is enabled by default and will deny violations. As a result, resources that violate this policy will not be created.

## Problem

A major source of application downtime is insufficient capacity. For example, if a Node reaches 100% CPU utilization, then application Pods hosted on it will run slow, leading to bad end-user experience. If a Node runs into memory pressure, the application will run slower, as less memory is available for the [page cache](https://en.wikipedia.org/wiki/Page_cache). High memory pressure may lead to the Node triggering the infamous [Out-of-Memory (OOM) Killer](https://en.wikipedia.org/wiki/Out_of_memory#Recovery), killing a victim, either your application or a platform component.

## Solution

To avoid running into capacity issues, Kubernetes allows Pods to [specify resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) for each of its containers. This achieves two benefits:

1. It ensures that Pods are scheduled to Nodes that have the requested resources.
1. It ensures that a Pod does not exceed its resource limits, hence limiting its blast radius and protecting other application or platform Pods.

## How Does Welkin Help?

To make sure you don't forget to configure resource requests and limits, the administrator can configure Welkin to deny creation of Pods without explicit resource specifications.

If you get the following error:

```error
Error: UPGRADE FAILED: failed to create resource: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-resource-requests] Container "welkin-user-demo" has no resource requests
```

Then you are missing resource requests for some containers of your Pods. The [user demo](https://github.com/elastisys/welkin/blob/main/user-demo/deploy/welkin-user-demo/values.yaml#L42-L51) gives a good example to get you started.

If your administrator has not enforced this policy yet, you can view current violations of the policy by running:

```bash
kubectl get k8sresourcerequests.constraints.gatekeeper.sh require-resource-requests -ojson | jq .status.violations
```

## Further Reading

- [Managing Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
