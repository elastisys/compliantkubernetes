# Access control

This guide describes how to set up and make use of group claims for applications.

!!!note
    This guide assumes your group claim name is `groups`

## Kubernetes

To set up [kubelogin](https://github.com/int128/kubelogin) to fetch and use groups make sure that your kubeconfig looks something like this.

```yaml
users:
  - name: user@my-cluster
    user:
      exec:
        apiVersion: client.authentication.k8s.io/v1beta1
        args:
          - oidc-login
          - get-token
          - --oidc-issuer-url=https://dex.my-cluster-domain.com
          - --oidc-client-id=my-client-id
          - --oidc-client-secret=my-client-secret
          - --oidc-extra-scope=email,groups # Make sure groups are here
        command: kubectl
```

!!!tips
    Your token can be found in `~/.kube/cache/oidc-login/`.
    This is useful if you're trying to debug your claims since you can just paste the token to [jwt.io](https://jwt.io) and check it.

    Example:

    ```console
    $ ls ~/.kube/cache/oidc-login/

    $ kubectl get pod
    <log in>

    $ ls ~/.kube/cache/oidc-login/
    13b165965d8e80749ce3b8d442da3e4e9f5ff5e38900ef104eee99fde85a39d4

    $ cat ~/.kube/cache/oidc-login/13b165965d8e80749ce3b8d442da3e4e9f5ff5e38900ef104eee99fde85a39d4 | jq -r .id_token
    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2RleC5teS1jbHVzdGVyLWRvbWFpbi5jb20iLCJpYXQiOjE2MjE1MTUxNzcsImV4cCI6MTY1MzEzNzU3NywiYXVkIjoibXktY2xpZW50LWlkIiwic3ViIjoiSGlVUE92S1BKMmVwWUkwR1R1U0JYWGRxYTJTV2ZxRnc1ZjBXNVBQeThTWSIsIm5vdW5jZSI6IkNoVXhNRFk0TVRZNE1qRXpORFUzTURVM01ERXlNREFTQm1kdmIyZHNaUSIsImF0X2hhc2giOiI1aUZjbF9Sc1JvblhHekZaMU0xQ2JnIiwiZW1haWwiOiJ1c2VyQG15LWRvbWFpbi5jb20iLCJlbWFpbF92ZXJpZmllZCI6InRydWUiLCJncm91cHMiOlsibXktZ3JvdXAtb25lIiwibXktZ3JvdXAtdHdvIl19.s65Aowfn6B1PiyQvRGPRu9KgX7G39nkLtx6yCAEElao
    ```

    Copy the token to [jwt.io](https://jwt.io) and ensure that the payload includes the expected groups claim.

## Kibana

To enable kibana to use the groups for kibana access.

```yaml
elasticsearch:
  sso:
    scope: "... groups" # Add groups to existing
  extraRoleMappings:
    - mapping_name: kibana_user
      definition:
        backend_roles:
          - my-group-name
    - mapping_name: kubernetes_log_reader
      definition:
        backend_roles:
          - my-group-name
    - mapping_name: readall_and_monitor
      definition:
        backend_roles:
          - my-group-name
```

## Harbor

Set correct group claim name since the default scopes includes groups already.
This groups can be assigned to projects or as admin group.

```yaml
harbor:
  oidc:
    groupClaimName: groups
```

## Grafana

!!!note
    This section assumes that [elastisys/compliantkubernetes-apps/pull/450](https://github.com/elastisys/compliantkubernetes-apps/pull/450) is merged

### OPS Grafana

```yaml
prometheus:
  grafana:
    oidc:
      enabled: true
      userGroups:
        grafanaAdmin: my-admin-group
        grafanaEditor: my-editor-group
        grafanaViewer: my-viewer-group
      scopes: ".... groups" # Add groups to existing
      allowedDomains:
        - my-domain.com
```

### User Grafana

```yaml
user:
  grafana:
    oidc:
      scopes: "... groups" # Add groups to existing
      allowedDomains:
        - my-domain.com
    userGroups:
      grafanaAdmin: my-admin-group
      grafanaEditor: my-editor-group
      grafanaViewer: my-viewer-group
```
