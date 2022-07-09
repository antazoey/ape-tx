from typing import Optional

from ape.api import AccountAPI
from ape.contracts import ContractContainer
from ape.exceptions import SignatureError


def deploy_contract(cli_ctx, contract: str, *args, sender: Optional[str] = None):
    container = load_contract(cli_ctx, contract)
    if sender:
        account = load_account(cli_ctx, sender)
        container.deploy(*args, sender=account)
    else:
        try:
            container.deploy(*args)
        except SignatureError:
            return cli_ctx.abort(f"Account required to deploy '{contract}'")


def load_contract(cli_ctx, contract_id: str) -> ContractContainer:
    try:
        return cli_ctx.project_manager.get_contract(contract_id)
    except ValueError as err:
        return cli_ctx.abort(str(err))


def load_account(cli_ctx, account_id: str) -> AccountAPI:
    try:
        if account_id.startswith("0x"):
            return cli_ctx.account_manager[account_id]
        else:
            return cli_ctx.account_manager.load(account_id)

    except IndexError as err:
        return cli_ctx.abort(str(err))
