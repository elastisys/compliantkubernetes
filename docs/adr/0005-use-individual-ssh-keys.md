# Use Individual SSH Keys

* Status: accepted
* Deciders: Cristian, Fredrik, Olle, Johan
* Date: 2021-01-28

Technical Story:

* [Do not fiddle with the SSH key](https://github.com/elastisys/compliantkubernetes-kubespray/issues/21)
* [Create a process of how we should move to use personal SSH keys](https://github.com/elastisys/ck8s-ops/issues/54)

## Context and Problem Statement

Currently, we create per-cluster SSH key pairs, which are shared among administrators. This is problematic from an information security perspective for a few reasons:

1. It reduces the auditability of various actions, e.g., who SSH-ed into the Kubernetes control plane Nodes.
2. It makes credential management challenging, e.g., when onboarding/offboarding administrators.
3. It makes credential rotation challenging, e.g., the new SSH key pair needs to be transmitted to all administrators.
4. It encourages storing the SSH key pair without password protection.
5. It makes it difficult to store SSH key pairs on an exfiltration-proof medium, such as a YubiKey.
6. It violates the Principle of Least Astonishment.

## Decision Drivers

* We need to stick to information security best-practices.

## Considered Options

* Inject SSH keys via cloud-init.
* Manage SSH keys via an Ansible role.

## Decision Outcome

We will manage SSH keys via an Ansible role, since it allows rotating/adding/deleting keys without rebooting nodes. Also, it caters to more environments, e.g., BYO-VMs and BYO-metal. The [compliantkubernetes-kubespray](https://github.com/elastisys/compliantkubernetes-kubespray) project will make it easy to configure SSH keys.

### Bootstrapping

The above decision raises a chicken-and-egg problem: Ansible needs SSH access to the nodes, but the SSH access is managed via Ansible. This issue is solved as follows.

For cloud deployments, all Terraform providers support injecting at least one public SSH key via cloud-init:

* [AWS](https://github.com/kubernetes-sigs/kubespray/blob/release-2.15/contrib/terraform/aws/variables.tf#L9)
* [Exoscale](https://github.com/kubernetes-sigs/kubespray/blob/master/contrib/terraform/exoscale/variables.tf#L24)
* [GCP](https://github.com/kubernetes-sigs/kubespray/blob/release-2.15/contrib/terraform/gcp/variables.tf#L57)
* [OpenStack](https://github.com/kubernetes-sigs/kubespray/blob/release-2.15/contrib/terraform/openstack/variables.tf#L81)

The administrator who creates the cluster bootstraps SSH access by providing their own public SSH key via cloud-init. Then, the Ansible role adds the public SSH keys of the other administrators.

BYO-VM and BYO-metal deployments are handled similarly, except that the initial public SSH key is delivered by email/Slack to the VM/metal administrator.

## Recommendations to Operators

* Operators should devise procedures for onboarding and offboarding member of the on-call team, as well as rotating SSH keys.

* The public SSH keys of all on-call administrators could be stored in a repository in a single file with one key per line.
The comment of the key should clearly identify the owner.

* Operator logs (be it stand-alone documents, git or GitOps-like repositories) should clearly list the SSH keys and identities of the administrators configured for each environment.

## Links

* [ansible.posix.authorized_key Ansible Module](https://docs.ansible.com/ansible/latest/collections/ansible/posix/authorized_key_module.html)
