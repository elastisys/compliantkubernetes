---
search:
  boost: 2
tags: []
---

# Avoid Downtime with Replicas

Compliant Kubernetes by default recommends a minimum of 2 replicas for Deployments and StatefulSets.

Therefore a warning will be issued when you add or update a Deployment or StatefulSet where the number of replicas is less than 2.

```console
[elastisys-warn-minimum-replicas] The provided number of replicas is low for Deployment: demo-ck8s-user-demo. Elastisys Compliant Kubernetes recommends a minimum of 2 replicas.
```

You can either resolve this by setting the number of replicas to a minimum of 2.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-demo
spec:
  replicas: 2
```

Or, in the case where the Deployment or StatefulSet is not of high priority or there are technical limitations preventing you from using more than one replica, you can suppress the warning by adding an annotation.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-demo
  annotations:
    elastisys.io/ignore-minimum-replicas: "yes" # The value part can be anything.
spec:
  replicas: 1
```
