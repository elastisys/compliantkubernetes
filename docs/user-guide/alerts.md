# Alerts

Compliant Kubernetes (CK8S) includes alerts via [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/).

!!!note
    This document specifically refers to user alerts or **application-level alerts**, i.e., alerts under the control and responsibility of the Compliant Kubernetes user.
    
    Alerts that are due to the Compliant Kubernetes itself or the underlying infrastructure are under the control and responsibility of the Compliant Kubernetes administrator.

## Compliance needs

Many regulations require you to have an incident management process. Alerts help you discover abnormal application behavior that need attention. This maps to [ISO 27001 – Annex A.16: Information Security Incident Management](https://www.isms.online/iso-27001/annex-a-16-information-security-incident-management/).

TODO:

* Document that user alertmanager needs to be enabled.
* Document that user alertmanager needs to be configured.
* Document how to access user alertmanager.
* Document how to configure an alert.
