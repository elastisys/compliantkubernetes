# Maintaining and Upgrading your Compliant Kubernetes environment.

In order to keep your Compliant Kubernetes environment running smoothly, and to assure that you are up to date with the latest patches you need to perform regular maintenance on it.

This guide assumes that:

- Your Compliant Kubernetes environment is running normally, if not, please see the [Troubleshooting guide](https://elastisys.io/compliantkubernetes/operator-manual/troubleshooting/).
- Your Compliant Kubernetes environment is properly [sized](https://elastisys.io/compliantkubernetes/operator-manual/cluster-sizing/)
- You have performed the actions in the [Go-live Checklist](https://elastisys.io/compliantkubernetes/user-guide/go-live/) as failure to do so might cause downtime during maintenance.

## Compliance needs

Many regulations require you to secure your information system against unauthorized access, data loss, and breaches.
An important part of this is keeping your Compliant Kubernetes environment up to date with the latest security patches not run outdated versions of components that are no longer supported.
This maps to objectives in ISO Annex [A.12.6.1 Management of Technical Vulnerabilities](https://www.isms.online/iso-27001/annex-a-12-operations-security/).

## What maintenance do I need to do and how?
In short, there are three levels of maintenane that should be performed on a regular basis.

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
Compliant Kuberenets consists of a multitude of open source components that interact to form a smooth end user experience.
In order to free you of the burden of keeping track of when to upgrade the various components, new versions of Complaint Kubernetes are regularly release.
When a new version is released, it becomes available as a [tagged release](https://github.com/elastisys/compliantkubernetes-apps/tags) in the github repo.

> Before upgrading to a new release, please review the [changelog](https://github.com/elastisys/compliantkubernetes-apps/blob/main/CHANGELOG.md) if possible, apply the upgrade to a staging environment before updgrading any environments with production data.

### Upgrading compliantkubernetes-apps

For security, compliance, and support reasons, environments should stay up to date with the latest version of [compliankubernetes-apps](https://github.com/elastisys/compliantkubernetes-apps).

Note what version of compliantkubernetes-apps that is currently used and the version that you want to upgrade to.
Then check the release notes for each version in between to see if there are anything that might cause any problems, if so then consult the rest of the operations team before proceeding.
**You should never upgrade more than one minor version of compliantkubernetes-apps at a time.**

1. Checkout the next compliantkubernetes-apps version

    ```bash
    # you should be in the root folder of compliantkubernetes-apps
    git checkout <next-version>
    ```

2. Check if there is a [migration document](https://github.com/elastisys/compliantkubernetes-apps/tree/main/migration) for the relesae you want to upgrade to, (e.g. [for upgrade to 0.11.0](https://github.com/elastisys/compliantkubernetes-apps/blob/5d8f4f1b3cc053b3b515711549ab80df9617f2f4/migration/v0.10.x-v0.11.x/upgrade-apps.md) ) and follow the instructions there.
Note that you should check the documentation at the release tag instead of `main` to be sure that it's correct.

3. If there is no relevant migration document, first do a dry-run.

    ```bash
    ./bin/ck8s dry-run sc
    ./bin/ck8s dry-run wc

4. If dry-run reports no errors, proceed with the upgrade.

    ```bash
    ./bin/ck8s apply sc
    ./bin/ck8s apply wc
    ```

5. Verify that everything is running after the upgrade.
At the minimum, at least run the tests in compliantkubernetes-apps.

    ```bash
    ./bin/ck8s test sc
    ./bin/ck8s test wc
    ```

6. Go back to step 1 and repeat one new release of compliantkubernetes-apps at a time until you are at the latest release.

### Upgrading Kubespray/Kubernetes

All clusters should stay up to date with the latest Kubespray version used in [compliantkubernetes-kubespray](https://github.com/elastisys/compliantkubernetes-kubespray).

1. Note what version of Kubespray that is currently used in the cluster and the Kubespray version we want to upgrade to.
Then check the release notes for each version in between to see if there are anything that might cause any problems, if so then consult the rest of the operations team before proceeding.
Also check if the newer Kubespray version would upgrade Kubernetes to a new minor version, if so then the customer should get a notice of x weeks before proceeding to let them check for any deprecated APIs that they might be using.
You should never upgrade more than one patch version of Kubespray at a time.
E.g. if you are at Kubespray version 2.13.3 and are going to 2.15.0 then the upgrade path would be 2.13.3 -> 2.13.4 -> 2.14.0 -> 2.14.1 -> 2.14.2 -> 2.15.0.
Patches that are released to an older minor version can be skipped, e.g. new patches to 2.14 after 2.15 has been released.
Read more about Kubespray upgrades in their [documentation](https://kubespray.io/#/docs/upgrades).

1. Checkout the next Kubespray version by checking out the last compliantkubernetes-kubespray commit (the commit is `next-version` in the snippet below) that used that version and updating the submodule.

    ```bash
    # you should be in the root folder of compliantkubernetes-kubespray
    git checkout <next-version>
    git submodule update
    ```

2. Upgrade compliantkubernetes-kubespray by following the relevant [documentation](https://github.com/elastisys/compliantkubernetes-kubespray/tree/main/migration) (e.g. [for upgrade to v2.17.x-ck8s1](https://github.com/elastisys/compliantkubernetes-kubespray/blob/v2.17.1-ck8s1/migration/v2.16.0-ck8s1-v2.17.x-ck8s1/upgrade-cluster.md)).

## After doing any upgrades or maintenance

It is a good idea to perform a **log review** after each maintenance.
The purpose is two-fold:

1. To catch potential issues caused by the maintenance.
2. To piggy-back log review on top of a known-good process.

For instructions on how to do this, please follow the [log review guide](https://compliantkubernetes.io/ciso-guide/log-review/).
