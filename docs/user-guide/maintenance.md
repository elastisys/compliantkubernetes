---
description: Learn what to expect from our different kinds of Compliant Kubernetes maintenance windows.
---

# What to expect from maintenance

## Different kinds of maintenance

- Patching the underlying OS on the nodes
- Upgrading the Compliant Kubernetes application stack
- Upgrading Kubernetes

## What impact could these kinds of maintenance have on your application?

Let's go through them one by one.

### Patching the OS on the nodes

Some service disruption is expected here, the nodes need to reboot in order to install the OS upgrades/security patches. This should be done automatically by Kured in almost all cases going forward, luckily Kured can be scheduled to perform these upgrades during night-time or whenever application traffic is expected to be low. Thanks to Kured these upgrades are not usually a problem.

### Upgrading the Compliant Kubernetes application stack

There is barely any downtime expected from upgrading the base Compliant Kubernetes application stack. This is because most of the components being upgraded are not intertwined with your application, the only exception being NGINX Ingress Controller, which is not commonly upgraded.

If you have any other managed services from us such as PostgreSQL, Redis, RabbitMQ or TimescaleDB, these services might be upgraded during the application maintenance windows. Upgrading these services can cause some short service disruptions and making them temporarily unreachable for your application.

### Upgrading Kubernetes

The most impactful type of maintenance are the Kubernetes upgrades, which means that the nodes need to be rebooted. Currently there is no automatic process of doing this upgrade, so it has to be done manually. We do these upgrades on scheduled maintenance windows **during office hours**. The way we handle the upgrades is that we drain and reboot all nodes, one at the time.

If parts of your application is running on just one node, then service disruptions are to be expected and parts of the application may become unreachable for short periods during the maintenance window.

The worst case would be if the nodes were near full on resources, then the pods may not be able to be scheduled on another node while getting rebooted. This would mean that the pods running on that node would need to wait for its node to be ready again before it can be scheduled, which could be minutes of downtime.

Note that this is not just a problem for Compliant Kubernetes, the same process would need to be followed when upgrading a "vanilla" Kubernetes cluster.

To minimize the impact on the application you should use [two replicas](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L5) for your application and also set up [topologySpreadConstraints](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L84) to make sure that the replicas do not get scheduled on the same node.
