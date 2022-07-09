import json
import shutil
from pathlib import Path
from tempfile import mkdtemp

import ape
import pytest
from click.testing import CliRunner

from ape_tx._cli import cli as _cli

# NOTE: Ensure that we don't use local paths for these
ape.config.DATA_FOLDER = Path(mkdtemp()).resolve()
PROJECT_FOLDER = Path(mkdtemp()).resolve()
ALIAS = "test"


@pytest.fixture(scope="session")
def accounts():
    return ape.accounts


@pytest.fixture(scope="session")
def config():
    return ape.config


@pytest.fixture(scope="session")
def networks():
    return ape.networks


@pytest.fixture(scope="session")
def project(config):
    with config.using_project(PROJECT_FOLDER) as project:
        yield project


@pytest.fixture(scope="session", autouse=True)
def provider(networks):
    with networks.ethereum.local.use_provider("test") as provider:
        yield provider


@pytest.fixture(scope="session")
def runner():
    return CliRunner()


@pytest.fixture(scope="session")
def cli():
    return _cli


@pytest.fixture(scope="session")
def keyfile_params():
    # NOTE: password is '123'.
    # NOTE: account is same as accounts.test_accounts[0] so it has funding.
    return {
        "address": "1e59ce931b4cfea3fe4b875411e280e173cb7a9c",
        "crypto": {
            "cipher": "aes-128-ctr",
            "cipherparams": {"iv": "3ff681755852970be81d1098626fa557"},
            "ciphertext": "6885728b31acd33f555a9cd434e9bfb28fbd44a59f5ae90678b5fef16507a806",
            "kdf": "scrypt",
            "kdfparams": {
                "dklen": 32,
                "n": 262144,
                "r": 1,
                "p": 8,
                "salt": "9c07fdd7984569ec7072b027add7c525",
            },
            "mac": "c8b014834360682098573b27cf4265858982796ac76305ab01ad9b1eb4fb468d",
        },
        "id": "99a88fb6-48d4-4c70-adbe-752f7361555c",
        "version": 3,
    }


@pytest.fixture(scope="session")
def accounts_path(config):
    path = Path(config.DATA_FOLDER) / "accounts"
    path.mkdir(exist_ok=True, parents=True)

    yield path

    if path.exists():
        shutil.rmtree(path)


@pytest.fixture(scope="session", autouse=True)
def keyfile_path(accounts_path):
    path = accounts_path / f"{ALIAS}.json"

    if path.exists():
        # Corrupted from a previous test
        path.unlink()

    return path


@pytest.fixture(autouse=True)
def keyfile(keyfile_path, keyfile_params):
    keyfile_path.write_text(json.dumps(keyfile_params))

    yield keyfile_path

    if keyfile_path.exists():
        keyfile_path.unlink()


@pytest.fixture(autouse=True, scope="session")
def contracts_folder(project):
    source_path = Path(__file__).parent / "contracts"
    destination_path = project.contracts_folder
    shutil.copytree(source_path, destination_path)
    return destination_path


@pytest.fixture()
def account(accounts):
    return accounts.load(ALIAS)
