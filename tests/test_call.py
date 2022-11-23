import pytest
from ape.utils import ZERO_ADDRESS

NUMBER_SET = "667"


@pytest.fixture
def contract_with_number_set(contract, account_0):
    account_0.set_autosign(True, passphrase="123")
    contract.set_number(int(NUMBER_SET), sender=account_0)
    account_0.set_autosign(False)
    return contract


def test_call_unknown_contract(runner, cli):
    result = runner.invoke(
        cli,
        [
            "call",
            "--contract",
            ZERO_ADDRESS,
            "--method",
            "favorite_number",
        ],
    )
    assert str(result.exception) == f"Failed to get contract type for address '{ZERO_ADDRESS}'."


def test_call_missing_method(runner, cli, contract):
    result = runner.invoke(
        cli,
        [
            "call",
            "--contract",
            contract.address,
            "123",
        ],
    )
    assert "Error: Missing option '--method'" in result.output


def test_call(runner, cli, contract_with_number_set):
    result = runner.invoke(
        cli,
        [
            "call",
            "--contract",
            contract_with_number_set.address,
            "--method",
            "favorite_number",
        ],
    )
    assert result.exit_code == 0, result.output
    assert result.output == f"{NUMBER_SET}\n"
