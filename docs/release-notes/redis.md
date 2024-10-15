# Release Notes

## Compliant Kubernetes Redis

<!-- BEGIN TOC -->

- [v7.2.5-ck8s1](#v725-ck8s1) - 2024-10-07
- [v6.2.6-ck8s4](#v626-ck8s4) - 2024-05-03
- [v6.2.6-ck8s1](#v626-ck8s1) - 2023-05-10
- [v1.1.1-ck8s4](#v111-ck8s4) - 2022-12-09
- [v1.1.1-ck8s3](#v111-ck8s3) - 2022-10-04
- [v1.1.1-ck8s2](#v111-ck8s2) - 2022-08-23
- [v1.1.1-ck8s1](#v111-ck8s1) - 2022-03-07
- [v1.0.0-ck8s1](#v100-ck8s1) - 2021-12-23
<!-- END TOC -->

!!!note

    These are only the user-facing changes.

## v7.2.5-ck8s1

Released 2024-10-07

### Release highlights

- Redis version will be upgraded from v6.2.6 to v7.2.5

### Feature(s)

- Added netpolicy for Harbor HA

### Improvement(s)

- Split CPU usage alert by container (Redis and sentinel)
- Update Redis image to 7.2.5
    - Redis version will be upgraded from v6.2.6 to v7.2.5

### Other(s)

- Add Redis_CLUSTER_NAME to user-access-ConfigMap
- Fixed the sentinel metrics port

## v6.2.6-ck8s4

Released 2024-05-03

!!! warning "Application Developer Notice(s)"

    - From now on Network Policies will deny access to the Redis cluster by default. To gain access to the Redis clusters add this label to your pods: `elastisys.io/redis-<cluster_name>-access: allow`

### Feature(s)

- Network Policies are added to the cluster deployments which will deny access by default.

### Improvement(s)

- Added stricter Sentinel scheduling for better resilience to node failure.
- Scaled down `maxmemory` to better prevent Redis pods from getting OOMKilled.

## v6.2.6-ck8s1

Released 2023-05-10

!!!note

    From this release the version tracks the Redis version rather than the Redis operator version.

Changes:

- Changed to standard timezone in Grafana dashboard
- Upgraded the redis-operator to `v1.2.4` and Chart version to `v3.2.8`

Added:

- Added RBAC for users to be able to port-forward to Redis
- Added nodeAffinity for the label `elastisys.io/ams-cluster-name` which will be set for each cluster in `values.yaml`

## v1.1.1-ck8s4

Released 2022-12-09

Changes:

- Improved alerting and scheduling for better operational management and safety.

## v1.1.1-ck8s3

Released 2022-10-04

Changes:

- Fixed the safety of replication when master has persistence turned off

## v1.1.1-ck8s2

Released 2022-08-23

Changes:

- Improved support for running multiple Redis clusters in one Kubernetes environment.

## v1.1.1-ck8s1

Released 2022-03-07

Changes:

- Upgraded redis-operator to `v1.1.1`

## v1.0.0-ck8s1

Released 2021-12-23

First stable release!
