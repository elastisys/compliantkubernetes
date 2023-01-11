# CISO Control Plugin for Mkdocs

This is a PoC solving the following use-case. The Compliant Kubernetes documentation uses tags to capture various Information Security Management System (ISMS) controls, such as:

```
# In the YAML frontmatter of the page
tags:
- ISO 27001 A13.1
- HIPAA S13
```

The goal of this plugin is to:

1. Create tag indexes for each requirement source. In the example above "ISO 27001" and "HIPAA" is each a requirement source.

2. Create bi-directional links between tag indexes and pages.

## Usage

In `mkdocs.yaml`:

```
plugins:
  - ciso-controls:
      root_url: /ciso-guide/controls/
      control_sources:
        - 'ISO 27001'
        - 'HIPAA'
        - 'BSI IT-Grundschutz'
```

Tag indexes will be generated at:

* `/ciso-guide/controls/iso-27001`;
* `/ciso-guide/controls/hipaa`;
* `/ciso-guide/controls/bsi-it-grundschutz`.
