---
description: Checklist before going live on Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
tags:
- HIPAA S26 - Contingency Plan - Testing and Revision Procedure - § 164.308(a)(7)(ii)(D)
---

# Go-live Checklist

The administrator set up a shiny new Compliant Kubernetes environment.
You containerized your application, deployed it, configured a working CI/CD pipeline, configured application alerts, etc. etc.
All seems fine, but somehow you feel anxious about going into production 24/7.

To move from production anxiety to production karma, here is a checklist to go through before going live 24/7. Make sure to perform this checklist in a shared session with the administrator.

- [ ] Load testing was performed.
    * **Why?** This ensures that enough capacity was allocated for the environment.
    * **How?** Set up a synthetic workload generator or replay a relevant workload. Ask the administrator to monitor your environment's capacity usage, including that related to components necessary for application logs and application metrics.
    * **Desired outcome**: Allocated capacity is sufficient.
    * **Possible resolution**: Ensure the application has proper resource requests and limits (see our [user demo as an example](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L42-L51)).
- [ ] Load testing was performed while updating the application.
    * **Why?** This ensures that the application can be updated without downtime.
    * **How?** Make a trivial change to your application, e.g., add "Lorem ipsum" in the output of some API, and redeploy.
    * **Desired outcome**: Measured downtime is acceptable.
    * **Possible resolutions**: Make sure you have the right [deployment strategy](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/). Prefer `RollingUpdate` over `Recreate`. Ensure other parameters of the deployment strategy are tuned as needed.
- [ ] Load testing was performed while doing a rolling reboot of Nodes:
    * **Why?** Node failure may cause application downtime. Said downtime can be large if it happens at night, when administrators need to wake up before they can respond. Also, administrators need some extra capacity for performing critical security updates on the base operating system of the Nodes.
    * **How?** As above, but now ask the administrator to perform a rolling reboot of Nodes.
    * **Desired outcome**: The measured downtime (due to Pod migration) during Node failure or drain is acceptable. Capacity is sufficient to tolerate one Node failure or drain.
    * **Possible resolution**:
        * Ensure the application has proper resource requests and limits (see our [user demo for an example](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L42-L51)).
        * Ensure the application has at least two replicas (see our [user demo for an example](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L5)).
        * Ensure the application has `topologySpreadConstraints` to ensure Pods do not end up on the same Node (see our [user demo for an example](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L76-L82)).
- [ ] [For multi-Zone environments] Load testing was performed while failing an entire Zone:
    * **Why?** If a multi-Zone environment was requested, then the additional resilience must be tested. Otherwise, Zone failure may cause application downtime.
    * **How?** As above, but now ask the administrator to fail an entire Zone.
    * **Desired outcome**: The measured downtime (due to Pod migration) during Zode failure is acceptable. Capacity is sufficient to tolerate one Zode failure.
    * **Possible resolution**:
        * Ensure the application has proper resource requests and limits (see our [user demo for an example](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L42-L51)).
        * Ensure the application has at least two replicas (see our [user demo for an example](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L5)).
        * Ensure the application has `topologySpreadConstraints` to ensure Pods do not end up on the same Zone (see our [user demo for an example](https://github.com/elastisys/compliantkubernetes/blob/main/user-demo/deploy/ck8s-user-demo/values.yaml#L76-L82)).
- [ ] Disaster recovery testing was performed:
    * **Why?** This ensures that the application and platform team agreed on who backs up what, instead of ending up thinking that "backing up this thingy" is the other team's problem.
    * **How?** Ask the administrator to destroy the environment and restore from off-site backups. Check if your application is back up and its data is restored as expected.
    * **Desired outcome**: Measured recovery point and recovery time is acceptable.
    * **Possible resolution**: Ensure you store application either in PersistentVolumes -- these are backed up by default in Compliant Kubernetes -- or a managed database hosted inside Compliant Kubernetes.
- [ ] Redeployment of the application from scratch works.
    * **Why?** This ensures that no tribal knowledge exists and your Git repository is truly the only source of truth.
    * **How?** Ask your administrator to "reset" the environment, i.e., remove all container images, remove all cached container images, remove all Kubernetes resources, etc. Redeploy your application.
    * **Desired outcome**: Measured setup time is acceptable.
    * **Possible resolutions**: Make sure to add all code and Kubernetes manifests to your Git repository. Make sure that relevant documentation exists.
