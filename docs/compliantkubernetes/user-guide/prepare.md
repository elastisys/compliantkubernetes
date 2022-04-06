---
description: Learn how to prepare for Elastisys Compliant Kubernetes, the security-hardened Kubernetes distribution
---

# Step 1: Prepare

Hi there, Application Developer! Happy to have you on board with Elastisys Compliant Kubernetes!

In this part, you will learn about the things you should do to prepare to get started with the platform.

We assume somebody else, your administrator, has already set up the platform for you. You will therefore have received:

{%
    include "setup.md"
    start="<!--bill-of-materials-service-start-->"
    end="<!--bill-of-materials-service-end-->"
%}

Do you not already have an Elastisys Compliant Kubernetes platform up and running? Request one from [a managed service provider](https://elastisys.com/) and get started!

## Install Prerequisite Software

{%
    include "setup.md"
    start="<!--prerequisite-software-start-->"
    end="<!--prerequisite-software-end-->"
%}

Once installed, you can verify that configuration is correct by [issuing a few simple commands](setup.md).

## Access Your Web Portals

Those URLs that your Elastisys Compliant Kubernetes administrator gave you all have a `$DOMAIN`, which will typically include your company name and perhaps the environment name.

Your web portals are available at:

* `harbor.$DOMAIN` -- the Harbor container image registry, which will be the home to all your container images
* `opensearch.$DOMAIN` -- the OpenSearch Dashboards portal, where you will view your application and audit logs
* `grafana.$DOMAIN` -- the Grafana portal, where you will view your monitoring metrics for both the platform, as such, and your application-specific metrics

## Containerize Your Application

Elastisys Compliant Kubernetes runs containerized applications in a Kubernetes platform. It is a Certified Kubernetes distribution, which means that if an application is possible to deploy on a standard Kubernetes environment, it can be deployed on Elastisys Compliant Kubernetes.

However, there are some restrictions in place for security reasons. In particular, **containers cannot be run as root**. Following this [best practice](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user) is a simple way to ensure additional security for your containerized applications deployed in Kubernetes.

There are additional safeguards in place that reflect the security posture of Elastisys Compliant Kubernetes that impact your application. These prevent users from doing potentially unsafe things. In particular, users are not allowed to:

{%
    include "demarcation.md"
    start="<!--safeguards-start-->"
    end="<!--safeguards-end-->"
%}

## Next step? Deploying!

Ready with a contianerized application? Head over to the next step, where you learn how to [deploy](deploy.md) it!
