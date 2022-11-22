from typing import Any, List, Optional, Tuple, Union

import ape
import click
from ape.api import AccountAPI, ReceiptAPI
from ape.cli import Abort
from ape.contracts import ContractContainer, ContractInstance
from ape.contracts.base import ContractCallHandler, ContractTransactionHandler
from ape.exceptions import ArgumentsLengthError, SignatureError
from ethpm_types.abi import MethodABI


def deploy_contract(contract: str, *args, sender: Optional[str] = None):
    container = get_contract(contract)
    if sender:
        account = get_account(sender)
        container.deploy(*args, sender=account)
    else:
        try:
            container.deploy(*args)
        except SignatureError:
            raise Abort(f"Account required to deploy '{contract}'")


def transfer_money(sender: str, receiver: str, value: int):
    sender_account = get_account(sender)
    sender_account.transfer(receiver, value)


def get_balance(account: str, pretty: bool = False):
    # Only load account when its an alias to support getting balances for non-local accounts.
    account = get_account(account).address if not account.startswith("0x") else account
    balance = ape.networks.provider.get_balance(account)
    if not pretty:
        return balance

    ecosystem_name = ape.networks.provider.network.ecosystem.name.lower()
    if ecosystem_name == "ethereum":
        symbol = "ETH"
        decimals = 18
    else:
        raise Abort(f"'--pretty' not currently supported on ecosystem '{ecosystem_name}'.")

    rounded_value = round(balance / 10**decimals, 8)
    if rounded_value == int(rounded_value):
        # Is whole number
        rounded_value = int(rounded_value)

    return f"{rounded_value} {symbol}"


def get_contract(contract_id: str) -> ContractContainer:
    try:
        return ape.project.get_contract(contract_id)
    except ValueError as err:
        raise Abort(str(err))


def get_account(account_id: str) -> AccountAPI:
    if not account_id:
        raise Abort(f"Missing account '{account_id}'.")

    try:
        if account_id.startswith("0x"):
            return ape.accounts[account_id]
        else:
            return ape.accounts.load(account_id)

    except IndexError as err:
        raise Abort(str(err))


def trace_transactions(txn_hash: List[str], raw: bool, verbose: bool):
    if not txn_hash:
        raise Abort("No transaction hashes given.")

    for index in range(len(txn_hash)):
        receipt = ape.networks.provider.get_receipt(txn_hash[index])

        if raw:
            call_tree = ape.networks.provider.get_call_tree(receipt.txn_hash)
            click.echo(repr(call_tree))
        else:
            receipt.show_trace(verbose=verbose)

        if index < len(txn_hash) - 1:
            click.echo()


def call_function(contract_address: str, method_name: str, *arguments) -> Any:
    contract = ape.Contract(contract_address)
    return _call_contract_method(contract, method_name, *arguments)


def invoke_function(sender: str, contract_address: str, method_name: str, *arguments) -> ReceiptAPI:
    contract = ape.Contract(contract_address)
    account = get_account(sender)
    return _call_contract_method(contract, method_name, *arguments, sender=account)


def _call_contract_method(contract: ContractInstance, method_name: str, *args, **kwargs):
    contract_method = getattr(contract, method_name)
    arguments = _fix_args(contract_method, *args)
    return contract_method(*arguments, **kwargs)


def _fix_args(
    method_handler: Union[ContractCallHandler, ContractTransactionHandler], *arguments
) -> List:
    selected_abi = _select_method_abi(method_handler.abis, arguments)
    converted_arguments: List[Any] = []

    # The CLI always uses str for ints, fix that here
    for abi, argument in zip(selected_abi.inputs, arguments):
        if "int" in str(abi.type) and not str(abi.type).endswith("]"):
            converted_arguments.append(int(argument))
        elif "int" in str(abi.type) and str(abi.type).endswith("]"):
            converted_arguments.append([int(v) for v in argument])
        else:
            converted_arguments.append(argument)

    return converted_arguments


def _select_method_abi(abis: List[MethodABI], args: Union[Tuple, List]) -> MethodABI:
    args = args or []
    selected_abi = None
    for abi in abis:
        inputs = abi.inputs or []
        if len(args) == len(inputs):
            selected_abi = abi

    if not selected_abi:
        raise ArgumentsLengthError(len(args))

    return selected_abi
