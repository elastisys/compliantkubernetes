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

* To view locally: `mike serve`.
* To re-generate figures: `make -C docs/img`. **For simplicity, please commit generated figures. Prefer PNG (width == 1200px), to facilitate embedded logos.**
* For continuous preview of figures: `make -C docs/img preview`.

## Tech Stack

* [mkdocs](https://www.mkdocs.org/)
* [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
* [GitHub Pages](https://pages.github.com/)
* [Graphviz](https://graphviz.org/)
* [mike](https://github.com/jimporter/mike)

## Deployment

GitHub Actions will deploy the `main` branch automatically.
