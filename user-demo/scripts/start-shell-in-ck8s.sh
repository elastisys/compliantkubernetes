#!/bin/bash

IMAGE=alpine/curl
CMD=sh

OVERRIDES='''
{
  "apiVersion": "v1",
  "spec": {
     "containers": [{
       "name": "shell",
       "image": "'$IMAGE'",
       "args": ["'$CMD'"],
       "tty": true,
       "stdin": true,
       "securityContext": {
         "runAsUser": 1000
       },
       "resources": {
         "requests": {
            "cpu": "100m",
            "memory": "100m"
         }
       }
    }]
  }
}
'''

kubectl run --rm -ti shell-$USER --overrides="$OVERRIDES" --image=overridden -- overridden
