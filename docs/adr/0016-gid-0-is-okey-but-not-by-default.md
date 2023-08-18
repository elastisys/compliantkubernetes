# [Superseded by [ADR-0040](0040-allow-group-id-0.md)] gid=0 is okay, but not by default

* Status: superseded by [ADR-0040](0040-allow-group-id-0.md)
* Deciders: Cristian, Lars, Olle
* Date: 2021-08-23

## Context and Problem Statement

OpenShift likes to shift (pun intended) the UID -- i.e., assign arbitrary UIDs -- to containers. They do this as an additional security feature, given that OpenShift is a multi-tentant Kubernetes solution. Each OpenShift project received a non-overlapping UID range. Hence, in case an attacker escapes a container, it will be more difficult to interfere with other processes.

However, this shifting of UIDs introduces an additional complexity: What if a process wants to write to the filesystem? What uid, gid and permissions should the files and folders have? To solve this problem, the OpenShift documentation (see ["Support arbitrary user ids"][openshift-docs]) recommends setting gid=0 on those files and folders. Specifically, the Dockerfiles of the container images should contain:

```Dockerfile
RUN chgrp -R 0 /some/directory && chmod -R g=u /some/directory
```

During execution, OpenShift assigns `gid=0` as a supplementary group to containers, so as to give them access to the required files.

In contrast to OpenShift, Compliant Kubernetes is not a multi-tenant solution. Given previous vulnerabilities in Kubernetes that affected tenant isolation (e.g., [CVE-2020-8554][cve]
), we believe that non-trusting users should not share a Workload Cluster. Hence, we do not assign arbitrary UIDs to containers and do not need to assign `gid=0` as a supplementary group.

The `gid=0` practice above seems to have made its way in [quite a few Dockerfiles][github-search], however, it is far from being the default outside OpenShift.

What should Compliant Kubernetes do with the `gid=0` practice?

## Decision Drivers

* For user expectations, we want to make it easy to start with Compliant Kubernetes.
* For better security and easier audits, we do not want to add unnecessary permissions.
* [ID mapping in mounts][idmapping] has landed in Linux 5.12. Once this feature is used in container runtimes and Kubernetes, the `gid=0` problem will go away.

## Considered Options

* Allow `gid=0` by default.
* Disallow `gid=0` by default -- this is what Kubespray does.
* Never allow `gid=0`.

## Decision Outcome

Chosen option: "disallow `gid=0` by default". Enabling it on a case-by-case basis is okay.

### Positive Consequences

* We do not unnecessarily add a permission to containers.

### Negative Consequences

* Some users will complain about their container images not starting, and we will need to add a less restricted PodSecurityPolicy in their cluster.

## Other Considerations

PodSecurityPolicies are deprecated in favor of [PodSecurity Admission][psa]. This decision will have to be revisited once PodSecurity Admission is stable.

In case we notice that the `gid=0` practice is gaining significant uptake, we will have to revisit this decision to allow `gid=0` by default.

In case [ID mapping][idmapping] is implemented in container runtimes and Kubernetes, this problem will likely go away. In that case, this decision might be revisited to never allow `gid=0`.

[openshift-docs]: https://docs.openshift.com/container-platform/4.8/openshift_images/create-images.html
[github-search]: https://github.com/search?l=Dockerfile&q=%22chgrp+-R%22&type=Code
[cve]: https://nvd.nist.gov/vuln/detail/CVE-2020-8554
[psa]: https://kubernetes.io/docs/concepts/security/pod-security-admission/
[idmapping]: https://kernelnewbies.org/Linux_5.12#ID_mapping_in_mounts
