# CISO Control Plugin for Mkdocs

This is a PoC solving the following use-case. The Compliant Kubernetes documentation uses tags to capture various Information Security Management System (ISMS) controls, such as:

```
# In the YAML frontmatter of the page
tags:
- ISO 27001 A13.1
- HIPAA S13
- BSI IT-Grundschutz APP.X
```

The goal of this plugin is to:

1. Create tag indexes for each requirement source. In the example above "ISO 27001" and "HIPAA" is each a requirement source.

2. Create bi-directional links between tag indexes and pages.

## Usage

In `mkdocs.yaml`:

```
plugins:
  - ciso-controls:
      root_url: ciso-guide/controls/
```

For the example above, the following files are expected to exist:

* `ciso-guide/controls/iso-27001.md`;
* `ciso-guide/controls/bsi-it-grundschutz.md`;
* `ciso-guide/controls/hipaa.md`.

These files are expected to contain the string `[TAGS]`, which will be replaced with an index to all tags prefixed with the name of the page.
