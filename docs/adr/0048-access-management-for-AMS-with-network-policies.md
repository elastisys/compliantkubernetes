# Access Management for Additional Managed Services (AMS)- Redis

* Status: Accepted
* Deciders: Arch Meeting
* Date: 2024-01-19

## Context and Problem Statement

Elastisys is working around the clock to improve the security of our platform, so as to allow you to better protect Personal Data. Currently, we don't have the access management for the AMS-Redis i.e how these are supposed to be accessed by pods that are deployed by application developers.

We are considering network policies for AMS-Redis to enhance security and control. A key aspect of this change concerns how these services, such as our additional managed Redis instances, interact with applications deployed by you.

How should the access be managed and how should it be communicated to the application developers so that we have a smooth transition?

## Decision Drivers

* We want to maintain Platform security and stability.
* We want to find a solution which is scalable and minimizes Platform Administrator burden.
* We want to best serve the Application Developers.
* We want to make the Platform Administrator life easier.

## Considered Options

1. Allow Specific AMS-Redis Namespace Labels

    - `Good`, because we have precise control over which namespaces can access the AMS-Redis, enhancing security.
    - `Good` because labels clearly indicate intent for access, making policy enforcement and audits simpler.
    - `Bad`, because it requires manual labelling of namespaces, which can be cumbersome in large environments.

2. Give Application Developers a heads up before deploying the new AMS-Redis Release with network policies enabled and let Application Developers label the namespaces they Want to communicate with AMS-Redis.

    - `Good`, because Application Developers will have the freedom to choose which namespaces need access, promoting responsibility and autonomy.
    - `Good`, because notification from us will allow developers to prepare and avoid sudden access issues upon AMS-Redis deployment.
    - `Bad`, because some developers might overlook the communication, leading to inconsistencies in access management.

3. Still Give Application Developers a heads up but we label all the Application Developer namespaces that already exist and let them add and remove labels after the deployment.

    - `Good`, because it ensures all current applications maintain access post-deployment of AMS-Redis new release, preventing service disruptions.
    - `Bad`, because initially grants broad access, potentially exposing AMS-Redis to namespaces that no longer require it.

4. Allow Application Developer Namespace Labels

    - `Good`, because it simplifies the process for developers, as they can use existing namespace labels without needing specific AMS-Redis labels.
    - `Bad`, because it does not offer fine-grained access control specifically for AMS-Redis, potentially leading to broader than necessary access.

5. Allow All Namespaces in Cluster

    - `Good`, because it ensures all namespaces have immediate access to AMS-Redis, simplifying connectivity and integration.
    - `Bad`, because it significantly increases the risk of unauthorized access, making AMS-Redis vulnerable to potential breaches.


## Decision Outcome

**Access Management Strategy:**

Chosen option 1 & 2 i.e We will allow specific AMS-Redis pod labels, specifically `elastisys.io/redis-<redis-cluster-name>-access: allow` and Application developers need to add the labels to their existing application pods with `elastisys.io/redis-<redis-cluster-name>-access: allow` to ensure continuity.

This label will enable communication between your application pods and the designated AMS-Redis.

**For New Redis Clusters Ordered:**

Network Policy will be enabled by default. You will need to actively label your application pods with `elastisys.io/redis-<redis-cluster-name>-access: allow` to gain access to our AMS-Redis.

**For Existing Redis Clusters:**

The implementation will be an opt-in process.

Application developers need to add the labels to their existing application pods with `elastisys.io/redis-<redis-cluster-name>-access: allow` to ensure continuity.

Application developers need to get back to Elastisys when they are done so that we can enforce the changes on our end.

### Positive Consequences

* There will be no sudden disruption in communication between your applications and our AMS-Redis.
* We don't increase the operational complexity.
* We avoid the security theatre.
* This approach not only enhances security but also gives you greater control over which applications can communicate with our managed services. Among others, this facilitates compliance with:
  - GDPR Art. 32 “Security of Processing”;
  - ISO 27001:2022 Annex A Control 8.22 “Segregation of Networks”.

### Negative Consequences

* Initial overhead for Application Developers.
* With some responsibility shifted to developers, there's a risk of misconfiguration like incorrectly labelled namespaces could deny access to AMS-Redis.
