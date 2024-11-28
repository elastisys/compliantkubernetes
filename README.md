# Welkin Documentation

[![Regularly check links](https://github.com/elastisys/welkin/actions/workflows/checklinks.yml/badge.svg)](https://github.com/elastisys/welkin/actions/workflows/checklinks.yml)

This is the main repository for documentation about the Welkin project. For Welkin code, please refer to:

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

> [!NOTE]
> For Mac users, you might have to install cairo: `brew install cairo`

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

- To view locally: `mike deploy welkin -t 'main'` and then `mike serve`.
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

## Known Issues

### nodeenv provided with Ubuntu 24.04 is old

If you get the following errors:

```console
$ pre-commit run --all
[...]
An unexpected error has occurred: CalledProcessError: command: ('/usr/bin/python3', '-mnodeenv', '--prebuilt', '--clean-src', '/home/cklein/.cache/pre-commit/repoxgjtxt_g/node_env-default')
[...]
      File "/usr/lib/python3/dist-packages/nodeenv.py", line 881, in main
        opt.node = get_last_stable_node_version()

                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

Then this could be caused by the version of nodeenv delivered with Ubuntu 24.04.
You have two options.

#### Option 1: Run pre-commit from a virtual environment

1. Remove Ubuntu's pre-commit and nodeenv: `sudo apt purge nodeenv --autoremove`.
1. Activate the virtual environment you created above: `. .venv/bin/activate`.
1. Install pre-commit in the virtual environment: `pip install pre-commit`.
1. Run pre-commit from the virtual environment: `pre-commit run --all`.

#### Option 2: Break system package

```shell
sudo apt install pre-commit
sudo apt install python3-pip
sudo pip install nodeenv --break-system-packages --upgrade
```
