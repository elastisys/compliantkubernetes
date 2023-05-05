Keycloak (self-managed)
===========

## Initial preparation
1. Create a HNC namespace
```
kubectl apply -f - <<EOF
apiVersion: hnc.x-k8s.io/v1alpha2
kind: SubnamespaceAnchor
metadata:
  name: <descendant-namespame>
  namespace: <parent-namespace>
EOF
```
2. [Setup an application database and user in postgreSQL](https://elastisys.io/compliantkubernetes/user-guide/additional-services/postgresql)

3. 



## Configure Keycloak with managed Postgres

