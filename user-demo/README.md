# Compliant Kubernetes User Demo

To make the most out of Compliant Kubernetes, this documentation features a minimalistic NodeJS application. I allows to explore all Compliant Kubernetes benefits, including, such as HTTPS Ingresses, logging, metrics and user alerts.

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
