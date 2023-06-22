# Platform Administrator FAQ

## I updated some OpenSearch options but it didn't work, now what?

If you update the OpenSearch `securityConfig` you will have to make sure that the master Pod(s) are restarted so that they pick up the new Secret and then run the `securityadmin.sh` script.
This happens for example if you switch from non-SSO to SSO.

To reload the configuration you need to run the following commands:

```bash
# Make the script executable
kubectl -n opensearch-system exec opensearch-master-0 -- chmod +x ./plugins/opensearch-security/tools/securityadmin.sh
# Run the script to update the configuration
kubectl -n opensearch-system exec opensearch-master-0 -- ./plugins/opensearch-security/tools/securityadmin.sh \
    -f plugins/opensearch-security/securityconfig/config.yml \
    -icl -nhnv \
    -cacert config/admin/ca.crt \
    -cert config/admin/tls.crt \
    -key config/admin/tls.key
```

Note that the above only reloads the `config.yml` (as specified with the `-f`).
If you made changes to other parts of the system you will need to point to the relevant file to reload, or reload everything like this:

```bash
# Run the script to update "everything" (internal users, roles, configuration, etc.)
kubectl -n opensearch-system exec opensearch-master-0 -- ./plugins/opensearch-security/tools/securityadmin.sh \
    -cd plugins/opensearch-security/securityconfig/ \
    -icl -nhnv \
    -cacert config/admin/ca.crt \
    -cert config/admin/tls.crt \
    -key config/admin/tls.key
```

When you update things other than `config.yml` you will also need to rerun the Configurer Job by syncing the `opensearch-configurer` chart.
