def test_bal_alias(cli, runner, account_0):
    result = runner.invoke(cli, ["bal", account_0.alias])
    actual = result.output.strip()
    assert actual.isnumeric()
    assert int(actual) > 0


def test_bal_address(cli, runner, account_0):
    result = runner.invoke(cli, ["bal", account_0.address])
    actual = result.output.strip()
    assert actual.isdecimal()
    assert int(actual) > 0


def test_bal_pretty(cli, runner, account_0):
    result = runner.invoke(cli, ["bal", account_0.alias, "--pretty"])
    actual = result.output.strip()
    parts = actual.split(" ")
    assert len(parts) == 2
    assert parts[0].split(".")[0].isdecimal()
    assert parts[1] == "ETH"
