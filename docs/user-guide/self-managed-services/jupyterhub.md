# JupyterHub (self-managed)
===========

{%
   include-markdown './_common.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

JupyterHub brings Jupyter Notebooks to the cloud. It gives the users access to computational environments and resources without burdening users with installation and maintenance tasks. This documents shows a guide on how to setup JupyterHub in a Compliant Kubernetes cluster.

## Pushing the Jupyeterhub images to Harbor
This sections shows how to pull the required images for JupyterHub and push them to another registery. If you are using the managed Harbor as your container registry, please follow [these instructions](../deploy.md) on how to authenticate, create a new project, and how to create a robot account and using it in a pull-secret to be able to pull an image from Harbor to your cluster safely:

```sh
CHP_TAG=4.5.6
JUPYTER_TAG=3.0.3
PAUSE_TAG=3.9
TRAEFIK_TAG=v2.10.4
REGISTRY=harbor.$DOMAIN
REGISTRY_PROJECT=jupyterhub

docker pull jupyterhub/configurable-http-proxy:$CHP_TAG
docker tag jupyterhub/configurable-http-proxy:$CHP_TAG $REGISTRY/$REGISTRY_PROJECT/configurable-http-proxy:$CHP_TAG
docker push $REGISTRY/$REGISTRY_PROJECT/configurable-http-proxy:$CHP_TAG

docker pull jupyterhub/k8s-hub:$JUPYTER_TAG
docker tag jupyterhub/k8s-hub:$JUPYTER_TAG $REGISTRY/$REGISTRY_PROJECT/k8s-hub:$JUPYTER_TAG
docker push $REGISTRY/$REGISTRY_PROJECT/k8s-hub:$JUPYTER_TAG

docker pull jupyterhub/k8s-image-awaiter:$JUPYTER_TAG
docker tag jupyterhub/k8s-image-awaiter:$JUPYTER_TAG $REGISTRY/$REGISTRY_PROJECT/k8s-image-awaiter:$JUPYTER_TAG
docker push $REGISTRY/$REGISTRY_PROJECT/k8s-image-awaiter:$JUPYTER_TAG

docker pull jupyterhub/k8s-network-tools:$JUPYTER_TAG
docker tag jupyterhub/k8s-network-tools:$JUPYTER_TAG $REGISTRY/$REGISTRY_PROJECT/k8s-network-tools:$JUPYTER_TAG
docker push $REGISTRY/$REGISTRY_PROJECT/k8s-network-tools:$JUPYTER_TAG

docker pull jupyterhub/k8s-secret-sync:$JUPYTER_TAG
docker tag jupyterhub/k8s-secret-sync:$JUPYTER_TAG $REGISTRY/$REGISTRY_PROJECT/k8s-secret-sync:$JUPYTER_TAG
docker push $REGISTRY/$REGISTRY_PROJECT/k8s-secret-sync:$JUPYTER_TAG

docker pull jupyterhub/k8s-singleuser-sample:$JUPYTER_TAG
docker tag jupyterhub/k8s-singleuser-sample:$JUPYTER_TAG $REGISTRY/$REGISTRY_PROJECT/k8s-singleuser-sample:$JUPYTER_TAG
docker push $REGISTRY/$REGISTRY_PROJECT/k8s-singleuser-sample:$JUPYTER_TAG

docker pull registry.k8s.io/pause:$PAUSE_TAG
docker tag registry.k8s.io/pause:$PAUSE_TAG $REGISTRY/$REGISTRY_PROJECT/pause:$PAUSE_TAG 
docker push $REGISTRY/$REGISTRY_PROJECT/pause:$PAUSE_TAG 

docker pull traefik:$TRAEFIK_TAG
docker tag traefik:$TRAEFIK_TAG $REGISTRY/$REGISTRY_PROJECT/traefik:$TRAEFIK_TAG
docker push $REGISTRY/$REGISTRY_PROJECT/traefik:$TRAEFIK_TAG
```


