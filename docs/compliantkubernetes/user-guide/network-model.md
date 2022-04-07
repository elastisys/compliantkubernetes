---
description: Explanation of the network model in Elastisys Compliant Kubernetes, the security-focused kubernetes distribution.
---

Network Model
=============

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.10.1.2 Key Management
    * A.13.1.1 Network Controls
    * A.13.1.2 Security of Network Services
    * A.13.1.3 Segregation in Networks

![Compliant Kubernetes Network Model](img/network-model.drawio.svg)

The diagram above present a useful model when reasoning about networking in Compliant Kubernetes.

!!!note
    This is just a **model** and not an architectural diagram. Under the hood, things are a lot more complicated.

## Private Network

Your application Pods, as well as Pods of [additional services](/compliantkubernetes/user-guide/additional-services/), can communicate on a secure private network, via [RFC1918](https://datatracker.ietf.org/doc/html/rfc1918) private IP addresses. It is analogous to a [VPC](https://en.wikipedia.org/wiki/Virtual_private_cloud) in VM-based workloads.

In Compliant Kubernetes, it is the responsibility of the administrator to ensure the in-cluster private network is secure and trusted, either by performing an [infrastructure audit](/compliantkubernetes/operator-manual/provider-audit/) or deploying [Pod-to-Pod encryption](https://elastisys.com/redundancy-across-data-centers-with-kubernetes-wireguard-and-rook/).

You should use NetworkPolicies to segregate your Pods. This improves your security posture by reducing the blast radius in case parts of your application are under attack.

!!!example
    Feel free to take inspiration from the [user demo](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/networkpolicy.yaml).

## Private DNS

The private network also features a private DNS. A Service `my-svc` in the namespace `my-namespace` can be accessed from within the Kubernetes cluster as `my-svc.my-namespace`.

IP addresses of Pods are not stable. For example, the rollout of a new container image creates new Pods, which will have new IP addresses. Therefore, you should always use private DNS names of Services to connect your application Pods, as well as to connect your application to [additional services](/compliantkubernetes/user-guide/additional-services/).

## Ingress

Your application users should never ever access the private network directly. Instead external access is enabled by creating Ingress objects. Compliant Kubernetes already comes with cert-manager and is already configured with a ClusterIssuer. A secure ACME protocol is used to issue and rotate certificates using the [LetsEncrypt](https://letsencrypt.org/) public service.

You only need to create an Ingress object with the right `metadata.annotations` and `spec.tls`, as exemplified below:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ck8s-user-demo
  annotations:
    # To list your current ClusterIssuers, simply use 'kubectl get ClusterIssuers'.
    cert-manager.io/cluster-issuer: letsencrypt-prod
    kubernetes.io/ingress.class: nginx
    ## Uncomment the line below to implement source IP allowlisting.
    ## Blocklisted IPs will get HTTP 403.
    # nginx.ingress.kubernetes.io/whitelist-source-range: 98.128.193.2/32
spec:
  rules:
    - host: "demo.example.com"
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-ck8s-user-demo
                port:
                  number: 3000
  tls:
    - hosts:
        - "demo.example.com"
      secretName: demo.example.com-tls
```

!!!example
    Feel free to take inspiration from the [user demo](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L34).

!!!important
    The DNS name in `spec.rules[0].host` and `spec.tls[0].hosts[0]` must be the same as the DNS entry used by your application users. Otherwise, the application users will get a "Your connection is not private" error.

!!!important
    Some load-balancers fronting Compliant Kubernetes do not preserve source IP. This makes source IP allowlisting unusable.

    To check if source IP is preserved, check the HTTP request headers received by your application, specifically `x-forwarded-for` and `x-real-ip`. The [user demo](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/app.js#L24) logs all HTTP request headers, as shown in the screenshot below.

    ![HTTP request headers shown in the user demo](img/http-request-headers.png)

## Demarcation of Responsibilities

You are responsible for:

- creating Pods (via Deployments), Service and Ingress;
- segregating the private network via NetworkPolicies;
- configuring Ingresses as required to enable HTTPS encryption.

The [user demo](https://github.com/elastisys/compliantkubernetes/tree/main/user-demo/deploy/ck8s-user-demo) already showcases the above.

The Compliant Kubernetes administrator is responsible for:

- ensuring cert-manager works and is configured correctly;
- ensuring ClusterIssuers exist and are configured correctly;
- ensure the private network is secure or trusted.

## Further Reading

* [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
* [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
* [NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
