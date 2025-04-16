from ape.utils import ZERO_ADDRESS


def test_invoke_unknown_contract(runner, cli, account_0):
    result = runner.invoke(
        cli,
        (
            "invoke",
            "--contract",
            ZERO_ADDRESS,
            "--method",
            "set_number",
            "--sender",
            account_0.alias,
            "123",
        ),
    )
    assert str(result.exception) == f"Failed to get contract type for address '{ZERO_ADDRESS}'."


def test_invoke_missing_sender(runner, cli, contract):
    result = runner.invoke(
        cli,
        (
            "invoke",
            "--contract",
            contract.address,
            "--method",
            "set_number",
            "123",
        ),
    )
    assert "Error: Missing option '--sender'" in result.output


def test_invoke_missing_method(runner, cli, contract, account_0):
    result = runner.invoke(
        cli,
        (
            "invoke",
            "--contract",
            contract.address,
            "--sender",
            account_0.alias,
            "123",
        ),
    )
    assert "Error: Missing option '--method'" in result.output


def test_invoke_missing_arguments_when_needed(runner, cli, account_0, contract):
    result = runner.invoke(
        cli,
        (
            "invoke",
            "--contract",
            contract.address,
            "--method",
            "set_number",
            "--sender",
            account_0.alias,
        ),
    )
    assert (
        str(result.exception)
        == "The number of the given arguments (0) do not match what is defined in the ABI."
    )


def test_invoke(runner, cli, account_0, contract):
    result = runner.invoke(
        cli,
        (
            "invoke",
            "--contract",
            contract.address,
            "--method",
            "set_number",
            "--sender",
            account_0.alias,
            "123",
        ),
        input="y\n123\n",
    )
    assert result.exit_code == 0, result.output
    assert contract.address in result.output
    assert account_0.address in result.output
