from typing import List, Optional

import click
from ape.api import AccountAPI
from ape.contracts import ContractContainer
from ape.exceptions import SignatureError


def deploy_contract(cli_ctx, contract: str, *args, sender: Optional[str] = None):
    container = get_contract(cli_ctx, contract)
    if sender:
        account = get_account(cli_ctx, sender)
        container.deploy(*args, sender=account)
    else:
        try:
            container.deploy(*args)
        except SignatureError:
            return cli_ctx.abort(f"Account required to deploy '{contract}'")


def transfer_money(cli_ctx, sender: str, receiver: str, value: int):
    sender_account = get_account(cli_ctx, sender)
    sender_account.transfer(receiver, value)


def get_balance(cli_ctx, account: str, pretty: bool = False):
    # Only load account when its an alias to support getting balances for non-local accounts.
    account = get_account(cli_ctx, account).address if not account.startswith("0x") else account
    balance = cli_ctx.provider.get_balance(account)
    if not pretty:
        return balance

    ecosystem_name = cli_ctx.provider.network.ecosystem.name.lower()
    if ecosystem_name == "ethereum":
        symbol = "ETH"
        decimals = 18
    else:
        return cli_ctx.abort(f"'--pretty' not currently supported on ecosystem '{ecosystem_name}'.")

    rounded_value = round(balance / 10**decimals, 8)
    if rounded_value == int(rounded_value):
        # Is whole number
        rounded_value = int(rounded_value)

    return f"{rounded_value} {symbol}"


def get_contract(cli_ctx, contract_id: str) -> ContractContainer:
    try:
        return cli_ctx.project_manager.get_contract(contract_id)
    except ValueError as err:
        return cli_ctx.abort(str(err))


def get_account(cli_ctx, account_id: str) -> AccountAPI:
    if not account_id:
        return cli_ctx.abort(f"Missing account '{account_id}'.")

    try:
        if account_id.startswith("0x"):
            return cli_ctx.account_manager[account_id]
        else:
            return cli_ctx.account_manager.load(account_id)

    except IndexError as err:
        return cli_ctx.abort(str(err))


def trace_transactions(cli_ctx, txn_hash: List[str], raw: bool, verbose: bool):
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
