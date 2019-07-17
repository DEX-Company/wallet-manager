"""

Conftest.py


"""
import pytest
import tempfile
import os

from unittest.mock import Mock

PARITY_NODE_URL = 'http://localhost:8545'
KEY_CHAIN_FILENAME = 'test_key_chain.json'
TEST_ACCOUNT_ADDRESS = '0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0'
TEST_ACCOUNT_PASSWORD = 'secret'

@pytest.fixture(scope="module")
def resources():
    data = Mock()
    data.host_url = PARITY_NODE_URL
    data.key_chain_filename = os.path.join(tempfile.gettempdir(), KEY_CHAIN_FILENAME)
    data.test_account = Mock()
    data.test_account.address = TEST_ACCOUNT_ADDRESS
    data.test_account.password = TEST_ACCOUNT_PASSWORD
    return data
