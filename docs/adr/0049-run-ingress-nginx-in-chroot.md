# Running NGINX with Chroot Option

- Status: Accepted
- Deciders: Arch Meeting
- Date: 2023-12-23

## Context and Problem Statement

Elastisys is continuously working to improve the security of our platform to better protect Personal Data for Application Developers. Currently, the `ingress-nginx` controller has the ability to list all secrets in the environment, which poses a security risk.

We needed a way to restrict NGINX's access to only necessary TLS secrets. The initial approach to use Gatekeeper constraints was not feasible due to the Kubernetes admission API's [limitations](https://github.com/kubernetes/kubernetes/blob/v1.28.3/pkg/apis/admission/types.go#L157-L166) as it doesn't check for `READ (get/list/watch)` operations.

Should we consider using `Role-Based Access Control (RBAC)` and potentially running NGINX in a `chroot` mode for enhanced security?

## Decision Drivers

- We want to maintain Platform security and stability.
- We want to find a solution which is scalable and minimizes the Platform Administrator burden.
- We want to best serve the Application Developers.
- We want to make the Platform Administrator life easier.

## Considered Options

1. Write an Operator for RBAC Management

    - `Good`, because it provides precise control over which secrets NGINX can access, enhancing security.
    - `Good` because it automatically applies RBAC policies, reducing manual configuration and potential errors.
    - `Bad`, because it requires development and maintenance of a custom operator, which is complex and time-consuming.

1. Use Namespaced RoleBindings

    - `Good`, because it is easier and faster to implement compared to developing an operator.
    - `Bad`, because it requires manual configuration of RoleBindings, which can be cumbersome in large environments and prone to human error.
    - `Bad`, because it increases overhead as namespaces need to be manually managed and updated.

1. Run Ingress-NGINX in chroot with custom seccomp profile

    - `Good`, because attackers can not exploit recent CVEs to access secrets cluster-wide.
    - `Bad`, because if someone were to break out of the chroot and attack the controller itself, they would have access to the `clone` and `unshare` syscalls on the host. This allows the attacker to create threads on the host as well as any type of namespace. It is not entirely clear what kind of harm this could cause.

## Decision Outcome

Chosen option `3` i.e We will run `ingress-nginx` in a `chroot` environment to limit its access to the host system, improving security and also, maintaining the custom Ingress-NGINX chroot `seccomp profile`.

The solution proposed has already been implemented and will be available from app version `0.35` onwards.

### Positive Consequences

- Attackers can not exploit recent CVEs to access secrets cluster-wide.
- Increased platform security and reliability.
- We avoid the security theater.

### Negative Consequences

- Initial overhead for Platform Administrators.

## Links

- [Exploiting CVE-2023-5044](https://raesene.github.io/blog/2023/10/29/exploiting-CVE-2023-5044/)
- [Kubernetes Blog on Ingress-NGINX 1.2.0](https://kubernetes.io/blog/2022/04/28/ingress-nginx-1-2-0/)
- [Elastisys/compliantkubernetes-apps#1854](https://github.com/elastisys/compliantkubernetes-apps/issues/1854)
