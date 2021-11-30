# Reduce blast radius: Preventing forgotten roots

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.9.4.4 Use of Privileged Utility Programmes
    * A.12.6.1 Management of Technical Vulnerabilities
    * A.14.2.5 Secure System Engineering Principles

Many container runtimes and operating system vulnerabilities need code running as root to become a threat. To minimize this risk, application should only run as root when strictly necessary.

Unfortunately, many Dockerfiles -- and container base images -- today are shipped running as root by default. This makes it easy to slip code running as root into production, exposing data to unnecessary risks.

To reduce blast radius, Compliant Kubernetes will protect you from accidentally deploying application running as root.

## How to solve: CreateContainerConfigError

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

## Further Reading

* [Dockerfile USER](https://docs.docker.com/engine/reference/builder/#user)
* [SecurityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
