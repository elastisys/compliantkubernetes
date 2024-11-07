# Enabling user alerts

This is administrator-facing documentation associated with [this user guide](../user-guide/alerts.md). Please read that one first.

!!!important

    Alertmanager should not be accessed via an Ingress, since this circumvents access control and audit logs. Please find the appropriate access method in the user guide linked above.

Ensure the following configuration changes are set in `wc-config.yaml`:

<!-- markdownlint-disable MD044 -->
1. Ensure [user.alertmanager.enabled](schema/config-properties-user-config-properties-alertmanager-config.md#enabled) is **true**.
1. Ensure [user.alertmanager.ingress.enabled](schema/config-properties-user-config-properties-alertmanager-config.md#ingress) is **false**.
<!-- markdownlint-enable MD044 -->

Then apply Welkin Apps.

## Example

Please find below an example taken from `wc-config.yaml`:

```yaml
user:
  ## User controlled alertmanager configuration.
  alertmanager:
    enabled: true
    ## Create basic-auth protected ingress to alertmanager
    ingress:
      enabled: false
```
