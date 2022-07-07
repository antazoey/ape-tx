import click
from ape.cli import NetworkBoundCommand, ape_cli_context, network_option

verbose_option = click.option("--verbose", is_flag=True, help="Show more information on the trace.")
raw_option = click.option("--raw", is_flag=True, help="Show the raw, non-pretty trace.")


@click.group()
def cli():
    """Transaction utilities"""


@cli.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
@click.argument("contract")
@click.argument("arguments", nargs=-1)
@click.option("--sender", help="An account alias")
def deploy(cli_ctx, network, contract, arguments, sender):
    _ = network_option  # Needed for NetworkBoundCommand
    contract_container = cli_ctx.project_manager.get_contract(contract)

    if sender:
        contract_container.deploy(*arguments, sender=cli_ctx.account_manager.load(sender))
    else:
        contract_container.deploy(*arguments)


def txn_hash_callback(ctx, param, value):
    # Removes duplicate entries
    hash_set = set()
    for tx_hash in value:
        hash_set.add(tx_hash)

    return [h for h in hash_set]


@cli.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
@verbose_option
@raw_option
@click.argument("txn_hash", nargs=-1, callback=txn_hash_callback)
def trace(cli_ctx, network, verbose, raw, txn_hash):
    _ = network  # Needed for NetworkBoundCommand
    if not txn_hash:
        return

    for index in range(len(txn_hash)):
        receipt = cli_ctx.network_manager.provider.get_transaction(txn_hash[index])

        if raw:
            call_tree = cli_ctx.provider.get_call_tree(receipt.txn_hash)
            click.echo(repr(call_tree))
        else:
            receipt.show_trace(verbose=verbose)

        if index < len(txn_hash) - 1:
            click.echo()
