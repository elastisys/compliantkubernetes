---
tags:
- ISO 27001 A.14.2.9 System Acceptance Testing
---
# Quality Assurance

Compliant Kubernetes provides a stable and secure platform for containerized applications.
To achieve this, quality assurance is an integral part of development.
When we say "quality", we really refer to the following quality criteria.

Feature can be delivered ...

* ... at scale
    * Feature has good developer-facing documentation. The documentation includes:
        * the [happy path](https://en.wikipedia.org/wiki/Happy_path);
        * a running example based on the [user demo](https://github.com/elastisys/compliantkubernetes/tree/main/user-demo), if applicable;
        * limitations, if applicable;
        * further reading.
    * Feature is self-serviced
    * Feature is well-understood and aligned in marketing, sales, product and operations
    * Feature is clearly covered by ToS
    * Feature is implemented using a stable upstream API
    * Feature is used by at least 2 Application Developers
    * Feature generates a manageable number of service tickets, whether questions or change orders
    * Feature has well understood packaging and pricing
    * Feature can be billed easily
    * Feature integrates well with application developer observability (alerting, logging, metrics)
    * Feature integrates well with application developer authentication

* ... without ruining admin's life
    * At least 2 admins have required training
    * Feature has good admin-facing documentation (2nd day ops, all processes in place and documented, etc.)
    * Feature triggers a manageable number of P1 alerts
    * Feature triggers a manageable number of P2 alerts
    * Feature has good upstream support
    * All information security risks related to feature have been identified
    * (In case of a new supplier) Supplier collaborates directly with Elastisys admins
    * Feature is covered by QA
    * Feature is sufficiently redundant to be able to operate in degraded state upon faults
    * Feature integrates well with Ops observability (alerting, logging, metrics)

* ... without compromising our security posture
    * Feature has good and well-understood access control towards Application Developer
    * Feature does not expose platform to additional risk (needs escalated privilegies that were not analyzed, etc.)
    * Feature has good and well-understood security patching
    * Feature has good and well-understood upgrades
    * Feature has good and well-understood business continuity, i.e., high availability or self-healing
    * Feature has good and well-understood disaster recovery
    * Feature does not impair ability to upgrade underlying infrastructure and base OS
    * (In case of a new supplier) Supplier provides sufficient security for our needs
    * Feature has good and well understood way of measuring SLA fulfillment

These criteria should be taken as a direction, not a "task list".
For some features, some of these criteria won't apply.
For other features, we might accept that some of these criteria cannot be fully satisfied.
It is the role of our QA manager to decide how to apply these criteria to each feature.

## How to perform quality assurance?

When you have created your Compliant Kubernetes cluster it can be wise to run some checks to ensure that it works as expected.
This document details some snippets that you can follow in order to ensure some functionality of the cluster.

## Application Developer API and Harbor access

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
