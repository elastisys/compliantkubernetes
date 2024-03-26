---
tags:
  - ISO 27001 A.12.4.4 Clock Synchronization
  - MSBFS 2020:7 4 kap. 13 §
  - NIST SP 800-171 3.3.7
---

# Clock Synchronization

!!!important

    Compliant Kubernetes is about to add clock synchronization with `ntp.se` by default.
    This will be done according to [best practices](https://www.netnod.se/blog/best-practices-connecting-ntp-servers).
    To check progress, see [this issue](https://github.com/elastisys/compliantkubernetes-kubespray/issues/250).

Clock synchronization is important for the following reasons:

- Several Kubernetes components, in particular etcd, Rook/Ceph, do not work correctly if Nodes' clock drifts by more than 100ms;
- Several data protection regulations require it.

Be aware of the following:

- Some regulations require synchronization with **at least two** clock sources. This could be two different NTP servers which can be traced to two different atomic clocks.
- Some regulations require synchronization with a specific time source. For example, MSBFS 2020:7 4 kap. 13 § specifically requires synchronization with [ntp.se](https://www.netnod.se/swedish-distributed-time-service).
