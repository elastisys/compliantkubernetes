# Compliant Kubernetes Documentation

This is the main repository for documentation about the Compliant Kubernetes project.

## Prerequisites

```
pip3 install mkdocs mkdocs-material
```

For generating figures, please install:

```
sudo apt-get install graphviz make
```

## Usage

* To view locally: `mkdocs serve`.
* To publish on GitHub Pages: `mkdocs gh-deploy`.
* To re-generate figures: `make -C docs/img`. **For simplicity, please commit generated figures. Prefer PNG (width <= 1200px), to facilitate embedded logos.**
* For continous preview of figures: `make -C docs/img preview`.

## Tech Stack

* [mkdocs](https://www.mkdocs.org/)
* [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
* [GitHub Pages](https://pages.github.com/)
* [Graphviz](https://graphviz.org/)
