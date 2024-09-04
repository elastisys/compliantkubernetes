---
search:
  boost: 2
tags: []
---

# Avoid deploying a Load Balancer Service on unsupported cloud providers

!!!important

    This safeguard is enabled by default for some infrastructure providers and will deny violations. As a result, on those specific infrastructure providers resources that violate this policy will not be created.

Some infrastructure providers do not support `Service` of `type: LoadBalancer`, e.g. because the load-balancers don't integrate with Kubernetes.
In such cases your administrator will deploy a policy to prevent such Services from being deployed.

When attempting to apply a `Service` with `type: LoadBalancer` anyway, the following error message would be returned:

```console
Creation of LoadBalancer Service is not supported.
Contact your platform administrator for questions about Load Balancers.
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

## How to solve

Consult your platform documentation for how to handle load balancing.

- [Service type: LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer)
