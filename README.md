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
* Capitalize Kubernetes concepts: Pod, Node, Service.

## Deployment

GitHub Actions will deploy the `main` branch automatically.
