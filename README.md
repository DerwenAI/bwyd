# Bwyd culinary DSL

A domain specific language (DSL) to assist in taking notes about
culinary work which is intended to be repeated.

This includes support for running in a Jupyter notebook, plus using
graph technologies for analytics and preparation planning.

---

## build a local environment

This project uses [`poetry`](https://python-poetry.org/docs/basic-usage/)
for dependency management, virtual environment, builds, packaging, etc.
To set up an environment locally:

```bash
git clone https://github.com/DerwenAI/bwyd.git
cd bwyd

poetry install --extras=demo
```

The source code is currently based on Python 3.11 or later.


## run the demo script to generate HTML

```bash
poetry run python3 cli.py
```

Then load the `examples/index.html` in a browser.


## eval a specific Bwyd file

```bash
poetry run python3 eval_rig.py <slug>
```


## prep for Jupyter notebooks

```bash
poetry run python3 -m pip install -e .
poetry run python3 -m bwyd.install
```

```bash
poetry run jupyter-lab
```


## development

To set up the `test` environment:

```bash
poetry install --extras=test
```

To run unit tests, type checking, and linting:

```bash
./lint.sh
```

To validate the generated HTML:
<https://validator.w3.org/nu/#file>


## files

  - `bwyd/__main__.py`: Jypter kernel CLI
  - `bwyd/install.py`: Jupyter kernel installer
  - `bwyd/kernel.py`: Jupyter wrapper kernel

  - `config.toml`: sample configuration settings

  - `examples/*.bwyd`: example recipes as Bwyd scripts
  - `examples/*.ipynb`: example recipes in Bwyd as Jupyter notebooks
  - `examples/*.json`: example recipes data model in JSON files


######################################################################
TBD:

## uninstall

```bash
./venv/bin/jupyter kernelspec uninstall bwyd
python3 -m pip uninstall bwyd
```
