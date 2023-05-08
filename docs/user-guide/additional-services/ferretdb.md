# FerretDB (self-service)
[FerretDB](https://www.ferretdb.io/) is a database that is an open-source alternative to MongoDB that uses Postgres as its backend database. This documentation details how to run FerretDB in a Compliant Kubernetes cluster using the managed [Postgres service](postgresql.md).

## Build and push

The upstream FerretDB image cannot run as non-root due to folder permission issues. The following Dockerfile can be used to build an image for FerretDB that can run as non-root:
```Dockerfile
FROM busybox:1.36 as builder

RUN mkdir /state

FROM ghcr.io/ferretdb/ferretdb

ARG user=1001

COPY --from=builder --chown=$user:$user /state /state

USER $user
```

Save the file as `Dockerfile` and build the image:
```
docker build . -t $REGISTRY/$PROJECT/ferretdb:$TAG
```

Push the image:
```
docker push $REGISTRY/$PROJECT/ferretdb:$TAG
```

> **Note** <br/>
> If you are using managed Harbor as your container registry, please follow [these instructions](../deploy.md) for authenticating, setting up projects, as well as creating robot accounts and using them in a pull secret to safely pull the image from Harbor.

## Install

In a managed CK8s environment, follow [these instructions](postgresql.md#getting-access) on how to access the managed postgres service and how to create an application user and database.

Create secret containing a postgres url to authenticate to the managed postgres service and newly created database with the application user credentials:
```sh
kubectl create secret generic --from-literal=ferretdb-url="postgresql://$APP_USERNAME:$APP_PASSWORD@$PGHOST:$PGPORT/$APP_DATABASE" ferretdb-postgres-credentials -n ferretdb
```

Deploy:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ferretdb
  namespace: ferretdb
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
      imagePullSecrets: # https://elastisys.io/compliantkubernetes/user-guide/deploy/#configure-an-image-pull-secret
      - name: pull-secret
      containers:
      - name: ferretdb
        image: $REGISTRY/$PROJECT/ferretdb:$TAG # replace this
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
        securityContext:
          runAsUser: 1001
```

To access the FerretDB instance, create the following Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ferretdb-service
  namespace: ferretdb
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
