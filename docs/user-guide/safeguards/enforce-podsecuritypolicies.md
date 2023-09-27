# Reduce blast radius: Enforcing restricted privileges

This page helps you understand why warnings are emitted when deploying workloads similar to:

```console
Warning: would violate PodSecurity "restricted:latest":
    allowPrivilegeEscalation != false (container "<container-name>" must set securityContext.allowPrivilegeEscalation=false),
    unrestricted capabilities (container "<container-name>" must set securityContext.capabilities.drop=["ALL"]),
    runAsNonRoot != true (container "<container-name>" must not set securityContext.runAsNonRoot=false),
    seccompProfile (pod or container "<container-name>" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```

Additionally, why pods are not scheduled and events are emitted from workloads similar to:
```console
$ kubectl -n <namespace> get events
...
<time>    Warning    FailedCreate    replicaset/<replicaset-name>    Error creating: pods "<pod-name>" is forbidden: violates PodSecurity "restricted:latest": runAsNonRoot != true (container "<container-name>" must not set securityContext.runAsNonRoot=false)
...
```

!!! elastisys "For Elastisys Managed Services Customers"
    These restrictions are put in place to protect **your** data. They are meant to help you comply with GDPR. For more details, please read our Terms of Service, specifically:

    - [ToS A1.3 Security Measures](https://elastisys.com/legal/terms-of-service/#a13-security-measures)
    - [ToS A2.3 Safeguards](https://elastisys.com/legal/terms-of-service/#a23-safeguards).

    If any of these restrictions causes friction when deploying your application, please file a [service ticket](https://elastisys.atlassian.net/servicedesk/) and we'll happily advise you on how to reduce privileges required by your application.

Kubernetes by default allows any Pod to run with any privileges it requests, which easily allows an application to take full control over a cluster and everything in it.
To minimise this risk Compliant Kubernetes employs two systems to restrict what privileges an application can request:

- [Kubernetes - Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) (PSA)
    - Coarse-grained enforcement built into Kubernetes
- [Open Policy Agent Gatekeeper - Pod Security Policies](https://github.com/open-policy-agent/gatekeeper-library/tree/master/library/pod-security-policy/) (PSP)
    - Fine-grained enforcement built with OPA Gatekeeper

In addition to enforcement Compliant Kubernetes also employ OPA Gatekeeper mutations to modify security contexts of applications to make it easier to comply with the enforced rules.
This modification happens at the stage when Pods are created, which means that their security context may contain additional content compared to the resource they were created for.
Only fields that are unset can be modified in this way.

!!! warning
    This means that Kubernetes may warn on workloads that may be permitted based on the results of the mutations.
    Example of this will follow below.

!!! note
    This model is used to emulate the behaviour of [Kubernetes own Pod Security Policies which have been deprecated and removed in favour of Pod Security Admission](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future/).

    One limitation with the OPA Gatekeeper constraints and mutations is that they target resource only based on labels, in contrast to the old Pod Security Policies which gave access to additional permissions through Kubernetes RBAC.

## Restricted Pod Security Standard

The default enforcement in Compliant Kubernetes follows the upstream [Restricted Pod Security Standard as defined by Kubernetes](https://kubernetes.io/docs/concepts/security/pod-security-standards/#restricted).
This standard includes the following:

- Escalation and privileged mode are disallowed.

    Usually applications don't need this unless they need to have low-level access to the nodes to access and manage hardware

- Host namespaces, host networks, host ports, and host paths are disallowed

    Usually applications don't need this unless they need to have low-level access to the nodes to access and manage system resources.

- Running with the seccomp profile `Localhost` or `RuntimeDefault` (set by default)

    This restricts the system call applications can make, [the `RuntimeDefault` profile is provided by containerd](https://github.com/containerd/containerd/blob/main/contrib/seccomp/seccomp_default.go#L55), the container runtime, with sane default that should not be an issue for most applications.

- Running as non root user (with a non-zero UID)

    Recommended is to run a high UID and GID over 10000 that doesn't match with other running software.

- Running with the `NET_BIND_SERVICE` capability added and `ALL` capabilities dropped (set by default)

    Usually applications don't need any capabilities unless they need to have low-level access to the nodes to access and manage system resources. The `NET_BIND_SERVICE` is an exception that allows processes to bind ports under 1024.

- Running with the following volume types:

    - configMap
    - csi
    - downwardAPI
    - emptyDir
    - ephemeral
    - persistentVolumeClaim
    - projected
    - secret

!!! warning
    This standard only enforces that `runAsNonRoot` is set to `true`, one must still either configure a numerical user in the container image or with `runAsUser` that is non-zero for the Pod to be allowed as described in [Enforce No Root](enforce-no-root.md).

!!! note
    This standard does not enforce `fsGroup`, `runAsGroup` and `supplementalGroups` to be non-zero, however these will be set to `1` by default.

??? example "Example of a minimal Pod template and the resulting mutated Pod spec"

    This example of a minimal Pod template does not conform to the Restricted Pod Security Standard, and will generate warnings as they are applied.
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      ...
    spec:
      templates:
        spec:
          containers:
            - name: nginx
              ...
              securityContext:
                runAsUser: 1000 # May be skipped if the Contatinerfile / Dockerfile contains the USER directive with numerical user
        ...
        securityContext: {}
        ...
    ```

    However with the help of mutations the template will turn into this Pod spec that conforms to the restricted standard:

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      ...
    spec:
      containers:
        - name: nginx
          ...
          securityContext:
            allowPrivilegeEscalation: false
            privileged: false
            runAsNonRoot: true
            runAsUser: 1000
            runAsGroup: 1
            seccompProfile:
              type: RuntimeDefault
            capabilities:
              drop:
                - ALL
          ...
      ...
      hostIPC: false
      hostPID: false
      securityContext:
        fsGroup: 1
        supplementalGroups:
          - 1
      ...
    ```

    It is still recommended that non-conforming workloads are updated to conform to the restricted standard and with the minimal set of privileges it requires.

## Custom Pod Security Policy

Certain applications may need more privileges than what is allowed from the restricted standard, and platform administrators may configure custom policies to allow application developers more freedom to applications in certain namespaces.

To do so application developers should put together a Pod Security Policy to be evaluated and accepted by the platform administrator, which then can allow access to these privileges in a certain namespace for resources with a certain label.
The format should be as follows:
```yaml
podSelectorLabels: # Must be provided
  <key>: <value>
  ...
allow:
  allowPrivilegeEscalation: <boolean> # Default false
  privileged: <boolean> # Default false
  allowedCapabilities: # Default empty
    - <linux capability>
    - ...
  allowedUnsafeSysctls: # Default empty (1)
    - <unsafe sysctl>
    - ...
  hostNetworkPorts: <boolean> # Default false (2)
  hostNamespace: <boolean> # Default false
  allowedHostPaths: # Default empty
    - pathPrefix: <hostpath>
      readOnly: <boolean>
    - ...
  runAsUser: MustRunAsNonRoot | RunAsAny  # Default MustRunAsNonRoot
  runAsGroup:
    rule: MustRunAs | RunAsAny # Default RunAsAny
    ranges: # Only required with MustRunAs
      - max: <GID>
        min: <GID>
      - ...
  fsGroup:
    rule: MustRunAs | RunAsAny # Default RunAsAny
    ranges: # Only required with MustRunAs
      - max: <GID>
        min: <GID>
      - ...
  supplementalGroups:
    rule: MustRunAs | RunAsAny # Default RunAsAny
    ranges: # Only required with MustRunAs
      - max: <GID>
        min: <GID>
      - ...
  volumes: # Default [ configMap, downwardAPI, emptyDir, persistentVolumeClaim, projected, secret ]
    - <volume-type>
    - ...
mutations:
  dropAllCapabilities: <boolean> # Default true
  setDefaultSeccompProfile: <boolean> # Default true
  runAsUser: <UID> # Default none (3)
  runAsGroup: <GID> # Default 1
  fsGroup: <GID> # Default 1
```

1. Sysctls may still be denied by the kubelet.
2. Allows both host network and host ports.
3. Must be configured in the container image or security context.

!!! danger
    Custom Pod Security Policies opens the platform up for potential security threats and should be as restrictive as possible and to a minimum to safeguard the security of the platform!

??? example "Example of a Pod manifest with higher privileges and associated custom Pod Security Policy"

    This Pod manifest for an application that would be capable of modifying routes on nodes:
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      labels:
        app.kubernetes.io/name: route-manager
      name: route-manager
    spec:
      containers:
        - name: manager
          ...
          securityContext:
            allowPrivilegeEscalation: true # (1)!
            runAsNonRoot: true
            runAsUser: 400
            capabilities:
              add:
                - NET_ADMIN
      ...
      hostNetwork: true
      ...
    ```

    1. Required when adding privileges that exceed the container runtime, in this case the `NET_ADMIN` capability.

    Would translate into this Pod Security Policy:
    ```yaml
    podSelectorLabels:
      app.kubernetes.io/name: route-manager
    allow:
      allowPrivilegeEscalation: true
      allowedCapabilities:
        - NET_ADMIN
      hostNetworkPorts: true
      runAsUser:
      rule: MustRunAs
      ranges:
        - max: 400
          min: 400
    ```
