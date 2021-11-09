
# Quality Assurance

When you have created your Compliant Kubernetes cluster it can be wise to run some checks to ensure that it works as expected.
This document details some snippets that you can follow in order to ensure some functionality of the cluster.

## Customer API and Harbor access

### Pre-requisites
- You've got Docker installed.
- You've exported `CK8S_CONFIG_PATH` in your shell.
- You've set `baseDomain` in your shell to what's used in your cluster.
- Your current working directory is the `compliantkubernets-apps` repository.
- You've installed the `kubectl` plugin `kubelogin`.
    See [instructions](https://github.com/int128/kubelogin#setup) on how to install it.

### Create and set user kubeconfig
```shellSession
./bin/ck8s user-kubeconfig
sops -d -i --config ${CK8S_CONFIG_PATH}/.sops.yaml ${CK8S_CONFIG_PATH}/user/kubeconfig.yaml
export KUBECONFIG=${CK8S_CONFIG_PATH}/user/kubeconfig.yaml
```
Authenticate by issuing any `kubectl` command, e.g. `kubectl get pods`
Your browser will be opened and you'll be asked to login through Dex.

### Login to Harbor GUI and create 'test' project
- Go to `https://harbor.${baseDomain}`, and login though OIDC.
- Create project 'test'.
- Click on your user in the top right corner and select User profile.
- Copy CLI secret.

### Push image to Harbor and scan it
- Pull Nginx from dockerhub `docker pull nginx`.
- Login to the Harbor registry `docker login https://harbor.${baseDomain}`
    Enter your Harbor username and the copied CLI secret.
- Prepare Nginx image for pushing to Harbor registry `docker tag nginx harbor.${baseDomain}/test/nginx`
- Push image to Harbor `docker push harbor.${baseDomain}/test/nginx`
- Enter 'test' project in the Harbor GUI, select the newly pushed image and scan it.

### Create secret for pulling images from harbor
```shellSession
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=${HOME}/.docker/config.json \
    --type=kubernetes.io/dockerconfigjson

kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "regcred"}]}'
```

### Test pulling from Harbor and start privileged and unprivileged pods
```shellSession
kubectl run --image nginxinc/nginx-unprivileged nginx-unprivileged
kubectl run --image harbor.${baseDomain}/test/nginx nginx-privileged

# You should see that both pods and that nginx-unprivileged eventually becomes running while nginx-privileged does not.
kubectl get pods

# Check events from the nginx-privileged.
kubectl describe pod nginx-privileged
# You should see 'Error: container has runAsNonRoot and image will run as root'.
```

### Cleanup of created Kubernetes resources
```shellSession
kubectl delete pod --all
kubectl delete secret regcred
```
