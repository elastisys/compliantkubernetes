---
search:
  boost: 2
tags: []
---

# Improve platform stability: Job TTL

In Kubernetes, Jobs that are not managed by a higher-level resource such as a Cronjob, will most likely not get cleaned up automatically as Jobs do not have a default time-to-live, TTL, configured.
In worst case the number of finished jobs could accumulate to such a volume that it might impact the stability of the Kubernetes cluster.

However, by default in Compliant Kubernetes, Jobs that do not explicitly set a TTL (`spec.ttlSecondsAfterFinished`) automatically get a TTL of 7 days.

## Further Reading

- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/#clean-up-finished-jobs-automatically)
