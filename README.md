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

## Contributor Guide

> Documentation is like sex:
> when it is good, it is very, very good;
> and when it is bad, it is better than nothing
>
> (Pretty inappropriate programmer humor.)

* Done today is better than perfect tomorrow.
* A picture is worth a 1000 words. Use Graphviz, Terminal screenshots or GIFs. Focus on the content, leave aesthetics for another day.
* Use "we" for the writer(s). Use "you" for the reader.
* Write in [plain English](http://www.plainenglish.co.uk/how-to-write-in-plain-english.html).
* Aim for the happy flow: How would a first-time user/operator interact with the system?
* Link to relevant upstream documentation.
