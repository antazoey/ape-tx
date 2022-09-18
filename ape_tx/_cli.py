import click
from ape.cli import NetworkBoundCommand, network_option

from ape_tx.options import (
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
from ape_tx.utils import (
    call_function,
    deploy_contract,
    get_balance,
    invoke_function,
    trace_transactions,
    transfer_money,
)


@click.group()
def cli():
    """Transaction utilities"""


@cli.command(cls=NetworkBoundCommand)
@network_option()
@click.argument("contract")
@txn_args()
@sender_option(help="Account to send deploy tx")
def deploy(network, contract, arguments, sender):
    _ = network  # Needed for NetworkBoundCommand
    deploy_contract(contract, *arguments, sender=sender)


@cli.command(cls=NetworkBoundCommand)
@network_option()
@sender_option(help="The account to transfer from", required=True)
@receiver_option(help="The account to receiver the funds", required=True)
@value_option()
def transfer(network, sender, receiver, value):
    _ = network  # Needed for NetworkBoundCommand
    transfer_money(sender, receiver, value)


@cli.command(cls=NetworkBoundCommand)
@network_option()
@click.argument("account")
@pretty_option()
def bal(network, account, pretty):
    _ = network  # Needed for NetworkBoundCommand
    balance = get_balance(account, pretty=pretty)
    click.echo(balance)


@cli.command(cls=NetworkBoundCommand)
@transaction_hash_argument()
@network_option()
@verbose_option()
@raw_option()
def trace(network, verbose, raw, txn_hash):
    _ = network  # Needed for NetworkBoundCommand
    trace_transactions(txn_hash, raw, verbose)


@cli.command(cls=NetworkBoundCommand)
@network_option()
@contract_option()
@method_option()
@sender_option(required=True)
@txn_args()
def invoke(network, contract, method, sender, arguments):
    _ = network  # Needed for NetworkBoundCommand
    receipt = invoke_function(sender, contract, method, *arguments)
    click.echo(receipt)


@cli.command(cls=NetworkBoundCommand)
@network_option()
@contract_option()
@method_option()
@txn_args()
def call(network, contract, method, arguments):
    _ = network  # Needed for NetworkBoundCommand
    result = call_function(contract, method, *arguments)
    click.echo(result)
