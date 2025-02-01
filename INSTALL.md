## requirements

 - Python 3.10+


## dependencies

  - [`icecream`](https://github.com/gruns/icecream)
  - [`jupyterlab`](https://jupyter.org/)
  - [`pydantic-graph`](https://ai.pydantic.dev/graph/#graph-types)
  - [`textX`](https://textx.github.io/textX/)


## prepare a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -U pip wheel setuptools
```


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


## set up the developer environment

```bash
python3 -m pip install -r requirements-dev.txt
```


## run unit tests

```bash
python3 -m pytest
```


## files

  - `bwyd/parser.py`: Bwyd language parser/simulator
  - `bwyd/resources/bwyd.tx`: Bwyd language grammar in `textX`

  - `bwyd/kernel.py`: Jupyter wrapper kernel
  - `bwyd/install.py`: Jupyter kernel installer

  - `demo.py`: Python demo app
  - `examples/gnocchi.bwyd`: example Gnocchi recipe in Bwyd, as a script
  - `examples/gnocchi.ipynb`: example Gnocchi recipe in Bwyd, as a Jupyter notebook

  - `tests/*.py`: unit tests
