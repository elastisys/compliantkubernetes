---
description: How to prepare your application for Welkin, the security-focused Kubernetes distribution.
search:
  boost: 2
tags:
  - ISO 27001 A.12.6.1 Management of Technical Vulnerabilities
  - BSI IT-Grundschutz APP.4.4.A21
---

# Prepare Your Application

<!--user-demo-overview-start-->

To make the most out of Welkin, prepare your application so it features:

- some REST endpoints: [NodeJS](https://github.com/elastisys/welkin/blob/main/user-demo/app.js#L38), [.NET](https://github.com/elastisys/welkin/blob/main/user-demo-dotnet/Program.cs#L19);
- structured logging: [NodeJS](https://github.com/elastisys/welkin/blob/main/user-demo/app.js#L18), [.NET](https://github.com/elastisys/welkin/blob/main/user-demo-dotnet/Program.cs#L45);
- metrics endpoint: [NodeJS](https://github.com/elastisys/welkin/blob/main/user-demo/app.js#L34), [.NET](https://github.com/elastisys/welkin/blob/main/user-demo-dotnet/Program.cs#L44);
- Dockerfile, which showcases:
    - How to run as non-root: [NodeJS](https://github.com/elastisys/welkin/blob/main/user-demo/Dockerfile#L10-L13), [.NET](https://github.com/elastisys/welkin/blob/main/user-demo-dotnet/Dockerfile#L17);
- [Helm Chart](https://github.com/elastisys/welkin/tree/main/user-demo/deploy/welkin-user-demo), which showcases:
    - [HTTPS Ingresses](https://github.com/elastisys/welkin/blob/main/user-demo/deploy/welkin-user-demo/values.yaml#L37-L40);
    - [ServiceMonitor for metrics collection](https://github.com/elastisys/welkin/blob/main/user-demo/deploy/welkin-user-demo/templates/servicemonitor.yaml);
    - [PrometheusRule for alerting](https://github.com/elastisys/welkin/blob/main/user-demo/deploy/welkin-user-demo/templates/prometheusrule.yaml);
    - [topologySpreadConstraints for tolerating single Node or single Zone failure](https://github.com/elastisys/welkin/blob/main/user-demo/deploy/welkin-user-demo/values.yaml#L76-L82);
    - [resources for capacity management](https://github.com/elastisys/welkin/blob/main/user-demo/deploy/welkin-user-demo/values.yaml#L42-L51);
    - [NetworkPolicies for network segmentation](https://github.com/elastisys/welkin/blob/main/user-demo/deploy/welkin-user-demo/values.yaml#L83-L94);
- [Grafana dashboards for metrics visualization](https://github.com/elastisys/welkin/tree/main/user-demo/deploy/welkin-user-demo/dashboards);
- [script for local development and testing](https://github.com/elastisys/welkin/tree/main/user-demo/scripts);

Bonus:

- [ability to make it crash](https://github.com/elastisys/welkin/blob/main/user-demo/routes/crash.js) (`/crash`).

Feel free to clone our user demo for inspiration:

```bash
git clone https://github.com/elastisys/welkin/
cd welkin/user-demo
```

## Make Sure Your Application Can Terminate Gracefully

In Kubernetes Pods and their Containers will sometimes be terminated.
The cause can differ a lot, everything from you updating your application to a new version, to a Node being replaced or the Node running out of memory.
Regardless of the cause, your application needs to be able to handle terminations unexpectedly.

When a Pod termination is started there is usually a grace period where the Pod can clean up and then shut down gracefully.
This grace period is usually 30 seconds, but can sometimes differ.
If the Pod is not done shutting down at the end of this period, then it will be forcefully shut down.
This process usually looks something like this:

1. Something triggers the Pod termination
1. Any `preStop` [hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/) in the Pod are triggered.
1. TERM signal is sent to each Container in the Pod.
1. If the `preStop` hook or the Pod has not terminated gracefully within the grace period, then the KILL signal is sent to all processes in the Pod.

Your application might need to do some cleanup before terminating, like finishing transactions, closing connections, writing data to disk, etc.
If that is the case, then you have two options to utilize the grace period before the Pod is forcefully terminated.
You can utilize the `preStop` hook to start a script in a container or it can make a HTTP call to a container.
You can have one `preStop` hook per Container in your Pod.
You can also utilize the TERM signal that is sent to the containers by catching them in you application and having that trigger a graceful shutdown.
You can both have `preStop` hooks and catch the TERM signal for the same container.

You can read more about the Pod termination process in the [official Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination).

## Make Sure Your Application Tolerates Nodes Replacement

!!!important

    This section helps you implement ISO 27001, specifically:

    * A.12.6.1 Management of Technical Vulnerabilities

Welkin recommends **against** [PodDisruptionBudgets (PDBs)](https://kubernetes.io/docs/tasks/run-application/configure-pdb/).
PDBs can easily be misconfigured to block draining Nodes, which interferes with automatic OS patching and compromises the security posture of the environment.
Instead, prefer engineering your application to deal with disruptions.
The user demo already showcases how to achieve this with replication and topologySpreadConstraints.
Make sure to move state, even soft state, to [specialized services](additional-services/index.md).

## Further reading

- [Dealing with Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/#dealing-with-disruptions)

<!--user-demo-overview-end-->

## List of Non-Functional Requirements

In some contexts, it is useful to have a more-or-less exhaustive list of [non-functional requirements](https://en.wikipedia.org/wiki/Non-functional_requirement) which the application needs to fulfill to make the best use of the underlying platform.
Sometimes, these may loosely be called "IT requirements".

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

{%
    include "./list-of-non-functional-application-requirements.html"
%}
