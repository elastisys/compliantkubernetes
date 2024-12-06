# Understand Welkin

This page give you a basic understanding of Welkin from the point-of-view of the Platform Administrator.
For a basic understanding of Welkin from the point-of-view of the Application Developers, head to [Application Developer Overview](../user-guide/index.md).

## Welkin Architecture

To begin with, you should familiarize yourself with [Welkin's architecture](../architecture.md).
It describes what components are part of Welkin and what component talks to which other components.
It allows you to create a mental model and reason about complex failure modes, such as "a buffer overflow in fluentd may be caused by OpenSearch lacking sufficient capacity to ingest all logs".

In particular, notice that:

- Welkin is composed of at least two Kubernetes clusters:
  - at least one Workload Cluster: this hosts the applica
  - one Service Cluster.
- Welkin is composed of two layers: Kubernetes-lifecycle, which we call the "Kubespray" or "Cluster API" layer, and
