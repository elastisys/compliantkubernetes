# Prepare Your Application

<!--user-demo-overview-start-->
To make the most out of Compliant Kubernetes, prepare your application so it features:

- [some REST endpoints](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/app.js#L32) (`/`, `/users`);
- [structured logging](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/app.js#L13);
- [metrics endpoint](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/app.js#L28);
- [Dockerfile](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/Dockerfile), which showcases:
    - [How to run as non-root](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/Dockerfile#L10-L13);
- [Helm Chart](https://github.com/elastisys/compliantkubernetes/tree/main/user-demo/deploy/ck8s-user-demo), which showcases:
    - [HTTPS Ingresses](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L37-L40);
    - [ServiceMonitor for metrics collection](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/servicemonitor.yaml);
    - [PrometheusRule for alerting](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/templates/prometheusrule.yaml);
    - [topologySpreadConstraints for tolerating single Node or single Zone failure](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L76-L82);
    - [resources for capacity management](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L42-L51);
    - [NetworkPolicies for network segmentation](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L83-L94);
- [Grafana dashboards for metrics visualization](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/dashboards);
- [script for local development and testing](https://github.com/elastisys/compliantkubernetes/tree/main/user-demo/scripts);

Bonus:

- [ability to make it crash](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/routes/crash.js) (`/crash`).

Feel free to clone our user demo for inspiration:

```bash
git clone https://github.com/elastisys/compliantkubernetes/
cd compliantkubernetes/user-demo
```
<!--user-demo-overview-end-->
