RabbitMQ®
=========

![RabbitMQ Deployment Model](img/rabbitmq.drawio.svg)

This page will help you succeed in connecting your application to a RabbitMQ-based message queue which meets your security and compliance requirements.

## Provision a New RabbitMQ Cluster

Ask your service-specific administrator to install a RabbitMQ cluster inside your Compliant Kubernetes environment. The service-specific administrator will ensure the RabbitMQ cluster complies with your security requirements, including:

* **Business continuity**: We recommend a highly available setup with three instances.
* **Disaster recovery**: Note that, because messages are often short-lived and possibly transient, backing them up from under a running node is highly discouraged and can lead to an inconsistent snapshot of the data. Generally, disaster recovery for message queue only makes sense for the [dead letter exchange](https://www.rabbitmq.com/dlx.html).
* **Capacity management**: Your service-specific administrator will ensure RabbitMQ runs on dedicated (i.e., tainted) Kubernetes Nodes, as required to get the best performance.
* **Incident management**: Your administrator will set up the necessary Probes, dashboards and alerts, to discover issues and resolve them, before they become a problem.
* **Access control**: To comply with access minimization policies, your service-specific administrator cannot hand you the RabbitMQ administrator username and password. Instead, ask you administrator to declare exchanges, queues, bindings, users, virtual hosts and user permissions, as required.

Compliant Kubernetes recommends the [RabbitMQ Cluster Operator for Kubernetes](https://www.rabbitmq.com/kubernetes/operator/operator-overview.html).

## Install Prerequisites

Before continuing, make sure you have access to the Kubernetes API, as describe [here](/compliantkubernetes/user-guide/setup/).

Make sure to install the RabbitMQ client on your workstation. On Ubuntu, this can be achieved as follows:

```bash
sudo apt install rabbitmq-server
```

## Getting Access

Your administrator will set up a Secret inside Compliant Kubernetes, which contains all information you need to access your RabbitMQ cluster.
The Secret has the following shape:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: $SECRET
  namespace: $NAMESPACE
stringData:
  # AMPQ_URL represents a cluster-scoped AMQP URL, which makes sense inside the Kubernetes cluster.
  # E.g., amqp://user:password@rabbit1.rabbitmq-system:5672/vhost
  AMQP_URL: $AMQP_URL
```

!!!important
    The Secret is very precious! Prefer not to persist any information extracted from it, as shown below.

To extract this information, proceed as follows:

```bash
export SECRET=            # Get this from your administrator
export NAMESPACE=         # Get this from your administrator

export AMQP_URL=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.AMQP_URL}' | base64 -d)
```

## Create a Secret

First, check that you are on the right Compliant Kubernetes cluster, in the right **application** namespace:

```bash
kubectl get nodes
kubectl config view --minify --output 'jsonpath={..namespace}'; echo
```

Now, create a Kubernetes Secret in your application namespace to store the AMPQ URL:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
    name: app-amqp-secret
type: Opaque
stringData:
    AMQP_URL: $AMQP_URL
EOF
```

## Expose AMQP URL to Your Application

To expose the AMQP URL to your application, follow one of the following upstream documentation:

* [Create a Pod that has access to the secret data through a Volume](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#create-a-pod-that-has-access-to-the-secret-data-through-a-volume)
* [Define container environment variables using Secret data](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#define-container-environment-variables-using-secret-data)

## Follow the Go-Live Checklist

You should be all set.
Before going into production, don't forget to go through the [go-live checklist](../go-live.md).

## Further Reading

* [AMQP URL spec](https://www.rabbitmq.com/uri-spec.html)
* [AMQP Clients](https://www.rabbitmq.com/clients.html)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
