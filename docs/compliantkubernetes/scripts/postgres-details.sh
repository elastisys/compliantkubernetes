#!/bin/bash

set -euo pipefail

NAMESPACE=${NAMESPACE:-postgres-system}
SECRET=${SECRET:-postgres-user}

echo "export PGHOST=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.PGHOST}' | base64 --decode)"
echo "export PGUSER=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.PGUSER}' | base64 --decode)"
echo "export PGPASSWORD=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.PGPASSWORD}' | base64 --decode)"
echo "export PGSSLMODE=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.PGSSLMODE}' | base64 --decode)"
echo "export USER_ACCESS=$(kubectl -n $NAMESPACE get secret $SECRET -o 'jsonpath={.data.USER_ACCESS}' | base64 --decode)"

