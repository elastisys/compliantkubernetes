# CISO FAQ

## Will GrafanaLabs change to AGPL licenses affect Compliant Kubernetes?

!!!note "TL;DR"
    Users and administrators of Compliant Kubernetes are unaffected.

Part of Compliant Kubernetes -- specifically the CISO dashboards -- are built on top of Grafana, which recently [changed its license to AGPLv3](https://grafana.com/blog/2021/04/20/grafana-loki-tempo-relicensing-to-agplv3/). In brief, if Grafana is exposed via a network connection -- as is the case with Compliant Kubernetes -- then AGPLv3 requires all source code including modifications to be made available.

The exact difference between "aggregate" and "modified version" is [somewhat unclear](https://www.gnu.org/licenses/gpl-faq.en.html#MereAggregation). Compliant Kubernetes only configures Grafana and does not change its source code. Hence, we determined that Compliant Kubernetes is an "aggregate" work and is unaffected by the ["viral" clauses](https://en.wikipedia.org/wiki/Viral_license) of AGPLv3.

As a result, Compliant Kubernetes continues to be distributed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) as before.

## Will Min.io change to AGPL licenses affect Compliant Kubernetes?

!!!note "TL;DR"
    Users and administrators of Compliant Kubernetes are unaffected.

Min.io recently changed its license to [AGPLv3](https://blog.min.io/from-open-source-to-free-and-open-source-minio-is-now-fully-licensed-under-gnu-agplv3/).

Certain installations of Compliant Kubernetes may use Min.io for accessing object storage on Azure or GCP. However, Compliant Kubernetes does not currently include Min.io. In brief, if Min.io is exposed via a network connection, then AGPLv3 requires all source code including modifications to be made available.

The exact difference between "aggregate" and "modified version" is [somewhat unclear](https://www.gnu.org/licenses/gpl-faq.en.html#MereAggregation). When using Min.io with Compliant Kubernetes, we only use Min.io via its S3-compatible API. Hence, we determined that Compliant Kubernetes is an "aggregate" work and is unaffected by the ["viral" clauses](https://en.wikipedia.org/wiki/Viral_license) of AGPLv3.

As a result, Compliant Kubernetes continues to be distributed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) as before.