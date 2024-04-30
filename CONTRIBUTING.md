# Contributor Guide

- Done today is better than perfect tomorrow.
- Write for the project, not the company.
- A picture is worth 1000 words. Use Graphviz, Terminal screenshots, or GIFs. Focus on the content, leave aesthetics for another day. Prefer PNG with a width of 1200px.
- Perspective: Put yourself in the shoes of the user or administrator. What documentation would you like to read as a newcomer?
- Use "we" for the writer(s). Use "you" for the reader.
- Write in [plain English](http://www.plainenglish.co.uk/how-to-write-in-plain-english.html).
- Ordering of ideas: Aim for the happy flow: How would a first-time user/administrator interact with the system? In what order would they do things?
- Please capitalize Kubernetes concepts (Pod, Volume, etc.) for consistency with the [Kubernetes documentation](https://kubernetes.io/docs/concepts/workloads/pods/).
- Link to relevant upstream documentation.
- Please contribute to a branch and create a PR.
- Capitalize all letters of acronyms: DNS, TCP, AWS.
- Capitalize proper nouns, in particular, names of projects, companies, and products: Kubernetes, Amazon, Azure.
- Use [inclusive naming](https://inclusivenaming.org/).
- Prefer absolute URLs in SVGs (including protocol and domain) to facilitate re-usage outside this website.
- Respect trademarks. If in doubt, prefer [nominative use](https://en.wikipedia.org/wiki/Nominative_use) and no logo.

## Stable URL Policy

Please observe a stable URL policy. This means:

- Try to avoid breaking URLs.
- If you need to break URLs, make sure you set up redirects. (Search for `redirects` in [mkdocs.yml](mkdocs.yml).)

## Code Snippets

Code snippets should be written in a way that is transparent, predictable and flexible. They should be written with two roles in mind: devs and ops. Devs need commands that "mostly work", but need access to the underlying tools to select only the component they currently work on (e.g., Ansible `-t` or Helmfile `-l`). Ops need access to dry-run. Both these roles will be called "administrator" below.

- Separate pre-requisite installation snippets, config snippets (which includes init snippets), apply snippets and test snippets.
- Apply snippets should not execute when copy-pasted, e.g., do not add a final newline. They should allow the administrator to review the command, potentially edit the command, before confirming execution by typing ENTER.
- Apply snippets should be idempotent, i.e., running apply multiple times should give the same result as applying only once.
- Avoid auto-approve in apply snippets. Encourage (but don't force) dry-running.
- Include test snippets after every major apply step. These should allow the administrator to confirm that the previous apply step succeeded. The test should be as realistic as possible, e.g., "I can run a Pod", "PVCs I create are bound", etc. Tests should both confirm that the administrator can proceed with the next step and serve as troubleshooting.
- Test snippets should be non-destructive. If this is not possible, add big warnings.

Examples:

```bash
## Config snippet, almost always requires human input
export CK8S_ENVIRONMENT_NAME=my-environment-name
#export CK8S_FLAVOR=[dev|prod|air-gapped] # defaults to dev
export CK8S_CONFIG_PATH=~/.ck8s/my-cluster-path
export CK8S_CLOUD_PROVIDER=# [exoscale|safespring|citycloud|aws|baremetal]
export CK8S_PGP_FP=<your GPG key fingerprint>  # retrieve with gpg --list-secret-keys
export CLUSTERS=( "sc" "wc" )
./bin/ck8s init both

## Apply snippets
# Good, because administrator can review command, change command as necessary, review its effects and approves those effects
for CLUSTER in "${CLUSTERS[@]}"; do
    pushd inventory/$CLUSTER
    terraform init ../../contrib/terraform/exoscale
    terraform apply \
        -var-file default.tfvars \
        -state=tfstate-$CLUSTER.tfstate  \
        ../../contrib/terraform/exoscale
    popd
done

# Okay
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

## Diagrams

### From diagrams.net (source of truth in this repo)

Files ending in `*.drawio.svg` are produced using [diagrams.net](https://www.diagrams.net/). They are exported as follows:

1.  File -> Export As -> SVG
1.  Change "zoom" to 100%.
1.  Enable "Embed Images".
1.  Enable "Embed Fonts".
1.  Enable "Include a copy of my diagram".
1.  Select "Links: In new window".
1.  Leave everything else as default.

To facilitate editing architecture diagrams, import the [Compliant Kubernetes DrawIO library](docs/img/ck8s-library.drawio.xml).

### From graphviz

Other diagrams are produced in graphviz. To regenerate them, edit the relevant `dot` file, then type:

```bash
make -C docs/img
```

For "live preview" open the output file (e.g., SVG or PNG) in a viewer supporting live refresh (e.g., eog), then type:

```bash
make -C docs/img preview
```

The viewer's output should be updated live as you save the source `dot` file.
