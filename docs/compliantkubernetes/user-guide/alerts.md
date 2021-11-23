# Alerts

Compliant Kubernetes (CK8S) includes alerts via [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/).

!!!important
    By default, you will get some platform alerts, specifically those originating from the workload cluster. This may benefit you, by giving you improved "situational awareness". Please decide if these alerts are of interest to you or not. Feel free to silence them, as the Compliant Kubernetes administrator will take responsibility for them.

    Your focus should be on **user alerts** or **application-level alerts**, i.e., alerts under the control and responsibility of the Compliant Kubernetes user. We will focus on user alerts in this document.

## Compliance needs

Many regulations require you to have an incident management process. Alerts help you discover abnormal application behavior that need attention. This maps to [ISO 27001 – Annex A.16: Information Security Incident Management](https://www.isms.online/iso-27001/annex-a-16-information-security-incident-management/).

## Enabling user alerts

User alerts are handled by a project called [AlertManager](https://prometheus.io/docs/alerting/latest/alertmanager/), which needs to be enabled by the administrator. Get in touch with the administrator and they will be happy to help.

## Configuring user alerts

User alerts are configured via the Secret `alertmanager-alertmanager` located in the `alertmanager` namespace. This configuration file is specified [here](https://prometheus.io/docs/alerting/latest/configuration/#configuration-file).

```bash
# retrieve the old configuration
kubectl get -n alertmanager secret alertmanager-alertmanager -o jsonpath='{.data.alertmanager\.yaml}' | base64 -d > alertmanager.yaml

# edit alertmanager.yaml as needed

# re-apply the new configuration
kubectl delete -n alertmanager secret alertmanager-alertmanager
kubectl create secret generic -n alertmanager alertmanager-alertmanager --from-file=alertmanager.yaml
```

Make sure to configure **and test** a receiver for you alerts, e.g., Slack or OpsGenie.

!!!note
    If you get an access denied error, check with your Compliant Kubernetes administrator.

## Accessing user AlertManager

If you want to access AlertManager, for example to confirm that its configuration was picked up correctly, proceed as follows:

1. Type: `kubectl proxy`.
2. Open [this link](http://127.0.0.1:8001/api/v1/namespaces/alertmanager/services/alertmanager-operated:web/proxy/) in your browser.

## Setting up an alert

Before setting up an alert, you must create a [ServiceMonitor](metrics) to collect metrics from your application. Then, create a `PrometheusRule` following the example below:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  creationTimestamp: null
  labels:
    prometheus: example
    role: alert-rules
  name: prometheus-example-rules
spec:
  groups:
  - name: ./example.rules
    rules:
    - alert: ExampleAlert
      expr: vector(1)
```

## Running Example

<!--user-demo-alerts-start-->

The user demo already includes a [PrometheusRule](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/prometheusrule.yaml), to configure an alert:

```yaml
--8<---- "user-demo/deploy/ck8s-user-demo/templates/prometheusrule.yaml"
```

The screenshot below gives an example of the application alert, as seen in AlertManager.

![Example of User Demo Alerts](/compliantkubernetes/img/user-demo-alerts.png)

<!--user-demo-alerts-end-->
