# Release Notes

## Welkin PostgreSQL

<!-- BEGIN TOC -->

- [v1.12.2-ck8s1](#v1122-ck8s1) - 2024-09-25
- [v1.8.2-ck8s1](#v182-ck8s1) - 2022-08-24
- [v1.7.1-ck8s2](#v171-ck8s2) - 2022-04-26
- [v1.7.1-ck8s1](#v171-ck8s1) - 2021-12-21
<!-- END TOC -->

!!!note

    These are only the user-facing changes.

!!!note

    The public changelog has not been kept up-to-date with development and new releases.
    Expect the naming schema to change and the content of new releases to be more full and descriptive.

### v1.12.2-ck8s1

Released 2024-09-25

Default PostgreSQL versions:

- 16.4
- 15.8
- 14.13
- 13.16

Changes:

- TimescaleDB version bumped to `2.14.2`
- pgvector version bumped to `0.7.4`

### v1.8.2-ck8s1

Released 2022-08-24

Changes:

- Upgraded postgres-operator to version `v1.8.2`
- Added a service which allows users to port-forward to the service instead of directly to pods

### v1.7.1-ck8s2

Released 2022-04-26

Changes:

- Fixed a vulnerability with logical backups

### v1.7.1-ck8s1

Released 2021-12-21

First stable release!
