# Getting Started

Setting up Compliant Kubernetes consists of two parts: setting up [at least two vanilla Kubernetes clusters](../architecture.md#level-2-clusters) and deploying `compliantkubernetes-apps` on top of them.

## Pre-requisites for Creating Vanilla Kubernetes clusters

In theory, any vanilla Kubernetes cluster can be used for Compliant Kubernetes. We suggest the [kubespray](https://github.com/kubernetes-sigs/kubespray) way. To this end, you need:

* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Python3 pip](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers)
* [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli#install-terraform)
* [Ansible](https://ansible.com)
* [pwgen](https://manpages.ubuntu.com/manpages/trusty/man1/pwgen.1.html)

Ansible is best installed as follows:

```shell
git clone --recursive https://github.com/elastisys/compliantkubernetes-kubespray
cd compliantkubernetes-kubespray
pip3 install -r kubespray/requirements.txt
```

Optional: For debugging, you may want CLI tools to interact with your chosen cloud provider:

* [AWS CLI](https://github.com/aws/aws-cli)
* [Exoscale CLI](https://github.com/exoscale/cli)
* [OpenStack Client](https://pypi.org/project/python-openstackclient/)
* [VMware vSphere CLI (govmomi)](https://github.com/vmware/govmomi)

## Pre-requisites for compliantkubernetes-apps

Using Ansible, these can be retrieved as follows:

```shell
git clone https://github.com/elastisys/compliantkubernetes-apps
cd compliantkubernetes-apps
ansible-playbook -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass --connection local --inventory 127.0.0.1, get-requirements.yaml
```

## Misc

Compliant Kubernetes relies on SSH for accessing nodes. If you haven't already done so, generate an SSH key as follows:

```bash
ssh-keygen
```

Configuration secrets in Compliant Kubernetes are encrypted using [SOPS](https://github.com/mozilla/sops).
We currently only support using PGP when encrypting secrets.
If you haven't already done so, generate your own PGP key as follows:

```bash
gpg --full-generate-key
```
