# Compliant Kubernetes Documentation

[![Regularly check links](https://github.com/elastisys/compliantkubernetes/actions/workflows/checklinks.yml/badge.svg)](https://github.com/elastisys/compliantkubernetes/actions/workflows/checklinks.yml)

This is the main repository for documentation about the Compliant Kubernetes project. For Compliant Kubernetes code, please refer to:

- [`compliantkubernetes-kubespray`](https://github.com/elastisys/compliantkubernetes-kubespray) for setting up a vanilla Kubernetes cluster on top of a compliant cloud provider;
- [`compliantkubernetes-apps`](https://github.com/elastisys/compliantkubernetes-apps) for augmenting a vanilla Kubernetes cluster with security and observability.

## Prerequisites

[Python 3](https://www.python.org/). You can check that it is already present on your Linux/macOS as follows:

```sh
python3 --version
```

For generating figures, please install:

```sh
sudo apt-get install graphviz make
```

For generating `docs/stylesheets/style.css`, please install:

```sh
npm install -g sass
```

## Usage

To view locally:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

mkdocs serve
```

> [!CAUTION]
> The command `mike serve` also works to preview a page, but it does not seem to support live preview.
> This means that you need to restart `mike serve` after every file change, which is not really productive

- To view locally: `mike deploy compliantkubernetes ck8s -t 'main'` and then `mike serve`.
- To re-generate figures: `make -C docs/img`. **For simplicity, please commit generated figures. Prefer PNG (width == 1200px), to facilitate embedded logos.**
- For continuous preview of figures: `make -C docs/img preview`.
- To generate `docs/stylesheets/style.css`, please use `sass extra_sass/style.css.scss > docs/stylesheets/style.css`.

## Tech Stack

- [mkdocs](https://www.mkdocs.org/)
- [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages](https://pages.github.com/)
- [Graphviz](https://graphviz.org/)
- [mike](https://github.com/jimporter/mike)
- [sass](https://www.npmjs.com/package/sass)

## Deployment

GitHub Actions will deploy the `main` branch automatically.
