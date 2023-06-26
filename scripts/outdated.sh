#!/usr/bin/env bash

set -euo pipefail

declare -a null
declare -a past

DEBUG="${DEBUG:-}"

usage() {
  echo "usage:"
  echo "  ${0} <command> <arguments>..."
  echo ""
  echo "commands:"
  echo "- at <time>                  - check 'tested-at' tag for outdated pages"
  echo "                               example: ${0} at 30 days"
  echo "                               example: ${0} at 2 months"
  echo "- with <component> <version> - check 'tested-with' tag for outdated pages"
  echo "                               example: ${0} with apps 0.30"
  echo "                               example: ${0} with apps/harbor/app 2.8.2"
  echo "                               example: ${0} with apps/harbor/chart 1.12.2"
}

case "${1:-}" in
"")
  echo "err: missing command"
  echo
  usage
  exit 1
  ;;

"at")
  if [[ -z "${2:-}" ]]; then
    time="$(date -Idate --date="1 month ago")"
  else
    time="$(date -Idate --date="${*:2} ago")"
  fi

  for file in $(find docs -not -path 'docs/adr/*' -type f -name "*.md" | sort); do
    mark="$(yq -f=extract '.tested-at' "${file}" 2>&1 || true)"

    if [[ "${mark}" =~ ^Error:* ]]; then
      null+=("missing front matter - ${file}")
    elif [[ "${mark}" =~ ^(null|)$ ]]; then
      null+=("missing tested-at - ${file}")
    else
      test_interval="$(yq -f=extract '.test-interval' "${file}" 2>&1 || true)"

      if ! [[ "${test_interval}" =~ ^(null|)$ ]]; then
        time_interval="$(date -Idate --date="${test_interval} ago")"

        if [[ "${mark}" < "${time_interval}" ]]; then
          past+=("tested-at: ${mark} - ${file} - test-interval: ${test_interval}")
        fi

      elif [[ "${mark}" < "${time}" ]]; then
        past+=("tested-at: ${mark} - ${file}")
      fi
    fi
  done

  if [[ -n "${DEBUG}" ]]; then
    echo "---"
    echo "files with errors:"
    for file in "${null[@]}"; do
      echo "- ${file}"
    done
    echo "---"
  fi

  echo "files with 'tested-at' mark before ${time}:"
  for file in "${past[@]}"; do
    echo "- ${file}"
  done
  ;;

"with")
  if [[ -z "${2:-}" ]]; then
    echo "err: missing component argument"
    usage
    exit 1
  elif [[ -z "${3:-}" ]]; then
    echo "err: missing version argument"
    usage
    exit 1
  else
    component="${2}"
    version="${3#v}"
  fi

  major="${version%%.*}"
  if [[ "${version}" =~ ^.*\..*$ ]]; then
    version="${version#*.}"
  else
    version=""
  fi
  minor="${version%%.*}"
  if [[ "${version}" =~ ^.*\..*$ ]]; then
    version="${version#*.}"
  else
    version=""
  fi
  patch="${version%%-*}"


  for file in $(find docs -not -path 'docs/adr/*' -type f -name "*.md" | sort); do
    mark="$(yq -f=extract ".tested-with.$component" "${file}" 2>&1 || true)"
    mark="${mark#v}"

    if [[ "${mark}" =~ ^Error:* ]]; then
      null+=("missing front matter - ${file}")
    elif [[ "${mark}" =~ ^(null|)$ ]]; then
      null+=("missing tested-with - ${file}")
    else
      mark_major="${mark%%.*}"
      if [[ "${mark}" =~ ^.*\..*$ ]]; then
        mark="${mark#*.}"
      else
        mark=""
      fi
      mark_minor="${mark%%.*}"
      if [[ "${mark}" =~ ^.*\..*$ ]]; then
        mark="${mark#*.}"
      else
        mark=""
      fi
      mark_patch="${mark%%-*}"

      if [[ -n "${major}" ]] && [[ -n "${mark_major}" ]]; then
        if [[ "${mark_major}" < "${major}" ]]; then
          past+=("tested-with v${mark_major:-*}.${mark_minor:-*}.${mark_patch:-*}: ${file}")
        elif [[ "${mark_major}" > "${major}" ]]; then
          continue;
        fi
      fi
      if [[ -n "${minor}" ]] && [[ -n "${mark_minor}" ]]; then
        if [[ "${mark_minor}" < "${minor}" ]]; then
          past+=("tested-with v${mark_major:-*}.${mark_minor:-*}.${mark_patch:-*}: ${file}")
        elif [[ "${mark_minor}" > "${minor}" ]]; then
          continue;
        fi
      fi
      if [[ -n "${patch}" ]] && [[ -n "${mark_patch}" ]] && [[ "${mark_patch}" < "${patch}" ]]; then
        past+=("tested-with v${mark_major:-*}.${mark_minor:-*}.${mark_patch:-*}: ${file}")
      fi
    fi
  done

  if [[ -n "${DEBUG}" ]]; then
    echo "---"
    echo "files with errors:"
    for file in "${null[@]}"; do
      echo "- ${file}"
    done
    echo "---"
  fi

  echo "files with 'tested-with.${component}' before v${major:-*}.${minor:-*}.${patch:-*}:"
  for file in "${past[@]}"; do
    echo "- ${file}"
  done
  ;;
esac
