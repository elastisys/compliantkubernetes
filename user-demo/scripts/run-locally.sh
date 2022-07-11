#!/bin/bash
docker run \
    -p 3000:3000 \
    --rm \
    -ti \
    --name ck8s-user-demo \
    ck8s-user-demo
