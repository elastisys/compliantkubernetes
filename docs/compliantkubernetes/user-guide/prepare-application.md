---
description: How to prepare your application for Elastisys Compliant Kubernetes, the security-focused kubernetes distribution.
tags:
- ISO 27001 A.12.6.1
- BSI IT-Grundschutz APP.4.4.A21
---

# Prepare Your Application

<!--user-demo-overview-start-->
To make the most out of Compliant Kubernetes, prepare your application so it features:

- some REST endpoints: [NodeJS](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/app.js#L32), [.NET](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo-dotnet/Program.cs#L19);
- structured logging: [NodeJS](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/app.js#L13), [.NET](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo-dotnet/Program.cs#L45);
- metrics endpoint: [NodeJS](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/app.js#L28), [.NET](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo-dotnet/Program.cs#L44);
- Dockerfile, which showcases:
    - How to run as non-root: [NodeJS](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/Dockerfile#L10-L13), [.NET](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo-dotnet/Dockerfile#L17);
- [Helm Chart](https://github.com/elastisys/compliantkubernetes/tree/main/user-demo/deploy/ck8s-user-demo), which showcases:
    - [HTTPS Ingresses](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L37-L40);
    - [ServiceMonitor for metrics collection](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/servicemonitor.yaml);
    - [PrometheusRule for alerting](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/prometheusrule.yaml);
    - [topologySpreadConstraints for tolerating single Node or single Zone failure](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L76-L82);
    - [resources for capacity management](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L42-L51);
    - [NetworkPolicies for network segmentation](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L83-L94);
- [Grafana dashboards for metrics visualization](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/dashboards);
- [script for local development and testing](https://github.com/elastisys/compliantkubernetes/tree/main/user-demo/scripts);

Bonus:

- [ability to make it crash](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/routes/crash.js) (`/crash`).

Feel free to clone our user demo for inspiration:

```bash
git clone https://github.com/elastisys/compliantkubernetes/
cd compliantkubernetes/user-demo
```

## Make Sure Your Application Tolerates Nodes Replacement
!!!important

    This section helps you implement ISO 27001, specifically:

    * A.12.6.1 Management of Technical Vulnerabilities

Compliant Kubernetes recommends **against** [PodDisruptionBudgets (PDBs)](https://kubernetes.io/docs/tasks/run-application/configure-pdb/). PDBs can easily be misconfigured to block draining Nodes, which interferes with automatic OS patching and compromises the security posture of the environment. Instead, prefer engineering your application to deal with disruptions. The user demo already showcases how to achieve this with replication and topologySpreadConstraints. Make sure to move state, even soft state, to [specialized services](/compliantkubernetes/user-guide/additional-services/).

Further reading:

* [Dealing with Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/#dealing-with-disruptions)

<!--user-demo-overview-end-->
