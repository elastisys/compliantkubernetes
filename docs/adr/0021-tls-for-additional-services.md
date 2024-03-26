# Default to TLS for performance-insensitive additional services

- Status: accepted
- Deciders: arch meeting
- Date: 2022-02-16

## Context and Problem Statement

We run additional services in the Workload Cluster, currently databases (PostgreSQL), in-memory caches (Redis) and message queues (RabbitMQ).
Traditionally, when these services are provided as managed services, they are exposed via a TLS-encrypted endpoint. See examples for:

- [Redis](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-nodejs-get-started#create-a-new-nodejs-app) -- notice `rediss://`;
- [RabbitMQ](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/data-protection.html#data-protection-encryption-in-transit);
- [PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html).

In Compliant Kubernetes, the network is assumed trusted, either because we performed a [provider audit](../operator-manual/provider-audit.md) or because we enabled Pod-to-Pod encryption via [WireGuard](https://elastisys.com/redundancy-across-data-centers-with-kubernetes-wireguard-and-rook/). Hence, TLS does not improve data security.

How should we expose additional services in Compliant Kubernetes? With or without TLS?

## Decision Drivers

- We want to stick to best practices and sane defaults.
- We want to make it easy to port applications to Compliant Kubernetes and its additional services.
- Some services are performance-sensitive: Redis [suffers a significant performance drop with TLS](https://dzone.com/articles/redis-tls-can-significantly-reduce-performance-a-l)
- The Spotahome Redis Operator [does not support TLS](https://github.com/spotahome/redis-operator/issues/268).
- Some services are performance-insensitive: PostgreSQL and RabbitMQ feature negligible performance impact with TLS.

## Considered Options

- Always disable TLS, since the network in Compliant Kubernetes is trusted.
- Always enable TLS.
- By default, enable TLS for performance-insensitive services and disable TLS for performance-sensitive services. Allow TLS to be disabled if the user requests it.

## Decision Outcome

Chosen option: "By default, enable TLS for performance-insensitive services and disable TLS for performance-sensitive services. Allow TLS to be disabled if the user requests it."

Specifically:

- Never enable TLS for Redis: Performance impact is huge and the network is already trusted. Furthermore, the Spotahome Redis Operator [does not support TLS](https://github.com/spotahome/redis-operator/issues/268).
- Enable TLS by default for PostgreSQL and RabbitMQ: Performance impact is negligible and most application are already configured for it.
- Allow TLS to be disabled if requested for PostgreSQL and RabbitMQ.
