---
search:
  boost: 2
---
# Kafka® (self-managed)

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

[Apache Kafka®](https://kafka.apache.org/) is an open-source distributed event streaming platform. To run an Apache Kafka® cluster on Kubernetes you can use an operator. This guide uses the [Strimzi Kafka Operator](https://github.com/strimzi/strimzi-kafka-operator).

Strimzi is a [CNCF Sandbox project](https://www.cncf.io/projects/strimzi/).

This page will show you how to install Strimzi Kafka Operator on Welkin. You can configure the operator to watch a single or multiple namespaces.

!!! Note "Supported versions"

    This installation guide has been tested with Strimzi Kafka Operator version [0.38.0](https://github.com/strimzi/strimzi-kafka-operator/tree/0.38.0).

## Enable Self-Managed Kafka

This guide depends on the [self-managed cluster resources](../../operator-manual/user-managed-crds.md) feature to be enabled. This is so Strimzi Kafka Operator gets the necessary CRDs and ClusterRoles installed.

Strimzi Kafka Operator also requires the image repository `quay.io/strimzi` to be allowlisted. Ask your Platform Administrator to do this while enabling the self-managed cluster resources feature.

## Setup CRDs and RBAC

In Kubernetes you will need to:

1. Install the required CRDs.

1. Create a namespace for Strimzi Kafka Operator.

1. Create Roles/RoleBindings for Strimzi Kafka Operator.

1. Create ServiceAccount and ConfigMap for Strimzi Kafka Operator.

### CRDs

You need to apply the Custom Resource Definitions (CRDs) required by Strimzi Kafka Operator. This is typically not allowed in a Welkin Environment, but with Kafka enabled with the self-managed cluster resources feature, this allows you to apply these yourself.

```bash
mkdir crds

# Fetches Strimzi Kafka Operator CRDs for v0.38.0 and saves it in the crds directory
curl -L https://github.com/strimzi/strimzi-kafka-operator/releases/download/0.38.0/strimzi-crds-0.38.0.yaml > crds/kafka-crds.yaml

kubectl apply -f crds/kafka-crds.yaml
```

### Namespace

You need to create a namespace where Strimzi Kafka Operator will work. This namespace should be called `kafka`. Create this [sub-namespace](../namespaces.md) under e.g. `production`.

`kubectl hns create -n production kafka`

### Roles and RoleBindings

You need to create the necessary Roles for Strimzi Kafka Operator to function. This needs to be done in every namespace that you want Strimzi Kafka Operator to work in.

Since Welkin uses the Hierarchical Namespace Controller, the easiest way to achieve this is to place the Roles and RoleBindings in the parent namespace where `kafka` was created from. By doing so, all namespaces created under the same parent namespace will inherit the Roles and RoleBindings.

If you have multiple namespaces that ought to be targets for Strimzi Kafka Operator, you can add the Roles and RoleBindings to more than one "parent" namespace. For instance, to `staging`, to get Strimzi Kafka Operator to work with the `staging` namespace and any namespace anchored to it.

```bash
mkdir roles

# Fetches the necessary Roles and saves it in the roles directory
curl https://raw.githubusercontent.com/elastisys/welkinmain/docs/user-guide/self-managed-services/kafka-files/roles/kafka-role.yaml > roles/kafka-role.yaml
curl https://raw.githubusercontent.com/elastisys/welkinmain/docs/user-guide/self-managed-services/kafka-files/roles/kafka-rolebinding.yaml > roles/kafka-rolebinding.yaml
curl https://raw.githubusercontent.com/elastisys/welkinmain/docs/user-guide/self-managed-services/kafka-files/roles/kustomization.yaml > roles/kustomization.yaml

# If you created the namespace kafka from another namespace other than production, edit the namespace in roles/kustomization.yaml

kubectl apply -k roles
```

### ServiceAccount and ConfigMap

You need to create the ServiceAccount and ConfigMap that Strimzi Kafka Operator will use.

```bash
mkdir sa-cm

# Fetches the ServiceAccount and ConfigMap and saves it in the sa-cm directory
curl https://raw.githubusercontent.com/elastisys/welkinmain/docs/user-guide/self-managed-services/kafka-files/sa-cm/kafka-sa-cm.yaml > sa-cm/kafka-sa-cm.yaml

kubectl apply -f sa-cm/kafka-sa-cm.yaml
```

## Install Strimzi Kafka Operator

With the initial prep done, you are now ready to deploy the operator.

You can find the deployment manifest [here](https://raw.githubusercontent.com/strimzi/strimzi-kafka-operator/0.38.0/install/cluster-operator/060-Deployment-strimzi-cluster-operator.yaml). Deploying this on Welkin does require some securityContext to be added.

Edit the manifest and add this under `spec.template.spec.containers[0]`:

```yaml
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault
```

After that you can apply the manifest with `kubectl apply -f 060-Deployment-strimzi-cluster-operator.yaml -n kafka`.

Alternatively you can fetch an already edited file:

```bash
mkdir deployment

# Fetches the edited operator Deployment and saves it in the deployment directory
curl https://raw.githubusercontent.com/elastisys/welkinmain/docs/user-guide/self-managed-services/kafka-files/deployment/kafka-operator-deployment.yaml > deployment/kafka-operator-deployment.yaml

kubectl apply -f deployment/kafka-operator-deployment.yaml
```

To configure the Strimzi Kafka Operator to watch multiple namespaces (e.g. running Kafka clusters in different namespaces other than the kafka namespace), refer to [Further reading](#further-reading).

## Deploy your Kafka cluster

You are now ready to deploy your Kafka cluster!

The example files provided by Strimzi [here](https://github.com/strimzi/strimzi-kafka-operator/tree/0.38.0/examples/kafka) serves as a good starting point.

Welkin requires that resource requests are specified for all containers. By default, the Strimzi Cluster Operator does not specify CPU and memory resource requests and limits for its deployed operands.

Refer to [Further reading](#further-reading) for more information about resources.

You can fetch a modified persistent-single example that includes resource requests:

```bash
mkdir kafka-cluster

# Fetches the edited kafka cluster example and saves it in the kafka-cluster directory
curl https://raw.githubusercontent.com/elastisys/welkinmain/docs/user-guide/self-managed-services/kafka-files/kafka-cluster/persistent-single.yaml > kafka-cluster/persistent-single.yaml

kubectl apply -f kafka-cluster/persistent-single.yaml
```

!!! note "Note"

    The example above has very low resource requests. It is recommended to adjust these according to your cluster.

Refer to [Further reading](#further-reading) to learn more about how you can configure your Kafka cluster.

## Testing

After you have deployed your Kafka cluster, you can test sending and receiving messages to see if it works!

To do this, you can use a producer and consumer as seen [here](https://strimzi.io/quickstarts/), under the section "Send and receive messages". But since Welkin requires resource requests to be specified, just copy pasting those commands will not work.

You need to create a Pod manifest using the image `quay.io/strimzi/kafka:0.38.0-kafka-3.6.0`, and then you need to add your resource requests to this manifest. You also need to have an initial sleep command in the Pod manifest, to sleep the container for a while, this is to avoid the Pod going into the "Completed" stage instantly.

Alternatively you can download a ready to use producer and consumer Pod manifests:

```bash
mkdir kafka-testing

# Fetches Pod manifests for a producer and consumer and saves it in the kafka-testing directory
curl https://raw.githubusercontent.com/elastisys/welkinmain/docs/user-guide/self-managed-services/kafka-files/kafka-testing/kafka-producer.yaml > kafka-testing/kafka-producer.yaml
curl https://raw.githubusercontent.com/elastisys/welkinmain/docs/user-guide/self-managed-services/kafka-files/kafka-testing/kafka-consumer.yaml > kafka-testing/kafka-consumer.yaml

kubectl apply -f kafka-testing/kafka-producer.yaml
kubectl apply -f kafka-testing/kafka-consumer.yaml
```

After the pods have started you can send and receive messages with `kubectl exec`.

```bash
kubectl exec -it kafka-producer -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic

kubectl exec -it kafka-consumer -- bin/kafka-console-consumer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic --from-beginning
```

!!! note "Note"

    If you are running the producer and/or consumer in different namespace than where your Kafka cluster is, make sure you specify the path to the bootstrap service. E.g. "my-cluster-kafka-bootstrap.kafka.svc:9092", if the Kafka cluster is in the "kafka" namespace.

## Further reading

- [Strimzi Overview](https://strimzi.io/docs/operators/0.38.0/overview)

- [Deploying and Upgrading](https://strimzi.io/docs/operators/0.38.0/deploying)

- [API Reference](https://strimzi.io/docs/operators/0.38.0/configuring)

- [Configure Operator to watch multiple namespaces](https://strimzi.io/docs/operators/0.38.0/deploying#deploying-cluster-operator-to-watch-multiple-namespaces-str)

- [About resources for Strimzi containers](https://strimzi.io/docs/operators/0.38.0/configuring#con-common-configuration-resources-reference)

- [Configuring Kafka](https://strimzi.io/docs/operators/0.38.0/deploying#con-config-kafka-str)

- [Configuring Kafka and ZooKeeper storage](https://strimzi.io/docs/operators/0.38.0/deploying#assembly-storage-str)
