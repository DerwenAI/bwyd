## files

  - `bwyd/__init__.py`: Bwyd package definitions
  - `bwyd/error.py`: Bwyd error handling
  - `bwyd/measure.py`: Bwyd language measurement objects
  - `bwyd/module.py`: Bwyd module interpreter
  - `bwyd/ops.py`: Bwyd language operations objects
  - `bwyd/parser.py`: Bwyd language parser
  - `bwyd/structure.py`: Bwyd language structural objects

  - `bwyd/resources/bwyd.tx`: Bwyd language grammar in `textX`
  - `bwyd/resources/bwyd.svg`: Bwyd icon
  - `bwyd/resources/bwyd.jinja`: Jinja2 HTML template
  - `bwyd/resources/convert.json`: measure conversions

  - `bwyd/__main__.py`: Jypter kernel CLI
  - `bwyd/install.py`: Jupyter kernel installer
  - `bwyd/kernel.py`: Jupyter wrapper kernel

  - `tests/*.py`: unit tests

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

```bash
poetry run pytest
poetry run mypy bwyd
poetry run pylint bwyd
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
