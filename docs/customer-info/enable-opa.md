# Enable OPA

## Why

To ensure that your applications deployed in the Compliant Kubernetes environment are following our recommended security standards.

## What

Compliant kubernetes includes a service called Open Policy Agent (OPA). It includes a few policies to help ensure that your application will run according to operational best practices. In your cluster these are currently not enforced, but we would like to enable it. So that all of your applications must follow these policies. The following are the policies we would like to enforce for now:

1.  Require resource requests: This would require all of your pods to have resource requests for CPU and memory. This will help ensure that your Kubernetes nodes are not overused and that pods are better spread out across all nodes. This would also give you an indication when additional nodes are needed, or existing nodes need to be resized.

    For more information about resource requests look at our public docs: https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-resources/

1.  Require network policies:  This would require all of your pods to have a network policy attached. This will help ensure that your pods are protected from unexpected network communication to and from malicious actors. We do not place any restrictions on how these network policies are written, but our recommendation is to make them as restrictive as possible and only allow communication that is needed.

    For more information about network policies look at our public docs: https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-networkpolicies/

1.  Require trusted registries: This would limit your pods to only use images from a specific list of container registries that you know and trust. This will help ensure that you (or a malicious actor in case of a breach) don’t start to run unsafe images. You will get to choose what is on that list, you can include whole registries (such as our Harbor) or specific images in specific registries (e.g. nginx from dockerhub).

    For more information about limiting container registries look at our public docs: https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-trusted-registries/

1.  Disallowed tags: This would disallow specific container tags to run in your pods. This will help to ensure that you don’t run on unsafe tags or tags that might change image over time. You will get to choose what tags are on this list, you can disallow tags with a prefix using “*” (e.g “dev-*”).

    Some examples:

    The “latest” tag will often change which can result in unknown behaviors if a pod restarts and downloads a newer image version
    Tags made for development that should not be added to production clusters.

    For more information about disallowed tags look at our public docs: https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-no-latest-tag/

Once we enable all or some of these policies, if you try to start a pod that does not follow the enforced policies you will get an error stating which policy you are violating and why.

## How

To enable OPA policies please file a jira ticket with the following information:

- The environment name to enforce OPA policies on (prod, dev, ...)
- What container registries you would like added to the list of trusted registries (we would recommend just using our Harbor registry)
- Which container tags should be disallowed (we would recommend disallowing latest)
