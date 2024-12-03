# Only allow Ingress Snippet Annotations after Proper Risk Acceptance

- Status: Accepted
- Deciders: Product Team
- Date: 2024-11-07

## Context and Problem Statement

We previously decided to allow [configuration snippet annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#configuration-snippet) for Ingress NGINX, but only after formal risk acceptance from the Application Developer. However, we had not yet decided on handling specific use cases, such as whether [server snippets](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#server-snippet) should have stricter controls due to their higher risk profile.

The difference is that configuration snippets allows to configure for whole location blocks and are validated by the Ingress Controller, while server snippets allows to configure for whole server block and are not validated by the Ingress Controller, they are passed directly to NGINX, which increases the vulnerability exposure area.

[Snippet Annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/) are a powerful tool to allow injecting custom configurations, including both configuration and server snippets, into the Ingress NGINX Controller. For example, it allows things such as header renaming, custom authentication, or other advanced use cases etc.

However, with great power comes great responsibility. Snippet annotations may break the Ingress Controller and cause downtime for all applications hosted in the Workload Cluster. Also, it opens up [CVE-2021-25742](https://github.com/kubernetes/ingress-nginx/issues/7837), and possibly other CVEs, which means that Application Developers can exfiltrate all Secrets in the Workload Cluster.

How shall we best serve Application Developers without compromising platform stability and security?

## Decision Drivers

- We want to best serve Application Developers.
- We want to ensure platform stability and security.

## Considered Options

- Allow `the use of "snippet annotations" with Ingress` by default.
- Disallow `the use of "snippet annotations" with Ingress` by default.
- Never allow `the use of "snippet annotations" with Ingress`.
- Allow `the use of "snippet annotations" with Ingress`, but only after Application Developer accepted the downtime and security risks.

## Decision Outcome

Chosen option: Allow `the use of "snippet annotations" with Ingress`, but only after Application Developer accepted the downtime and security risks.

### Positive Consequences

- Several use-cases commonly requested by Application Developers can be satisfied.

### Negative Consequences

- Platform security is at a small risk if this feature is misused by Application Developers.
- Platform stability is at a small risk if this feature is misused by Application Developers.

## Recommendation to Platform Administrators

If you enable this feature, then make sure Application Developers understand and accept the added stability and security risks. A message as follows could be used:

```text
Hello!

After talking with the team, we have decided that it is okay to enable the snippet annotations provided that:

(a) There is no alternative method to achieve the required customization;
(b) The Application Developers fully understands and accepts the security risks involved;
(c) The Application Developers takes responsibility for any downtime caused by misconfiguration; and
(d) The Application Developers takes responsibility for updating the annotation as required.

For (a), please confirm you have evaluated and ruled out other options.

For (b), confirm you understand and accept potential vulnerabilities, such as CVEs like https://github.com/kubernetes/ingress-nginx/issues/7837.

For (c), please confirm that you understand that this snippet annotations is quite powerful, meaning that misconfiguration can lead to downtime for all your Ingress resources. Obviously, if Nginx goes down due to any custom configuration, then we cannot take responsibility for that.

For (d), please confirm that you are okay to take responsibility for making sure that the custom configuration is supported in newer versions of Nginx, as we sometimes upgrade Nginx. Both our release notes and calendar invites for the maintenance windows mention if we are upgrading Nginx.

To sum up, if you can confirm (a)-(d) then we can proceed with enabling snippet annotations for your use case.

Regards,
```
