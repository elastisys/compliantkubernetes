# Release Notes

## Compliant Kubernetes RabbitMQ

<!-- BEGIN TOC -->

- [v3.12.6-ck8s1](#v3126-ck8s1) - 2024-01-17
- [v3.11.18-ck8s1](#v31118-ck8s1) - 2023-07-03
- [v3.10.7-ck8s1](#v3107-ck8s1) - 2022-09-21
- [v1.11.1-ck8s2](#v1111-ck8s2) - 2022-06-08
- [v1.11.1-ck8s1](#v1111-ck8s1) - 2022-03-11
- [v1.7.0-ck8s1](#v170-ck8s1) - 2021-12-23
<!-- END TOC -->

!!!note

    These are only the user-facing changes.

### v3.12.6-ck8s1

Released 2024-01-17

#### Updated

- Updated server to `3.12.6`
- Update release process and use new changelog generator

### v3.11.18-ck8s1

Released 2023-07-03

#### Updated

- Updated cluster operator to `v2.3.0`, updated server to `3.11.18`
- Include updated Overview dashboard

### v3.10.7-ck8s2

Released 2022-11-28

#### Fixed

- **Corrected the Queue Details Grafana dashboard and improved alerting**

### v3.10.7-ck8s1

Released 2022-09-21

!!!note

    From this release the version tracks the RabbitMQ server version rather than the RabbitMQ cluster operator version.

#### Updated

- **Upgraded RabbitMQ server version to `3.10.7`** <br/>
  This is a two minor version jump that introduces new upstream features while remaining compatible with current clients.
  The most exciting features includes the new Stream queue type tuned for bulk messaging, and much improved efficiency for Quorum and Classic queue types.
  See [the upstream changelog](https://www.rabbitmq.com/changelog.html) for more detailed information.

#### Added

- **Added support for external access** <br/>
  Using either a LoadBalancer or NodePort Service, additionally with a self-signed chain of trust to enable TLS and host verification.

#### Changed

- **Improved observability** <br/>
  Improved the alerting and replaced the per queue metrics source and dashboard, removing the need for an external exporter.

### v1.11.1-ck8s2

Released 2022-06-08

#### Changed

- **Reworked monitoring** <br/>
  Added additional metrics collection and a new dashboard to show metrics per queue, and fixed those added by the previous release.
- **Tuned performance** <br/>
  Configured and tuned the performance according to RabbitMQ upstream production checklist.
  Including better constraints to improve scheduling for redundancy.

### v1.11.1-ck8s1

Released 2022-03-11

#### Updated

- **Upgraded RabbitMQ to version `3.8.21`** <br/>
  Using Cluster operator version `1.11.1` providing bugfixes.

#### Added

- **Added definitions-exporter** <br/>
  Taking daily backups of the RabbitMQ messaging topology and users for quick and easy reconfiguring in case of disaster.

#### Changed

- Reduced RabbitMQ privilege for security.
- Improved RabbitMQ observability through better monitoring.

### v1.7.0-ck8s1

Released 2021-12-23

First stable release using RabbitMQ version `3.8.16`!
