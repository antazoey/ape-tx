import ape
import click


def sender_option(**kwargs):
    data = {"help": "The account to send the transaction", **kwargs}
    return click.option("--sender", **data)


def receiver_option(**kwargs):
    data = {"help": "The account to receive the transaction", **kwargs}
    return click.option("--receiver", **data)


def txn_args():
    return click.argument("arguments", nargs=-1)


def _value_callback(ctx, param, value):
    if not value.isnumeric():
        return ape.convert(value, int)

    return int(value)


def value_option():
    return click.option(
        "--value",
        help="The amount to include in the transaction",
        required=True,
        callback=_value_callback,
    )


def _txn_hash_callback(ctx, param, value):
    # Removes duplicate entries
    hash_set = set()
    for tx_hash in value:
        hash_set.add(tx_hash)

    return [h for h in hash_set]


def transaction_hash_argument():
    return click.argument("txn_hash", nargs=-1, callback=_txn_hash_callback)


def contract_option():
    return click.option("--contract", help="A contract address.")


def method_option():
    return click.option("--method", help="A contract function name.", required=True)


def pretty_option():
    return click.option("--pretty", is_flag=True)


def verbose_option():
    return click.option("--verbose", is_flag=True, help="Show more information.")


def raw_option():
    return click.option("--raw", is_flag=True, help="Show raw, un-pretty data.")
