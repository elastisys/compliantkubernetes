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

The `scripts` folder should have self-describing scripts on how to build, test locally and deploy the application. Generally one would do:

```
# Change variables accordingly
SC_DOMAIN=cksc.a1ck.io
WC_DOMAIN=ckwc0.a1ck.io
REGISTRY_DOMAIN=harbor.$SC_DOMAIN
REGISTRY_PROJECT=default
TAG=v1

docker build -t $REGISTRY_DOMAIN/$REGISTRY_PROJECT/ck8s-user-demo:$TAG .
helm upgrade \
    --install \
    myapp \
    deploy/ck8s-user-demo/ \
    --set image.repository=$REGISTRY_DOMAIN/$REGISTRY_PROJECT/ck8s-user-demo \
    --set image.tag=$TAG \
    --set imagePullSecrets[0].name=harbor-pull-secret \
    --set ingress.hostname=demo.$WC_DOMAIN
```
