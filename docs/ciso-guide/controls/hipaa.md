# HIPAA Controls

{%
   include-markdown '_common.include'
   start='<!--legal-disclaimer-start-->'
   end='<!--legal-disclaimer-end-->'
%}

Click on the links below to navigate the documentation by control.

[TAGS]

## Other HIPAA Controls

HIPAA controls are taken from these documents:

* [HIPAA Security Series - Security Standards: Administrative Safeguards](https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/administrative/securityrule/adminsafeguards.pdf)
* [HIPAA Security Series - Security Standards: Physical Safeguards](https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/administrative/securityrule/physsafeguards.pdf)
* [HIPAA Security Series - Security Standards: Technical Safeguards](https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/administrative/securityrule/techsafeguards.pdf)

The following controls are outside the scope of Compliant Kubernetes and **need to be implemented by the organization operating Compliant Kubernetes**. ISO-27001-certified Compliant Kubernetes operators, such as [Elastisys](https://elastisys.com) already have the right processes in place.

* S1 - Security Management Process - § 164.308(a)(1)
* S2 - Security Management Process - Risk Analysis - § 164.308(a)(1)(ii)(A)
* S3 - Security Management Process - Risk Management - § 164.308(a)(1)(ii)(B)
* S4 - Security Management Process - Sanction Policy - § 164.308(a)(1)(ii)(C)
* S6 - Assigned Security Responsibility - § 164.308(a)(2)
* S7 - Workforce Security - § 164.308(a)(3)
* S8 - Workforce security - Authorization and/or Supervision - § 164.308(a)(3)(ii)(A)
* S9 - Workforce security - Workforce Clearance Procedure - § 164.308(a)(3)(ii)(B)
* S10 - Workforce security - Establish Termination Procedures - § 164.308(a)(3)(ii)(C)
* S11 - Information Access Management - § 164.308(a)(4)
* S12 - Information Access Management - Isolating Healthcare Clearinghouse Functions - § 164.308(a)(4)(ii)(A)

    !!!important
        Compliant Kubernetes recommends to setting up at least two separate environments: one for testing and one for production.

* S15 - Security Awareness and Training - § 164.308(a)(5)
* S19 - Security Awareness, Training, and Tools - Password Management - § 164.308(a)(5)(ii)(D)
* S21 - Security Incident Procedures - Response and Reporting - § 164.308(a)(6)
* S22 - Contingency Plan - § 164.308(a)(7)
* S25 - Contingency Plan - Emergency Mode Operation Plan - § 164.308(a)(7)(ii)(C)
* S27 - Contingency Plan - Application and Data Criticality Analysis - § 164.308(a)(7)(ii)(E)
* S28 - Evaluation - § 164.308(a)(8)
* S30 - Business Associate Contracts and Other Arrangements - Written Contract or Other Arrangement - § 164.308(b)(4)
* S36 - Workstation Use - § 164.310(b)
* S37 - Workstation Security - § 164.310(c)
* S38 - Device and Media Controls - § 164.310(d)(1)
* S40 - Device and Media Controls - Media Re-use - § 164.310(d)(2)(ii)
* S41 - Device and Media Controls - Accountability - § 164.310(d)(2)(iii)
* S42 - Device and Media Controls - Data Backup and Storage Procedures - § 164.310(d)(2)(iv)
* S46 - Access Control - Automatic Logoff - § 164.312(a)(2)(iii)

    !!!important
        Compliant Kubernetes API access is configured so as to require a new OpenID flow every 12 hours.

* S49 - Integrity - § 164.312(c)(1)
* S50 - Integrity - Mechanism to Authenticate ePHI - § 164.312(c)(2)
* S51 - Person or Entity Authentication - § 164.312(d)
