---
search:
  boost: 2
---
# Jaeger™ (preview)

!!! elastisys "For Elastisys Managed Services Customers"

    You can order Managed Jaeger™ by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/).

    This is a preview feature. For more information, please read [ToS 9.1 Preview Features](https://elastisys.com/legal/terms-of-service/#91-preview-features).

!!!Warning "Deprecation notice: Jaeger Agent"

    `jaeger-agent` is deprecated in [upstream](https://www.jaegertracing.io/docs/1.52/architecture/#agent) and will get removed in the future. The new method is using `OTEL(OpenTelemetry) SDK` and send traces directly to Jaeger collector using `OTLP` protocol.

<figure>
    <img alt="Jaeger Deployment Model" src="../img/jaeger.drawio.svg" >
    <figcaption>
        <strong>Jaeger on Welkin Deployment Model</strong>
        <br>
        This help you build a mental model on how to access Jaeger as an Application Developer and how to connect your application to Jaeger.
    </figcaption>
</figure>

This page will help you succeed in connecting your application to Jaeger tracing which meets your security and compliance requirements.

## Getting Access

Your administrator will set up the authentication reverse proxy inside Welkin, which will give you access to Jaeger UI.

## Prepare your application

### Using OTEL SDK

You need to use the `OTEL(OpenTelemetry) SDK` client library and send the traces directly to the Jaeger collector using [OTLP protocol](https://opentelemetry.io/docs/specs/otel/protocol/). The application need to send the traces to the Jaeger collector endpoint, which in this case is `http://jaeger-operator-jaeger-collector.jaeger-system.svc.cluster.local:4318/v1/traces`.

Here is an example using python:

```py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

collector_endpoint = "http://jaeger-operator-jaeger-collector.jaeger-system.svc.cluster.local:4318/v1/traces"
otlp_exporter = OTLPSpanExporter(endpoint=collector_endpoint)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("foo"):
    print("Hello world!")
```

Next you need to assign the environment variable `OTEL_SERVICE_NAME` in your Deployment, which will become its name in collected traces.

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
        image: my-app:my-version
        env:
        - name: OTEL_SERVICE_NAME
          value: <service-name>
```

### Using Jaeger-agent (deprecated)

!!!Warning

    This method is deprecated and will be removed in the future.

The Jaeger agent is exposed as a DaemonSet. Your application needs to be told where the agent is located by setting the environment variable `JAEGER_AGENT_HOST` to the value of the Kubernetes node’s IP:

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

Check out the [release notes](../../release-notes/jaeger.md) for the Jaeger setup that runs in Welkin environments!

## Further Reading

- [Jaeger documentation](https://www.jaegertracing.io/docs/1.49/)
