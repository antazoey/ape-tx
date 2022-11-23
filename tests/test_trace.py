def test_trace_no_hash_given(cli, runner):
    result = runner.invoke(cli, ["trace"])
    assert "ERROR: No transaction hashes given" in result.output


def test_trace_txn_hash_not_found(cli, runner):
    txn_hash = "0x053cba5c12172654d894f66d5670bab6215517a94189a9ffc09bc40a589ec04d"
    result = runner.invoke(cli, ["trace", txn_hash])
    assert result.exit_code == 1
    assert str(result.exception) == f"Transaction '{txn_hash}' not found."
