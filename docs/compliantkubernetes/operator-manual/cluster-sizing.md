# Cluster Sizing

A full Compliant Kubernetes deployment requires a cluster with at least 40 CPUs and 82 GB of memory in total.

## Monitoring

Monitoring stack (InfluxDB) can handle 2500 metrics per second while provisioned with 4 CPUs and 16 GB of memory.

## Logging

Logging stack (Elasticsearch) can take 100 records per second while provisioned with 12 CPUs and 24 GB of memory.
