# Compliant Kubernetes User Demo

To make the most out of Compliant Kubernetes, this documentation features a minimalistic NodeJS application. It allows you to explore all Compliant Kubernetes benefits, including, such as HTTPS Ingresses, logging, metrics and user alerts.

The application provides:

- some REST endpoints (`/`, `/users`);
- structured logging;
- metrics endpoint;
- Dockerfile;
- Helm Chart;
- ability to make it crash (`/crash`).

Furthermore, the application caters to a security-hardened environment, and additionally:

- runs as non-root.

## Usage

The `scripts` folder should have self-describing scripts on how to build, test locally and deploy the application.

For examples on using the application with Compliant Kubernetes, check the user guide in the `/docs` folder.

### Run the app with distributed tracing and Jaeger UI
1. Run Docker compose. Update the `JAEGER_EXPORTER_ENDPOINT` variable with your own Jaeger endpoint URL.
```console
docker-compose build

JAEGER_EXPORTER_ENDPOINT="http://jaeger-all-in-one:14268/api/traces" docker-compose up
```
1. Make some requests to the user-demo app
[user-demo app](http://localhost:3000/)
1. Check Jaeger to see the traces (also be displayed in the app console)
[Jaeger UI](http://localhost:16686/)
1. Cleanup
```console
docker-compose stop && docker-compose rm -f
```
