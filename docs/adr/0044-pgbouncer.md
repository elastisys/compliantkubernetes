# PgBouncer feature for PostgreSQL

* Status: Accepted
* Deciders: Arch Meeting
* Date: 2023-10-19

## Context and Problem Statement

We have received a few requests from Application Developers to enable the PgBouncer on our AMS-PostgreSQL services so that they can improve the idle connection and short-lived connections at the database server and other use-cases.

Should we enable the PgBouncer feature in our postgreSQL offering , or should we offer an alternative?

## Decision Drivers

* We want to maintain Platform security and stability.
* We want to find a solution which is scalable and minimizes Platform Administrator burden.
* We want to best serve the Application Developers.
* We want to make the Platform Administrator life easier.

## Considered Options

1. We can enable the PgBouncer feature as our upstream postgres-operator has `PgBouncer` as a default connection pooler.

    - `Good`, because we satisfy the Application Developers need and are easily configurable.
    - `Bad`, because upstream postgres-operator doesn't allow custom configuration settings like `securityContext`,`serviceAccountName`, `nodeAffinty` and so default values allows the PgBouncer to run in restricted environment.
    - `Bad`, because upstream postgres-operator allows only limited set of parameters to configure [connection-pooler](https://github.com/zalando/postgres-operator/blob/master/docs/reference/operator_parameters.md#connection-pooler-configuration).
    - `Bad`, because the PgBouncer image used by upstream postgres-operator is not open-source yet which can add more security risks, control and transparency issues. See [here](https://github.com/zalando/postgres-operator/issues/1964).

2. We don't enable the PgBouncer feature and instead we provide the documentation on how to configure, so Application Developers can configure themselves.

    - `Good`, because we keep our postgres services much simpler and don't have to do any changes/work.
    - `Good`, because the integrity, security and stability of the platform is kept intact.
    - `Good`, because we still satisfy the Application Developers need by providing the documentation on how to configure it.

## Decision Outcome

Chosen option: 2

After careful evaluation and analysis, we have decided not to offer PgBouncer as a part of our postgreSQL offering and instead provide the public documentation for Application Developers how to configure it. See [here](https://github.com/elastisys/compliantkubernetes/pull/714/files)

We will continue to monitor our upstream [postgres-operator](https://github.com/zalando/postgres-operator/tree/master) features and once our security concerns are addressed in upstreams, We may revisit this decision as needed to ensure it aligns with our evolving requirements.

### Positive Consequences

* We don't increase the operational complexity.
* We avoid the security theatre.

## Links

* [postgres-operator](https://github.com/zalando/postgres-operator/tree/master)
* [pgbouncer](https://github.com/pgbouncer/pgbouncer)
