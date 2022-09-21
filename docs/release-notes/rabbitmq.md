# Release Notes


## Compliant Kubernetes RabbitMQ
<!-- BEGIN TOC -->
- [v3.10.7-ck8s1](#v3107-ck8s1) - 2022-09-21
- [v1.11.1-ck8s2](#v1111-ck8s2) - 2022-06-08
- [v1.11.1-ck8s1](#v1111-ck8s1) - 2022-03-11
- [v1.7.0-ck8s1](#v170-ck8s1) - 2021-12-23
<!-- END TOC -->

!!!note
    These are only the user-facing changes.

### v3.10.7-ck8s1

Released 2022-09-21

Changes:

- Changed versioning to be based on the server version rather than the operator version. The version is now `<server version>-<ck8s patch>`, e.g. v3.10.7-ck8s1.
- Improved monitoring and alerting
- Added queue details Grafana dashboard based on metrics from the prometheus plugin, made to replace the metrics exporter dashboard
- Added support for external access using load balancer or node port service
- Added issuer to generate chain of trust for TLS support
- Updated cluster operator to v1.14.0, updated server to 3.10.7
- Improved support for multi-cluster setup
- Removed metrics exporter and dashboard

### v1.11.1-ck8s2

Released 2022-06-08

Changes:

- Added a dashboard that shows metrics per queue

### v1.11.1-ck8s1

Released 2022-03-11

Changes:

- Upgraded rabbitmq-operator to version `v1.11.1`

### v1.7.0-ck8s1

Released 2021-12-23

First stable release!
