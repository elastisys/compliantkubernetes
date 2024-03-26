# FerretDB® (self-managed)

{%
   include-markdown './_common.include'
   start='<!--disclaimer-start-->'
   end='<!--disclaimer-end-->'
%}

!!!danger
FerretDB® tries to be a drop-in replacement for MongoDB®. However:

    * There are [known differences](https://docs.ferretdb.io/diff/).
    * There might also be performance implications.

    Make sure to load-test your application with FerretDB before going into production.

[FerretDB](https://www.ferretdb.com/) is a database that is an open-source alternative to MongoDB that uses PostgreSQL as its backend database. This documentation details how to run FerretDB in a Compliant Kubernetes cluster using the Managed [PostgreSQL service](../additional-services/postgresql.md).

## Pushing FerretDB image to Harbor

These instructions will pull the FerretDB container image and push it to another registry. If you are using managed Harbor as your container registry, please follow [these instructions](../deploy.md) on how to authenticate, create a new project, and how to create a robot account and using it in a pull-secret to be able to pull an image from Harbor to your cluster safely:

```sh
TAG=1.0.0
REGISTRY=harbor.$DOMAIN
REGISTRY_PROJECT=demo

docker pull ghcr.io/ferretdb/ferretdb:$TAG
docker tag ghcr.io/ferretdb/ferretdb:$TAG $REGISTRY/$REGISTRY_PROJECT/ferretdb:$TAG
docker push $REGISTRY/$REGISTRY_PROJECT/ferretdb:$TAG
```

## Install

In a managed CK8s environment, follow [these instructions](../additional-services/postgresql.md#getting-access) on how to access the Managed PostgreSQL service and how to create an application user and database.

Create secret containing a PostgreSQL URL to authenticate to the Managed PostgreSQL service and newly created database with the application user credentials:

```sh
kubectl create secret generic --from-literal=ferretdb-url="postgresql://$APP_USERNAME:$APP_PASSWORD@$PGHOST:$PGPORT/$APP_DATABASE" ferretdb-postgres-credentials
```

Deploy:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ferretdb
  labels:
    run: ferretdb
spec:
  replicas: 1
  selector:
    matchLabels:
      run: ferretdb
  template:
    metadata:
      labels:
        run: ferretdb
    spec:
      containers:
        - name: ferretdb
          image: $REGISTRY/$REGISTRY_PROJECT/ferretdb:$TAG # replace this
          args:
            - --listen-addr=0.0.0.0:27017
            - --telemetry=disable
            - --postgresql-url=$(FERRETDB_URL)
          env:
            - name: FERRETDB_URL
              valueFrom:
                secretKeyRef:
                  name: ferretdb-postgres-credentials
                  key: ferretdb-url
          resources:
            requests:
              cpu: "1000m"
              memory: "15M"
          securityContext:
            capabilities:
              drop:
                - ALL
            runAsNonRoot: true
            runAsUser: 1001
          volumeMounts:
            - mountPath: /state
              name: state
      securityContext:
        fsGroup: 1001
      volumes:
        - name: state
          emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: ferretdb-service
  labels:
    run: ferretdb
spec:
  type: ClusterIP
  selector:
    run: ferretdb
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
```

Check that FerretDB started properly:

```console
$ kubectl get svc,deploy,pod -l run=ferretdb
NAME                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)     AGE
service/ferretdb-service   ClusterIP   10.233.42.102   <none>        27017/TCP   75s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ferretdb   1/1     1            1           75s

NAME                            READY   STATUS    RESTARTS   AGE
pod/ferretdb-5887cc848c-brwjf   1/1     Running   0          75s
```

The Deployment should show `STATUS` is `Running`. The Pod(s) should have `STATUS` is `Running`.

To try out access to FerretDB, you can port-forward the Service to localhost and connect using mongosh:

```sh
kubectl port-forward svc/ferretdb-service 27017

mongosh mongodb://localhost:27017
```

## Python client example

The following is an example of how to connect to FerretDB using the [PyMongo](https://pymongo.readthedocs.io/en/stable/) Python library (using the localhost port-forwarding described above).

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

# List all databases
print(client.list_database_names())

# List collections in the database "mongodb"
print(client['mongodb'].list_collection_names())

# Create db and insert element into a collection
database   = client['test_db']
collection = database['customers']

mydict = { "name": "John", "address": "Highway 38" }

collection.insert_one(mydict)
print(collection.find_one())
```

See the following `pg_dump` below to see how the example above is mapped in the actual backend Postgres database.

<details>
<summary>pg_dump</summary>

```sql
--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6 (Ubuntu 14.6-1.pgdg22.04+1)
-- Dumped by pg_dump version 15.1 (Ubuntu 15.1-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: test_db; Type: SCHEMA; Schema: -; Owner: ferretdb
--

CREATE SCHEMA test_db;


ALTER SCHEMA test_db OWNER TO ferretdb;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: _ferretdb_database_metadata; Type: TABLE; Schema: test_db; Owner: ferretdb
--

CREATE TABLE test_db._ferretdb_database_metadata (
    _jsonb jsonb
);


ALTER TABLE test_db._ferretdb_database_metadata OWNER TO ferretdb;

--
-- Name: customers_c09344de; Type: TABLE; Schema: test_db; Owner: ferretdb
--

CREATE TABLE test_db.customers_c09344de (
    _jsonb jsonb
);


ALTER TABLE test_db.customers_c09344de OWNER TO ferretdb;

--
-- Data for Name: _ferretdb_database_metadata; Type: TABLE DATA; Schema: test_db; Owner: ferretdb
--

COPY test_db._ferretdb_database_metadata (_jsonb) FROM stdin;
{"$s": {"p": {"_id": {"t": "string"}, "table": {"t": "string"}, "indexes": {"i": [{"t": "object", "$s": {"p": {"key": {"t": "object", "$s": {"p": {"_id": {"t": "int"}}, "$k": ["_id"]}}, "name": {"t": "string"}, "unique": {"t": "bool"}, "pgindex": {"t": "string"}}, "$k": ["pgindex", "name", "key", "unique"]}}], "t": "array"}}, "$k": ["_id", "table", "indexes"]}, "_id": "customers", "table": "customers_c09344de", "indexes": [{"key": {"_id": 1}, "name": "_id_", "unique": true, "pgindex": "customers__id__e06693c2_idx"}]}
\.


--
-- Data for Name: customers_c09344de; Type: TABLE DATA; Schema: test_db; Owner: ferretdb
--

COPY test_db.customers_c09344de (_jsonb) FROM stdin;
{"$s": {"p": {"_id": {"t": "objectId"}, "name": {"t": "string"}, "address": {"t": "string"}}, "$k": ["_id", "name", "address"]}, "_id": "6454cd232da4567e5cd31f39", "name": "John", "address": "Highway 37"}
\.


--
-- Name: _ferretdb_database_metadata_id_idx; Type: INDEX; Schema: test_db; Owner: ferretdb
--

CREATE UNIQUE INDEX _ferretdb_database_metadata_id_idx ON test_db._ferretdb_database_metadata USING btree (((_jsonb -> '_id'::text)));


--
-- Name: customers__id__e06693c2_idx; Type: INDEX; Schema: test_db; Owner: ferretdb
--

CREATE UNIQUE INDEX customers__id__e06693c2_idx ON test_db.customers_c09344de USING btree (((_jsonb -> '_id'::text)));


--
-- PostgreSQL database dump complete
--
```

</details>

## Security

FerretDB supports securing connections between FerretDB and client with TLS. All you need is to specify additional run-time arguments or environment variables, as described in the [FerretDB documentation](https://docs.ferretdb.io/security/).

## Known Issues / Limitations

- FerretDB currently does not support user management.
- FerretDB currently does not support role management.
- FerretDB currently does not allow for optimizations or tweaks to the underlying PostgreSQL schema that is used by FerretDB as it translates MongoDB collections to PostgreSQL tables.

> **Note** <br/>
> As of May 2023, the project was recently released to its first major version (v1.0.0) and is constantly being developed and improved, hence, these issues may have already been solved depending on when you are reading this. Check [supported commands](https://docs.ferretdb.io/reference/supported-commands/) for FerretDB to see what is currently available.

## Further Reading

- [FerretDB GitHub](https://github.com/FerretDB/FerretDB)
- [FerretDB documentation](https://docs.ferretdb.io/)
- [FerretDB supported commands](https://docs.ferretdb.io/reference/supported-commands/)
- [MongoDB Shell (mongosh)](https://www.mongodb.com/docs/mongodb-shell/)
