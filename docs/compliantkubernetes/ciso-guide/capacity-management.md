# Capacity Management (Kubernetes Status) Dashboard

## Relevant Regulations

### GDPR

[GDPR Article 32](https://gdpr-info.eu/art-32-gdpr/):

> The ability to ensure the ongoing confidentiality, integrity, **availability and resilience** of processing systems and services; [highlights added]

### Swedish Patient Data Law

!!!note
    This regulation is only available in Swedish. To avoid confusion, we decided not to produce an unofficial translation.

[HSLF-FS 2016:40](https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/artikelkatalog/foreskrifter-och-allmanna-rad/2016-4-44.pdf):

> 10 § Vårdgivaren ska vid utveckling, idrifttagande och ändring av informationssystem som används för behandling av personuppgifter säkerställa att personuppgifternas tillgänglighet, riktighet, konfidentialitet och spårbarhet inte riskeras.

## Mapping to ISO 27001 Controls

* [A.12.1.3 Capacity Management](https://www.isms.online/iso-27001/annex-a-12-operations-security/)

    > The use of resources must be monitored, tuned and projections made of future capacity requirements to ensure the required system performance to meet the business objectives.

## Compliant Kubernetes Status Dashboard

![Kubernetes Status Dashboard](img/kubernetes-status.png)

The Compliant Kubernetes Status Dashboard shows a quick overview of the status of your kubernetes cluster.
This includes:

* Unhealthy pods
* Unhealthy nodes
* Resource requested of the total resources in the cluster
* Pods with missing resource requests

This makes it easy to identify when your cluster is not working correctly and helps you identify configuration that isn't following best practise.
