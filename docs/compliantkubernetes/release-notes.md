# Release Notes


## Compliant Kubernetes
<!-- BEGIN TOC -->
- [v0.22.0](#v0220) - 2022-06-01
- [v0.21.0](#v0210) - 2022-05-04
- [v0.20.0](#v0200) - 2022-03-21
- [v0.19.1](#v0191) - 2022-03-01
- [v0.19.0](#v0190) - 2022-02-01
- [v0.18.2](#v0182) - 2021-12-16
- [v0.17.2](#v0172) - 2021-12-16
- [v0.18.1](#v0181) - 2021-12-08
- [v0.17.1](#v0171) - 2021-12-08
- [v0.18.0](#v0180) - 2021-11-04
- [v0.17.0](#v0170) - 2021-06-29
- [v0.16.0](#v0160) - 2021-05-27
<!-- END TOC -->

!!!note
    For a more detailed look check out the full [changelog](https://github.com/elastisys/compliantkubernetes-apps/blob/main/CHANGELOG.md).

### v0.22.0

Released 2022-06-01

#### Added

- **Added support for Elastx and UpCloud!**<br/>

- **New 'Welcoming' dashboard in OpenSearch and Grafana.**<br/>
  Users can now access public docs and different urls to the services provided by Compliant Kubernetes.

- **Improved availability of metrics and alerting.**<br/>
  Alertmanager now runs with two replicas by default, Prometheus can now be run in HA mode.

- **Added Falco rules to reduce alerts for services in Compliant Kubernetes.**<br/>
  Falco now alerts less on operations that are expected out of these services.

#### Fixed

- **Fixed a bug where users couldn't silence alerts when portforwarding to alertmanager.**<br/>

- **Improved logging stack and fixed a number of issues to ensure reliability.**<br/>


### v0.21.0

Released 2022-05-04

#### Changed

- **Users can now view ClusterIssuers.**<br/>

- **User admins can now add users to the ClusterRole user-view.**<br/>
  This is done by adding users to the ClusterRoleBinding `extra-user-view`.

- **User can now get ClusterIssuers.**<br/>

- **Ensured all CISO dashboards are available to users.**<br/>
  All the grafana dashboards in our [CISO docs](https://elastisys.io/compliantkubernetes/ciso-guide/) are now available.

- **Better stability for dex**<br/>
  Dex now runs with two replicas and has been updated.

#### Updated

- **Image upgrades to reduce number of vulnerabilities**<br/>
  Upgrades for fluentd, grafana, and harbor chartmuseum.

### v0.20.0

Released 2022-03-21

#### Added

- **Added kured - Kubernetes Reboot Daemon.**<br/>
  This enables automatic node reboots and security patching of the underlying base Operating System image, container runtime and Kubernetes cluster components.

- **Added fluentd grafana dashboard and alerts.**<br/>

- **Added RBAC for admin users.**<br/>
  Admin users can now list pods cluster wide and run the kubectl top command.

- **Added containerd support for fluentd.**<br/>

#### Changed

- **Added the new OPA policy.**<br/>
  To disallow the latest image tag.

- **Persist Dex state in Kubernetes.**<br/>
  This ensure the JWT token received from an OpenID provider is valid even after security patching of Kubernetes cluster components.

- **Add ingressClassName in ingresses where that configuration option is available.**<br/>

- **Thanos is now enabled by default.**<br/>

#### Updated

- **Upgraded nginx-ingress helm chart to v4.0.17**<br/>
  This upgrades nginx-ingress to v1.1.1. When upgrading an ingressClass object called nginx will be installed, this class has been set as the default class in Kubernetes. Ingress-nginx has been configured to still handle existing ingress objects that do not specify any ingressClassName.

- **Upgraded starboard-operator helm chart to v0.9.1**<br/>
  This is upgrading starboard-operator to v0.14.1

#### Removed

- **Removed influxDB and dependent helm charts.**<br/>


### v0.19.1

Released 2022-03-01

#### Fixed

- Fixed critical stability issue related to Prometheus rules being evaluated without metrics.

### v0.19.0

Released 2022-02-01

#### Added

- **Added Thanos as a new metrics backend.**<br/>
  Provides a much more efficient and reliable platform for long-term metrics, with the capabilities to keep metrics for much longer time periods than previously possible.<br/>
  InfluxDB will still be supported in this release.

- **Added a new feature to enable off-site replication of backups.**<br/>
  Synchronizes S3 buckets across regions or clouds to keep an off-site backup.

- **Added a new feature to create and log into separate indices per namespace.**<br/>
  *Currently considered to be an alpha feature.*

#### Changed

- **Replacing Open Distro for Elasticsearch with OpenSearch.**<br/>
  In this release, since [the Open Distro project has reached end of life](https://opendistro.github.io/for-elasticsearch/), Elasticsearch is replaced with OpenSearch and Kibana with OpenSearch Dashboards.
  OpenSearch is a fully open source fork of Elasticsearch with a compatible API and familiar User Experience.<br/>
  *Note that recent versions of official Elasticsearch clients and tools will not work with OpenSearch as they employ a product check, compatible versions can be found [here](https://opensearch.org/docs/latest/clients/index/).*

- **Enforcing OPA policies by default.**<br/>
  Provides [strict safeguards](/compliantkubernetes/user-guide/safeguards/) by default.

- **Allowing viewers to inspect and temporarily edit panels in Grafana.**<br/>
  Gives more insight to the metrics and data shown.

- **Setting Fluentd to log the reason why when it can't push logs to OpenSearch.**

#### Updated

- Large number of application and service updates, keeping up to date with new security fixes and changes.

### v0.18.2

Released 2021-12-16.

Changes:

 - Updated Open Distro for Elasticsearch to 1.13.3 to mitigate [CVE-2021-44228 & CVE-2021-45046](https://opendistro.github.io/for-elasticsearch/blog/2021/12/update-to-1-13-3/)

### v0.17.2

Released 2021-12-16.

Changes:

 - Updated Open Distro for Elasticsearch to 1.13.3 to mitigate [CVE-2021-44228 & CVE-2021-45046](https://opendistro.github.io/for-elasticsearch/blog/2021/12/update-to-1-13-3/)

### v0.18.1

Released 2021-12-08.

Changes:

 - updated Grafana to 8.0.7 in order to fix [CVE-2021-43798](https://grafana.com/blog/2021/12/07/grafana-8.3.1-8.2.7-8.1.8-and-8.0.7-released-with-high-severity-security-fix/)

### v0.17.1

Released 2021-12-08.

Changes:

 - updated Grafana to 8.0.7 in order to fix [CVE-2021-43798](https://grafana.com/blog/2021/12/07/grafana-8.3.1-8.2.7-8.1.8-and-8.0.7-released-with-high-severity-security-fix/)

### v0.18.0

Released 2021-11-04.

Changes:

- Ingress-nginx-controller has been updated from v0.28.0 to v0.49.3, bringing various updates.
    - Additionally, the configuration option `allow-snippet-annotations` has been set to `false` to mitigate known security issue [CVE-2021-25742](https://github.com/kubernetes/ingress-nginx/issues/7837)
- Fixes, minor version upgrades, improvements to resource requests and limits for applications, improvements to stability.

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

## Compliant Kubernetes Kubespray
<!-- BEGIN TOC -->
- [v2.18.1-ck8s1](#v2181-ck8s1) - 2022-04-26
- [v2.18.0-ck8s1](#v2180-ck8s1) - 2022-02-18
- [v2.17.1-ck8s1](#v2171-ck8s1) - 2021-11-11
- [v2.17.0-ck8s1](#v2170-ck8s1) - 2021-10-21
- [v2.16.0-ck8s1](#v2160-ck8s1) - 2021-07-02
- [v2.15.0-ck8s1](#v2150-ck8s1) - 2021-05-27
<!-- END TOC -->

!!!note
    For a more detailed look check out the full [changelog](https://github.com/elastisys/compliantkubernetes-kubespray/blob/main/CHANGELOG.md).

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
