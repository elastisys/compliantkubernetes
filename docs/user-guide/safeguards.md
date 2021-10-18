# Safeguards

> "Det ska vara lätt att göra rätt." (English: "It should be easy to do it right.")

We know you care about the security and uptime of your application. But all that effort goes wasted if the platform allows you to make trivial mistakes.

That is why Compliant Kubernetes is built with various safeguards, to allow you to make security and reliability easy for you.

## Reduce blast radius: Preventing forgotten roots

* Context
* Problem
* Solution
* Error
* Resolution

!!!note
    This section helps you implement ISO 27001 [A.12.6.1 Management of Technical Vulnerabilities](https://www.isms.online/iso-27001/annex-a-12-operations-security/).

Many container runtimes and operating system vulnerabilities need code running as root to become a threat. To minimize this risk, application should only run as root when strictly necessary.

Unfortunately, many Dockerfiles -- and container base images -- today are shipped running as root by default. This makes it easy to slip code running as root into production, exposing personal data to unnecessary risks.

To reduce blast radius, Compliant Kubernetes will protect you from accidentally deploying application running as root.

## Reduce blast radius: Application Firewall

```error
Error: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-networkpolicy] No matching networkpolicy found
```

## Avoid vulnerable container images

```error
Error: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-harbor-repo] container "ck8s-user-demo" has an invalid image repo "harbor.example.com/demo/ck8s-user-demo:1.16.0", allowed repos are ["harbor.cksc.a1ck.io"]
```


## Avoid downtime with Resource Requests

```error
Error: UPGRADE FAILED: failed to create resource: admission webhook "validation.gatekeeper.sh" denied the request: [denied by require-resource-requests] Container "ck8s-user-demo" has no resource requests
```

## Relevant Regulations

* [GDPR Article 32](https://gdpr-info.eu/art-32-gdpr/):

    > Taking into account the state of the art [...] the controller and the processor shall implement [...] as appropriate [...] a process for regularly testing, assessing and evaluating the effectiveness of technical and organisational measures for ensuring the security of the processing.
    >
    > In assessing the appropriate level of security account shall be taken in particular of the risks that are presented by processing, in particular from accidental or unlawful destruction, loss, alteration, **unauthorised disclosure of, or access to personal data transmitted**, stored or otherwise processed. [highlights added]
