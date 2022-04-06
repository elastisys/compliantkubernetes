---
description: Learn how to operate your application on Elastisys Compliant Kubernetes, the security-hardened Kubernetes distribution
---

# Step 3: Operate

Welcome to the third and final step, Application Developer!

In this step, you will learn how to operate your application on Elastisys Compliant Kubernetes.


## Configure Dashboards and Alerts

### Monitor your Application

To monitor your application, you will log in to your Grafana. Recall how to log in to your web portals from [Step 1: Prepare](prepare.md).

Grafana visually displays the monitoring data that Prometheus has collected on your behalf. A significant amount of metrics are already collected for you, out of the box, on Elastisys Compliant Kubernetes. This means you can visualize data about the cluster immediately.

But Prometheus can also be instructed to collect specific metrics from your own application. Perhaps this is more useful to you than monitoring metrics that relate to cluster health (in particular if somebody else managed Elastisys Compliant Kubernetes for you).

To instruct Promethus on how to do this, you create a [ServiceMonitor](https://blog.container-solutions.com/prometheus-operator-beginners-guide). This is a Kubernetes resource that configures Prometheus and specifies how to collect metrics from a particular application.

{%
    include "metrics.md"
    start="<!--user-demo-metrics-start-->"
    end="<!--user-demo-metrics-end-->"
%}

Go deeper into [metrics](metrics.md).

### Alert on Application Metrics

Visualizing monitoring metrics is one thing. Sometimes, you may need to act on what they show, immediately. For that reason, the Prometheus monitoring system includes AlertManager.

* Prometheus is responsible for maintaining a set of Rules, which express trigger conditions via expressions. Once a rule has triggered, it has entered an alerting state.
* AlertManager is responsible for forwarding information about any rules in the alerting state to your chosen destination, which could be your company's Slack or similar. [A number of integrations are available](https://prometheus.io/docs/alerting/latest/configuration/).

If you wish to create rules based on application-specific monitoring metrics, you must first create appropriate ServiceMonitors as described above.

{%
    include "alerts.md"
    start="<!--user-demo-alerts-start-->"
    end="<!--user-demo-alerts-end-->"
%}

Go deeper into [metric alerts](alerts.md).

### Alert on Log Contents

Similar to alerting based on monitoring metrics, you may need to alert based on application log contents. For instance, it might make sense to send any log line of the `FATAL` log level to your Slack channel for immediate attention.

The process of setting up log-based alerts is highly graphical, and supported by your OpenSearch Dashboards that is part of Elastisys Compliant Kubernetes. Recall how to log in to your web portals from [Step 1: Prepare](prepare.md).

Go deeper into [log-based alerts](log-based-alerts.md).

## Test Backups and Capacity Management

Disaster recovery is about so much more than backing up and restoring data. Backing up data is a necessary, but not sufficient, part of that.

Not having sufficient capacity is also a kind of disaster, albeit, one that is easy to mitigate.

### Back up Application Data

{%
    include "backup.md"
    start="<!--user-demo-backup-start-->"
    end="<!--user-demo-backup-end-->"
%}

{%
    include "backup.md"
    start="<!--user-demo-restore-start-->"
    end="<!--user-demo-restore-end-->"
%}

Go deeper into [backups](backup.md).

### Capacity Management

Capacity management is about having sufficient capacity for your needs, be they in terms of storage or computational power.

Your Elastisys Compliant Kubernetes administrator should perform capacity management *of the platform*, to ensure that there is a sufficient amount of spare capacity on a cluster level.

As an application developer, you should perform capacity management on a Pod level. This primarily means setting [resource requests](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) correctly for containers inside Pods, making use of multiple instances in your Deployments and Stateful Sets (possibly via [horizontal Pod autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)). The use of resource requests and limits is enforced via an Elastisys Compliant Kubernetes [safeguard](safeguards/enforce-resources.md).

## Automate with CI/CD

Elastisys Compliant Kubernetes currently does not dictate or recommend any particular CI/CD solution over any other. It is, however, easy to integrate with various CI/CD solutions, such as GitHub Actions.

The basic steps for a generic push-style CI/CD solution (such as GitHub Actions) are to:

0. Create a limited `Role`, that has the least possible privileges required to deploy your application.
0. Create a `ServiceAccount` and binding to the role created earlier via a `RoleBinding`, granting it the permissions needed for deploying the application.
0. Getting the token for the ServiceAccount, so you can craft a `KUBECONFIG` to use with `kubectl` or `helm` in your CI/CD solution.

Adding an in-cluster CI/CD solution is a work in progress, pending security reviews of alternatives in the ecosystem.

Go deeper into [CI/CD](ci-cd.md).

## Next step? Going deeper!

By now, you're fully up and running! You have an application, updating it is a breeze, and you can monitor it and look at its logs. The next step is to open the "Go deeper" section of this documentation and read up on more topics that interest you.

Thank you for starting your journey beyond the clouds with Elastisys Compliant Kubernetes!
