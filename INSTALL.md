## dependencies

  - [`icecream`](https://github.com/gruns/icecream)
  - [`jupyterlab`](https://jupyter.org/)
  - [`pydantic-graph`](https://ai.pydantic.dev/graph/#graph-types)
  - [`textX`](https://textx.github.io/textX/)


## files

  - `bwyd/parser.py`: Bwyd language parser/simulator
  - `bwyd/resources/bwyd.tx`: Bwyd language grammar in `textX`

  - `bwyd/kernel.py`: Jupyter wrapper kernel
  - `bwyd/install.py`: Jupyter kernel installer

  - `demo.py`: Python demo app
  - `examples/gnocchi.bwyd`: example Gnocchi recipe in Bwyd, as a script
  - `examples/gnocchi.ipynb`: example Gnocchi recipe in Bwyd, as a Jupyter notebook

  - `tests/*.py`: unit tests


## build a local environment

This project uses [`poetry`](https://python-poetry.org/docs/basic-usage/)
for dependency management, virtual environment, builds, packaging, etc.
To set up an environment locally:

```bash
git clone https://github.com/DerwenAI/bwyd.git
cd bwyd

poetry install --no-root --extras=demo
```

The source code is currently based on Python 3.11 or later.


## run the demo script and notebooks

```bash
poetry run python3 demo.py
```

```bash
poetry run jupyter-lab
```


## development

First, to set up the `dev` and `test` environment:

```bash
poetry install --extras=dev
poetry install --extras=test
```

This project uses [`pre-commit`](https://pre-commit.com/) hooks for
code linting, etc., whenever `git` is used to commit or push.
Be sure to install *after* the `poetry install` is performed.

To run `pre-commit` explicitly:

```bash
poetry run pre-commit
```


######################################################################
TBD:

## install

```bash
python3 -m pip install -e .
python3 -m bwyd.install
```


## uninstall

```bash
./venv/bin/jupyter kernelspec uninstall bwyd
python3 -m pip uninstall bwyd
```
