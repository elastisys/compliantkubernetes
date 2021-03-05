# Network Security Dashboard

## Relevant Regulations

* [GDPR Article 32](https://gdpr-info.eu/art-32-gdpr/):

    > Taking into account the state of the art [...] the controller and the processor shall implement [...] as appropriate [...] encryption of personal data;
    >
    > In assessing the appropriate level of security account shall be taken in particular of the risks that are presented by processing, in particular from accidental or unlawful destruction, loss, alteration, **unauthorised disclosure of, or access to personal data transmitted**, stored or otherwise processed. [highlights added]

* [HIPAA Part 164—SECURITY AND PRIVACY](https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/administrative/combined/hipaa-simplification-201303.pdf)

    > (2) Protect against any reasonably anticipated threats or hazards to the security or integrity of such information.

## Mapping to ISO 27001 Controls

* [A.13 Communications Security](https://www.isms.online/iso-27001/annex-a-13-communications-security/)

## Compliant Kubernetes Network Security Dashboard

![Network Security Dashboard](img/network-security.png)

The Compliant Kubernetes Network Security Dashboard allows to audit violations of NetworkPolicies (i.e., "firewall rules"). In the best case, denied traffic indicates a misconfiguration. In worst case, denied traffic indicates an ongoing security attack. Therefore, this dashboard should be regularly reviewed, perhaps even daily.

## Handling Non-Compliance

Make sure you have a proper incident management policy in place. If an attack is ongoing, it might be better to take the system offline to protect data from getting in the wrong hands. Operators need to be trained on what events justify such an extreme action, otherwise, escalating the issue along the reporting chain may add delays that favor the attacker.

In less severe cases, simply contact the developers to investigate their code, fix needless communication attempts or update their NetworkPolicies accordingly to fix any potential misconfiguration.

## Further Reading

* [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
