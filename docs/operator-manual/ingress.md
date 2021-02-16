# Ingress

Compliant Kubernetes (CK8S) uses the Nginx Ingress controller to route external traffic to the correct Service inside the cluster. CK8S can configure the Ingress controller in two different ways depending on the underlying infrastructure. 

## Using a Service of type LoadBalancer

When using a cloud provider with a Kubernetes cloud integration such as AWS, Azure and Google cloud the Ingress 
controller can be exposed with a Service of type LoadBalancer. This will create an external load balancer in the cloud
provider with an external ip-address. Any dns records should be pointed to the ip-address of the load balancer.

!!!note 
    This is only currently supported in CK8S for AWS. It is however possible to configure this for Azure and Google cloud as well
    but it's not done by default

## Using the host network

For any cloud provider (or bare metal) not supporting these kind of public load balancers the Ingress controller
uses the host network instead. This is done by configuring the Ingress controller as a DaemonSet so one Pod
is created on each node. The Pods are configured to use the host network, so all traffic received on the node
on port 80 and 443 will be intercepted by the Ingress controller Pod and then routed to the desired Service.

On some clouds providers there is load balancing available for the worker nodes. For example Exoscale uses an "elastic ip"
which provides one external ip which load balances to the available worker nodes. For these cloud providers this external ip
of the load balancers should be used as the entry point in the dns.

For the cloud providers where this is not available the easiest option is to just point the dns to the ip of any, or all, of
the worker nodes. This is of course not a optimal solution because it adds a single point of failure on the worker node which
is selected by the dns. Another option is to use any existing load balancer service if this is available.

## Installation

The Nginx ingress is currently configured and installed by the 
[compliantkubernetes-apps](https://github.com/elastisys/compliantkubernetes-apps) repository.
The configuration is set in 
[sc-config.yaml](https://github.com/elastisys/compliantkubernetes-apps/blob/main/config/config/sc-config.yaml#L526-L530) 
and [wc-config.yaml](https://github.com/elastisys/compliantkubernetes-apps/blob/main/config/config/wc-config.yaml#L322-L334) under:
```yaml
ingressNginx:
  useHostPort: ""
  service:
    enabled: ""
    type: ""
```
If the apps repository is initiated with the correct cloud provider these config options will get the
correct defaults.

For more ways to install the Nginx Ingress controller see <https://kubernetes.github.io/ingress-nginx/deploy>

## Ingress resource

The Ingress resource is used to later route traffic to the desired Service. For more information about this
see the official [documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/).