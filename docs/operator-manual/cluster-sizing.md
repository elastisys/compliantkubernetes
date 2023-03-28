# Cluster Sizing

A full Compliant Kubernetes deployment requires a cluster with at least 40 CPUs and 82 GB of memory in total.

## Monitoring

Monitoring stack (Thanos) can handle 6000 metrics per second in our standard configuration. This can be increased on demand.

## Logging

Logging stack (OpenSearch) can take 100 records per second while provisioned with 12 CPUs and 24 GB of memory.
