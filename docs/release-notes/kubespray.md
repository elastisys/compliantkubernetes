# Release Notes


## Compliant Kubernetes Kubespray
<!-- BEGIN TOC -->
- [v2.20.0-ck8s2](#v2200-ck8s2) - 2022-10-24
- [v2.20.0-ck8s1](#v2200-ck8s1) - 2022-10-10
- [v2.19.0-ck8s3](#v2190-ck8s3) - 2022-09-23
- [v2.19.0-ck8s2](#v2190-ck8s2) - 2022-07-22
- [v2.19.0-ck8s1](#v2190-ck8s1) - 2022-06-27
- [v2.18.1-ck8s1](#v2181-ck8s1) - 2022-04-26
- [v2.18.0-ck8s1](#v2180-ck8s1) - 2022-02-18
- [v2.17.1-ck8s1](#v2171-ck8s1) - 2021-11-11
- [v2.17.0-ck8s1](#v2170-ck8s1) - 2021-10-21
- [v2.16.0-ck8s1](#v2160-ck8s1) - 2021-07-02
- [v2.15.0-ck8s1](#v2150-ck8s1) - 2021-05-27
<!-- END TOC -->

!!!note
    For a more detailed look check out the full [changelog](https://github.com/elastisys/compliantkubernetes-kubespray/blob/main/CHANGELOG.md).

### v2.20.0-ck8s2

Released 2022-10-24

Changes:

- Changed a Kubespray variable which is required for upgrading clusters on cloud providers that don't have external IPs on their control plane nodes.

### v2.20.0-ck8s1

Released 2022-10-10

Changes:

- Scripts are now using yq version 4, this requires `yq4` as an alias to yq v4.
- Kubespray updated to `v2.20.0`.
- Kubernetes version upgraded to [v1.24.6](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.24.md#v1246).
- Fixed multiple kube-bench fails (01.03.07, 01.04.01, 01.04.02)

### v2.19.0-ck8s3

Released 2022-09-23

Changes:

- Bumped upcloud csi driver to `v0.3.3`

### v2.19.0-ck8s2

Released 2022-07-22

Changes:

- Added option to clusteradmin kubeconfigs to use OIDC for authentication.
- New ansible playbooks to manage kubeconfigs and some RBAC.

### v2.19.0-ck8s1

Released 2022-06-27.

Changes:

- Kubespray updated to v2.19.0
- Kubernetes version upgrade to version [1.23.7](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.23.md#v1237).

### v2.18.1-ck8s1

Released 2022-04-26.

Changes:

- Kubespray updated to v2.18.1
  This introduces some fixes for cluster using containerd as container manager.
- Changed default etcd version to 3.5.3
  This fixes an issue where [etcd data might get corrupted](https://groups.google.com/a/kubernetes.io/g/dev/c/B7gJs88XtQc/m/rSgNOzV2BwAJ)

### v2.18.0-ck8s1

Released 2022-02-18.

Changes:

- Kubespray updated, including a new Kubernetes version upgrade to version [1.22.5](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md#v1225).
  This introduces new features and fixes, including security updates.
  There's also a lot of deprecated API's that were removed in this version so take a good look at [these notes](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md#removal-of-several-beta-kubernetes-apis) before upgrading.

### v2.17.1-ck8s1

Released 2021-11-11.

Changes:

- Kubespray updated, including a new Kubernetes version upgrade to version <a href="https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md#v1216">1.21.6</a>. This patch is mostly minor fixes.

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
