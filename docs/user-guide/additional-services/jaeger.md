Jaeger®
===========

![Jaeger Deployment Model](img/jaeger.drawio.svg)

This page will help you succeed in connecting your application to Jaeger tracing  which meets your security and compliance requirements.

<!--jaeger-setup-start-->

## Provision a New Jaeger Cluster

Ask your service-specific administrator to install a Jaeger cluster inside your Compliant Kubernetes environment. The service-specific administrator will ensure the Jaeger cluster complies with your security requirements, including:

* **Business continuity**: We recommend a highly available setup with 3 instances for Jaeger and Opensearch.
* **Disaster recovery**: Your service-specific administrator will configure Opensearch with regular backups.
* **Capacity management**: Your service-specific administrator will ensure Jaeger and Opensearch runs on dedicated (i.e., tainted) Kubernetes Nodes, as required to get the best performance.
* **Incident management**: Your administrator will set up the necessary probes, dashboards and alerts, to discover issues and resolve them, before they become a problem.
* **Access control**: Your administrator will set up a reverse proxy that provides authentication using Dex.

Compliant Kubernetes recommends the [Jaeger operator](https://github.com/jaegertracing/jaeger-operator).

## Getting Access

Your administrator will set up the authentication reverse proxy inside Compliant Kubernetes, which will give you access to JaegerUI.

## Prepare your application

The Jaeger agent is exposed as a DaemonSet. Your application needs to be told where the agent is located by setting the environment variable JAEGER_AGENT_HOST to the value of the Kubernetes node’s IP:

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  selector:
    ...
  template:
    ...
    spec:
      containers:
      - name: my-app
        image: acme/my-app:my-version
        env:
        - name: JAEGER_AGENT_HOST
          valueFrom:
            fieldRef:
              fieldPath: status.hostIP
```

<!--jaeger-setup-end-->

## Follow the Go-Live Checklist

You should be all set.
Before going into production, don't forget to go through the [go-live checklist](../go-live.md).

## CK8S Jaeger Release Notes

Check out the [release notes](../../release-notes/jaeger.md) for the Jaeger setup that runs in Compliant Kubernetes environments!

## Further Reading

* [Jaeger documentation](https://www.jaegertracing.io/docs/latest/)
