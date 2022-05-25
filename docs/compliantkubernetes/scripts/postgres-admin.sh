#!/bin/bash

set -euo pipefail

source $(./postgres-details.sh)

echo "Opening a network tunnel to the PostgreSQL cluster called ${USER_ACCESS} in ${NAMESPACE}"
kubectl -n $NAMESPACE port-forward $USER_ACCESS 5432 &
forwarder=$!

echo "Starting PostgreSQL command line client against the 'postgres' database:"
psql -h 127.0.0.1 postgres || true

kill $forwarder || true
exit 0
