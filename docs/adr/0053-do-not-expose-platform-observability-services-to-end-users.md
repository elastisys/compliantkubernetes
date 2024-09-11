# Do not expose platform observability services to end-users

- Status: Accepted
- Deciders: Product team
- Date: 2024-04-04

## Context and Problem Statement

We are being asked whether we can manage observability data (logs, metrics, traces) from external and/or public clients, ensuring secure ingestion of data into our platform observability stack (OpenSearch for logs, Prometheus for metrics, and Jaeger for traces). There are two distinct categories of clients sending observability data:

**External Clients:** Systems or services under the control of Application Developers, such as VMs or servers running in trusted environments like Safespring etc. External clients can authenticate using an API key or equivalent.

**Public Clients:** Applications that run on devices or in browsers that are not under the control of Application Developers, such as mobile apps (Flutter) and Single-Page Applications (Angular), which are exposed to the public internet. Public clients cannot be authenticated using an API key or equivalent, since that API key could be easily extracted from the public client.

The core problem is how to securely manage the ingestion of observability data from both external and public clients into the platform observability stack.

- Can we allow external clients to push observability data directly to our platform observability services?
- Can we allow public clients (e.g., mobile apps, SPAs) to push observability data directly to our platform observability services?

## Decision Drivers

- We want to maintain platform security and stability.
- We want to avoid operational complexity.
- We want to best serve the Application Developers.
- We want to make the Platform Administrator life easier.

## Considered Options

1. Do not allow public clients to push data directly to our platform observability services but allow external clients with authentication and authorization mechanisms.

1. Allow public and external clients to push data directly to our platform observability services.

## Decision Outcome

**Chosen Option:** Option 1: Do not allow public clients to push data directly to our platform observability services but allow external clients with authentication and authorization mechanisms.

**External Clients:**
We will allow external clients to push observability data (logs, metrics, traces) directly into our platform observability services under the following conditions:

- **Logs:** External clients can push logs to our OpenSearch service with authentication and authorization mechanisms. However, as per our [ToS-A5.3 As a whole, for the intended use-case](https://elastisys.com/legal/terms-of-service/#a53-as-a-whole-for-the-intended-use-case), OpenSearch is optimized for platform and containerized application observability which means logs are expected to come from the application running in the workload cluster, and external logs should align with this use-case, with exceptions allowed for observability of legacy code that brings business value to the workload cluster.
- **Metrics:** External clients can push metrics to a Prometheus Pushgateway, which Prometheus scrapes periodically.
- **Traces:** While we do not currently support traces from external clients, we may explore the option of allowing external clients to push traces to an OpenTelemetry collector in our platform observability services.

**Additional Considerations Note**
In accordance with our [ToS-A5.3 As a whole, for the intended use-case](https://elastisys.com/legal/terms-of-service/#a53-as-a-whole-for-the-intended-use-case), please note the following:

- It is critical to acknowledge that while these components (OpenSearch, Prometheus) are technically capable of handling external clients, our platform observability services is designed and optimized to function as a secure platform for containerized applications. Using these components in isolation or for other use-cases introduces unknown risks, and such configurations are not covered by the Self-managed Plan. Therefore, support for external clients observability data is limited to Application Developers compliance with the intended use-case of our platform observability services.
- Authentication and authorization mechanisms will be in place to ensure only trusted external clients can send observability data. Any use of these services outside of the intended platform observability scope may not be supported by the platform.

**Public Clients:**
We will not allow public clients to push observability data directly to platform observability services for the following reasons:

- **System Design** We assessed that the systems we use (Jaeger, OpenSearch, Prometheus) are not designed for public clients.
- **Security Risks:** Embedding authentication credentials in client-side code (e.g., in a mobile app or web app) exposes them to the public, making it easy for attackers to intercept and misuse those credentials. This poses a significant risk to the security of our platform.
- **Data Leakage:** Publicly exposing observability endpoints (such as OpenSearch, Prometheus, or Jaeger) could lead to sensitive data leaks.

**General Recommendation - Secure forwarding approach for public clients:**
We recommend that Application Developers route observability data through a secure backend API that authenticates logged-in users to significantly reduce the attack surface, forwards the data to our platform observability services for processing, and thus it ensures that our sensitive observability endpoints remain protected from public exposure.

### Security considerations for End-User access

- We also concluded that our platform observability stack (OpenSearch, OpenSearch Dashboards, Thanos, and Grafana) is strictly intended for **application and platform observability** by Application Developers and Platform Administrators. These services are **not meant to be accessed by end-users, either directly or indirectly**, as this would pose significant security risks, not just performance concerns. This could expose our internal platform data, potentially compromising the security of our entire platform. We do not trust the isolation of these observability components to the extent of granting access to end-users.

- Allowing end-users access to these observability services violates our secure design principles. Even if the isolation mechanisms of these services were trusted, exposing them to end-users would not align with our secure platform design. The risk is not limited to performance degradation but extends to the core security posture of our platform.

- **Conclusion:** So if the end-users require direct or indirect access to our platform observability services (e.g., Grafana), these should be considered **application components** rather than platform components. In such cases, Application Developers should install and manage these components in a **self-service manner within the Workload Cluster**, separate from our core platform observability services.

### Positive Consequences

- It reduces the risk of unauthorized access to our platform observability services, protecting the cluster from data leaks, credential abuse, and DoS attacks.
- By routing observable data from public clients through a backend API, we maintain control over the data flow and can apply additional security measures, such as logging and throttling.
- We can selectively allow trusted external services to push observability data directly, without exposing our platform observability services to the broader internet.

### Negative Consequences

- Implementing a secure backend API for public clients adds complexity to the system and increases the workload for Application Developers.
- Routing observability data through a backend API may introduce some delays compared to direct ingestion.

## Pros and Cons of the Options <!-- optional -->

### Option 1

- Good, because embedding credentials in public-facing apps exposes our infrastructure to potential attacks, while trusted external clients are allowed to push data directly with proper authentication and authorization mechanisms, ensuring security without sacrificing performance for external clients.
- Good, because public clients, which are less trusted, must route data through a backend API developed by Application Developers, ensuring secure data handling, whereas external clients can push data directly to the platform observability services without the latency that public clients experience due to the intermediary backend API.
- Good, because directly exposing observability endpoints to public clients could lead to data leakage, compromising sensitive information.
- Bad, because it might require the development, maintenance to allow external clients to push data to our platform observability services.

### Option 2

- Good, because direct ingestion allows for immediate observability from both public and external clients, which enables faster insights and issue resolution.
- Bad, because public clients expose sensitive credentials (e.g., API keys or tokens), making them vulnerable to theft and misuse by attackers.
- Bad, because unauthorized access t our platform observability services could lead to data breaches or system compromise.
- Bad, because public clients could overwhelm platform observability services with large volumes of requests or malicious data, causing performance degradation and potential service outages.

## Links

- [opentelemetry-collector](https://medium.com/opentelemetry/securing-your-opentelemetry-collector-1a4f9fa5bd6f)
- [k8s-otel-expose](https://opentelemetry.io/blog/2022/k8s-otel-expose/)
- [deployment](https://opentelemetry.io/docs/collector/deployment/)
- [Data-leakage](https://www.oxeye.io/resources/how-insecure-application-tracing-and-telemetry-may-lead-to-sensitive-data-and-pii-leakage)
- [ToS-A5.3 As a whole, for the intended use-case](https://elastisys.com/legal/terms-of-service/#a53-as-a-whole-for-the-intended-use-case)
