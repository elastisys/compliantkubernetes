!!! elastisys "For Elastisys Managed Services Customers"
    You can ask for this feature to be enabled by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/customer/portals).

The Swedish [SjuNet](https://www.inera.se/tjanster/alla-tjanster-a-o/sjunet/) is a private network, managed by Inera, designed for healthcare systems with strict requirements. It is used by regioner, komuner and private actors with in the healthcare system. As the healthcare system has high requirements when it comes to distributing sensitive information. SjuNet as a private network, means they can validate that the strict requirements, such as high availability, stability and bandwidth, are meet. Also, that only authorized and audited users are allowed to use it.

## Who is SjuNet for?

SjuNet is for actors that are working with the Swedish healthcare system that require a high available, stable and secure network. Today there are over 100 services, such as Nationell patientöversikt, Intygstjänster and Födelseanmälan, using SjuNet to be reliably available for hospital and healthcare centers.

## How Compliant Kubernetes connects to SjuNet

The architecture diagram below shows how Compliant Kubernetes connects to SjuNet and who is responsible for what.

The platform administrator configures NodeLocalDNS to use SjuNet's DNS to resolve SjuNet domains. Together with static routes, network traffic heading to SjuNet is routed to a virtual machine acting as a gateway. The gateway will be co-located within the same security group as the cluster to ensure that traffic between the cluster and the gateway is secure and closed off from the outside.

Inera, which is the administrators of SjuNet, require you to use a [VPN](https://inera.atlassian.net/wiki/spaces/OISJU/pages/406618308/Teknisk+anslutning#Anslutning-via-VPN-%C3%B6ver-internet) when connecting to SjuNet over the public network.

The application developer is responsible to install a supported VPN client on the VM acting as the gateway and connect it to SjuNet's VPN. Together with the static networking route within the cluster, this means that traffic intended for SjuNet will be routed correctly via the gateway.

![Architectural diagram](img/SjuNet.svg)

*![Compliant Kubernetes](img/bac8d3.png) `Platform administrators` area of responsibility ![Application Developer](img/b1ddf0.png) `Application developers` area of responsibility ![Inera](img/76608a.png) `Ineras` area of responsibility*

!!! elastisys "For Elastisys Managed Services Customers"
    Inform your platform administrator by filling a [service ticket](https://elastisys.atlassian.net/servicedesk/customer/portals) if additional IPs are required to be routed via the gateway machine.
    Or if additional security group ports, UDP/TCP, are required to be opened to allow traffic to flow in or out from the machine.

## Further Reading
- [SjuNet](https://www.inera.se/tjanster/alla-tjanster-a-o/sjunet/)
- [Order](https://www.inera.se/tjanster/alla-tjanster-a-o/sjunet/#section-5699)
- [Regulatory Framework](https://inera.atlassian.net/wiki/spaces/OISJU/pages/403736889/Regelverk)
- [Technical Information](https://inera.atlassian.net/wiki/spaces/OISJU/pages/403736906/Teknisk+information)
- [VPN](https://en.wikipedia.org/wiki/Virtual_private_network)
    - [WireGuard](https://www.wireguard.com/)
    - [OpenVPN](https://openvpn.net/)
