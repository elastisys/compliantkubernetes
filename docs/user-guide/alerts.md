# Alerts

Compliant Kubernetes (CK8S) includes alerts via [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/).

!!!note
    This document specifically refers to **user alerts** or **application-level alerts**, i.e., alerts under the control and responsibility of the Compliant Kubernetes user.

    Alerts that are due to Compliant Kubernetes itself or the underlying infrastructure are under the control and responsibility of the Compliant Kubernetes administrator.

## Compliance needs

Many regulations require you to have an incident management process. Alerts help you discover abnormal application behavior that need attention. This maps to [ISO 27001 – Annex A.16: Information Security Incident Management](https://www.isms.online/iso-27001/annex-a-16-information-security-incident-management/).

## Enabling user alerts

User alerts are handled by a project called [AlertManager](https://prometheus.io/docs/alerting/latest/alertmanager/), which needs to be enabled by the administrator. Get in touch with the administrator and they will be happy to help.

## Configuring user alerts

User alerts are configured via the Secret `alertmanager-alertmanager` located in the `alertmanager` namespace. This configuration file is specified [here](https://prometheus.io/docs/alerting/latest/configuration/#configuration-file).

```bash
# retrieve the old configuration
kubectl get -n alertmanager secret alertmanager-alertmanager -o json | jq -r '.data["alertmanager.yaml"]' | base64 -d > alertmanager.yaml

# edit alertmanager.yaml as needed

# re-apply the new configuration
kubectl delete -n alertmanager secret alertmanager-alertmanager
kubectl create secret generic -n alertmanager alertmanager-alertmanager --from-file=alertmanager.yaml
```

!!!note
    If you get an access denied error, check with your Compliant Kubernetes administrator.

## Accessing user AlertManager

If you want to access AlertManager, for example to confirm that its configuration was picked up correctly, proceed as follows:

1. Type: `kubectl proxy`.
2. Open this link: http://127.0.0.1:8001/api/v1/namespaces/alertmanager/services/alertmanager-operated:web/proxy/

TODO:

* Document how to configure an alert.
