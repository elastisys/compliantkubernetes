# CISO Control Plugin for Mkdocs

This plugin is similar to the [tags plugin](https://squidfunk.github.io/mkdocs-material/setup/setting-up-tags/) which is built into mkdocs-material.
However, it allows to generate separate tags index pages, depending on the prefix of the tag.

It aims to solve the following use-case.
The Compliant Kubernetes documentation uses tags to capture various Information Security Management System (ISMS) controls.
This plugin will:

1.  Create tags indexes for each requirement source.
1.  Create bi-directional links between tags indexes and pages.

## Usage

Start by adding the following in `mkdocs.yaml`:

```yaml
plugins:
  - ciso-controls:
      root_url: $ROOT_URL
```

The plugin will scan the specified folder for Markdown documents which will serve as tags indexes.
These files are expected to:

1.  be named with the prefix of tags to be included in that tags index;
1.  contain the string `[TAGS]`.

The string `[TAGS]` will be replaced with an HTML index to all relevant pages.
In the other direction, all relevant pages will link back to the tags index.
Tags will be sorted naturally via the [natsort](https://pypi.org/project/natsort/) package.

For inclusion in the tags index, the tags index filename without extension must be a prefix of the [slugified](https://stackoverflow.com/a/427160) tag.

## Example

Create the following files:

- `ciso-guide/controls/iso-27001.md`;
- `ciso-guide/controls/bsi-it-grundschutz.md`;
- `ciso-guide/controls/hipaa.md`.

You can add any content you want, but make sure you have the string `[TAGS]` somewhere.

Next, add something as follows in the frontmatter:

```yaml
tags:
  - ISO 27001 A13.1
  - HIPAA S13
  - BSI IT-Grundschutz APP.X
```

This will add `ISO 27001 A13.1` to `ciso-guide/controls/iso-27001`, etc.
