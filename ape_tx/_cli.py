import click
from ape.cli import NetworkBoundCommand, ape_cli_context, network_option

from ape_tx._options import (
    contract_option,
    method_option,
    pretty_option,
    raw_option,
    receiver_option,
    sender_option,
    transaction_hash_argument,
    txn_args,
    value_option,
    verbose_option,
)
from ape_tx._utils import deploy_contract, get_balance, trace_transactions, transfer_money


@click.group()
def cli():
    """Transaction utilities"""


@cli.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
@click.argument("contract")
@txn_args()
@sender_option(help="Account to send deploy tx")
def deploy(cli_ctx, network, contract, arguments, sender):
    _ = network  # Needed for NetworkBoundCommand
    deploy_contract(cli_ctx, contract, *arguments, sender=sender)


@cli.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
@sender_option(help="The account to transfer from", required=True)
@receiver_option(help="The account to receiver the funds", required=True)
@value_option()
def transfer(cli_ctx, network, sender, receiver, value):
    _ = network  # Needed for NetworkBoundCommand
    transfer_money(cli_ctx, sender, receiver, value)


@cli.command(cls=NetworkBoundCommand)
@ape_cli_context()
@network_option()
@click.argument("account")
@pretty_option()
def bal(cli_ctx, network, account, pretty):
    _ = network  # Needed for NetworkBoundCommand
    balance = get_balance(cli_ctx, account, pretty=pretty)
    click.echo(balance)


@cli.command(cls=NetworkBoundCommand)
@ape_cli_context()
@transaction_hash_argument()
@network_option()
@verbose_option()
@raw_option()
def trace(cli_ctx, network, verbose, raw, txn_hash):
    _ = network  # Needed for NetworkBoundCommand
    trace_transactions(cli_ctx, txn_hash, raw, verbose)


@cli.command(cls=NetworkBoundCommand)
@network_option()
@contract_option()
@method_option()
def invoke(network, contract, method):
    pass
