# Compliant Kubernetes Documentation

This is the main repository for documentation about the Compliant Kubernetes project. For Compliant Kubernetes code, please refer to:

* [`compliantkubernetes-kubespray`](https://github.com/elastisys/compliantkubernetes-kubespray) for setting up a vanilla Kubernetes cluster on top of a compliant cloud provider;
* [`compliantkubernetes-apps`](https://github.com/elastisys/compliantkubernetes-apps) for augmenting a vanilla Kubernetes cluster with security and observability.

## Prerequisites

```
pip3 install -r requirements.txt
```

For generating figures, please install:

```
sudo apt-get install graphviz make
```

## Usage

* To view locally: `mkdocs serve`.
* To re-generate figures: `make -C docs/img`. **For simplicity, please commit generated figures. Prefer PNG (width == 1200px), to facilitate embedded logos.**
* For continuous preview of figures: `make -C docs/img preview`.

## Tech Stack

* [mkdocs](https://www.mkdocs.org/)
* [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
* [GitHub Pages](https://pages.github.com/)
* [Graphviz](https://graphviz.org/)

## Contributor Guide

> Documentation is like sex:
> when it is good, it is very, very good;
> and when it is bad, it is better than nothing
>
> (Pretty inappropriate programmer humor.)

* Done today is better than perfect tomorrow.
* Write for the project, not the company.
* A picture is worth 1000 words. Use Graphviz, Terminal screenshots, or GIFs. Focus on the content, leave aesthetics for another day. Prefer PNG with a width of 1200px.
* Perspective: Put yourself in the shoes of the user or operator. What documentation would you like to read as a newcomer?
* Use "we" for the writer(s). Use "you" for the reader.
* Write in [plain English](http://www.plainenglish.co.uk/how-to-write-in-plain-english.html).
* Ordering of ideas: Aim for the happy flow: How would a first-time user/operator interact with the system? In what order would they do things?
* Please capitalize Kubernetes concepts (Pod, Volume, etc.) for consistency with the [Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/pods/).
* Link to relevant upstream documentation.
* Please contribute to a branch and create a PR.
* Capitalize all letters of acronyms: DNS, TCP, AWS.
* Capitalize proper nouns, in particular, names of projects, companies, and products: Kubernetes, Amazon, Azure.

### Code Snippets

Code snippets should be written in a way that is transparent, predictable and flexible. They should be written with two roles in mind: devs and ops. Devs need commands that "mostly work", but need access to the underlying tools to select only the component they currently work on (e.g., Ansible `-t` or Helmfile `-l`). Ops need access to dry-run. Both these roles will be called "operator" below.

* Separate config snippets (which includes init snippets), apply snippets and test snippets.
* Apply snippets should not execute when copy-pasted, e.g., do not add a final newline. They should allow the operator to review the command, potentially edit the command, before confirming execution by typing ENTER.
* Apply snippets should be idempotent, i.e., running apply multiple times should give the same result as applying only once.
* Avoid auto-approve in apply snippets. Encourage (but don't force) dry-running.
* Include test snippets after every major apply step. These should allow the operator to confirm that the previous apply step succeeded. The test should be as realistic as possible, e.g., "I can run a Pod", "PVCs I create are bound", etc. Tests should both confirm that the operator can proceed with the next step and serve as troubleshooting.
* Test snippets should be non-destructive. If this is not possible, add big warnings.

Examples:

```
## Config snippet, almost always requires human input
export CK8S_ENVIRONMENT_NAME=my-environment-name
#export CK8S_FLAVOR=[dev|prod] # defaults to dev
export CK8S_CONFIG_PATH=~/.ck8s/my-cluster-path
export CK8S_CLOUD_PROVIDER=# [exoscale|safespring|citycloud|aws|baremetal]
export CK8S_PGP_FP=<your GPG key fingerprint>  # retrieve with gpg --list-secret-keys
./bin/ck8s init

## Apply snippets
# Good, because operator can review command, change command as necessary, review its effects and approves those effects
for CLUSTER in ${SERVICE_CLUSTER} "${WORKLOAD_CLUSTERS[@]}"; do
    pushd inventory/$CLUSTER
    terraform init ../../contrib/terraform/exoscale
    terraform apply \
        -var-file default.tfvars \
        -state=tfstate-$CLUSTER.tfstate  \
        ../../contrib/terraform/exoscale
    popd
done

# Okay
ln -sf $CK8S_CONFIG_PATH/.state/kube_config_${SERVICE_CLUSTER}.yaml $CK8S_CONFIG_PATH/.state/kube_config_sc.yaml
./bin/ck8s apply sc  # Respond "n" if you get a WARN

# Bad, because the effects are difficult to predict and adjust
for x in arr; do
    pushd $x
    sops exec-file secrets "command --auto-approve $complicated_unexplained_arguments | yq r 'a.b.c' | xarg somthing-something"
    popd
done

## Test snippet
# Good
kubectl get my-resource -o wide
curl https://example.com/

# Bad
kubectl delete all --all --all-namespaces
```

## Deployment

GitHub Actions will deploy the `main` branch automatically.
