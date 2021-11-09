# Backup Dashboard

## Relevant Regulations

### GDPR

[GDPR Article 32](https://gdpr-info.eu/art-32-gdpr/):

> In assessing the appropriate level of security account shall be taken in particular of the risks that are presented by processing, **in particular from accidental or unlawful destruction, loss**, alteration, unauthorised disclosure of, or access to personal data transmitted, stored or otherwise processed. [highlights added]

### Swedish Patient Data Law

!!!note
    This regulation is only available in Swedish. To avoid confusion, we decided not to produce an unofficial translation.

[HSLF-FS 2016:40](https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/artikelkatalog/foreskrifter-och-allmanna-rad/2016-4-44.pdf):

> **Säkerhetskopiering**
>
> 12 § Vårdgivaren ska säkerställa att personuppgifter som behandlas i informationssystem säkerhetskopieras med en fastställd periodicitet.
> Säkerhetskopiorna ska förvaras på ett säkert sätt, väl åtskilda från originaluppgifterna.
>
> 13 § Vårdgivaren ska besluta om hur länge säkerhetskopiorna ska sparas och hur ofta återläsningstester av kopiorna ska göras.
>
> Allmänna råd: Hur ofta återläsningstester ska göras bör styras av resultaten av återkommande riskanalyser.

## Mapping to ISO 27001 Controls

* [A.12.3.1 Information Backup](https://www.isms.online/iso-27001/annex-a-12-operations-security/)
* [A.17.1.1 Planning Information Security Continuity](https://www.isms.online/iso-27001/annex-a-17-information-security-aspects-of-business-continuity-management/)

## Compliant Kubernetes Backup Dashboard

![Backup Dashboard](img/backup.png)

The Compliant Kubernetes Backup Dashboard allows to quickly audit the status of backups and ensure the [Recovery Point Objective](https://en.wikipedia.org/wiki/Disaster_recovery#Recovery_Point_Objective) are met.

## Handling Non-Compliance

In case there is a violation of backup policies:

* Ask the administrator to check the status of the [backup jobs](../operator-manual/disaster-recovery.md).
* Ask the developers to check if they correctly marked Kubernetes resources with the necessary [backup annotations](../user-guide/backup.md).
