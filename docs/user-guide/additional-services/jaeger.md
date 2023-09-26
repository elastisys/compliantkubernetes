Jaeger™ (preview)
=================

!!! elastisys "For Elastisys Managed Services Customers"

    You can order Managed Jaeger™ by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/).

    This is a preview feature. For more information, please read [ToS 9.1 Preview Features](https://elastisys.com/legal/terms-of-service/#91-preview-features).

<figure>
    <img alt="Jaeger Deployment Model" src="../img/jaeger.drawio.svg" >
    <figcaption>
        <strong>Jaeger on Compliant Kubernetes Deployment Model</strong>
        <br>
        This help you build a mental model on how to access Jaeger as an Application Developer and how to connect your application to Jaeger.
    </figcaption>
</figure>

This page will help you succeed in connecting your application to Jaeger tracing which meets your security and compliance requirements.

## Getting Access

Your administrator will set up the authentication reverse proxy inside Compliant Kubernetes, which will give you access to Jaeger UI.

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

## Follow the Go-Live Checklist

You should be all set.
Before going into production, don't forget to go through the [go-live checklist](../go-live.md).

## CK8S Jaeger Release Notes

Check out the [release notes](../../release-notes/jaeger.md) for the Jaeger setup that runs in Compliant Kubernetes environments!

## Further Reading

* [Jaeger documentation](https://www.jaegertracing.io/docs/1.49/)
