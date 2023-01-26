---
tags:
- ISO 27001 A.12.4.4 Clock Synchronization
- MSBFS 2020:7 4 kap. 13 §
---
# Clock Synchronization

## TL;DR

By default, Compliant Kubernetes sets up clock synchronization with the [Swedish Distributed Time Service](https://www.ntp.se), a.k.a., `ntp.se`:

> There are six time nodes in different locations in Sweden.
> The time nodes are continuously monitored and steered to follow UTC(SP).
> Each time node has two atomic clocks generating separate time scales for high availability.

This complies with MSBFS 2020:7 4 kap. 13 § and `ntp.se` [best practices](https://www.netnod.se/blog/best-practices-connecting-ntp-servers).

You might need to override this behaviour depending on your security policy, e.g., add US NIST or German PTB. You can do so from [here](https://github.com/elastisys/compliantkubernetes-kubespray/blob/main/config/common/group_vars/k8s_cluster/ck8s-k8s-cluster.yaml#:~:text=ntp_servers:).

## Why Clock Synchronization?

Clock synchronization is important for the following reasons:

- Several Kubernetes components, in particular etcd, Rook/Ceph, do not work correctly if Nodes' clock drifts by more than 100ms;
- Several data protection regulations require it.

Be aware of the following:

- Some regulations require synchronization with **at least two** clock sources. This could be two different NTP servers which can be traced to two different atomic clocks.
- Some regulations require synchronization with a specific time source. For example, MSBFS 2020:7 4 kap. 13 § specifically requires synchronization with [ntp.se](https://www.ntp.se).
