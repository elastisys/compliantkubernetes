PgBouncer connection pooler for PostgreSQL (self-managed)
===========

{%
   include-markdown './_common.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

{%
   include-markdown './_common-crds.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

This page will help you to configure [PgBouncer](https://www.pgbouncer.org/faq.html), so that you will be able to quickly configure PgBouncer for the PostgreSQL cluster.

## Installation options

PgBouncer installation options:
1. As a sidecard to the application Pod
1. As a Deployment

Option 1 is recommended to be used when you have 1 application Deployment with 1 to 5 replicas.
Running as a sidecar when the application has more than 5 replicas will lead to resource waste. For example, 20 Pods with 20 PgBouncers sidecars, each using 0.5 CPU and 300M RAM, would consume **6GB RAM**.

Option 2 adds an extra network hop, but it scales better than option 1 if you have many application Deployments that connect to the same database cluster.
This option is not wasting resources as option 1 does.

Recommend using option 2 with 2 or 3 replicas for high load systems.

There are many options from where to pick a PgBouncer image or Helm Chart to use to deploy PgBouncer. We will not cover them here as it is outside the scope of this document.

## Configuration

PgBouncer comes with a configuration file that is `pgbouncer.ini` .
In the `pgbouncer.ini` file you have the configuration options.
Not all of them are listed by default in the images available, but the full list can be seen [here](https://www.pgbouncer.org/config.html)

This file is usually divided into 2 sections that are demarcated using square brackets and the sections are `[databases]` and `[pgbouncer]`.

### Simple configuration:

```console
[databases]
* = host=<Change-Me-to-name-of-postgre-service>.postgres-system port=5432

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 5432
unix_socket_dir =
user = postgres
auth_file = /etc/pgbouncer/userlist.txt
auth_type = plain
pool_mode = transaction
max_client_conn = 3000
ignore_startup_parameters = extra_float_digits
server_tls_sslmode = require

# Log settings
admin_users = postgres
```

Depending on the image that is provided you can have:
- `auth_file = /etc/pgbouncer/userlist.txt` and in this case you need to provide a list of users per database
- or `auth_file = /etc/pgbouncer/auth_file.txt` and in this case you will also have `admin_users = <some-user like-'pooler'>` -> for this to work the user needs to have read access to pg_authid as it will pull the users details from there.

Using the above you will have most of the parameters set to default.
Please be aware that defaults might be overwritten in the PgBouncer image you will use.

### More advanced configuration:

```console
[databases]
<Change-Me-to-Name-of-a-database> = host=<Change-Me-name-of-postgre-service>.postgres-system port=5432 dbname=<Change-Me-to-Name-of-a-database>
* = host=<Change-Me-to-name-of-postgre-service>.postgres-system port=5432

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 5432
unix_socket_dir =
user = postgres
auth_file = /etc/pgbouncer/userlist.txt
auth_type = plain
pool_mode = transaction
max_client_conn = 3000
ignore_startup_parameters = extra_float_digits
server_tls_sslmode = require

# How many server connections to allow per user/database pair.
default_pool_size = 10

# How many additional connections to allow to a pool
reserve_pool_size = 5

# Do not allow more than this many connections per database (regardless of
# pool, i.e. user)
max_db_connections = 30

# If a client has been in "idle in transaction" state longer, it will be
# disconnected. [seconds]
idle_transaction_timeout = 600

# If login failed, because of failure from connect() or authentication that
# pooler waits this much before retrying to connect. Default is 15. [seconds]
server_login_retry = 5

# Log settings
admin_users = postgres
```

The full list of parameters and their default values can be found [here](https://www.pgbouncer.org/config.html)

There you will see that you can configure default values that apply to all users and all databases or you can configure different values for each database and each user individually.

!!! WARNING - Make sure that PostgreSQL "max_connections" is greater than "(default_pool_size * no-of-dbatabases) * no-of-pgbouncers".

If `(default_pool_size * no-of-dbatabases)` is greater then the PostgreSQL `max_connections`, you will end up with errors like `no more connections allowed (max_client_conn)`.

# Recommendations

First decide what pooling type you need based on what your application needs are.
Choose from `session` , `transaction` and `statement`.
Default is `session` and most commonly used is `transaction`.
For advanced configurations you can have default set to `transaction` and in the `[users]` section for a specific user you can set `pool_mode=session` or `pool_mode=statement`.

If you do not have specific uses cases that require you to prioritize one of the databases in the cluster more than the others it is recommended to use simple configuration with default values like the ones mentioned above.

# Further Reading

- [PgBouncer official page](https://www.pgbouncer.org/)
- [PgBouncer Github page](https://github.com/pgbouncer/pgbouncer)
- [PgBouncer config options](https://www.pgbouncer.org/config.html)
