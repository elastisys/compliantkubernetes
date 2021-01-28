# Use Individual SSH Keys

* Status: proposed
* Deciders: Cristian, Fredrik, Olle, Johan
* Date: 2021-01-28

Technical Story:

* [Do not fiddle with the SSH key](https://github.com/elastisys/compliantkubernetes-kubespray/issues/21)
* [Create a process of how we should move to use personal SSH keys](https://github.com/elastisys/ck8s-ops/issues/54)

## Context and Problem Statement

Currently, we create per-cluster SSH keypairs, which are shared among operators. This is problematic from an information security perspective for a few reasons:

1. It reduces the auditability of various actions, e.g., who SSH-ed into the Kubernetes master.
2. It makes credential management challenging, e.g., when onboarding/offboarding operators.
3. It makes credential rotation challenging, e.g., the new SSH keypair needs to be transmitted to all operators.
4. It encourages storing the SSH keypair without password protection.
5. It makes it difficult to store SSH keypairs on an exfiltration-proof medium, such as a YubiKey.
6. It violates the Principle of Least Astonishment.

## Decision Drivers

* We need to stick to information security best-practices.

## Considered Options

* Inject SSH keys via cloud-init.
* Manage SSH keys via an Ansible role.

## Decision Outcome

We will managed SSH keys via an Ansible role, since it allows rotating/adding/deleting keys without rebooting nodes. Also, it caters to more environments, e.g., BYO-VMs and BYO-metal. The public SSH keys of all operators will be put in a file in `https://github.com/elastisys/compliantkubernetes-kubespray`, one key per line. The comment of the key needs to clearly identify the owner.

## Links

* [ansible.posix.authorized_key Ansible Module](https://docs.ansible.com/ansible/latest/collections/ansible/posix/authorized_key_module.html)
