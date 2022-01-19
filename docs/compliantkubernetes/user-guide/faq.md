Frequently Asked Questions (FAQ)
================================

## How do I give access to a new application developer to a Compliant Kubernetes environment?

Add the new user to the correct **group via your Identity Provider (IdP)**, and Compliant Kubernetes will automatically pick it up.

Feeling lost? To find out what users and groups currently have access to your Compliant Kubernetes environment, type:

```bash
kubectl get rolebindings.rbac.authorization.k8s.io workload-admin -o yaml
# look at the 'subjects' field
```

If you are not using groups, contact your administrator.

## How do I add a new namespace?

Unfortunately, it is currently not possible to make adding/changing/removing namespaces self-serviced without compromising the security of the platform. While [several promising approaches](https://kubernetes.io/blog/2020/08/14/introducing-hierarchical-namespaces/) exist, they have yet to reach the maturity we require for Compliant Kubernetes.

Therefore, for the time being, please ask your administrator for creating a new namespace.

## What is encrypted at rest?

Compliant Kubernetes encrypts everything at rest, including Kubernetes resources, PersistentVolumeClaims, logs, metrics and backups, **if the underlying cloud provider supports it**.

Get in touch with your administrator to check the status. They are responsible for performing a [provider audit](/compliantkubernetes/operator-manual/provider-audit).

