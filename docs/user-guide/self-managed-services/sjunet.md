---
search:
  boost: 2
---
<!-- markdownlint-disable-file first-line-h1 -->

!!! elastisys "For Elastisys Managed Services Customers"

    You can ask for this feature to be enabled by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/customer/portals).

The Swedish [Sjunet](https://www.inera.se/tjanster/alla-tjanster-a-o/sjunet/) is a private network, managed by Inera, designed for healthcare systems with strict requirements. It is used by regioner, kommuner and private actors with in the healthcare system. As the healthcare system has high requirements when it comes to distributing sensitive information. Sjunet as a private network, means they can validate that the strict requirements, such as high availability, stability and bandwidth, are meet. Also, that only authorized and audited users are allowed to use it.

## Who is Sjunet for?

Sjunet is for actors that are working with the Swedish healthcare system that require a high available, stable and secure network. Today there are over 100 services, such as Nationell patientöversikt, Intygstjänster and Födelseanmälan, using Sjunet to be reliably available for hospital and healthcare centers.

## How Compliant Kubernetes connects to Sjunet

The architecture diagram below shows how Compliant Kubernetes connects to Sjunet and who is responsible for what.

The Platform Administrator configures NodeLocalDNS to use Sjunet's DNS to resolve Sjunet domains. Together with static routes, network traffic heading to Sjunet is routed to a virtual machine acting as a gateway. The gateway will be co-located within the same security group as the cluster to ensure that traffic between the cluster and the gateway is secure and closed off from the outside.

Inera, which is the administrators of Sjunet, require you to use a [VPN](https://inera.atlassian.net/wiki/spaces/OISJU/pages/406618308/Teknisk+anslutning#Anslutning-via-VPN-%C3%B6ver-internet) when connecting to Sjunet over the public network.

The Application Developer is responsible to install a supported VPN client on the VM acting as the gateway and connect it to Sjunet's VPN. Together with the static networking route within the cluster, this means that traffic intended for Sjunet will be routed correctly via the gateway.

![Architectural diagram](img/sjunet.svg)

_![Compliant Kubernetes](img/bac8d3.png) `Platform Administrators` area of responsibility ![Application Developer](img/b1ddf0.png) `Application Developers` area of responsibility ![Inera](img/76608a.png) `Ineras` area of responsibility_

!!! elastisys "For Elastisys Managed Services Customers"

    Inform your Platform Administrator by filling a [service ticket](https://elastisys.atlassian.net/servicedesk/customer/portals) if additional IPs are required to be routed via the gateway machine.
    Or if additional security group ports, UDP/TCP, are required to be opened to allow traffic to flow in or out from the machine.

## Further Reading

- [Sjunet](https://www.inera.se/tjanster/alla-tjanster-a-o/sjunet/)
- [Order](https://www.inera.se/tjanster/alla-tjanster-a-o/sjunet/#section-5699)
- [Regulatory Framework](https://inera.atlassian.net/wiki/spaces/OISJU/pages/403736889/Regelverk)
- [Technical Information](https://inera.atlassian.net/wiki/spaces/OISJU/pages/403736906/Teknisk+information)
- [VPN](https://en.wikipedia.org/wiki/Virtual_private_network)
    - [WireGuard](https://www.wireguard.com/)
    - [OpenVPN](https://openvpn.net/)
