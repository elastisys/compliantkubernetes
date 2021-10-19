# Safeguards

> "Det ska vara lätt att göra rätt." (English: "It should be easy to do it right.")

We know you care about the security and uptime of your application. But all that effort goes wasted if the platform allows you to make trivial mistakes.

That is why Compliant Kubernetes is built with various safeguards, to allow you to make security and reliability easy for you.

<!--
Note to contributors: Aim for the following format.

* Title: Highlight benefit to application developer
* Context
* Problem
* Solution
* Error
* Resolution
-->

## Reduce blast radius: Preventing forgotten roots

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.9.4.4 Use of Privileged Utility Programmes
    * A.12.6.1 Management of Technical Vulnerabilities
    * A.14.2.5 Secure System Engineering Principles

Many container runtimes and operating system vulnerabilities need code running as root to become a threat. To minimize this risk, application should only run as root when strictly necessary.

Unfortunately, many Dockerfiles -- and container base images -- today are shipped running as root by default. This makes it easy to slip code running as root into production, exposing personal data to unnecessary risks.

To reduce blast radius, Compliant Kubernetes will protect you from accidentally deploying application running as root.

### How to solve: CreateContainerConfigError

You may encounter the following issue:

```console
$ kubectl get pods
NAME                                   READY   STATUS                       RESTARTS   AGE
myapp-ck8s-user-demo-564f8dd85-2bs8r   0/1     CreateContainerConfigError   0          84s
myapp-ck8s-user-demo-bfbf9c459-dmk4l   0/1     CreateContainerConfigError   0          13m
$ kubectl describe pods myapp-ck8s-user-demo-564f8dd85-2bs8r
[...]
Error: container has runAsNonRoot and image has non-numeric user (node), cannot verify user is non-root (pod: "myapp-ck8s-user-demo-bfbf9c459-dmk4l_demo1(1b53b1a8-4845-4db5-aecf-6bebcc54e396)", container: ck8s-user-demo)
```

This means that your Dockerfile uses a non-numeric user and Kubernetes cannot validate whether the image truly runs as non-root.

Alternatively, you may get:

```console
$ kubectl describe pods myapp-ck8s-user-demo-564f8dd85-2bs8r
[...]
Error: container has runAsNonRoot and image will run as root (pod: "myapp-ck8s-user-demo-564f8dd85-2bs8r_demo1(a55a25f3-7b77-4fae-9f92-11e264446ecc)", container: ck8s-user-demo)
```

This means that your Dockerfile has no `USER` directive and your application would run as root.

To ensure your application does not run as root, you have two options:

1. Change the Dockerfile to `USER 1000` or whatever numeric ID corresponds to your user. This is what the [user demo does](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/Dockerfile#L10-L11).
2. Add the following snippet to the `spec` of your Pod manifest:
    ```yaml
    securityContext:
        runAsUser: 1000
    ```

If possible, prefer changing the Dockerfile, to ensure your application runs as non-root not only in production, but also during development and testing. The smaller the difference between development, testing and production, the fewer surprises down the time.

### Further Reading

* [Dockerfile USER](https://docs.docker.com/engine/reference/builder/#user)
* [SecurityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

## Reduce blast radius: NetworkPolicies

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.13.1.1 Network Controls
    * A.13.1.2 Security of Network Services
    * A.13.1.3 Segregation in Networks

!!!important
    This feature is disabled by default. Ask the Compliant Kubernetes administrator to enable it.

If you run several applications -- e.g., frontend, backend, backoffice, database, message queue -- in a single Kubernetes cluster, it is a best practice to segregrate them.
By segregating your applications and only allowing required ingress and egress network traffic, you further reduce blast radius in case of an attack.

Compliant Kubernetes allows you to segregate applications by installing suitable NetworkPolicies. These are a bit like firewalls, but in the container world: Since containers are supposed to be deleted and recreated frequently, they change IP address a lot. Clearly the old "allow/deny IP" method does not scale. Therefore, NetworkPolicies select source and destination Pods based on labels or namespace labels.

To make sure you don't forget to configure NetworkPolicies, the administrator can configure Compliant Kubernetes to deny creation of Pods with no matching NetworkPolicies.

If you get the following error:

```error
Error: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-networkpolicy] No matching networkpolicy found
```

Then you are missing NetworkPolicies which select your Pods. The [user demo](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/networkpolicy.yaml) gives a good example to get you started.

### Further Reading

* [NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

## Avoid vulnerable container images

```error
Error: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-harbor-repo] container "ck8s-user-demo" has an invalid image repo "harbor.example.com/demo/ck8s-user-demo:1.16.0", allowed repos are ["harbor.cksc.a1ck.io"]
```

TBD

## Avoid downtime with Resource Requests

```error
Error: UPGRADE FAILED: failed to create resource: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-resource-requests] Container "ck8s-user-demo" has no resource requests
```

TBD

## Relevant Regulations

* [GDPR Article 32](https://gdpr-info.eu/art-32-gdpr/):

    > Taking into account the state of the art [...] the controller and the processor shall implement [...] as appropriate [...] a process for regularly testing, assessing and evaluating the effectiveness of technical and organisational measures for ensuring the security of the processing.
    >
    > In assessing the appropriate level of security account shall be taken in particular of the risks that are presented by processing, in particular from accidental or unlawful destruction, loss, alteration, **unauthorised disclosure of, or access to personal data transmitted**, stored or otherwise processed. [highlights added]
