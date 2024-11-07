# Rely on Infrastructure Provider for encryption-at-rest

- Status: accepted
- Deciders: arch meeting
- Date: 2023-05-11

## Context and Problem Statement

A reason why people want encryption-at-rest is to add another safeguard to data confidentiality.
Encryption-at-rest is a must have for phones and laptops as they can easily be stolen or get lost.
However, in our opinion, it is a nice-to-have addition for servers, which are supposed to be in a physically protected and secure data-center, with the disks being safely disposed.
The same should be true if the Infrastructure Provideroffers object storage - the disks comprising the storage layer should be nicely tucked away deep inside a secure data-center.

Anyhow, we are sometimes asked by Application Developers on why we don't simply do full-disk encryption at the VM level, using something like [cryptsetup](https://linux.die.net/man/8/cryptsetup), or why we don't always encrypt data before it is shipped to object storage.
Furthermore, some Application Developers require that _all_ data is encrypted-at-rest.
How should we in Welkin handle encryption-at-rest both for VMs and object storage?

## Decision Drivers

- We want to avoid security theatre.
- We want to avoid operational complexity.
- We want to avoid cloud-provider dependent implementation sprawl.
- We want to make Application Developers that require encryption-at-rest happy.

## Considered Options

VM disk encryption:

1. Store the encryption key on the VM's /boot disk.
    This is obvious security theatre. For example, if server disks are stolen, the VM's data is in the hands of the thief.
1. Let admins type the encryption key on the VM's console.
    Asking admins to do this is time-consuming, error-prone, effectively jeopardizing uptime. Instead, Welkin recommends automatic VM reboots during application "quiet times", such as at night, to ensure the OS is patched without sacrificing uptime.
1. Let the VM pull the encryption key via instance metadata or instance configuration.
    This would imply storing the encryption key on the Infrastructure Provider. If the Infrastructure Provider doesn't have encryption-at-rest, then the encryption key is also stored unencrypted, likely on the same server as the VM is running. Hence, this quickly ends up being security theatre.
1. Let the VM pull the encryption key from an external location which features encryption-at-rest.
    This would imply that the VM needs some kind of credentials to authenticate to the external location. Again these credentials are stored unencrypted on the Infrastructure Provider, so we are back to option 3.
1. Rely on Infrastructure Provider to provide encryption-at-rest.

Object storage encryption:

1. Encrypt data before shipping to object storage.
    This is not doable since not all applications that interacts with object storage in Welkin supports this.
    Using a proxy gateway that can handle the encryption could have been a solution, however the only tool that we've found, MinIO Gateway, has been [deprecated](https://blog.min.io/deprecation-of-the-minio-gateway/).
1. Encrypt data using server-side-encryption.
    In Welkin we use Openstack Swift and the S3 API when interacting with object storage.
    Openstack swift has no notion of server-side encryption where the data is encrypted at rest with a user provided key.
    The S3 API has server-side encryption but again some applications in Welkin lacks the features necessary to leverage it.
1. Rely on Infrastructure Provider to provide encryption-at-rest.

## Decision Outcome

Chosen options:

- VM disk encryption: "Rely on Infrastructure Provider to provide encryption-at-rest".
- Object storage encryption: "Rely on Infrastructure Provider to provide encryption-at-rest".

### Positive Consequences

- We can offer encryption-at-rest for Application Developers that require it.
- We don't increase the operational complexity.
- We avoid security theatre.

### Negative Consequences

- We limit what Infrastructure Providers Application Developers can choose if they require encryption-at-rest.
