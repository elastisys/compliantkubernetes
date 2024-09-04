---
search:
  boost: 2
tags:
  - ISO 27001 A.12.1.2 Change Management
  - ISO 27001 A.14.2.2 System Change Control Procedures
  - ISO 27001 A.14.2.4 Restrictions on Changes to Software Packages
---

# Avoid unexpected changes: disallowed tags

!!!note

    This section helps you implement ISO 27001, specifically:

    * A.12.1.2 Change Management
    * A.14.2.2 System Change Control Procedures
    * A.14.2.4 Restrictions on Changes to Software Packages

!!!important

    This safeguard is enabled by default and will deny violations. As a result, resources that violate this policy will not be created.

Using the `:latest` tag can lead to inconsistent deployments, where it is difficult to rollback. In Compliant Kubernetes we suggest using explicit tags for your container images. This way you know that image version `v1.0.0` will be deployed if you are using the `:v1.0.0` tag.

## How to solve: [container-image-must-not-have-disallowed-tags]

You may encounter the following issue:

```console
Error from server ([container-image-must-not-have-disallowed-tags] container <example-container> uses a disallowed tag <harbor.$DOMAIN/$REGISTRY_PROJECT/example-container:latest>; disallowed tags are ["latest"])
```

This means that you are not allowed to use the `:latest` tag on your images. If no tag is specified, Kubernetes assumes `:latest`, but that does not mean that the most recent version of the image will actually be used. `:latest` is just a tag and is not dynamically updated to the most recent version of the image. It also becomes difficult to track which version of the image was used if you were to do a rollback.

To fix this, you have to start specifying tags for your images i.e. `v1.0.0`.

We recommend that you treat all tags as immutable, i.e. you don't use tags like `dev` or `prod` that you intend to continue to push tags to. Do this by always creating a new tag when you push a new image, you can include some versioning or a hash to make the tag unique. E.g. `prod-v1.2.3` or `dev-f6451806e5b6`. If you do not treat tags as immutable, then you get the same risk of having inconsistent deployments.

It is possible to add more tags that will be denied. Perhaps you want to deny images with `dev` tags in your production environment. If you want to add more tags that should be denied, then contact your administrator.

If your administrator has not enforced this policy yet, you can view current violations of the policy by running:

```bash
kubectl get k8sdisallowedtags.constraints.gatekeeper.sh container-image-must-not-have-disallowed-tags -ojson | jq .status.violations
```

## Further Reading

- [Images](https://kubernetes.io/docs/concepts/containers/images/)
