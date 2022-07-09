def test_deploy_missing_contract(runner, cli):
    result = runner.invoke(cli, ["deploy"])
    assert result.exit_code == 2
    assert "Missing argument 'CONTRACT'" in result.output


def test_deploy_contract_not_found(runner, cli):
    result = runner.invoke(cli, ["deploy", "NotExists"])
    assert result.exit_code == 1
    assert "ERROR: No contract found with name 'NotExists'" in result.output


def test_deploy_missing_sender(runner, cli):
    result = runner.invoke(cli, ["deploy", "Test"])
    assert result.exit_code == 1
    assert "ERROR: Account required to deploy 'Test'" in result.output


def test_deploy_unknown_sender(runner, cli):
    result = runner.invoke(cli, ["deploy", "Test", "--sender", "not-exists"])
    assert result.exit_code == 1
    assert "ERROR: No account with alias 'not-exists'" in result.output


def test_deploy(runner, cli, account_0):
    result = runner.invoke(cli, ["deploy", "Test", "--sender", account_0.alias], input="y\n123\n")
    assert result.exit_code == 0


def test_deploy_with_ctor_args(runner, cli, account_0):
    result = runner.invoke(
        cli,
        ["deploy", "TestWithCtorArgs", account_0.address, "--sender", account_0.alias],
        input="y\n123\n",
    )
    assert result.exit_code == 0
