---
tags:
- MSBFS 2020:7 2 kap. 4 §
---
# Architecture

Below we present the architecture of Compliant Kubernetes, using the [C4 model](https://c4model.com/).

For the nitty-gritty details, see [Architectural Decision Records](adr/index.md).

## Level 1: System Context

Let us start with the system context.

![C4 Model, Level 1 Diagram](img/ck8s-c4model-level1.drawio.svg)

Compliance imposes restrictions on all levels of the tech stack. Your compliance focus should mostly lie on your application. Compliant Kubernetes ensures that the platform hosting your application is compliant. Finally, you need the whole software stack on a hardware that is managed in a compliant way, either via an ISO 27001-certified cloud provider or using on-prem hardware.

## Level 2: Clusters

Most regulations require logging to a tamper-proof environment. This is usually interpreted as an attacker gaining access to your application should not be able to delete logs showing their attack and the harm caused by their attack.

To achieve this, Compliant Kubernetes is implemented as two Kubernetes clusters

* A **workload cluster**, which hosts your application, and
* A **management cluster**, which hosts services for monitoring, logging and vulnerability management.

![C4 Model, Level 2 Diagram](img/ck8s-c4model-level2.png)

## Level 3: Individual Components

Click on the diagram below to see the nuts-and-bolts of Compliant Kubernetes.

[![C4 Model, Level 3 Diagram](img/ck8s-c4model-level3.drawio.svg)](img/ck8s-c4model-level3.drawio.svg)

!!!note
    Due to technical limitations, some compliance-related components still need to run in the workload cluster. These are visible when inspecting the workload cluster, for example, via the [Kubernetes API](user-guide/kubernetes-api.md). Currently, these components are:

    * Falco, for intrusion detection;
    * Prometheus, for collecting metrics;
    * Fluentd, for collecting logs;
    * OpenPolicyAgent, for enforcing Kubernetes API policies.

    Note that, the logs, metrics and alerts produced by these components are immediately pushed into the tamper-proof logging environment, hence this technical limitation does not weaken compliance.

## Level 3: Authentication

Click on the diagram below to see the nuts-and-bolts of Compliant Kubernetes authentication.

[![C4 Model, Level 3 Diagram, Authentication](img/ck8s-c4model-level3-auth.drawio.svg)](img/ck8s-c4model-level3-auth.drawio.svg)

## Level 3: Backup

Click on the diagram below to see the nuts-and-bolts of Compliant Kubernetes backup.

[![C4 Model, Level 3 Diagram, Backup](img/ck8s-c4model-level3-backup.drawio.svg)](img/ck8s-c4model-level3-backup.drawio.svg)

## Level 3: Metrics and Metrics-based Alerting

[![C4 Model, Level 3 Diagram, Metrics](img/ck8s-c4model-level3-metrics.drawio.svg)](img/ck8s-c4model-level3-metrics.drawio.svg)

## Level 3: Logs and Log-based Alerting

[![C4 Model, Level 3 Diagram, Logs](img/ck8s-c4model-level3-logs.drawio.svg)](img/ck8s-c4model-level3-logs.drawio.svg)

## Level 3: Access Control

[![C4 Model, Level 3 Diagram, Access Control](img/ck8s-c4model-level3-access-control.drawio.svg)](img/ck8s-c4model-level3-access-control.drawio.svg)
