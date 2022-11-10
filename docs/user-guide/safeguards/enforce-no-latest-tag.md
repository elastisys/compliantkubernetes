---
tags:
- ISO 27001 A.12.1.2
- ISO 27001 A.14.2.2
- ISO 27001 A.14.2.4
---
# Avoid unexpected changes: disallowed tags

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.12.1.2 Change Management
    * A.14.2.2 System Change Control Procedures
    * A.14.2.4 Restrictions on Changes to Software Packages

Using the `:latest` tag can lead to inconsistent deployments, where it is difficult to rollback. In Compliant Kubernetes we suggest using explicit tags for your container images. This way you know that image version `v1.0.0` will be deployed if you are using the `:v1.0.0` tag.

## How to solve: [container-image-must-not-have-disallowed-tags]

You may encounter the following issue:

```
Error from server ([container-image-must-not-have-disallowed-tags] container <example-container> uses a disallowed tag <harbor.$DOMAIN/$REGISTRY_PROJECT/example-container:latest>; disallowed tags are ["latest"])
```

This means that you are not allowed to use the `:latest` tag on your images. If no tag is specified, Kubernetes assumes `:latest`, but that does not mean that the most recent version of the image will actually be used. `:latest` is just a tag and is not dynamically updated to the most recent version of the image. It also becomes difficult to track which version of the image was used if you were to do a rollback.

To fix this, you have the following options:

- Use a meaningful tag for your images i.e. `v1.0.0`.

If your administrator has not enforced this policy yet, you can view current violations of the policy by running
```bash
kubectl get k8sdisallowedtags.constraints.gatekeeper.sh container-image-must-not-have-disallowed-tags -ojson | jq .status.violations
```

## Further Reading

* [Images](https://kubernetes.io/docs/concepts/containers/images/)
