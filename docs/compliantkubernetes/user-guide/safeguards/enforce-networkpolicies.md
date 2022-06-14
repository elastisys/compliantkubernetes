---
tags:
- ISO 27001 A.13.1.1
- ISO 27001 A.13.1.2
- ISO 27001 A.13.1.3
---
# Reduce blast radius: NetworkPolicies

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.13.1.1 Network Controls
    * A.13.1.2 Security of Network Services
    * A.13.1.3 Segregation in Networks

!!!important
    This safeguard is enabled by default since [Compliant Kubernetes apps v0.19.0](/compliantkubernetes/release-notes/#v0190).

NetworkPolicies are useful in two cases: segregating tenants hosted in the same environment and further segregating application components. Both help you achieve better data protection.

## Segregating tenants hosted in the same environment

Say you want to host a separate instance of your application for each tenant. For example, your end-users may belong to different -- potentially competing -- organizations, and you promised them to take extra care of not mixing their data. Say you want to reduce complexity by hosting all tenants inside the same environment, but without compromising data protection.

Each application instance could be installed as a separate Helm Release, perhaps even in its own Namespace. These instances should be segregated from other application instances using NetworkPolicies. This insures that network traffic from one application instance cannot reach another application instance. Besides reducing attack surface, it also prevents embarrassing mistakes, like connecting one application to the database of another.

## Further segregation of application components

If you run several applications -- e.g., frontend, backend, backoffice, database, message queue -- in a single Kubernetes cluster, it is a best practice to segregrate them.
By segregating your applications and only allowing required ingress and egress network traffic, you further reduce blast radius in case of an attack.

## Compliant Kubernetes helps enforce segregation

Compliant Kubernetes allows you to segregate applications by installing suitable NetworkPolicies. These are a bit like firewalls, but in the container world: Since containers are supposed to be deleted and recreated frequently, they change IP address a lot. Clearly the old "allow/deny IP" method does not scale. Therefore, NetworkPolicies select source and destination Pods based on labels or namespace labels.

To make sure you don't forget to configure NetworkPolicies, the administrator can configure Compliant Kubernetes to deny creation of Pods with no matching NetworkPolicies.

If you get the following error:

```error
Error: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-networkpolicy] No matching networkpolicy found
```

Then you are missing NetworkPolicies which select your Pods. The [user demo](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/networkpolicy.yaml) gives a good example to get you started.

## Further Reading

* [NetworkPolicies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
