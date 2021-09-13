# Removing Compliant Kubernetes Apps from your cluster

To remove the applications added by Compliant Kubernetes you can use the two scripts `clean-sc.sh` and `clean-wc.sh`, they are located here in the [scripts folder](https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts).

They perform the following actions:

1. Delete the added helm charts
2. Delete the added namespaces
3. Delete any remaining PersistentVolumes
4. Delete the added CustomResourceDefinitions

!!!note
    If user namespaces are managed by Compliant Kubernetes apps then they will also be deleted if you clean up the workload cluster.
