## Why can't I `kubectl run`?

To increase security, Compliance Kubernetes does not allow by default to run containers as root.
Additionally, the container image is not allowed to be pulled from a public docker hub registry and all Pods are required to be selected by some NetworkPolicy.
This ensures that an active decision has been made for what network access the Pod should have and helps avoid running "obscure things found on the internet".

Considering the above, you should start by pushing the container image you want to use to Harbor and [make sure it doesn't run as root][docker-user].
See [this document][harbor-oidc-docker] for how to use OIDC with docker.
With that in place, you will need to create a NetworkPolicy for the Pod you want to run.
Here is an example of how to create a NetworkPolicy that allows all TCP traffic (in and out) for Pods with the label `run: blah`.

!!!note
    This is just an example, not a good idea!
    You should limit the policy to whatever your application really needs.

```bash
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: blah
spec:
  podSelector:
    matchLabels:
      run: blah
  policyTypes:
  - Ingress
  - Egress
  ingress:
  # Allow all incoming traffic
  - {}
  egress:
  # Allow all outgoing traffic
  - {}
EOF
```

Now you are ready to run a Pod!
Make sure you match the name with the label you used for the NetworkPolicy.
Kubectl will automatically set the label `run: <name-of-pod>` when you create a Pod with `kubectl run <name-of-pod>`.
Here is an example command (please replace the `$MY_HARBOR_IMAGE`):

```bash
kubectl run blah --rm -ti --image=$MY_HARBOR_IMAGE
```

If your image runs as root by defaults, but can handle running as another user, you may override the user by adding a flag like this to the above command:

```
--overrides='{ "spec": { "securityContext": "runAsUser": 1000, "runAsGroup": 1000 } }'
```

[harbor-oidc-docker]: https://goharbor.io/docs/1.10/administration/configure-authentication/oidc-auth/#using-oidc-from-the-docker-or-helm-cli
[docker-user]: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user

## I updated some Elasticsearch options but it didn't work

If you update the Elasticsearch `securityConfig` you will have to make sure that the master Pod(s) are restarted so that they pick up the new Secret and then run the `securityadmin.sh` script.
This happens for example if you switch from non-SSO to SSO.

To reload the configuration you need to run the following commands:

```bash
# Make the script executable
kubectl -n elastic-system exec opendistro-es-master-0 -- chmod +x ./plugins/opendistro_security/tools/securityadmin.sh
# Run the script to update the configuration
kubectl -n elastic-system exec opendistro-es-master-0 -- ./plugins/opendistro_security/tools/securityadmin.sh \
    -f plugins/opendistro_security/securityconfig/config.yml \
    -icl -nhnv \
    -cacert config/admin-root-ca.pem \
    -cert config/admin-crt.pem \
    -key config/admin-key.pem
```

Note that the above only reloads the `config.yml` (as specified with the `-f`).
If you made changes to other parts of the system you will need to point to the relevant file to reload, or reload everything like this:

```bash
# Run the script to update "everything" (internal users, roles, configuration, etc.)
kubectl -n elastic-system exec opendistro-es-master-0 -- ./plugins/opendistro_security/tools/securityadmin.sh \
    -cd plugins/opendistro_security/securityconfig/ \
    -icl -nhnv \
    -cacert config/admin-root-ca.pem \
    -cert config/admin-crt.pem \
    -key config/admin-key.pem
```

When you update things other than `config.yml` you will also need to rerun the Configurer Job (e.g. by making some small change to the resource requests and applying the chart again).
