---
tags:
- ISO 27001 A.12.4.3
- HIPAA S18 - Security Awareness, Training, and Tools - Log-in Monitoring - § 164.308(a)(5)(ii)(C)
- HIPAA S48 - Audit Controls - § 164.312(b)
- MSBFS 2020:7 4 kap. 16 §
---
# Audit Logs

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.12.4.3 Administrator & Operator Logs

Compliant Kubernetes comes built in with audit logs, which can be accessed via [OpenSearch Dashboard](/compliantkubernetes/user-guide/logs).
The audit logs are stored in the `kubeaudit*` index pattern.
The audit logs cover calls to the Kubernetes API, specifically **who** did **what** and **when** on **which** Kubernetes cluster.

Thanks to integration with [your Identity Provider](/compliantkubernetes/user-guide/kubernetes-api/#authentication-and-access-control-in-compliant-kubernetes) (IdP), if who is a person, their email address will be shown. If who is a system -- e.g., a CI/CD pipeline -- the name of the ServiceAccount is recorded.

Your change management or incident management process should ensure that you also cover **why**.

Both users (application developers) and administrators will show in the audit log. The former will change resources related to their application, whereas the latter will change Compliant Kubernetes system components.

![Example of Audit Logs](img/audit-logs.png)

!!!note
    It might be tempting to enable audit logging for "everything", e.g., service cluster Kubernetes API, Harbor, Grafana, Kibana, etc. Compliant Kubernetes takes a risk-reward approach and captures audit logs for the events that pose the highest risk to personal data. Don't forget that, at the end of the day, logs are only as useful as [someone looks at them](./log-review).

## SSH Access Logs

Compliant Kubernetes also captures highly privileged SSH access to the worker Nodes in the `authlog*` index pattern. Only administrators should have such access.

![Example of SSH Access Logs](img/authlog.png)

!!!note
    This section helps you implement ISO 27001, specifically:

    * A.9.2.1 User Registration and Deregistration

    Many data protection regulation will require you to [individually identify administrators](http://localhost:8000/compliantkubernetes/adr/0005-use-individual-ssh-keys/), hence individual SSH keys. This allows you to individually identify administrators in the SSH access log.

## Audit Logs for Additional Services

The Kubernetes Audit Logs capture user access to additional services, i.e., `kubectl exec` or `kubectl port-forward` commands. Additional services usually do not have audit logging enabled, since that generates a lot of log entries. Too often the extra bandwidth, storage capacity, performance loss comes with little benefit to data security.

**Prefer audit logs in your application to capture audit-worthy events**, such as login, logout, patient record access, patient record change, etc. Resist the temptation to enable audit logging too "low" in the stack. Messages like "Redis client connected" are plenty and add little value to your data protection posture.

Out of all additional services, audit logging for the [database](/compliantkubernetes/user-guide/additional-services/postgresql) makes the most sense. It can be enabled via [pgaudit](https://github.com/pgaudit/pgaudit/blob/master/README.md). Make sure you discuss your auditing requirements with the service-specific administrator, to ensure you find the best risk-reduction-to-implementation-cost trade-off. Typically, you want to discuss:

- which databases and tables are audited: e.g., audit `app.users`, but not `app.emailsSent`;
- what operations are audited: e.g., audit `INSERT/UPDATE/DELETE`, but not `SELECT`;
- by which users: e.g., audit person access, but not application access.

## Further Reading

* [Kubernetes Auditing](https://kubernetes.io/docs/tasks/debug-application-cluster/audit/)
* [pgaudit](https://www.pgaudit.org/)
