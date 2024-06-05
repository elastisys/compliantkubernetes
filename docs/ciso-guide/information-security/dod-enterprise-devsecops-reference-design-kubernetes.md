# DoD Enterprise DevSecOps Reference Design for Kubernetes

This page highlights the project's commitment to security best practices
by comparing it to the US Department of Defense's DevSecOps Reference
design. 
The section is based on the document entitled "DoD Enterprise DevSecOps Reference Design: CNCF Kubernetes", version 2.0, published in March 2021 ([PDF download link](https://dl.dod.cyber.mil/wp-content/uploads/devsecops/pdf/DoD-Enterprise-DevSecOps-Reference-Design-v2.0-CNCF-Kubernetes.pdf)).

## Disclaimer

The DoD Enterprise DevSecOps Reference Design (henceforth referred to as the Reference Design) is a publicly available document, and has had a profound impact on the field. 
However, it also makes references to DoD-specific systems and other DoD or US Military-internal systems, such as:

-   "Iron Bank" container registry and associated requirements
-   "Platform One" Kubernetes platform

The exact properties and the functionality of these systems are not public.

This section is therefore written from the perspective of a typical Compliant Kubernetes application developer that wishes to adhere to the best practices that are properly and publicly available from the Reference Design.

The rest of this page will go section-by-section through the Reference Design and map it to Compliant Kubernetes.

## Section 1, Introduction

The first section of the Reference Design defines the background, purpose, and scope of the document. 
It also lists the intended audience and how the document relates to others in the same suite.

## Section 2, Assumptions and Principles

The second section of the Reference Design clarifies assumptions and principles.
These are addressed in the following list:

-   Compliant Kubernetes [is a Certified Kubernetes distribution](https://landscape.cncf.io/?item=platform--certified-kubernetes-distribution--elastisys-compliant-kubernetes).
-   Compliant Kubernetes has no vendor-specific tooling, instead opting for pure open source that is portable and avoids vendor lock-in (as per [ADR-0015](https://elastisys.io/compliantkubernetes/adr/0015-we-believe-in-community-driven-open-source/)).
-   Compliant Kubernetes does not dictate a particular definition of "hardened containers". Instead, Compliant Kubernetes puts multiple important safeguards in place, such as:
    -   [forbidding containers to run as root](https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-no-root/);
    -   mandating [adherence to the Restricted Pod Security Standard](https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-podsecuritypolicies/);
    -   requiring [microsegmentation via Network Policies](https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-networkpolicies/);
    -   [vulnerability scanning](https://elastisys.io/compliantkubernetes/user-guide/registry/);\
        [intrusion detection](https://elastisys.io/compliantkubernetes/ciso-guide/intrusion-detection/) for running applications; and
    -   requiring container images to be pulled from only [allowlisted container registries](https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-trusted-registries/).

Taken together, these measures provide comprehensive defense in depth.

## Section 3, Software Factory Interconnects

Note that the majority of Section 3 of the Reference Design describes the software distribution that DoD has in place, which is not public.

Table 1 (Page 15) makes it clear that the DoD and the Compliant Kubernetes have divergent views on what is appropriate to run inside a Pod. 
The features listed there make it clear that the sidecar that DoD issues in their environments must run with very high privilege.
Otherwise, features such as rerouting all network traffic via service mesh, scanning the underlying node for vulnerabilities, and adaptively restricting the main container's runtime behavior would simply not be possible.

In the view of Compliant Kubernetes, this means that such a sidecar would *itself* become an attack vector.
By design, it is reachable by the application running within the main container in the Pod.
Given its high level of privilege, it is going to be a highly valuable target.

Instead, Compliant Kubernetes takes a more restrictive approach to containers that run within it.
We add layers upon layers of security ontop of it, and keep it running with low privileges.
This means that allsafeguards put in place work for us, rather than against us.
And we do not circumvent them by putting all our faith in a privileged sidecar.

Table 1 calls out the following named security features, and we describe what we do within that space as follows:

-   **Logging Agent**, for which we use fluentd to forward all logs into the logging system. Going beyond the requirements of the Reference Design, our setup with two clusters ensures that no application in the Workload Cluster can overwrite or modify the logs that are stored in the OpenSearch instance in the Management Cluster. Thereby, we offer tamper-proof logging, which the DoD Reference Design does not.
-   **Logging Storage and Retrieval**, which is what OpenSearch is for.
-   **Log Visualization and Analysis**, which is what OpenSearch Dashboards offer.
-   **Container Policy Enforcement**, which in the DoD Reference Design is about ensuring compliance with the US military's Security Content Automation Protocol (SCAP). In Compliant Kubernetes, the aforementioned safeguards (i.e., [forbidding containers to run as root](https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-no-root/); mandating [adherence to the Restricted Pod Security Standard](https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-podsecuritypolicies/); requiring [microsegmentation via Network Policies](https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-networkpolicies/); providing both [vulnerability scanning](https://elastisys.io/compliantkubernetes/user-guide/registry/) and [intrusion detection](https://elastisys.io/compliantkubernetes/ciso-guide/intrusion-detection/) for applications; and enforcing container images pulls from only [allowlisted container registries](https://elastisys.io/compliantkubernetes/user-guide/safeguards/enforce-trusted-registries/)) provide defense in depth, which is similar in scope.
-   **Runtime Defense**, which in Compliant Kubernetes is offered via the intrusion detection system Falco.
-   **Service Mesh Proxy** and **Service Mesh**, which the document later spells out as offering in-cluster workload identity and network traffic encryption features. In all Kubernetes-integrated service meshes, the workload identity ultimately comes from the Kubernetes API, which means that they are from a security perspective equivalent to the Pod selectors used in e.g. Network Policies: if an attacker can fool or impersonate the Kubernetes API server, no amount of additional use of cryptography will help because the Kubernetes API as source of truth is regarded as authoritative. Network traffic can be encrypted in Compliant Kubernetes by enabling node-to-node encryption in Calico, the CNI of choice. So while Compliant Kubernetes does not ship with a service mesh, it has equivalent workload identity and over-the-wire network security features as one.
-   **Vulnerability Management** and **CVE Service**, for which Compliant Kubernetes includes the Trivy vulnerability scanner for both the Harbor container registry and for scanning the running workloads using the Trivy Operator.
-   **Host Based Security**, which Compliant Kubernetes addresses by making it easy to apply upgrades and to reboot nodes with kured or to replace them, depending on if the cluster is installed via kubespray or Cluster API.
-   **Artifact Repository**, which in Compliant Kubernetes is offered by the Harbor container registry.
-   **Zero Trust Model Down to the Container Level**, which is poorly defined in the Reference Design document, but the table contents suggests that it relates to the features of a Service Mesh, so see that bullet for the answer.

## Section 4, Software Factory Kubernetes Reference Design

Section 4 of the Reference Design is highly DoD-specific, but Application Developers in Compliant Kubernetes are recommended to take inspiration from it in setting up their own CI/CD systems.
As for the final step, deploying to Compliant Kubernetes, it is recommended to either use the [Argo CD additional managed service](https://elastisys.io/compliantkubernetes/user-guide/additional-services/argocd/) or to set up deployment as a final step in a CI system, [as per our instructions](https://elastisys.io/compliantkubernetes/user-guide/ci-cd/).

## Section 5, Additional Tools and Activities

Section 5 of the Reference Design summarizes requirements from other sections and concretizes what is written in a related document, the "DevSeOps Tools and Activities Guidebook" ([version 2.0 PDF from March 2021 download link](https://dodcio.defense.gov/Portals/0/Documents/Library/DevSecOpsTools-ActivitiesGuidebook.pdf)).

### Container Hardening

Application Developers may be interested in extracting the steps and learnings that are not DoD-specific from the "Container Hardening Processing Guide" by DISA and DoD ([version 1, release 2 PDF from August 2022 download link](https://dl.dod.cyber.mil/wp-content/uploads/devsecops/pdf/Final_DevSecOps_Enterprise_Container_Hardening_Guide_1.2.pdf)). 
Disregarding all references to DoD-internal systems the following useful information remains for public consumption:

-   Define a base image that your organization issues and can properly secure.
-   Carry out vulnerability management on the base image. Let changes ripple to all other container images.
-   Ensure code dependencies are available through some means that does not require Internet access, if ability to build cannot be allowed to be compromised by a non-working Internet connection or server availability. Take care to also avoid downloading assets within Dockerfiles, for the same reason.
-   Understand default configuration, because it will be in effect in addition to your explicit configuration. Consider setting all configuration values explicitly, just like it is common practice to set dependencies explicitly. You would rather get an error at startup than strange behavior during runtime.
-   Emit logs to stdout, to make it possible to collect them via a log forwarder.
-   Always run containers as a non-root user.
-   Do not hard-code configuration or secret values, instead opting to get such values via ConfigMaps or Secrets in Kubernetes, injected using one of the standard options: environment variables, arguments, or as files in the Pod.
-   Remove all packages that are not required, since they just add to the attack surface of the container.
-   Consider removing setuid and setgid flags from binaries in your container, in a paranoid addition to requiring Kubernetes Pods to have `allowPrivilegeEscalation` set to false.
-   Scan containers for known vulnerabilities, and have a process in place to prevent ones with unacceptably high scores from being deployed to production. What that means for your organization is up to you.

### General Tools and Activity Advice

-   Using a GitOps-based deployment tool and process is advised, because of three reasons:
    -   Eliminates the need to open ports and to share keys with externally running CI/CD services, such as GitHub Actions.
    -   Eliminates environment configuration drift.
    -   Ensures the desired state is always represented in Git, which (although not mentioned in the Reference Design document) also brings the benefits of clear and non-repudiable auditability, thanks to signed commits.
-   Analyze network flows between components. In Compliant Kubernetes, this is done using the [Jaeger additional managed service](https://elastisys.io/compliantkubernetes/user-guide/additional-services/jaeger/), for applications deployed onto the environment. This is not the same as a full network flow analyzer, because it doesn't work on the low level of capturing all traffic across the entire network. However, it does show to a fine level of detail how applications interact with each other. The fact that it's more focused on application-only traffic may both be a strength or a weakness, depending on perspective.
-   Section 5.1 lists the common advanced deployment strategies: Blue/Green, Canary, Rolling, and Continuous (which is a special case of Rolling). All these can be implemented in Compliant Kubernetes in Argo and with a bit more effort in a manual or scripted way using normal Kubernetes primitives.
-   Section 5.2 is concerned with monitoring, logging, and alerting based on monitoring and logging. These are supported in Compliant Kubernetes, thanks to the Prometheus monitoring stack which includes Alert Manager, and log-based alerting in OpenSearch.

## Summary

This page has shown how Compliant Kubernetes incorporates a large number of the best practices that are described in the "DoD Enterprise DevSecOps Reference Design: CNCF Kubernetes", version 2.0, published in March 2021 ([PDF download link](https://dl.dod.cyber.mil/wp-content/uploads/devsecops/pdf/DoD-Enterprise-DevSecOps-Reference-Design-v2.0-CNCF-Kubernetes.pdf)). 
The most common source of deviation from them is the fact that the Reference Design refers to DoD-internal systems and practices, which are not publicly available, and hence not applicable to organizations outside of the US military.

Applications deployed on Compliant Kubernetes benefit from a comprehensive defense in depth approach on the platform and application runtime level.
Application developers are recommended to harden their containers as described in Section 5, and to release applications using fully automated GitOps.
