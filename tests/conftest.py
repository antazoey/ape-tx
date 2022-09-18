import json
import shutil
from pathlib import Path
from tempfile import mkdtemp
from typing import Dict

import ape
import pytest
from click.testing import CliRunner

from ape_tx._cli import cli as _cli

# NOTE: Ensure that we don't use local paths for these
ape.config.DATA_FOLDER = Path(mkdtemp()).resolve()
PROJECT_FOLDER = Path(mkdtemp()).resolve()
ALIAS_0 = "test_0"
ALIAS_1 = "test_1"


@pytest.fixture(scope="session")
def accounts():
    return ape.accounts


@pytest.fixture(scope="session")
def config():
    return ape.config


@pytest.fixture(scope="session")
def convert():
    return ape.convert


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
def account_params_0():
    # accounts.test_accounts[0], passphrase=123
    return _get_keyfile_params(
        "1e59ce931b4cfea3fe4b875411e280e173cb7a9c",
        "3ff681755852970be81d1098626fa557",
        "6885728b31acd33f555a9cd434e9bfb28fbd44a59f5ae90678b5fef16507a806",
        "9c07fdd7984569ec7072b027add7c525",
        "c8b014834360682098573b27cf4265858982796ac76305ab01ad9b1eb4fb468d",
        "99a88fb6-48d4-4c70-adbe-752f7361555c",
    )


@pytest.fixture(scope="session")
def account_params_1():
    # accounts.test_accounts[1], passphrase=123
    return _get_keyfile_params(
        "c89d42189f0450c2b2c3c61f58ec5d628176a1e7",
        "6e557bac331a8f2f1c13eba40e751b56",
        "685574378bd358767180965ce947be0a11f3cc7ce1dca2f716f61cd8655daca2",
        "6b2987ee458ec02c8254b9025927097d",
        "2bae97aeb06b1b5acbb04e10a944e1ed6cf54b582ac382eec9a53935cde3f36f",
        "8b5ce98f-51a2-4876-9562-976946fbd45c",
    )


def _get_keyfile_params(
    address: str, cipherparams: str, ciphertext: str, salt: str, mac: str, id: str
) -> Dict:
    return {
        "address": address,
        "crypto": {
            "cipher": "aes-128-ctr",
            "cipherparams": {"iv": cipherparams},
            "ciphertext": ciphertext,
            "kdf": "scrypt",
            "kdfparams": {
                "dklen": 32,
                "n": 262144,
                "r": 1,
                "p": 8,
                "salt": salt,
            },
            "mac": mac,
        },
        "id": id,
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
def account_path_0(accounts_path):
    return _make_account_path(accounts_path, ALIAS_0)


@pytest.fixture(scope="session", autouse=True)
def account_path_1(accounts_path):
    return _make_account_path(accounts_path, ALIAS_1)


def _make_account_path(base_path: Path, alias: str):
    path = base_path / f"{alias}.json"

    if path.exists():
        # Corrupted from a previous test
        path.unlink()

    return path


@pytest.fixture(autouse=True)
def account_file_0(account_path_0, account_params_0):
    path = _make_account(account_path_0, account_params_0)
    yield path
    _clean_account_path(path)


@pytest.fixture(autouse=True)
def account_file_1(account_path_1, account_params_1):
    path = _make_account(account_path_1, account_params_1)
    yield path
    _clean_account_path(path)


def _make_account(path: Path, params: Dict):
    path.write_text(json.dumps(params))
    return path


def _clean_account_path(path: Path):
    if path.exists():
        path.unlink()


@pytest.fixture(autouse=True, scope="session")
def contracts_folder(project):
    source_path = Path(__file__).parent / "contracts"
    destination_path = project.contracts_folder
    shutil.copytree(source_path, destination_path)
    return destination_path


@pytest.fixture()
def account_0(accounts):
    return accounts.load(ALIAS_0)


@pytest.fixture()
def account_1(accounts):
    return accounts.load(ALIAS_1)


@pytest.fixture
def dev_account(accounts):
    return accounts.test_accounts[0]


@pytest.fixture
def contract(project, dev_account):
    return project.Test.deploy(sender=dev_account)
