# Release Notes


## Compliant Kubernetes
<!-- BEGIN TOC -->
- [v0.17.0](#v0170) - 2021-06-29
- [v0.16.0](#v0160) - 2021-05-27
- [v0.15.0](#v0150) - 2021-05-05
<!-- END TOC -->

!!!note
    For a more detailed look check out the full [changelog](https://github.com/elastisys/compliantkubernetes-apps/blob/main/CHANGELOG.md).

### v0.17.0

Released 2021-06-29.

Changes:

- The dashboard tool Grafana has been updated to a new major version of 8.x.x. This introduces new features and fixes, as well as some possibly breaking changes. See their [release notes](https://grafana.com/docs/grafana/v8.0/whatsnew/whats-new-in-v8-0/) for more information.
- The single-sign-on service Dex has been updated, bringing small changes and better consistency to the UI.
- Fixes, improvements to resource limits, resource usage, and stability.

### v0.16.0

Released 2021-05-27.

Changes:

- The default retention values have been changed and streamlined for `authlog*` and `other*`. The former will be kept for a longer period of time while the latter for shorter, both have reduced sized according to their actual usage.
- Updates, fixes, and features to improve the security of the platform.

### v0.15.0

Released 2021-05-05.

Changes:

- The search and analythics engine ElasticSearch now indexes the `authlog*` logs.
- Updates, fixes, and streamlined the install components to avoid redundant ones.

## Compliant Kubernetes Kubespray
<!-- BEGIN TOC -->
- [v2.17.0-ck8s1](#v2170-ck8s1) - 2021-10-21
- [v2.16.0-ck8s1](#v2160-ck8s1) - 2021-07-02
- [v2.15.0-ck8s1](#v2150-ck8s1) - 2021-05-27
<!-- END TOC -->

!!!note
    For a more detailed look check out the full [changelog](https://github.com/elastisys/compliantkubernetes-kubespray/blob/main/CHANGELOG.md).

### v2.17.0-ck8s1

Released 2021-10-21.

Changes:

- Kubespray updated, including a new Kubernetes version upgrade to version <a href="https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md#v1215">1.21.5</a>. This introduces new features and fixes, including security updates and storage capacity tracking.


### v2.16.0-ck8s1

Released 2021-07-02.

Changes:

- Kubespray updated, including Kubernetes upgrade to version <a href="https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md#v1207">1.20.7</a>. This introduces new features and fixes, including API and component updates.

### v2.15.0-ck8s1

Released 2021-05-27.

First stable release!
