# BSI IT-Grundschutz Controls

Click on the links below to navigate the documentation by control.

[TAGS]

## Other IT-Grundschutz Controls

### APP.4.4.A17 Attestierung von Nodes (H)

The Kubespray layer in Welkin ensures that Data Plane Nodes and Control Plane Nodes are mutually authenticated via mutual TLS.

## BSI IT-Grundschutz Controls outside the scope of Welkin

Pending official translation into English, the controls are written in German.

### APP.4.4.A6 Initialisierung von Pods (S)

Application Developers must make sure that initialization happens in [init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/).

### APP.4.4.A11 Überwachung der Container (S)

Application Developers must ensure that their application has a liveliness and readiness probe, which are configured in the Deployment. This is illustrated by our [user demo](https://github.com/elastisys/welkin/blob/main/user-demo/deploy/welkin-user-demo/templates/deployment.yaml).

### APP.4.4.A12 Absicherung der Infrastruktur-Anwendungen (S)

This requirement essentially states that the Welkin environments are only as secure as the infrastructure around them. Make sure you have a proper IT policy in place. Regularly review the systems where you store backups and configuration of Welkin.

### APP.4.4.A20 Verschlüsselte Datenhaltung bei Pods (H)

Welkin recommends disk encryption to be provided at the infrastructure level. If you have this requirement, check for full-disk encryption via the [provider audit](../../operator-manual/provider-audit.md).
