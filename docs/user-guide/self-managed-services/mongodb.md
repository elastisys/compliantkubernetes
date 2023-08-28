MongoDB Community Operator (self-managed)
===========

{%
   include-markdown './_common.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

{%
   include-markdown './_common-crds.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

This page will help you to install [MongoDB Community Operator](https://github.com/mongodb/mongodb-kubernetes-operator), so that you are allowed to install the cluster-wide resources that are required by MongoDB.

This guide is a complement to the [MongoDB Community Operator's](https://github.com/mongodb/mongodb-kubernetes-operator/tree/v0.8.2) own documentation.

# Preparation

The self-managed cluster-wide resources feature adds specific Roles, ServiceAccounts, etc. for you.
This enables you to install and manage the resources that the MongoDB Community Operator needs.
These pre-installed resources are propagated via HNC from your root Namespace ([recall the documentation of this feature](../namespaces.md)).

First create a new Namespace using HNC, using the snippet below.
If you do not know which root namespace you should use, ask your platform administrator.

```yaml
apiVersion: hnc.x-k8s.io/v1alpha2
kind: SubnamespaceAnchor
metadata:
  name: mongodb
  namespace: <root namespace>
```

## Install MongoDB Community Operator


Please follow the official documentation for the [MongoDB Community Operator](https://github.com/mongodb/mongodb-kubernetes-operator/blob/v0.8.2/docs/install-upgrade.md).
Be sure to read through the documentation fully.

If default configuration choices are to your liking, you should be able to install the MongoDB Community Operator as follows:

```
helm upgrade --install community-operator mongodb/community-operator --namespace mongodb
```

## Further Reading

Please refer to the official documentation how to operate and connect to MongoDB.

- [Documentation](https://www.mongodb.com/docs/)
- [Operator Documentation](https://github.com/mongodb/mongodb-kubernetes-operator/blob/v0.8.2/docs/README.md)
- [Deploy Configuration](https://github.com/mongodb/mongodb-kubernetes-operator/blob/v0.8.2/docs/deploy-configure.md)
- [Secure MongoDB Resources](https://github.com/mongodb/mongodb-kubernetes-operator/blob/v0.8.2/docs/secure.md)
