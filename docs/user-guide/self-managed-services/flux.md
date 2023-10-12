Flux™ (self-managed)
===========

{%
 include-markdown './_common.include'
 start='<!--disclaimer-start-->'
 end='<!--disclaimer-end-->'
%}

{%
 include-markdown './_common-crds.include'
 start='<!--disclaimer-start-->'
 end='<!--disclaimer-end-->'
%}

Flux is an open-source tool for continuous delivery (CD) and GitOps in Kubernetes. It allows you to automate and manage the deployment of applications and configurations in a Kubernetes cluster using a Git repository as the source of truth.

Flux is a [CNCF Graduated project](https://www.cncf.io/projects/flux/).

This page will help you install Flux in a Compliant Kubernetes environment.

# Initial Prep

### Dependencies

This guide depends on the [self-managed cluster resources](../../operator-manual/user-managed-crds.md) feature to be enabled. This is so Flux gets the necessary CRDs and ClusterRoles installed.

Flux also requires the image repository `ghcr.io/fluxcd` to be whitelisted. Ask your platform administrator to do this while enabling the self-managed cluster resources feature.

### Git

You need to setup a git repository that will contain the manifest files. This can be a personal or organization repository. *It is recommended that it is a private repository.*

Next you need to generate an SSH key that will be used to communicate with the git repository. The private key will be used as a Kubernetes secret in a later step.
```
ssh-keygen -t rsa -C "flux-deploymentkey" -f <path-to-store-key>
```
After you have generated an SSH Key, you want to add it as a deploy key in your git repository. This can be done through `Settings` -> `Deploy keys`. Copy your public key that you just generated and paste here.

### Kubernetes

In Kubernetes you will need to:

1. Install CRDs

2. Create a namespace for Flux

3. Create a git secret in the namespace

4. Create roles/rolebindings for Flux.

##### CRDs

You need to apply the Custom Resource Definitions (CRDs) required by Flux. This is typically not allowed in a Compliant Kubernetes Environment, but with Flux enabled with the self-managed cluster resources feature, this allows you to apply these yourself.

```
mkdir crds

# Fetches latest Flux CRDs and saves it in the crds directory
curl https://raw.githubusercontent.com/fluxcd/flux2/main/manifests/crds/kustomization.yaml > crds/kustomization.yaml

kubectl apply -k crds
```

##### Namespace

You need create a namespace where Flux will work. This namespace should be called `flux-system`. Create this [sub-namespace](../namespaces.md) under eg. `production`.

`kubectl hns create -n production flux-system`

##### Git Secret

Next to allow Flux to interact with your Git Repository you need to create a secret containing the ssh private key created earlier. This can be done with the Flux CLI:
```
flux create secret git <repo-name>-auth \
    --url=ssh://git@github.com/<owner>/<repo-name>.git \
    --private-key-file=<path-to-ssh-private-key>
```

##### Roles and Rolebindings

You will need to create the necessary roles for Flux to function. This needs to be done in every namespace that you want Flux to work in. Or alternatively, in the parent namespace where `flux-system` was created from. This way all namespaces created under the same parent namespace will inherit the roles and rolebindings. You can add these roles to another parent namespace, eg. `staging`, to get Flux to work with the `staging` namespace and any namespace anchored to it.

```
mkdir roles

# Fetches the necessary roles and saves it in the roles directory
curl https://raw.githubusercontent.com/elastisys/compliantkubernetes/main/docs/user-guide/self-managed-services/flux-files/all-controllers-role.yaml > roles/all-controllers-role.yaml
curl https://raw.githubusercontent.com/elastisys/compliantkubernetes/main/docs/user-guide/self-managed-services/flux-files/source-controller-role.yaml > roles/source-controller-role.yaml

# Edit the namespace of the roles/rolebindings

kubectl apply -f roles
```

The kustomize and helm controller needs some extra permissions as well since it wants to deploy. The simplest is to add these controller serviceaccounts to the `extra-workload-admins` rolebinding in the parent namespace eg. `production`. This will grant Flux the maximum permission an application developer can give in the namespaces where it is configured. Edit the rolebinding and add the lines below.

```
kubectl edit rolebindings extra-workload-admins -n production

...
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
# Add these lines below
subjects:
- kind: ServiceAccount
  name: kustomize-controller
  namespace: flux-system
- kind: ServiceAccount
  name: helm-controller
  namespace: flux-system
```

# Setup

### Generate Manifests

*Note: Installing Flux with `flux bootstrap` command does not work when installing in a Compliant Kubernetes environment, please follow our instructions instead.*

The script below can be used to generate Flux manifests and a basic cluster folder structure similar to `flux bootstrap`. Be sure to configure the environment variables in the script.

```
# Generate Manifest files

# Be sure to edit the variables below!
CLUSTER_NAME="<cluster-name>"
REPO_NAME="<repo-name>"
URL="github.com/<owner>/<repo-name>"

mkdir -p clusters/$CLUSTER_NAME/flux-system
touch clusters/$CLUSTER_NAME/flux-system/gotk-components.yaml \
    clusters/$CLUSTER_NAME/flux-system/gotk-sync.yaml \
    clusters/$CLUSTER_NAME/flux-system/kustomization.yaml

# Generate flux manifests
flux install --export > clusters/$CLUSTER_NAME/flux-system/gotk-components.yaml

# Create repo manifest
flux create source git $REPO_NAME-repo \
    --url=ssh://git@"$URL" \
    --branch=main \
    --secret-ref=$REPO_NAME-auth \
    --export > clusters/$CLUSTER_NAME/flux-system/gotk-sync.yaml

# Create Kustomization manifest for Flux
flux create kustomization $REPO_NAME-repo \
    --namespace=flux-system \
    --source=GitRepository/$REPO_NAME-repo.flux-system \
    --path="./clusters/$CLUSTER_NAME/flux-system" \
    --prune=true \
    --interval=1m \
    --export >> clusters/$CLUSTER_NAME/flux-system/gotk-sync.yaml

# Fetches our patches and saves them in the clusters/$CLUSTER_NAME/flux-system directory
curl https://raw.githubusercontent.com/elastisys/compliantkubernetes/main/docs/user-guide/self-managed-services/flux-files/kustomization.yaml > clusters/$CLUSTER_NAME/flux-system/kustomization.yaml
```

Commit and push the files to the repository.

*Warning: If you created your SSH keys in the repository folder, make sure you do not push these to the repository.*

### Install

Simply install by applying the kustomization.

`kubectl apply -k clusters/$CLUSTER_NAME/flux-system`

# Further reading

[Flux core concepts](https://fluxcd.io/flux/concepts/)

[Flux multi-tenancy](https://fluxcd.io/flux/installation/configuration/multitenancy/)

[Controller options](https://fluxcd.io/flux/installation/configuration/boostrap-customization/)

[Flux components](https://fluxcd.io/flux/components/)

# Known Issues

#### Role and Rolebindings does not apply correctly

Error produced: `Error from server (NotFound): error when creating "roles/": roles.rbac.authorization.k8s.io "role" not found`

There is a [known issue](https://github.com/fluxcd/flux2/discussions/3203) with Role and Rolebindings not being able to be applied together using Flux in a GitOps way. For example, if you apply a role and a rolebinding that uses the role, then Flux will fail to apply. If the role already exists in the cluster then Flux will succeed.

Flux uses the [server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/), which requires the ‘bind’ permission to properly apply Rolebindings. And we cannot give you this due to [privilege escalation issues](https://kubernetes.io/docs/concepts/security/rbac-good-practices/#bind-verb) with this permission.

You can workaround this using the Flux Kustomization [dependsOn](https://fluxcd.io/flux/components/kustomize/kustomizations/#dependencies) functionality. By splitting the Roles and Rolebindings into separate folders and then creating two Kustomizations for them where the Rolebindings will depend on the Roles. Then the roles will be applied before the rolebindings and so the issue will not occur. Refer to the previous link for an example.

# Notes

We do not use the [multi-tenancy model](https://fluxcd.io/flux/installation/configuration/multitenancy/) described in Flux documentation since this is a self-managed service and we do not want Flux to be able to do privilege escalation using [impersonation](https://kubernetes.io/docs/concepts/security/rbac-good-practices/#impersonate-verb). But you can still configure the flags to, for example deny cross namespace references.
