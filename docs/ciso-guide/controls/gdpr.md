# GDPR (Regulation (EU) 2016/679)

{%
   include-markdown '_common.include'
   start='<!--legal-disclaimer-start-->'
   end='<!--legal-disclaimer-end-->'
%}

!!!note
    Fully implementing GDPR entails a lot of work, like:

    * Assigning a DPO;
    * Documenting Records of Processing Activities;
    * Writing Privacy Policies;
    * Signing Data Protection Agreements with your suppliers.

    This page only points you to the GDPR concerns relevant for Compliant Kubernetes.

If you process [personal data](https://gdpr.fan/a4) in the EU/EEA, you need to follow GDPR.

## GDPR Art. 32 Security of Processing

When it comes to security, GDPR is rather broad and non-prescriptive.
Pretty much everything we do in Compliant Kubernetes is done to secure data.
This includes, for instance, that we perform vulnerability scanning both at rest and at runtime, process logs in a separate cluster controlled with restrictive access controls to make them tamper-proof from hacked applications, and that we put safeguards in place to make developers enforce network segregation per application component.
And much more.
In fact, we could pretty much link every single page to GDPR Art. 32, but that would be rather noisy!

Hence, if you need a more precise understanding on how Compliant Kubernetes protects personal data as required by GDPR Art. 32, please look at our [ISO 27001 Controls](iso-27001.md), which links to both more technical controls, and continuous confidentiality, integrity, availability and resilience of processing processes, such as our go-live checklist.

[TAGS]

## Further reading

* [What is personal data?](https://gdpr.fan/a4)
* [Art. 28 GDPR Processor](https://gdpr.fan/a28)
* [Art. 17 GDPR Right to erasure ("right to be forgotten")](https://gdpr.fan/a17)
* [Art. 32 GDPR Security of processing](https://gdpr.fan/a32)
