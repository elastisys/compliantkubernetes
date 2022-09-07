---
tags:
- ISO 27001 A.12.6.1
---
<!--
Note to contributors: Aim for the following format.

* Title: Highlight benefit to application developer
* Context
* Problem
* Solution
* Error
* Resolution
-->

# Avoid vulnerable container images

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.12.6.1 Management of Technical Vulnerabilities

!!!important
    This safeguard is enabled by default since [Compliant Kubernetes apps v0.19.0](/compliantkubernetes/release-notes/#v0190).

## Problem

A healthy security posture requires you to ensure your code has no known vulnerabilities. Compliant Kubernetes comes with a [registry](/compliantkubernetes/user-guide/registry/) which includes vulnerability scanning of container images. It can even be configured to prevent the Kubernetes cluster from pulling images with vulnerabilities above a set criticality. This is a per-project setting, so you could, for example, have a stricter policy for publicly facing application components -- e.g., the front office -- and a less strict policy for internal application components -- e.g., the back office.

Public container registry, such as Docker Hub and Quay, might not stick to the vulnerability management you require, perhaps being at times too strict or too loose.

## Solution

You can designate a set of registries, a project within a registry or specific container images as trusted. By this you declared that you did a risk analysis and determined that they fulfill your security requirements.

## How Does Compliant Kubernetes Help?

Your administrator can configure Compliant Kubernetes to technically enforce a set of trusted container registries. This means that if you accidentally reference an image in an untrusted registry, you will get the following error:

```error
Error: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-harbor-repo] container "ck8s-user-demo" has an invalid image repo "harbor.example.com/demo/ck8s-user-demo:1.16.0", allowed repos are ["harbor.cksc.a1ck.io"]
```

The resolution is rather simple. You have two options:

1. Change the container image to point to a trusted registry.
2. Get in touch with your administrator and discuss augmenting the set of trusted registries.

!!!important
    Instead of adding a not-really-trusted registry to the set of trusted registries, prefer mirroring some public images in your Compliant Kubernetes registry.

## Further Reading

* [Container Images](https://kubernetes.io/docs/concepts/containers/images/)
* [Harbor Vulnerability Scanning](https://goharbor.io/docs/2.4.0/administration/vulnerability-scanning/)
