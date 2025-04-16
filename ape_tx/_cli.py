import click
from ape.cli import ConnectedProviderCommand

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


@cli.command(cls=ConnectedProviderCommand)
@click.argument("contract")
@txn_args()
@sender_option(help="Account to send deploy tx")
def deploy(contract, arguments, sender):
    deploy_contract(contract, *arguments, sender=sender)


@cli.command(cls=ConnectedProviderCommand)
@sender_option(help="The account to transfer from", required=True)
@receiver_option(help="The account to receiver the funds", required=True)
@value_option()
def transfer(sender, receiver, value):
    transfer_money(sender, receiver, value)


@cli.command(cls=ConnectedProviderCommand)
@click.argument("account")
@pretty_option()
def bal(account, pretty):
    balance = get_balance(account, pretty=pretty)
    click.echo(balance)


@cli.command(cls=ConnectedProviderCommand)
@transaction_hash_argument()
@verbose_option()
@raw_option()
def trace(verbose, raw, txn_hash):
    trace_transactions(txn_hash, raw, verbose)


@cli.command(cls=ConnectedProviderCommand)
@contract_option()
@method_option()
@sender_option(required=True)
@txn_args()
def invoke(contract, method, sender, arguments):
    receipt = invoke_function(sender, contract, method, *arguments)
    click.echo(receipt)


@cli.command(cls=ConnectedProviderCommand)
@contract_option()
@method_option()
@txn_args()
def call(contract, method, arguments):
    result = call_function(contract, method, *arguments)
    click.echo(result)
