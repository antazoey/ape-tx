# ape-tx

Transact using the command line

## Dependencies

* [python3](https://www.python.org/downloads) version 3.8 or greater, python3-dev

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

Check balances:

```bash
ape tx bal AccountAlias --network ethereum:mainnet
```

Transfer money:

```bash
ape tx transfer --from AccountAlias --to 0x8656bDDC790dA239824eE2eA782d350c80AA2Cf4 --value "1 ETH"
```

View transaction traces:

```bash
ape tx trace 0x053cba5c12172654d894f66d5670bab6215517a94189a9ffc09bc40a589ec04d
```

Make calls:

```bash
ape tx call \
  --network "ethereum:mainnet:alchemy" \
   --contract 0x0A56d07a0B8Ba800358DdEEb20eb46a618BFBE27 \
   --method balanceOf \
   0x8656bDDC790dA239824eE2eA782d350c80AA2Cf4
```

Make transactions:

```bash
ape tx invoke \
  --network "ethereum:mainnet:alchemy" \
  --contract 0x0A56d07a0B8Ba800358DdEEb20eb46a618BFBE27 \
  --method transfer \
  --sender AccountAlias \
  0x8656bDDC790dA239824eE2eA782d350c80AA2Cf4 123
```

## Development

This project is in development and should be considered a beta.
Things might not be in their final state and breaking changes may occur.
Comments, questions, criticisms and pull requests are welcomed.
