# Only allow Ingress Configuration Snippet Annotations after Proper Risk Acceptance

* Status: accepted
* Deciders: architecture meeting
* Date: 2022-08-11

## Context and Problem Statement

[Configuration snippet annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#configuration-snippet) are a powerful tool to allow injecting any kind of Nginx configuration into the Nginx Ingress Controller. For example, it allows things such as header renaming, custom authentication, etc.

However, with great power comes great responsibility. Configuration snippet may break the Ingress Controller and cause downtime for all applications hosted in the Workload Cluster. Also, it opens up [CVE-2021-25742](https://github.com/kubernetes/ingress-nginx/issues/7837), which means that application developers can exfiltrate all Secrets in the Workload Cluster.

How shall we best serve application developers without compromising platform stability and security?

## Decision Drivers

* We want to best serve application developers.
* We want to ensure platform stability and security.

## Considered Options

* Allow `the use of "config-snippets annotations" with Ingress` by default.
* Disallow `the use of "config-snippets annotations" with Ingress` by default.
* Never allow `the use of "config-snippets annotations" with Ingress`.
* Allow `the use of "config-snippets annotations" with Ingress`, but only after application developer accepted the downtime and security risks.

## Decision Outcome

Chosen option: Allow `the use of "config-snippets annotations" with Ingress`, but only after application developer accepted the downtime and security risks.

### Positive Consequences

* Several use-cases commonly requested by application developers can be satisfied.

### Negative Consequences

* Platform security is at a small risk if this feature is misused by application developers.
* Platform stability is at a small risk if this feature is misused by application developers.

## Recommendation to Platform Administrators

If you enable this feature, then make sure application developers understand and accept the added stability and security risks. A message as follows could be used:
```
Hello!

After talking with the team, we have decided that it is okay to enable the `nginx.ingress.kubernetes.io/configuration-snippet` annotation provided that:

(a) there is no other way for you to move forward;
(b) you understand and are willing to accept the security risks;
(c) you are okay to take responsibility for downtime caused by misconfiguration; and
(d) you are okay to take responsibility for updating the annotation as required.

For (a), please confirm that you checked that you cannot use other annotations instead for your use cases. https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/

For (b), please confirm you are aware and understand the consequences of this CVE. https://github.com/kubernetes/ingress-nginx/issues/7837.

For (c), please confirm that you understand that this annotation is quite powerful, meaning that misconfiguration can lead to downtime for all your Ingress resources. Obviously, if Nginx goes down due to any custom configuration, then we cannot take responsibility for that.

For (d), please confirm that you are okay to take responsibility for making sure that the custom configuration is supported in newer versions of Nginx, as we sometimes upgrade Nginx. Both our release notes and calendar invites for the maintenance windows mention if we are upgrading Nginx.

To sum up, if you can confirm (a)-(d) then I can enable the `nginx.ingress.kubernetes.io/configuration-snippet` annotation.

Regards,
```
