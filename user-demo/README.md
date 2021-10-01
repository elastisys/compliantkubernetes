# Compliant Kubernetes User Demo

This repository features a minimalistic NodeJS application to show off [Compliant Kubernetes](https://compliantkubernetes.io) features, such as Ingress, logging, metrics and user alerts.

The application provides:

- some REST endpoints (`/`, `/users`);
- structured logging;
- metrics endpoint;
- Dockerfile;
- Helm Chart;
- ability to make it crash (`/crash`).

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
