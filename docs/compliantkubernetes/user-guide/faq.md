Frequently Asked Questions (FAQ)
================================

## How do I give access to a new application developer to a Compliant Kubernetes environment?

Add the new user to the correct **group via your Identity Provider (IdP)**, and Compliant Kubernetes will automatically pick it up.

Feeling lost? To find out what users and groups currently have access to your Compliant Kubernetes environment, type:

```bash
kubectl get rolebindings.rbac.authorization.k8s.io workload-admin -o yaml
# look at the 'subjects' field
```

If you are not using groups, contact your administrator.

## How do I add a new namespace?

Unfortunately, it is currently not possible to make adding/changing/removing namespaces self-serviced without compromising the security of the platform. While [several promising approaches](https://kubernetes.io/blog/2020/08/14/introducing-hierarchical-namespaces/) exist, they have yet to reach the maturity we require for Compliant Kubernetes.

Therefore, for the time being, please ask your administrator for creating a new namespace.

## What is encrypted at rest?

Compliant Kubernetes encrypts everything at rest, including Kubernetes resources, PersistentVolumeClaims, logs, metrics and backups, **if the underlying cloud provider supports it**.

Get in touch with your administrator to check the status. They are responsible for performing a [provider audit](/compliantkubernetes/operator-manual/provider-audit).

!!!important "Why does Compliant Kubernetes not offer encryption-at-rest at the platform level?"

    **TL;DR**: operational scalability and to avoid [security theatre](https://en.wikipedia.org/wiki/Security_theater).

    We are frequently asked why we don't simply do full-disk encryption at the VM level, using something like [cryptsetup](https://linux.die.net/man/8/cryptsetup). Let us explain our rationale.

    The reason why people want encryption-at-rest is to add another safeguard to data confidentiality. Encryption-at-rest is a must-have for laptops, as they can easily be stolen or get lost. However, it is a nice-to-have addition for servers, which are supposed to be in a physically protected data-center, with disks being safely disposed. This is verified during a [provider audit](/compliantkubernets/operator-manual/provider-audit).

    At any rate, if encryption-at-rest is deployed it must: (a) actually safeguard data confidentiality; (b) without prohibitive costs in terms of administration.

    A Compliant Kubernetes environment may comprise as many as 10 Nodes, i.e., VMs. These Nodes need to be frequently rebooted, to ensure Operating System (OS) security patches are applied. This is especially important for Linux kernel, container runtime (Docker) and Kubernetes security patches. Thanks to the power of Kubernetes, a carefully engineered and deployed application can tolerate such reboots with zero downtime. (See the [go-live checklist](../go-live).)

    The challenge is how to deliver the disk encryption key to the VM when they are booting. Let us explore a few options:

    * Non-option 1: Store the encryption key on the VM's `/boot` disk. This is obvious security theatre. For example, if server disks are stolen, the VM's data is in the hands of the thiefs.

    * Non-option 2: Let admins type the encryption key on the VM's console. Asking admins to do this is time-consuming, error-prone, effectivly jeopardizing uptime. Instead, Compliant Kubernetes recommends automatic VM reboots during "quiet times", such as at night, to ensure the OS is patched without sacrificing uptime.

        . as it would require admins to frequently copy-pasteBetter to mention that it will add a problematic and time-consuming step that jeopardizes the uptime and prevents automatic rebooting of servers as a protective security measure.

        This would be prohibitive to the admins time. If they spend all their time copy-pasting encryption keys, they won't have time to do security patching and Compliant Kubernetes improvements, hence the overall security posture will suffer.

    * Non-option 3: Let the VM pull the encryption key via instance metadata or [instance configuration](https://cloudinit.readthedocs.io/en/latest/topics/format.html#cloud-config-data). This would imply storing the encryption key on the cloud provider. If the cloud provider doesn't have encryption-at-rest, then the encryption key is also stored unencrypted, likely on the same server as the VM is running. Hence, this quickly ends up being security theatre.

    * Non-option 4: Let the VM pull the encryption key from an external location which features encryption-at-rest. This would imply that the VM needs some kind of credentials to authenticate to the external location. Again these credentials are stored unencrypted on the cloud provider, so we are back to non-option 3.

    Okay, so what are real options then?

    Latest generation (physical) servers feature a [TPM](https://en.wikipedia.org/wiki/Trusted_Platform_Module) to store the disk encryption key. This can be [securely release to the Linux kernel](https://en.wikipedia.org/wiki/Disk_encryption#Full_disk_encryption) thanks to [pre-boot authentication](https://en.wikipedia.org/wiki/Pre-boot_authentication). This process is performance-neutral and fully transparent to the VMs running on top of the servers.

    And that is why Compliant Kubernetes encrypts everything at rest, **only if the underlying cloud provider supports it**.
