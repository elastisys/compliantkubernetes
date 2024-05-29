#!/usr/bin/env bash

set -euo pipefail

declare here target
here="$(dirname "$(dirname "$(readlink "${BASH_SOURCE[0]}")")")"
target="${here}/docs/operator-manual/schema"

log.trace() {
  echo "trace: ${@}" >&2
}

log.note() {
  if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
    echo "::notice::${@}"
  else
    echo "note: ${@}" >&2
  fi
}

log.error() {
  if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
    echo "::error::${@}"
  else
    echo "error: ${@}" >&2
  fi
  exit 1
}

yq() {
  if command -v yq4 > /dev/null; then
    command yq4 "${@}"
  else
    command yq "${@}"
  fi
}

# Special handling of release branches
declare revision
if [[ -n "${OVERRIDE_REF_NAME:-}" ]]; then
  revision="${OVERRIDE_REF_NAME}"
elif [[ "${GITHUB_REF_NAME:-}" =~ release- ]]; then
  revision="$(cut -d- -f2 <<< "${GITHUB_REF_NAME}")"

  declare tags
  tags="$(curl -s "https://api.github.com/repos/elastisys/compliantkubernetes-apps/tags")"

  # Resolve the full revision from tags
  revision="$(yq "[.[].name] | sort | reverse | [.[] | select(match(\"${revision}\"))] | .[0]" <<< "${tags}")"

  if [[ "${revision}" == "null" ]]; then
    log.error "unable to resolve full revision for ${GITHUB_REF_NAME}"
  fi

else
  revision="${GITHUB_REF_NAME:-main}"
fi

declare commit commit_url
commit="$(curl -s "https://api.github.com/repos/elastisys/compliantkubernetes-apps/commits/${revision}")"
commit_url="$(yq '.html_url' <<< "${commit}")"

log.note "resolved revision: ${revision}@${commit_url}"

declare generation_time
generation_time="$(date)"

declare temp staging
temp="$(mktemp -d)"
staging="$(mktemp -d)"

curl -sL "https://raw.githubusercontent.com/elastisys/compliantkubernetes-apps/${revision}/config/schemas/config.yaml" -o "${temp}/config.yaml"
curl -sL "https://raw.githubusercontent.com/elastisys/compliantkubernetes-apps/${revision}/config/schemas/secrets.yaml" -o "${temp}/secrets.yaml"

if [[ "$(head -n 1 "${temp}/config.yaml")" == "404: Not Found" ]]; then
  log.error "unable to fetch config schema: 404 not found"
fi
if [[ "$(head -n 1 "${temp}/secrets.yaml")" == "404: Not Found" ]]; then
  log.error "unable to fetch secrets schema: 404 not found"
fi

log.trace "fetched schema"

yq -oj ".\"\$id\" = \"https://raw.githubusercontent.com/elastisys/compliantkubernetes-apps/${revision}/config/schemas/config.yaml\"" < "${temp}/config.yaml" > "${temp}/config.schema.json"
yq -oj ".\"\$id\" = \"https://raw.githubusercontent.com/elastisys/compliantkubernetes-apps/${revision}/config/schemas/secrets.yaml\"" < "${temp}/secrets.yaml" > "${temp}/secrets.schema.json"

log.trace "converted schema"

npx jsonschema2md -d "${temp}" -f yaml -o "${staging}" -x "${staging}/json"

log.trace "generated documentation"

# Postfix: Change README to Index
sed -i -r 's/^# README/# Index/' "${staging}/README.md"

# Postfix: Simplify headers
# - Increments the header "Definitions"
# - Increments headers under "Definitions"
# - Changes the header "Definitions group" to the key of the definition
# - Changes the header "Constraints", "Default Value", "Examples", "Type", and "Properties" to bolded text
find "${staging}" -type f -name '*.md' -exec sed -r -i \
  -e 's/^# .+ Definitions/## Definitions/' \
  -e 's/^### (.+)/#### \1/' \
  -e 's/^## Definitions group /### /' \
  -e 's/^#+ .+ Constraints/**CONSTRAINTS**:/' \
  -e 's/^#+ .+ Default Value/**DEFAULTS**:/' \
  -e 's/^#+ .+ Examples/**EXAMPLES**:/' \
  -e 's/^#+ .+ Type/**TYPE**:/' \
  -e 's/^#+ .+ Properties/**PROPERTIES**:/' \
  '{}' '+'

# Postfix: Reference JSON Schemas in Apps repository
find "${staging}" -type f -regextype sed -regex '.*/\(config\|secrets\).*\.md' -exec sed -i -r \
  -e "s#json/config.schema.json#https://github.com/elastisys/compliantkubernetes-apps/blob/${revision}/config/schemas/config.yaml#" \
  -e "s#json/secrets.schema.json#https://github.com/elastisys/compliantkubernetes-apps/blob/${revision}/config/schemas/secrets.yaml#" \
  -e 's#config.schema.json#config/schemas/config.yaml#' \
  -e 's#secrets.schema.json#config/schemas/secrets.yaml#' \
  '{}' '+'

# Postfix: Add return reference (config)
find "${staging}" -type f -regextype sed -regex '.*/\(config-\).*\.md' -exec sed -i -r \
  -e '1 a\\n[Return to the root config schema](config.md)' \
  -e '$ a\\n[Return to the root config schema](config.md)' \
  '{}' '+'

# Postfix: Add return reference (secrets)
find "${staging}" -type f -regextype sed -regex '.*/\(secrets-\).*\.md' -exec sed -i -r \
  -e '1 a\\n[Return to the root secrets schema](secrets.md)' \
  -e '$ a\\n[Return to the root secrets schema](secrets.md)' \
  '{}' '+'

# Postfix: Add under construction alert, commit and date
find "${staging}" -type f -regextype sed -regex '.*\.md' -exec sed -i -r \
  -e '1 a\\n> [!note]\n>\n> This is auto-generated documentation from a JSON schema that is under construction, this will improve over time.' \
  -e "\$ a\\\\n---\\nGenerated ${generation_time} from [elastisys/compliantkubernetes-apps@${revision}](${commit_url})" \
  '{}' '+'

# Postfix: Unescape GFM alerts
find "${staging}" -type f -regextype sed -regex '.*\.md' -exec sed -i -r \
  -e 's/^> \\\[/> \[/' \
  '{}' '+'

# Postfix: Fix numbering of anchors
find "${staging}" -type f -regextype sed -regex '.*\.md' -exec sed -i -r \
  -e 's/\(#([-0-9a-z]+)-([0-9]+)\)/(#\1_\2)/' \
  '{}' '+'

log.trace "postfixed documentation"

cat > "${staging}/undefined.md" <<EOF
# Undefined Schema

> [!warning]
> This is auto-generated documentation from a JSON schema that is under construction, this will improve over time.
>
> The referring type is undefined in the schema.

- [Return to the root config schema](config.md)
- [Return to the root secrets schema](secrets.md)
EOF

log.trace "created undefined"

rm -rf "${target}"
cp -r "${staging}" "${target}"

log.trace "placed documentation"

rm -rf "${staging}"
rm -rf "${temp}"

log.trace "completed"
