# ISO 27001 and BSI IT-Grundschutz Controls

Click on the links below to navigate the documentation by ISO 27001 control:

[TAGS]

## Other IT-Grundschutz Controls

### APP.4.4.A17 Attestierung von Nodes (H)

The Kubespray layer in Compliant Kubernetes ensures that Data Plane Nodes and Control Plane Nodes are mutually authenticated via mutual TLS.

## BSI IT-Grundschutz Controls outside the scope of Compliant Kubernetes

Pending official translation into English, the controls are written in German.

### APP.4.4.A1 Planung der Separierung der Anwendungen (B)

Compliant Kubernetes recommends to setting up at least two separate environment: one for testing and one for production.

### APP.4.4.A6 Initialisierung von Pods (S)

Application developers must make sure that initialization happens in [init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/).

### APP.4.4.A11 Überwachung der Container (S)

Application developers must ensure that their application has a liveliness and readiness probe, which are configured in the Deployment. This is illustrated by our [user demo](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/deployment.yaml).

### APP.4.4.A12 Absicherung der Infrastruktur-Anwendungen (S)

This requirement essentially states that the Compliant Kubernetes environments are only as secure as the infrastructure around them. Make sure you have a proper IT policy in place. Regularly review the systems where you store backups and configuration of Compliant Kubernetes.

### APP.4.4.A13 Automatisierte Auditierung der Konfiguration (H)

Compliant Kubernetes administrators must regularly audit the configuration of their environments. We recommend doing this on a quarterly basis.

### APP.4.4.A20 Verschlüsselte Datenhaltung bei Pods (H)

Compliant Kubernetes recommends disk encryption to be provided at the infrastructure level. If you have this requirement, check for full-disk encryption via the [provider audit](../../operator-manual/provider-manual).
