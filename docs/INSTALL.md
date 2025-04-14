## files

  - `bwyd/__init__.py`: package definitions
  - `bwyd/error.py`: error handling
  - `bwyd/measure.py`: measurement objects
  - `bwyd/module.py`: module interpreter
  - `bwyd/ops.py`: operations objects
  - `bwyd/parser.py`: parser, corpus operations
  - `bwyd/structure.py`: structural objects

  - `bwyd/resources/bwyd.tx`: Bwyd language grammar in `textX`
  - `bwyd/resources/bwyd.svg`: Bwyd icon
  - `bwyd/resources/convert.json`: measure conversions
  - `bwyd/resources/index.jinja`: Jinja2 HTML index template
  - `bwyd/resources/page.jinja`: Jinja2 HTML page template

  - `bwyd/__main__.py`: Jypter kernel CLI
  - `bwyd/install.py`: Jupyter kernel installer
  - `bwyd/kernel.py`: Jupyter wrapper kernel

  - `tests/*.py`: unit tests
  - `hooks.sh`: customized pre-commit hooks

  - `bwyd.cache`: serialized URL request cache
  - `config.ini`: sample configuration settings

  - `demo.py`: Python demo app
  - `examples/*.bwyd`: example recipes as Bwyd scripts
  - `examples/*.ipynb`: example recipes in Bwyd as Jupyter notebooks
  - `examples/*.json`: example recipes data model in JSON files


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


## run the demo script and notebooks

```bash
poetry run python3 demo.py
```

## run the notebooks

```bash
poetry run python3 -m pip install -e .
poetry run python3 -m bwyd.install
```

```bash
poetry run jupyter-lab
```


## development

To set up the `test` and `dev` environments:

```bash
poetry install --extras=test
poetry install --extras=dev
```

To run unit tests, type checking, and linting:

```bash
./hooks.sh
```

To validate the generated HTML:
<https://validator.w3.org/nu/#file>


######################################################################
TBD:

## uninstall

```bash
./venv/bin/jupyter kernelspec uninstall bwyd
python3 -m pip uninstall bwyd
```
