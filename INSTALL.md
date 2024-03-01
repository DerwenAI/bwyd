## requirements

 - Python 3.10+


## dependencies

  - [`textX`](https://textx.github.io/textX/)


## prepare a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -U pip wheel setuptools
```

## install the Jupyter kernel

```bash
./venv/bin/jupyter kernelspec install --user bwyd
./venv/bin/jupyter kernelspec list
```

## files

  - `bwyd.py`: Bwyd language parser/simulator
  - `bwyd.tx`: Bwyd language grammar in `textX`

  - `bwyd/kernel.json`: Jupyter kernel spec
  - `kernel.py`: Jupyter wrapper kernel

  - `gnocchi.ipynb`: example Gnocchi recipe in Bwyd, as a notebook
  - `gnocchi.bwyd`: example Gnocchi recipe in Bwyd, as a script
