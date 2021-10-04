#!/bin/bash

IP_ADDRESS=$(docker inspect \
    -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
    ck8s-user-demo
)

if [ -z "$IP_ADDRESS" ]; then
    echo "Could not find ck8s-user-demo container." >&2
    exit 1
fi

curl $IP_ADDRESS:3000
echo
