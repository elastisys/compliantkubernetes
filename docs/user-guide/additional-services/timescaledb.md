TimescaleDB®
============

!!! elastisys "For Elastisys Managed Services Customers"

    You can order Managed TimescaleDB® Community by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/customer/portals). Here are the highlights:

    * **Business continuity**:
        * Standard Plan is configured with two replicas (one primary and one standby).
        * Premium Plan is configured with three replicas (one primary and two standby-s).
    * **Disaster recovery**:
        * Backup scope includes user definitions, data definitions, and the data per-se.
        * A full backup is taken every day between 0:00 am and 6:00 am CET. The backup retention period is 30 days unless otherwise requested by the customer.
        * Point-in-Time Recovery (PITR) is provided for the last 7 days with a recovery point objective of 5 minutes.
        * Long-term backup schemes can be enabled after discussion with the customer.
    * **Only open-source features are included**
    * **Monitoring, security patching and incident management**: included.

    For more information, please read [ToS Appendix 3 Managed Additional Service Specification](https://elastisys.com/legal/terms-of-service/#appendix-3-managed-additional-service-specification).

<figure>
    <img alt="TimescaleDB Deployment Model" src="../img/timescaledb.drawio.svg" >
    <figcaption>
        <strong>TimescaleDB on Compliant Kubernetes Deployment Model</strong>
        <br>
        This help you build a mental model on how to access TimescaleDB as an Application Developer and how to connect your application to TimescaleDB.
    </figcaption>
</figure>

This page will help you succeed in connecting your application to the time-series database TimescaleDB which meets your security and compliance requirements.

TimescaleDB is an extension on top of our managed PostgreSQL.
This means that your administrator will be setting up a complete PostgreSQL cluster for you and you just use it for TimescaleDB via the TimescaleDB extension.

!!!Note
    TimescaleDB is not a viable option for collecting all metrics from the Kubernetes cluster. The data is uncompressed and would take a lot of space to store and use a lot of resources to analyze, unless you want to use it with a very short retention period.
    This is not usually a problem for collecting application specific metrics, since they are not as many as the metrics that are generated from the Kubernetes cluster.

!!!important
    Due to very different performance-tuning characteristics, Timescale and PostgreSQL databases should never run on the same PostgreSQL cluster.
    To comply with this, it is essential that every PostgreSQL database that gets created on the PostgreSQL cluster also has the Timescale extension created for it.

If you want to use TimescaleDB on your Compliant Kubernetes cluster, ask your administrator to [provision a new standard PostgreSQL cluster](timescaledb.md#provision-a-new-postgresql-cluster) inside your Compliant Kubernetes environment. Then set up the TimescaleDB extension.

{%
    include "./postgresql.md"
    start="<!--postgresql-setup-start-->"
    end="<!--postgresql-setup-end-->"
%}

## Set up the TimescaleDB extension on PostgreSQL

* Connect to the created database:
```bash
\c $APP_DATABASE
```
* Add the TimescaleDB extension:
```bash
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

## Follow the Go-Live Checklist

You should be all set.
Before going into production, don't forget to go through the [go-live checklist](../go-live.md).

## CK8S TimescaleDB Release Notes

Check out the [release notes](../../release-notes/postgres.md) for the TimescaleDB/PostgreSQL cluster that runs in Compliant Kubernetes environments!

## Further Reading

* [Getting started with Timescale](https://docs.timescale.com/getting-started/latest/)
* [Creating users](https://www.postgresql.org/docs/13/sql-createuser.html)
* [Creating databases](https://www.postgresql.org/docs/13/sql-createdatabase.html) - Remember to [create Timescale extension](timescaledb.md#set-up-the-timescaledb-extension-on-postgresql) on the new databases.
* [Granting permissions](https://www.postgresql.org/docs/13/sql-grant.html)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
