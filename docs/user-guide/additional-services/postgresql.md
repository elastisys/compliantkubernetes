PostgreSQL®
===========

!!! elastisys "For Elastisys Managed Services Customers"

    You can order Managed PostgreSQL® by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/). Here are the highlights:

    * **Business continuity**:
        * Standard Plan is configured with two replicas (one primary and one standby).
        * Premium Plan is configured with three replicas (one primary and two standby-s).
    * **Disaster recovery**:
        * Backup scope includes user definitions, data definitions, and the data per-se.
        * A full backup is taken every day between 0:00 am and 6:00 am CET. The backup retention period is 30 days unless otherwise requested by the customer.
        * Point-in-Time Recovery (PITR) is provided for the last 7 days with a recovery point objective of 5 minutes.
        * Long-term backup schemes can be enabled after discussion with the customer.
    * **Monitoring, security patching and incident management**: included.

    For more information, please read [ToS Appendix 3 Managed Additional Service Specification](https://elastisys.com/legal/terms-of-service/#appendix-3-managed-additional-service-specification).

<figure>
    <img alt="PostgreSQL Deployment Model" src="../img/postgresql.drawio.svg" >
    <figcaption>
        <strong>PostgreSQL on Compliant Kubernetes Deployment Model</strong>
        <br>
        This help you build a mental model on how to access PostgreSQL as an Application Developer and how to connect your application to PostgreSQL.
    </figcaption>
</figure>

This page will help you succeed in connecting your application to a primary relational database PostgreSQL which meets your security and compliance requirements.

<!--postgresql-setup-start-->

## Install Prerequisites

Before continuing, make sure you have access to the Kubernetes API, as describe [here](../prepare.md).

Make sure to install the PostgreSQL client on your workstation. On Ubuntu, this can be achieved as follows:

```bash
sudo apt-get install postgresql-client
```

## Getting Access

Your administrator will set up a Secret inside Compliant Kubernetes, which contains all information you need to access your PostgreSQL cluster.
The Secret has the following shape:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: $SECRET
  namespace: $NAMESPACE
stringData:
  # PGHOST represents a cluster-scoped DNS name or IP, which only makes sense inside the Kubernetes cluster.
  # E.g., postgresql1.postgres-system.svc.cluster.local
  PGHOST: $PGHOST

  # These fields map to the environment variables consumed by psql.
  # Ref https://www.postgresql.org/docs/13/libpq-envars.html
  PGUSER: $PGUSER
  PGPASSWORD: $PGPASSWORD
  PGSSLMODE: $PGSSLMODE

  # This is the Kubernetes Service name to which you can port-foward to in order to get access to the PostgreSQL cluster from outside the Kubernetes cluster.
  # Ref https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/
  USER_ACCESS: $USER_ACCESS
```

!!!important
    The Secret is very precious! Prefer not to persist any information extracted from it, as shown below.

To extract this information, proceed as follows:

```bash
export SECRET=            # Get this from your administrator
export NAMESPACE=         # Get this from your administrator

export PGHOST=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.PGHOST}' | base64 --decode)
export PGUSER=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.PGUSER}' | base64 --decode)
export PGPASSWORD=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.PGPASSWORD}' | base64 --decode)
export PGSSLMODE=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.PGSSLMODE}' | base64 --decode)
export USER_ACCESS=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.USER_ACCESS}' | base64 --decode)
```

!!!important
    Do not configure your application with the PostgreSQL admin username and password. Since the application will get too much permission, this will likely violate your access control policy.

!!!important
    If you change the password for $PGUSER, you are responsible for keeping track of the new password.

## Create an Application User

First, in one console, fetch the information from the access Secret as described above and port forward into the PostgreSQL master.

```bash
kubectl -n $NAMESPACE port-forward svc/$USER_ACCESS 5432
```

!!!important
    Since humans are bad at generating random passwords, we recommend using [pwgen](https://linux.die.net/man/1/pwgen).

Second, in another console, fetch the information from the access Secret again and run the PostgreSQL client to create the application database and user:

```bash
export APP_DATABASE=myapp
export APP_USERNAME=myapp
export APP_PASSWORD=$(pwgen 32)

cat <<EOF | psql -d postgres -h 127.0.0.1 -U $PGUSER \
    --set=APP_DATABASE=$APP_DATABASE \
    --set=APP_USERNAME=$APP_USERNAME \
    --set=APP_PASSWORD=$APP_PASSWORD
create database :APP_DATABASE;
create user :APP_USERNAME with encrypted password ':APP_PASSWORD';
grant all privileges on database :APP_DATABASE to :APP_USERNAME;
EOF
```

Continue with the second console in the next section to create a Secret with this information.

## Create an Application Secret

First, check that you are on the right Compliant Kubernetes cluster, in the right **application** namespace:

```bash
kubectl get nodes
kubectl config view --minify --output 'jsonpath={..namespace}'; echo
```

Now, create a Kubernetes Secret in your application namespace to store the PostgreSQL application username and password. For consistency, prefer sticking to naming connection parameters as the [environment variables consumed by psql](https://www.postgresql.org/docs/13/libpq-envars.html).

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
    name: app-postgresql-secret
type: Opaque
stringData:
    PGHOST: ${PGHOST}
    PGPORT: '5432'
    PGSSLMODE: ${PGSSLMODE}
    PGUSER: ${APP_USERNAME}
    PGPASSWORD: ${APP_PASSWORD}
    PGDATABASE: ${APP_DATABASE}
EOF
```

!!!warning
    Although most client libraries follow the `libpq` definition of these environment variables, some do not, and this will require changes to the application Secret.

    Notably [`node-postgres`](https://github.com/brianc/node-postgres) does not currently do so for `PGSSLMODE`.
    When this variable is set to `require`, it will do a full verification instead, requiring access to the PostgreSQL certificates to allow a connection.
    To get the intended mode for `require` set the variable to `no-verify` instead.

## Expose PostgreSQL credentials to Your Application

To expose the PostgreSQL cluster credentials to your application, follow one of the following upstream documentation:

* [Create a Pod that has access to the secret data through a Volume](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#create-a-pod-that-has-access-to-the-secret-data-through-a-volume)
* [Define container environment variables using Secret data](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/#define-container-environment-variables-using-secret-data)

<!--postgresql-setup-end-->

## Follow the Go-Live Checklist

You should be all set.
Before going into production, don't forget to go through the [go-live checklist](../go-live.md).

## CK8S PostgreSQL Release Notes

Check out the [release notes](../../release-notes/postgres.md) for the PostgreSQL cluster that runs in Compliant Kubernetes environments!

## Further Reading

* [Creating users](https://www.postgresql.org/docs/13/sql-createuser.html)
* [Creating databases](https://www.postgresql.org/docs/13/sql-createdatabase.html)
* [Granting permissions](https://www.postgresql.org/docs/13/sql-grant.html)
* [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
