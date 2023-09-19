---
tags:
- ISO 27001 A.18.1.2 Intellectual Property Rights
---
# CISO FAQ

## Do we need to make our application source code public when using Compliant Kubernetes?

!!!note "TL;DR"
    **Definitely NOT**, you own your application source code and you decide what to do with it.

Elastisys hereby confirms that Compliant Kubernetes and its Additional Managed Services (AMS) are NOT putting Application Developers (users) in a situation which obliges them to make their software or source code running on Compliant Kubernetes available to the public.

Should we at Elastisys become aware of such an issue existing, we will immediately rectify the situation by replacing problematic components. You can read more about how we take architectural decisions [here](../adr/index.md).

As evidence, that the architectural decision process works – in particular when it comes to licensing issues – here are some decisions we took:

* We decided only to offer TimescaleDB Apache 2 Edition (licensed under Apache 2.0) and NOT TimescaleDB “Community Edition” (licensed under the Timescale license). The Timescale license contains some problematic clauses and is, to our knowledge, not tested in court. You can read more about the subtle differences between the TimescaleDB versions [by opening this link](https://docs.timescale.com/timescaledb/latest/timescaledb-edition-comparison/).
* We replaced Elasticsearch with OpenSearch (licensed under Apache 2.0), when Elasticsearch changed to the Elastic license. You can read more about the context [by opening this link](https://opensearch.org/faq/).
* We replaced InfluxDB with Thanos. This was due to the fact that the open-source version was too limiting. You can read more about this decision [by opening this link](../adr/0019-push-metrics-via-thanos.md).
* We made a risk assessment regarding Grafana, and determined that its AGPL license does not pose a problem. You can read more about our assessment below.

You can read more about our commitment to community-driven open-source [by opening this link](../adr/0015-we-believe-in-community-driven-open-source.md).

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

## Can I use Datadog/Logz.io/Elastic Cloud with Compliant Kubernetes?

!!!note "TL;DR"
    Technically, yes, but legally speaking and from a GDPR perspective, **NO**. Why is that?

    * Logs contain personal data.
    * Personal data should NOT be shipped to US cloud providers.

    Use Compliant Kubernetes's [built-in OpenSearch](../user-guide/logs.md) instead.

Application and platform logs are highly likely to contain personal data.
Note that, according to [GDPR Art. 4](https://gdpr.fan/a4) any information that can be directly or indirectly related to an individual is personal data.
There are court rulings clarifying that:

- email addresses and user IDs are personal data;
- [IP addresses are personal data](https://curia.europa.eu/juris/document/document.jsf?docid=184668&doclang=EN&cid=1095511);
- [browser-generated information](https://www.judiciary.uk/wp-content/uploads/2018/10/lloyd-v-google-judgment.pdf) (e.g., cookies, URLs, fingerprints, user agents) can be personal data.

According to the [so-called "Schrems II" ruling](https://www.europarl.europa.eu/RegData/etudes/ATAG/2020/652073/EPRS_ATA(2020)652073_EN.pdf), US law -- in particular [US CLOUD Act](https://en.wikipedia.org/wiki/CLOUD_Act) and [US FISA](https://en.wikipedia.org/wiki/Foreign_Intelligence_Surveillance_Act) are incompatible -- with EU GDPR and personal data processing.

Furthermore, according to a [French court ruling](https://iapp.org/news/a/why-this-french-court-decision-has-far-reaching-consequences-for-many-businesses/) it doesn't matter if the data-center is located in the EU/EEA. A US company is still under US jurisdiction and considered at risk of US CLOUD Act and US FISA.

Most Software-as-a-Service log management platforms -- like Datadog, Logz.io and Elastic Cloud -- are operated by US entities and run on US clouds. Hence, using them to process logs poses a high risk that personal data ends up being processed on a US cloud. Therefore, personal data is at risk of US CLOUD Act and US FISA, which is incompatible with GDPR.

Fortunately, Compliant Kubernetes comes with [OpenSearch built-in](../user-guide/logs.md), so you can benefit from full-text search over your application logs while complying with GDPR.
