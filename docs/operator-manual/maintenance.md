---
tags:
- ISO 27001 A.12.6.1 Management of Technical Vulnerabilities
- BSI IT-Grundschutz APP.4.4.A21
- HIPAA S16 - Security Awareness and Training - Security Reminders - § 164.308(a)(5)(ii)(A)
- MSBFS 2020:7 4 kap. 12 §
---
# Maintaining and Upgrading your Compliant Kubernetes environment.

In order to keep your Compliant Kubernetes environment running smoothly, and to assure that you are up to date with the latest patches you need to perform regular maintenance on it.

This guide assumes that:

- Your Compliant Kubernetes environment is running normally, if not, please see the [Troubleshooting guide](troubleshooting.md).
- Your Compliant Kubernetes environment is properly [sized](cluster-sizing.md)
- You have performed the actions in the [Go-live Checklist](../user-guide/go-live.md) as failure to do so might cause downtime during maintenance.

## Compliance needs

Many regulations require you to secure your information system against unauthorized access, data loss, and breaches.
An important part of this is keeping your Compliant Kubernetes environment up to date with the latest security patches not run outdated versions of components that are no longer supported.
This maps to objectives in ISO Annex [A.12.6.1 Management of Technical Vulnerabilities](https://www.isms.online/iso-27001/annex-a-12-operations-security/).

## What maintenance do I need to do and how?

In short, there are three levels of maintenance that should be performed on a regular basis.

- Patching the underlying OS on the nodes
- Upgrading the Compliant Kubernetes application stack
- Upgrading Compliant Kubernetes-Kubespray

Let's go through them one by one.

### Patching the nodes

Security patches for the underlying OS on the nodes is constantly being released, and to ensure your environment is secured, the nodes that run Compliant Kubernetes must be updated with these patches.
We recommend that you use the [AutomaticSecurityUpdates](https://help.ubuntu.com/community/AutomaticSecurityUpdates) feature that is available in Ubuntu (similar feature exist in other distros) to install these updates.
Note that the nodes still need to be rebooted for some of these updates to be applied.
In order to reboot the nodes, you can either use a tool like [kured](https://github.com/weaveworks/kured) or you can do it manually by logging on to the nodes and rebooting them manually.
When doing that, reboot one node at the time and make sure that the rebooted node is 'Ready' and that pods are scheduled to it before you move on to the next, or you risk downtime.

There is a playbook in the compliantkubernetes-kubespray repo that can assist with the reboot of nodes.
It will cordon and reboot the nodes one by one.

```bash
./bin/ck8s-kubespray reboot-nodes <prefix> [--extra-vars manual_prompt=true] [<options>]
```

### Upgrading the Compliant Kubernetes application stack

Compliant Kubernetes consists of a multitude of open source components that interact to form a smooth End User experience.
In order to free you of the burden of keeping track of when to upgrade the various components, new versions of Complaint Kubernetes are regularly release.
When a new version is released, it becomes available as a [tagged release](https://github.com/elastisys/compliantkubernetes-apps/tags) in the GitHub repo.

> Before upgrading to a new release, please review the [changelog](https://github.com/elastisys/compliantkubernetes-apps/blob/main/CHANGELOG.md) if possible, apply the upgrade to a staging environment before upgrading any environments with production data.

### Prerequisites

- [ ] Notify the users (if any) before the upgrade starts;
- [ ] Check if there are any pending changes to the environment;
- [ ] Check the state of the environment, pods, nodes and backup jobs:

> **_NOTE:_** the below steps should be run from compliantkubernetes-apps root directory

```bash
./bin/ck8s test sc|wc
./bin/ck8s ops kubectl sc|wc get pods -A -o custom-columns=NAMESPACE:metadata.namespace,POD:metadata.name,READY-false:status.containerStatuses[*].ready,REASON:status.containerStatuses[*].state.terminated.reason | grep false | grep -v Completed
./bin/ck8s ops kubectl sc|wc get nodes
./bin/ck8s ops kubectl sc|wc get jobs -A
velero get backup
```

- [ ] Silence the notifications for the alerts. e.g you can use [alertmanager silences](https://prometheus.io/docs/alerting/latest/alertmanager/#silences);

### Upgrading compliantkubernetes-apps

For security, compliance, and support reasons, environments should stay up to date with the latest version of [compliankubernetes-apps](https://github.com/elastisys/compliantkubernetes-apps).

Note what version of compliantkubernetes-apps that is currently used and the version that you want to upgrade to.
Then check the release notes for each version in between to see if there are anything that might cause any problems, if so then consult the rest of the operations team before proceeding.
**You should never upgrade more than one minor version of compliantkubernetes-apps at a time.**

1. Pull the latest changes and switch to the correct branch:

    ```bash
    git pull
    git switch -d <next-version>
    ```

1. Update apps configuration:

    This will take a backup into `backups/` before modifying any files.

    ```bash
    ./bin/ck8s init
    ```

1. Check if there is a [migration document](https://github.com/elastisys/compliantkubernetes-apps/tree/main/migration) for the release you want to upgrade to, (e.g. [for upgrade to 0.11.0](https://github.com/elastisys/compliantkubernetes-apps/blob/5d8f4f1b3cc053b3b515711549ab80df9617f2f4/migration/v0.10.x-v0.11.x/upgrade-apps.md) ) and follow the instructions there.
Note that you should check the documentation at the release tag instead of `main` to be sure that it's correct.

1. If there is no relevant migration document, first do a dry-run.

    ```bash
    ./bin/ck8s dry-run sc
    ./bin/ck8s dry-run wc
    ```

1. If dry-run reports no errors, proceed with the upgrade.

    ```bash
    ./bin/ck8s apply sc
    ./bin/ck8s apply wc
    ```

1. Verify that everything is running after the upgrade.
At the minimum, at least run the tests in compliantkubernetes-apps.

    ```bash
    ./bin/ck8s test sc
    ./bin/ck8s test wc
    ```

1. Go back to step 1 and repeat one new release of compliantkubernetes-apps at a time until you are at the latest release.

### Upgrading Kubespray/Kubernetes

All clusters should stay up to date with the latest Kubespray version used in [compliantkubernetes-kubespray](https://github.com/elastisys/compliantkubernetes-kubespray).

1. Note what version of Kubespray that is currently used in the cluster and the Kubespray version we want to upgrade to.
Then check the release notes for each version in between to see if there are anything that might cause any problems, if so then consult the rest of the operations team before proceeding.
Also check if the newer Kubespray version would upgrade Kubernetes to a new minor version, if so then the Application Developer should get a notice of x weeks before proceeding to let them check for any deprecated APIs that they might be using.
You should never upgrade more than one patch version of Kubespray at a time.
E.g. if you are at Kubespray version 2.13.3 and are going to 2.15.0 then the upgrade path would be 2.13.3 -> 2.13.4 -> 2.14.0 -> 2.14.1 -> 2.14.2 -> 2.15.0.
Patches that are released to an older minor version can be skipped, e.g. new patches to 2.14 after 2.15 has been released.
Read more about Kubespray upgrades in their [documentation](https://kubespray.io/#/docs/upgrades).

1. Checkout the next Kubespray version by checking out the last compliantkubernetes-kubespray commit (the commit is `next-version` in the snippet below) that used that version and updating the submodule.

    ```bash
    # you should be in the root folder of compliantkubernetes-kubespray
    git switch -d <next-version>
    git submodule sync
    git submodule update --init --recursive
    ```

1. Upgrade compliantkubernetes-kubespray by following the relevant [documentation](https://github.com/elastisys/compliantkubernetes-kubespray/tree/main/migration) (e.g. [for upgrade to v2.17.x-ck8s1](https://github.com/elastisys/compliantkubernetes-kubespray/blob/v2.17.1-ck8s1/migration/v2.16.0-ck8s1-v2.17.x-ck8s1/upgrade-cluster.md)).

1. Download the required files on the nodes

    ```bash
    ./bin/ck8s-kubespray run-playbook sc upgrade-cluster.yml -b --tags=download
    ./bin/ck8s-kubespray run-playbook wc upgrade-cluster.yml -b --tags=download
    ```

1. Upgrade the cluster to a new Kubernetes version:

    ```bash
    ./bin/ck8s-kubespray run-playbook sc upgrade-cluster.yml -b --skip-tags=download
    ./bin/ck8s-kubespray run-playbook wc upgrade-cluster.yml -b --skip-tags=download
    ```

### After doing any upgrades or maintenance

- [ ] Check the state of the environment, pods and nodes:

> **_NOTE:_** the below steps should be run from compliantkubernetes-apps root directory

```bash
./bin/ck8s test sc|wc
./bin/ck8s ops kubectl sc|wc get pods -A -o custom-columns=NAMESPACE:metadata.namespace,POD:metadata.name,READY-false:status.containerStatuses[*].ready,REASON:status.containerStatuses[*].state.terminated.reason | grep false | grep -v Completed
./bin/ck8s ops kubectl sc|wc get nodes
```

- [ ] Check if any alerts generated by the upgrade didn't close;
- [ ] Check if you can login to Grafana, Opensearch or Harbor;
- [ ] Enable the notifications for the alerts;
- [ ] Notify the users (if any) when the upgrade is complete;
- [ ] Check that you can see fresh metrics and logs.
