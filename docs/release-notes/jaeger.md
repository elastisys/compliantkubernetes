# Release Notes

## Compliant Kubernetes Jaeger

<!-- BEGIN TOC -->

- [v1.52.0-ck8s1](#v1520-ck8s1) - 2024-04-26
- [v1.39.0-ck8s3](#v1390-ck8s3) - 2023-08-24
- [v1.39.0-ck8s2](#v1390-ck8s2) - 2023-06-12
- [v1.39.0-ck8s1](#v1390-ck8s1) - 2023-03-07
<!-- END TOC -->

## v1.52.0-ck8s1

Released 2024-04-26

!!! warning "Application Developer Notice(s)"

    - The Jaeger dashboard in Grafana was changed to a new upstream dashboard due to the removal of certain metrics used by the previous dashboard.

### Improvement(s)

- Upgraded Jaeger Operator to v1.52.0.
  - For a full list of changes, see the [changelog](https://github.com/jaegertracing/jaeger/blob/main/CHANGELOG.md#1520-2023-12-05).
- Upgraded Jaeger Opensearch and Opensearch Dashboards to v2.8.0
- Changed to new upstream Grafana dashboard

## v1.39.0-ck8s3

Released 2023-08-24

### Added

- Add alert for jaeger opensearch

### Changed

- Changed location for opensearch-curator image.

## v1.39.0-ck8s2

Released 2023-06-12

### Added

- Add gatekeeper PSPs

### Updated

- Updated prometheus-elasticsearch-exporter helm chart to 5.1.1

### Fixed

- Increased the proxy buffer size for the oauth ingress

### Removed

- Disabled k8s PSPs from the chart

## v1.39.0-ck8s1

Released 2023-03-07

First release using Jaeger operator version 1.39.0!
