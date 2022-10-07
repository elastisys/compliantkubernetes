---
tags:
- ISO 27001 A.18.1.2
---
# CISO FAQ

## Do we need to make our application source code public when using Compliant Kubernetes?

!!!note "TL;DR"
    **Definitely NOT**, you own your application source code and you decide what to do with it.

We hereby confirm that Compliant Kubernetes and its Additional Managed Services (AMS) are NOT putting application developers (users) in a situation which obliges them to make their software or source code running on Compliant Kubernetes available to the public.

Should we at Elastisys become aware of such an issue existing, we will immediately rectify the situation by replacing problematic components. You can read more about how we take architectural decisions [here](../../adr).

As evidence, that the architectural decision process works – in particular when it comes to licensing issues – here are some decisions we took:

* We decided only to offer TimescaleDB Apache 2 Edition (licensed under Apache 2.0) and NOT TimescaleDB “Community Edition” (licensed under the Timescale license). The Timescale license contains some problematic clauses and is, to our knowledge, not tested in court. You can read more about the subtle differences between the TimescaleDB versions [by opening this link](https://docs.timescale.com/timescaledb/latest/timescaledb-edition-comparison/).
* We replaced Elasticsearch with OpenSearch (licensed under Apache 2.0), when Elasticsearch changed to the Elastic license. You can read more about the context [by opening this link](https://opensearch.org/faq/).
* We replaced InfluxDB with Thanos. This was due to the fact that the open-source version was too limiting. You can read more about this decision [by opening this link](../../adr/0019-push-metrics-via-thanos/).
* We made a risk assessment regarding Grafana, and determined that its AGPL license does not pose a problem. You can read more about our assessment below.

You can read more about our commitment to community-driven open-source [by opening this link](../../adr/0015-we-believe-in-community-driven-open-source/).

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
