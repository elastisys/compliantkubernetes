---
description: The demarcation between what users can and cannot do in Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
tags:
- BSI IT-Grundschutz APP.4.4.A3
- HIPAA S13 - Information Access Management - Access Authorization - § 164.308(a)(4)(ii)(B)
- HIPAA S14 - Information Access Management - Access Establishment and Modification - § 164.308(a)(4)(ii)(C)
- HIPAA S43 - Access Control - § 164.312(a)(1)
- MSBFS 2020:7 4 kap. 3 §
- MSBFS 2020:7 4 kap. 4 §
- HSLF-FS 2016:40 4 kap. 3 § Styrning av behörigheter
---

!!!danger "TL;DR: You **cannot** install:"

    * ClusterRoles, ClusterRoleBindings
    * Roles and RoleBindings that would [escalate your privileges](../architecture.md)
    * CustomResourceDefinitions (CRDs)
    * PodSecurityPolicies
    * ValidatingWebhookConfiguration, MutatingWebhookConfiguration

    **This means that generally you cannot deploy [Operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).**

!!!danger "TL;DR: You **cannot**:"

    * Run containers as root (`uid=0`)
    * SSH into any Node


Can I?
======

Compliant Kubernetes comes with a lot of safeguards to ensure you protect your business reputation and earn the trust of your customers. Furthermore, it is a good idea to keep regulators happy, since they bring public trust into digitalization. Public trust is necessary to shift customers away from pen-and-paper to drive usage of your amazing application.

If you used Kubernetes before, especially if you acted as a Kubernetes administrator, then being a Compliant Kubernetes user might feel a bit limiting. For example, you might not be able to run containers with root (`uid=0`) as you were used to. Again, these are not limitations, rather safeguards.

Why?
----
As previously reported, [Kubernetes is not secure by default, nor by itself](https://searchitoperations.techtarget.com/news/252487963/Kubernetes-security-defaults-prompt-upstream-dilemma). This is due to the fact that Kubernetes prefers to keep its "wow, it just works" experience. This might be fine for a company that does not process personal data. However, if you are in a regulated industry, for example, because you process personal data or health information, your regulators will be extremely unhappy to learn that your platform does not conform to security best practices.

In case of Compliant Kubernetes this implies a clear separation of roles and responsibilities between Compliant Kubernetes users and administrators.
The mission of administrators is to make you, the Compliant Kubernetes user, succeed. Besides allowing you to develop features as fast as possible, the administrator also needs to ensure that you build on top of a platform that lives up to regulatory requirements, specifically data privacy and data security regulations.

General Principle
-----------------

Compliant Kubernetes does not allow users to make any changes which may compromise the security of the platform. This includes compromising or working around access control, logging, monitoring, backups, alerting, etc. For example, accidental deletion of the CustomResourceDefinitions of Prometheus would prevent administrators from getting alerts and fixing cluster issues before your application is impacted. Similarly, accidentally deleting fluentd Pods would make it impossible to capture the Kubernetes audit log and investigate data breaches.

Specifics
---------
To stick to the general principles above, Compliant Kubernetes puts the following technical safeguards. This list may be updated in the future to take into account the fast evolving risk and technological landscape.

More technically, Compliant Kubernetes does not allow users to:

<!--safeguards-start-->
* change the Kubernetes API through [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) or [Dynamic Webhooks](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#admission-webhooks);
* gain more container execution permissions by mutating [PodSecurityPolicies](https://kubernetes.io/docs/concepts/policy/pod-security-policy/); this implies that you cannot run container images as root or mount [hostPaths](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath);
* mutate ClusterRoles or Roles so as to [escalate privileges](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#privilege-escalation-prevention-and-bootstrapping);
* mutate Kubernetes resources in administrator-owned namespaces, such as `monitoring` or `kube-system`;
* re-configure system Pods, such as Prometheus or fluentd;
* access the hosts directly.
<!--safeguards-end-->

But what if I really need to?
-----------------------------
Unfortunately, many application asks for more permissions than Compliant Kubernetes allows by default. When looking at the Kubernetes resources, the following are problematic:

* ClusterRoles, ClusterRoleBindings
* Too permissive Roles and RoleBindings
* PodSecurityPolicy and/or use of `privileged` PodSecurityPolicy
* CustomResourceDefinitions
* WebhookConfiguration

In such a case, ask your administrator to make a risk-reward analysis. As long as they stick to the general principles, this should be fine. However, as much as they want to help, they might not be allowed to say "yes". Remember, administrators are there to help you focus on application development, but at the same time they are responsible to protect your application against security risks.
