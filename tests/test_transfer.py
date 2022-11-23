def test_transfer_missing_from(cli, runner, account_1):
    result = runner.invoke(cli, ["transfer", "--receiver", account_1.address, "--value", "10 gwei"])
    assert "Missing option '--sender'" in result.output


def test_transfer_missing_to(cli, runner, account_0):
    result = runner.invoke(cli, ["transfer", "--sender", account_0.address, "--value", "10 gwei"])
    assert "Missing option '--receiver'" in result.output


def test_transfer_missing_value(cli, runner, account_0, account_1):
    result = runner.invoke(
        cli, ["transfer", "--sender", account_0.address, "--receiver", account_1.address]
    )
    assert "Missing option '--value'" in result.output


def test_transfer_decimal_value(cli, runner, account_0, account_1, convert):
    value = convert("100 gwei", int)
    result = runner.invoke(
        cli,
        [
            "transfer",
            "--sender",
            account_0.address,
            "--receiver",
            account_1.address,
            "--value",
            str(value),
        ],
        input="y\n123\n",
    )
    assert result.exit_code == 0
