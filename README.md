# ape-tx

Transact using the command line

## Dependencies

* [python3](https://www.python.org/downloads) version 3.7.2 or greater, python3-dev

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-tx
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/unparalleled-js/ape-tx.git
cd ape-tx
python3 setup.py install
```

## Quick Usage

Deploy contracts:

```bash
ape tx deploy MyContract arg0 arg1 --sender AccountAlias
```

View transaction traces:

```bash
ape tx trace 0x053cba5c12172654d894f66d5670bab6215517a94189a9ffc09bc40a589ec04d
```

## Development

This project is in development and should be considered a beta.
Things might not be in their final state and breaking changes may occur.
Comments, questions, criticisms and pull requests are welcomed.

## License

This project is licensed under the [Apache 2.0](LICENSE).
