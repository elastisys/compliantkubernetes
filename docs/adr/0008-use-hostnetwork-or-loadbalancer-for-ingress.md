# Use HostNetwork or LoadBalancer for Ingress

* Status: accepted
* Deciders: Axel, Cristian, Fredrik, Johan, Olle, Viktor
* Date: 2021-02-09

Technical Story: [Ingress configuration](https://github.com/elastisys/compliantkubernetes-kubespray/issues/25)

## Context and Problem Statement

Many regulations require traffic to be encrypted over public Internet. Compliant Kubernetes solves this problem via an [Ingress controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) and [cert-manager](https://github.com/cert-manager/cert-manager). As of February 2021, Compliant Kubernetes comes by default with [nginx-ingress](https://kubernetes.github.io/ingress-nginx/), but [Ambassador](https://www.getambassador.io/) is planned as an alternative. The question is, how does traffic arrive at the Ingress controller?

## Decision Drivers

* We want to obey the [Principle of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment).
* We want to cater to hybrid cloud deployments, including bare-metal ones, which might lack support for [Kubernetes-controlled load balancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer).
* Some deployments, e.g., Bring-Your-Own VMs, might not allow integration with the underlying load balancer.
* We want to keep things simple.

## Considered Options

* [Via the host network](https://kubernetes.github.io/ingress-nginx/deploy/baremetal/#via-the-host-network), i.e., some workers expose the Ingress controller on their port 80 and 443.
* [Over a NodePort service](https://kubernetes.github.io/ingress-nginx/deploy/baremetal/#over-a-nodeport-service), i.e., `kube-proxy` exposes the Ingress controller on a port between 30000-32767 on each worker.
* [As a Service Type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), i.e., above plus Kubernetes provisions a load balancer via [Service controller](https://kubernetes.io/docs/concepts/architecture/cloud-controller/#service-controller).

## Decision Outcome

Chosen options:

1. Use host network if Kubernetes-controlled load balancer is unavailable or undesired. If necessary, front the worker nodes with a manual or Terraform-controlled load-balancer. This includes:

    * Where load-balancing does not add value, e.g., if a deployment is planned to have only a single-node or single-worker for the foreseeable future: Point the DNS entry to the worker IP instead.
    * Exoscale currently falls in this category, due to its Kubernetes integration being rather recent.
    * SafeSpring falls in this category, since it is missing load balancers.
    * If the Infrastructure Provider is missing a storage controller, it might be undesirable to perform integration "just" for load-balancing.

2. Use Service Type LoadBalancer when available. This includes: AWS, Azure, GCP and CityCloud.

Additional considerations: This means that, generally, it will not be possible to set up the correct DNS entries until *after* we apply Compliant Kubernetes Apps. There is a risk for "the Internet" -- Let's Encrypt specifically -- to perform DNS lookups too soon and cause negative DNS caches with a long lifetime. Therefore, placeholder IP addresses must be used, e.g.:

```
*.$BASE_DOMAIN     60s A 203.0.113.123
*.ops.$BASE_DOMAIN 60s A 203.0.113.123
```

203.0.113.123 is in TEST-NET-3 and okay to use as placeholder. This approach is inspired by [kops](https://github.com/kubernetes/kops/blob/d5d08a43034dd4c7242cf1faa020cf9a8c3965e2/upup/pkg/fi/cloudup/dns.go#L41) and should not feel astonishing.

### Positive Consequences

* We make the best of each Infrastructure Provider.
* Obeys principle of least astonishment.
* We do not add a load balancer "just because".

### Negative Consequences

* Complexity is a bit increased, however, this feels like essential complexity.

## Links

* [Cloud Controller Manager](https://kubernetes.io/docs/concepts/architecture/cloud-controller/)
* [Ingress Nginx: Bare Metal Considerations](https://kubernetes.github.io/ingress-nginx/deploy/baremetal/)
