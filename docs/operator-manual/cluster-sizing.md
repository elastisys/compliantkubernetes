# Cluster Sizing

Welkin requires 26 CPUs and 72 GB of memory in addition to the capacity needed by your applications. Which for example could be 2 CPU and 8 GB of memory.

## Monitoring

Monitoring stack (Thanos) can handle 6000 metrics per second in our standard configuration. This can be increased on demand.

## Logging

Logging stack (OpenSearch) can take 100 records per second while provisioned with 12 CPUs and 24 GB of memory.
