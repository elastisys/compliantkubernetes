Argo™ CD (preview)
==================

![ArgoCD Deployment Model](img/argocd.drawio.svg)

This page will help you succeed in connecting to Argo CD application which meets your security and compliance requirements.

## Provision a New Argo CD Cluster

Ask your service-specific administrator to install a Argo CD inside your Compliant Kubernetes environment.The service-specific administrator will ensure the Argo CD cluster complies with your security requirements, including:

* **Business continuity**: Due to its functionality, ArgoCD does not need high availability and Kubernetes's self-healing is sufficient for business continuity of ArgoCD. Hence, it is sufficient to run only one replica of ArgoCD provided at least two Nodes have capacity to host it.
* **Disaster recovery**: Your service-specific administrator will configure velero with regular backups.
* **Capacity management**: Your service-specific administrator will ensure Argo CD has enough capacity to meet your needs,as required to get the best performance.
* **Incident management**: Your administrator will set up the necessary probes, dashboards and alerts, to discover issues and resolve them, before they become a problem.
* **Access control**: Your administrator will provides Argo CD URL that has authentication using Dex.

For installing ArgoCD, Compliant Kubernetes recommends the [Argo CD Helm Chart](https://argoproj.github.io/argo-helm/).

## Getting Access

Your administrator will set up the authentication inside Compliant Kubernetes, which will give you access to ArgoCD UI.

## Follow the Go-Live Checklist

You should be all set.
Before going into production, don't forget to go through the [go-live checklist](../go-live.md).

## CK8S Argo CD Release Notes

Check out the [release notes](../../release-notes/argocd.md) for the Argo CD setup that runs in Compliant Kubernetes environments!

## Further Reading

* [ArgoCD documentation](https://argo-cd.readthedocs.io/en/stable/)
