"""

Test wallet_manager module

"""
import secrets
import time

from wallet_manager.wallet_manager import WalletManager

def test_accounts_local(resources):
    wallet = WalletManager(resources.key_chain_filename)
    password = secrets.token_hex(32)

    # new account
    address = wallet.new_account(password)
    assert(address)


    # find address in list
    account_list = wallet.list_accounts()
    assert(account_list)
    assert(address in account_list)

    # export_account_json
    json_data = wallet.export_account_json(address, password)
    assert(json_data)

    # export_account_key
    raw_key = wallet.export_account_key(address, password)
    assert(raw_key)

    # delete account
    wallet.delete_account(address, password)
    account_list = wallet.list_accounts()
    assert(account_list)
    assert(address not in account_list)


def test_accounts_host(resources):
    wallet = WalletManager(resources.key_chain_filename)
    password = secrets.token_hex(32)

    # new account
    address = wallet.new_account(password, resources.host_url)
    assert(address)

    # find address in list
    account_list = wallet.list_accounts(resources.host_url)
    assert(account_list)
    assert(address in account_list)

    # export_account_json
    json_data = wallet.export_account_json(address, password, resources.host_url)
    assert(json_data)

    # export_account_key
    raw_key = wallet.export_account_key(address, password, resources.host_url)
    assert(raw_key)

    # delete account
    wallet.delete_account(address, password, resources.host_url)
    account_list = wallet.list_accounts(resources.host_url)
    assert(account_list)
    assert(address not in account_list)

def test_account_import_from_local_to_host(resources):

    wallet = WalletManager(resources.key_chain_filename)
    password = secrets.token_hex(32)

    # new account in local
    address = wallet.new_account(password)
    assert(address)

    # export as json -> import as json to host
    # export_account_json
    json_data = wallet.export_account_json(address, password)
    assert(json_data)

    wallet.import_account_json(json_data, password, resources.host_url)
    # find address in list
    account_list = wallet.list_accounts(resources.host_url)
    assert(account_list)
    assert(address in account_list)

    # cleanup
    wallet.delete_account(address, password, resources.host_url)
    wallet.delete_account(address, password)


def test_account_import_from_host_to_local(resources):

    wallet = WalletManager(resources.key_chain_filename)
    password = secrets.token_hex(32)

    # new account in host
    address = wallet.new_account(password, resources.host_url)
    assert(address)

    # export as json -> import as json to local
    # export_account_json
    json_data = wallet.export_account_json(address, password, resources.host_url)
    assert(json_data)

    wallet.import_account_json(json_data, password)
    # find address in list
    account_list = wallet.list_accounts()
    assert(account_list)
    assert(address in account_list)
    # cleanup
    wallet.delete_account(address, password, resources.host_url)
    wallet.delete_account(address, password)


def test_send_ether(resources):

    wallet = WalletManager(resources.key_chain_filename)
    password = secrets.token_hex(32)

    # create local account
    local_address = wallet.new_account(password)
    assert(local_address)

    # send host -> local from host
    amount = 100
    test_account = resources.test_account
    wallet.send_ether(test_account.address, test_account.password, local_address, amount, resources.host_url)

    time.sleep(2)
    balance = wallet.balance_ether(local_address, resources.host_url)
    assert(balance == amount)

    # create new host account
    host_address = wallet.new_account(password, resources.host_url)
    assert(host_address)

    # send local -> host address from local signed transaction
    amount -= 1

    wallet.send_ether(local_address, password, host_address, amount, resources.host_url, is_local=True)
    time.sleep(2)

    balance = wallet.balance_ether(host_address, resources.host_url)
    assert(balance == amount)


    wallet.delete_account(local_address, password)
    wallet.delete_account(host_address, password, resources.host_url)

