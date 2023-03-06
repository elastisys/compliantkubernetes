# Release Notes


## Compliant Kubernetes PostgreSQL
<!-- BEGIN TOC -->
- [v1.8.2-ck8s1](#v182-ck8s1) - 2022-08-24
- [v1.7.1-ck8s6](#v171-ck8s6) - 2023-03-06
- [v1.7.1-ck8s2](#v171-ck8s2) - 2022-04-26
- [v1.7.1-ck8s1](#v171-ck8s1) - 2021-12-21
<!-- END TOC -->

!!!note
    These are only the user-facing changes.

### v1.8.2-ck8s1

Released 2022-08-24

Changes:

- Upgraded postgres-operator to version `v1.8.2`
- Added a service which allows users to port-forward to the service instead of directly to pods

### v1.7.1-ck8s6


Released 2023-03-06

Changes:

- Fixed so users without ck8s user admin permissions can port-forward to postgres

### v1.7.1-ck8s2

Released 2022-04-26

Changes:

- Fixed a vulnerability with logical backups

### v1.7.1-ck8s1

Released 2021-12-21

First stable release!
