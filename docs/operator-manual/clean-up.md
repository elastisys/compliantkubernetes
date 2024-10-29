# Removing Welkin Apps from your cluster

<!--clean-up-start-->

To remove the applications added by Welkin you can use the two scripts `clean-sc.sh` and `clean-wc.sh`, they are located here in the [scripts folder](https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts).

They perform the following actions:

1. Delete the added helm charts
1. Delete the added namespaces
1. Delete any remaining PersistentVolumes
1. Delete the added CustomResourceDefinitions

!!!note

    If user namespaces are managed by Welkin apps then they will also be deleted if you clean up the Workload Cluster.

<!--clean-up-stop-->
