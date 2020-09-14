## Why can't I `kubectl run`?

To increase security, Compliance Kubernetes does not allow by default to run containers as root. To do `kubectl run` as a non-root user, please type something as follow:

```
kubectl run \
    --rm \
    -ti \
    --generator=run-pod/v1 \
    --image=ubuntu:18.04 blah \
    --overrides='
{
    "kind": "Pod",
    "apiVersion": "v1",
    "metadata": {
        "name": "blah",
        "labels": {
            "run": "blah"
        }
    },
    "spec": {
        "securityContext": {
            "runAsUser": 1000,
            "runAsGroup": 3000
        },
        "containers": [
            {
                "name": "blah",
                "image": "ubuntu:18.04",
                "stdin": true,
                "tty": true
            }
        ]
    }
}
'
```
