JupyterHub (self-managed)
===========

{%
   include-markdown './_common.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

JupyterHub brings Jupyter Notebooks to the cloud. It gives the users access to computational environments and resources without burdening users with installation and maintenance tasks. This documents shows a guide on how to setup JupyterHub in a Compliant Kubernetes cluster.

## Pushing the JupyeterHub Images to Harbor
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

## Configure and Deploy JupyterHub
We chose to work with [official Helm charts](https://hub.jupyter.org/helm-chart/) provided by JupyterHub. They can be downloaded via the webpage or added to your local repository by running:
```sh
helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
helm repo update
```

### Configuring JupyterHub



Below is a sample **values.yaml** file that can be used to deploy JupyterHub, please read the notes and change what is necessary. This sample uses [Google OAuth](https://z2jh.jupyter.org/en/stable/administrator/authentication.html#google) for authentication and authorization.
```yaml
hub:
  revisionHistoryLimit:
  config:
    GoogleOAuthenticator:
        client_id: $YOUR_CLIENT_ID # replace this
        client_secret: $YOUR_CLIENT_SECRET # replace this
        oauth_callback_url: https://$PROJECT_DOMAIN/hub/oauth_callback # replace this
        hosted_domain:
          - $PROJECT_DOMAIN # replace this
        login_service: Google
        allow_all: true
    JupyterHub:
      admin_access: true
      authenticator_class: google
      admin_users: 
        - email@admin # replace this
  image:
    name: $REGISTRY/$REGISTRY_PROJECT/k8s-hub:$TAG # replace this
  resources: &resourceDefaults # these values are reused but can be specified for each pod
    requests: 
      memory: 512Mi 
      cpu: 10m 
    limits: 
      memory: 1Gi 
      cpu: 1 
  containerSecurityContext: &SCDefaults # these values are reused to comply with ck8s safeguards
    capabilities: 
      drop: ["ALL"] 
    runAsNonRoot: true 
    seccompProfile: 
      type: "RuntimeDefault" 

proxy:
  service:
    type: ClusterIP
  chp:
    containerSecurityContext: *SCDefaults # reusing values
    image:
      name: $REGISTRY/$REGISTRY_PROJECT/conf-http:$TAG  # replace this
    resources: *resourceDefaults # reusing values
  traefik:
    containerSecurityContext: *SCDefaults
    image:
      name: $REGISTRY/$REGISTRY_PROJECT/traefik:$TAG  # replace this
    resources: *resourceDefaults
  secretSync:
    containerSecurityContext: *SCDefaults
    image:
      name: $REGISTRY/$REGISTRY_PROJECT/k8s-secret-sync:$TAG  # replace this
    resources: *resourceDefaults
  https:
    hosts:
      - $PROJECT_HOST # replace this
    type: letsencrypt
    letsencrypt:
      contactEmail: email@email.com  # replace this

singleuser:
  networkTools:
    image:
      name: $REGISTRY/$REGISTRY_PROJECT/network-tools:$TAG # replace this
    resources: *resourceDefaults
  cloudMetadata:
    blockWithIptables: false
    ip: 169.254.169.254
  storage:
    type: none
  image:
    name: $REGISTRY/$REGISTRY_PROJECT/singleuser:$TAG # replace this
  cpu:
    limit: 1
    guarantee: 0.1
  memory:
    limit: 2G
    guarantee: 1G

scheduling:
  userScheduler:
    enabled: false
    containerSecurityContext: *SCDefaults
    image:
      name: registry.k8s.io/kube-scheduler:1.0
    resources: *resourceDefaults
  userPlaceholder:
    resources: *resourceDefaults
    image:
      name: $REGISTRY/$REGISTRY_PROJECT/pause:$TAG # replace this
    containerSecurityContext: *SCDefaults

prePuller:
  resources: *resourceDefaults
  containerSecurityContext: *SCDefaults
  hook:
    image:
      name: $REGISTRY/$REGISTRY_PROJECT/k8s-image-awaiter:$TAG # replace this
    containerSecurityContext: *SCDefaults
    resources: *resourceDefaults
  pause:
    image:
      name: $REGISTRY/$REGISTRY_PROJECT/pause:$TAG # replace this
    containerSecurityContext: *SCDefaults

ingress:
  enabled: true
  annotations: 
    cert-manager.io/cluster-issuer: letsencrypt-prod
  ingressClassName: "nginx"
  hosts: 
    - $PROJECT_DOMAIN # replace this
  tls:
    - hosts:
        - $PROJECT_DOMAIN # replace this
      secretName: jupyter-secret
```

### Deploying JupyterHub

To deploy simply use this command in combination with the modified values.yaml as provided above.
```sh
helm upgrade --install jupyterhub jupyterhub/jupyterhub --values values.yml
```



## Further Reading
- [General Documentation on Setting Up JupyterHub on Kubernetes](https://z2jh.jupyter.org/en/stable/index.html)
    - [Customizing User Management](https://z2jh.jupyter.org/en/stable/administrator/authentication.html)
