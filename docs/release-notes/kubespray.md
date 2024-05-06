# Release Notes

## Compliant Kubernetes Kubespray

<!-- BEGIN TOC -->

- [v2.23.0-ck8s3](#v2230-ck8s3) - 2024-02-27
- [v2.24.0-ck8s1](#v2240-ck8s1) - 2024-02-08
- [v2.23.0-ck8s2](#v2230-ck8s2) - 2024-01-11
- [v2.23.0-ck8s1](#v2230-ck8s1) - 2023-10-16
- [v2.22.1-ck8s1](#v2221-ck8s1) - 2023-07-27
- [v2.21.0-ck8s1](#v2210-ck8s1) - 2023-02-06
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

    For a more detailed look check out the full [changelog](https://github.com/elastisys/compliantkubernetes-kubespray/blob/main/changelog/).

### v2.23.0-ck8s3

#### Updated

- Upgrade containerd to 1.7.13, runc to 1.1.12 and Kubernetes to 1.27.10

  This is needed to fix [CVE-2024-21626](https://github.com/advisories/GHSA-xr7r-f8xq-vfvv)

### v2.24.0-ck8s1

#### Updated

- **Updated Kubespray to `v2.24.0`** <br/>
  Kubernetes version upgraded to [v1.28.6](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.28.md#changelog-since-v1270). <br/>

### v2.23.0-ck8s2

Released 2024-01-11

#### Updated

- Fixed a bug that was making Kubespray fail when running the `scale.yml` playbook.

### v2.23.0-ck8s1

Released 2023-10-16

#### Updated

- Rook version v1.11.9 and Ceph v17.2.6
- **Updated Kubespray to `v2.23.0`** <br/>
  Kubernetes version upgraded to [v1.27.5](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.27.md#changelog-since-v1260). <br/>

### v2.22.1-ck8s1

Released 2023-07-27

#### Updated

- **Updated Kubespray to `v2.22.1`** <br/>
  Kubernetes version upgraded to [v1.26.7](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.26.md#changelog-since-v1250). <br/>
  This version requires at least terraform version `1.3.0` in order to provision infrastructure using the Kubespray provided terraform modules.

#### Changed

- **Updated the Kubernetes audit log policy file**

### v2.21.0-ck8s1

Released 2023-02-06

#### Updated

- **Updated Kubespray to `v2.21.0`** <br/>
  Kubernetes version upgraded to [v1.25.6](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.25.md#v1256) in which Pod Security Policies (PSPs) are removed. You should not upgrade to this version if you are using PSPs. To deploy [Compliant Kubernetes Apps](https://github.com/elastisys/compliantkubernetes-apps) on this version it needs to be on a compatible version which depends on [this issue](https://github.com/elastisys/compliantkubernetes-apps/issues/1218). <br/>
  This version requires at least terraform version `0.14.0` in order to provision infrastructure using the Kubespray provided terraform modules.
- **Upgraded rook-ceph operator to `v1.10.5` and ceph to `v17.2.5`** <br/>
  If you are using the rook-ceph operator you can read the [migration docs](https://github.com/elastisys/compliantkubernetes-kubespray/blob/v2.21.0-ck8s1/rook/migration/rook-1.5.x-rook-1.10.5/upgrade.md) on how to upgrade these components.

#### Changed

- **Improved setup for OpenStack with additional server groups** <br/>
  This allows anti-affinity to be set between arbitrary nodes, improving scheduling and stability.
- **Switched from using upstream Kubespray repository as submodule to the Elastisys fork**

#### Added

- **Added a get-requirements file to standardize which terraform version to use, `1.2.9`**
- **Added ntp.se as standard ntp server**

### v2.20.0-ck8s2

Released 2022-10-24

#### Changed

- **Changed a Kubespray variable which is required for upgrading clusters on cloud providers that don't have external IPs on their control plane nodes**

### v2.20.0-ck8s1

Released 2022-10-10

#### Updated

- **Kubespray updated to `v2.20.0`** <br/>
  Kubernetes version upgraded to [v1.24.6](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.24.md#v1246).

#### Changed

- **Scripts are now using yq version 4, this requires `yq4` as an alias to yq v4**

#### Fixed

- **Fixed multiple kube-bench fails (01.03.07, 01.04.01, 01.04.02)**

### v2.19.0-ck8s3

Released 2022-09-23

#### Updated

- **Bumped upcloud csi driver to `v0.3.3`**

### v2.19.0-ck8s2

Released 2022-07-22

#### Added

- **Added option to clusteradmin kubeconfigs to use OIDC for authentication**
- **Added New Ansible playbooks to manage kubeconfigs and some RBAC**

### v2.19.0-ck8s1

Released 2022-06-27.

#### Updated

- **Kubespray updated to `v2.19.0`** <br/>
  Kubernetes version upgraded to [1.23.7](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.23.md#v1237).

### v2.18.1-ck8s1

Released 2022-04-26.

#### Updated

- **Kubespray updated to `v2.18.1`** <br/>
  This introduces some fixes for cluster using containerd as container manager.
- **Updated default etcd version to `3.5.3`**
  This fixes an issue where [etcd data might get corrupted](https://groups.google.com/a/kubernetes.io/g/dev/c/B7gJs88XtQc/m/rSgNOzV2BwAJ).

### v2.18.0-ck8s1

Released 2022-02-18.

#### Updated

- **Kubespray updated to `v2.18.0`** <br/>
  Kubernetes upgraded to version [1.22.5](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md#v1225).
  This introduces new features and fixes, including security updates.
  There's also a lot of deprecated API's that were removed in this version so take a good look at [these notes](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md#removal-of-several-beta-kubernetes-apis) before upgrading.

### v2.17.1-ck8s1

Released 2021-11-11.

#### Updated

- **Kubespray updated to `v2.17.1`** <br/>
  Kubernetes version upgraded to [1.21.6](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md#v1216), this patch is mostly minor fixes.

### v2.17.0-ck8s1

Released 2021-10-21.

#### Updated

- **Kubespray updated to `v2.17.0`** <br/>
  Kubernetes version upgraded to [1.21.5](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md#v1215), this introduces new features and fixes, including security updates and storage capacity tracking.

### v2.16.0-ck8s1

Released 2021-07-02.

#### Updated

- Kubespray updated to `v2.16.0`
  Kubernetes version upgraded to [1.20.7](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.20.md#v1207), this introduces new features and fixes, including API and component updates.

### v2.15.0-ck8s1

Released 2021-05-27.

First stable release!
