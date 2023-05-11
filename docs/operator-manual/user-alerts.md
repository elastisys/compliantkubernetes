# Enabling user alerts

This is administrator-facing documentation associated with [this user guide](../user-guide/alerts.md). Please read that one first.

!!!important
    Alertmanager should no longer be access via an Ingress, since this circumvents access control and audit logs. Please find the updated access method in the user guide linked above.

Perform the following configuration changes in `wc-config.yaml`:

1. Set `user.alertmanager.enabled=true`.
1. Ensure `user.alertmanager.ingress.enabled` is **false**.

For v0.18 and below include the following changes:

1. Update the `user.namespaces` list to include `alertmanager`.
1. Set `user.alertmanager.namespace=alertmanager`.

Then apply ck8s-apps.

## Example

Please find below an example taken from `wc-config.yaml`, which was tested with [compliantkubernetes-apps v0.17.0](https://github.com/elastisys/compliantkubernetes-apps/releases/tag/v0.17.0) and also applies to version v0.18:

```yaml
user:
  ## This only controls if the namespaces should be created, user RBAC is always created.
  createNamespaces: true
  ## List of user namespaces to create.
  namespaces:
    - alertmanager
    - demo1
    - demo2
    - demo3
  ## List of users to create RBAC rules for.
  adminUsers:
    - cristian.klein@elastisys.com
    - lars.larsson@elastisys.com
    - admin@example.com
  ## User controlled alertmanager configuration.
  alertmanager:
    enabled: true
    ## Namespace in which to install alertmanager
    namespace: alertmanager
    ## Create basic-auth protected ingress to alertmanager
    ingress:
      enabled: false
```

!!!note
    For versions after v0.18 `alertmanager` may not be listed under `user.namespaces` and the option `user.alertmanager.namespace` is deprecated.
