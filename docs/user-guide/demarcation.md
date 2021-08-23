Demarcation
===========

> It's not that I don't trust you. Rather, I don't want you to worry.

If you used Kubernetes before, especially if you acted as a Kubernetes administrator, then being a Compliant Kubernetes user might feel a bit limiting. For example, you might not be able to run containers with root (`uid=0`) as you were used to. These restrictions are not meant to be perceived as limitations. Rather they are safeguards to ensure you keep regulators happy. While pleasing regulators might not feel rewarding, they are there to ensure public trust in digitalization and the IT industry. Without public trust, customers would not use your application and stick to pen-and-paper instead.

Why?
----
As previously reported, [Kubernetes is not secure by default, nor by itself](https://searchitoperations.techtarget.com/news/252487963/Kubernetes-security-defaults-prompt-upstream-dilemma). This is due to the fact that Kubernetes prefers to keep its "wow, it just works" experience. This might be fine for a company that does not process personal data. However, if you are in a regulated industry, for example, because you process personal data or health information, your regulators will be extremely unhappy to learn that your platform does not conform to security best practices.

In case of Compliant Kubernetes this implies a clear separation of roles and responsibilities between Compliant Kubernetes users and operators.
The mission of operators is to make you, the Compliant Kubernetes user, succeed. Besides allowing you to develop features as fast as possible, the operator also needs to ensure that you build on top of a platform that lives up to regulatory requirements, specifically data privacy and data security regulations.

General Principle
-----------------

Compliant Kubernetes does not allow users to make any changes which may compromise the security of the platform. This includes compromising or working around access control, logging, monitoring, backups, alerting, etc.

Specifics
---------
More technically, Compliant Kubernetes does not allow users:

* to change the Kubernetes API through [CustomResourceDefinitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) or [Dynamic Webhooks](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#admission-webhooks);
* to gain more container execution permissions by mutating [PodSecurityPolicies](https://kubernetes.io/docs/concepts/policy/pod-security-policy/); this implies that you cannot run container images as root or mount [hostPaths](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath);
* to mutate ClusterRoles or Roles so as to [escalate privileges](https://v1-19.docs.kubernetes.io/docs/reference/access-authn-authz/rbac/#privilege-escalation-prevention-and-bootstrapping);
* to mutate Kubernetes resources in operator-owned namespaces, such as `monitoring` or `kube-system`;
* to re-configure system Pods, such as Prometheus or fluentd;
* to access the hosts directly.

But what if I really need to?
-----------------------------
Unfortunately, many application asks for more permissions than Compliant Kubernetes allows by default. In such a case, ask your operator to make a risk-reward analysis. As long as they stick to the general principles, this should be fine. However, if you ask your operator to install a super-new, untested Kubernetes operator needing cluster-admin permissions, prepare to have your request denied. Remember, Compliant Kubernetes and its operators are there to safeguard you against compliance violations. [Don't shoot the messenger](https://en.wikipedia.org/wiki/Shooting_the_messenger).
