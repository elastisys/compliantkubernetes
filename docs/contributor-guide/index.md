---
tags:
- ISO 27001 A.12.6.1
---
# Contributor guide

## Definition of Done

When working in regulated industries, it is really important to have the bar high for when something can be called "done". In Compliant Kubernetes, we use the following definition of done:

1. **Code and documentation is merged on the main branch of upstream projects.** This may cause time delays which are outside your control. However, if we cannot convince upstream projects to take our contributions, then we better know about this as soon as possible. A Compliant Kubernetes relying on an abandoned upstream branch is unsustainable.
2. **Code is merged in the Compliant Kubernetes project.**
3. **Documentation is up-to-date.** IT systems used in regulated industries need to have documentation. (See [ISO 27001 A.12.1.1 "Documented Operating Procedures"](https://www.isms.online/iso-27001/annex-a-12-operations-security/)).
You may either point to upstream documentation -- if Compliant Kubernetes does not add any specifics -- or write a dedicated section/page. Prefer to refer to upstream documentation -- potentially updating that one -- instead of duplicating it in Compliant Kubernetes.
4. **You provide evidence for completion.** This can be terminal output, screenshot or -- even better, but more time consuming -- a screencast with voice-over explanations. Ideally, these should be attached in the PR to convince the reviewer that the code and documentation are as intended.

## Submitting PRs

To make the review process as smooth as possible for everyone we have some steps that we'd like you to follow

* Look through our [DEVELOPMENT.md](https://github.com/elastisys/compliantkubernetes-apps/blob/main/DEVELOPMENT.md)

* The pre-commit hook will run on all PRs to `main`, so either make sure to have it installed by running:

    ```console
    pre-commit install
    ```

    Or manually run it before committing

    ```console
    pre-commit run
    ```

* Make sure to follow the PR template, see [this](https://raw.githubusercontent.com/elastisys/compliantkubernetes-apps/main/.github/pull_request_template.md) for more details.
  Alternatively start a PR and you'll see it there.

## Setting up your environment

To install all required tools, please follow the instructions [here](https://github.com/elastisys/compliantkubernetes-apps#requirements).

## Tips and tricks

To make your life easier we suggest to use language server for the language that you're editing.

E.g.

* terraform: [terraform-ls](https://github.com/hashicorp/terraform-ls)
* yaml: [yaml-language-server](https://github.com/redhat-developer/yaml-language-server)

To catch pre-commit errors early, direct in your editor, it's also suggested to install plugins for these tools.

* [markdownlint](https://github.com/markdownlint/markdownlint/)
* [shellcheck](https://github.com/koalaman/shellcheck/)

When developing and you only working on a single application it will be faster to only deploy that application instead of applying all charts.
This can be done by figuring out the app label for the application in question by running:

```console
bin/ck8s ops helmfile {wc|sc} list
```

When you figured out the app label (lets say it's `dex` in this case) you can check the diff of your work by running:

```console
bin/ck8s ops helmfile {wc|sc} -l app=dex diff
```

Instead of running `helmfile apply`, it might be useful to run `helmfile sync`.
This will do a 3-way upgrade and make sure that the helm state matches the objects actually running in kubernetes.
This will make sure that you haven't manually edited something for debugging and forgot about it.

```console
bin/ck8s ops helmfile {wc|sc} -l app=dex sync
```

### Object storage

To make creating and deletion of buckets easy, we've a script to help you with that, see [here](https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts/S3) *(the [quickstart](https://github.com/elastisys/compliantkubernetes-apps#quickstart) has instructions on how to use it)*.

### DNS

These following snippets can be used to setup/remove all DNS records required for ck8s using exoscales cli.

Start by setting up some variables:

```console
DOMAIN="example.com"
IP="203.0.113.123" # IP to LB/ingress endpoint for the service cluster
CK8S_ENVIRONMENT_NAME="my-cluster-name"

SUBDOMAINS=(  "*.ops.${CK8S_ENVIRONMENT_NAME}"
              "grafana.${CK8S_ENVIRONMENT_NAME}"
              "harbor.${CK8S_ENVIRONMENT_NAME}"
              "kibana.${CK8S_ENVIRONMENT_NAME}"
              "dex.${CK8S_ENVIRONMENT_NAME}"
              "notary.harbor.${CK8S_ENVIRONMENT_NAME}" )
```

```console
# Adding the A records
for SUBDOMAIN in "${SUBDOMAINS[@]}"; do
  exo dns add A "${DOMAIN}" -a "${IP}" -n "${SUBDOMAIN}"
done
```

```console
# Removing the records
for SUBDOMAIN in "${SUBDOMAINS[@]}"; do
  exo dns remove "${DOMAIN}" "${SUBDOMAIN}"
done
```

### Reusing clusters

If you for some reason need to reinstall Compliant Kubernetes from scratch, we have some scripts that removes all objects created by this repo.
The scripts can be found [here](https://github.com/elastisys/compliantkubernetes-apps/tree/main/scripts) *(clean-sc.sh and clean-wc.sh)*.
