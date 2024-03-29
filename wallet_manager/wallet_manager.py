
import json
import requests
import logging

from web3 import (
    Web3,
    HTTPProvider,
    gas_strategies,
)

from eth_account import Account as EthAccount
from wallet_manager.key_chain import KeyChain
from wallet_manager import logger


def as_attrdict(val):
    return dict(val)

class WalletManager():

    def __init__(self, key_chain_filename=None):
        if key_chain_filename:
            self._key_chain = KeyChain(key_chain_filename)


    def new_account(self, password, url=None):
        address = None
        if url:
            web3 = Web3(HTTPProvider(url))
            address = web3.personal.newAccount(password)
            accounts = web3.personal.listAccounts
            if not address in accounts:
                raise NameError(f'Unable to create a new account')
        else:
            local_account = EthAccount.create(password)
            address = local_account.address
            key_value = EthAccount.encrypt(local_account.privateKey, password)
            self._key_chain.set_key(address, key_value)
            self._key_chain.save()
        return address


    def get_chain_status(self, url):
        web3 = Web3(HTTPProvider(url))
        return web3.manager.request_blocking('parity_chainStatus', [])

    def get_chain_name(self, url):
        web3 = Web3(HTTPProvider(url))
        return web3.manager.request_blocking('parity_chain', [])

    def delete_account(self, address, password, url=None):
        if url:
            web3 = Web3(HTTPProvider(url))
            web3.manager.request_blocking('parity_killAccount', [address, password])
        else:
            self._key_chain.delete_key(address)
            self._key_chain.save()

    def list_accounts(self, url=None):
        result = None
        if url:
            web3 = Web3(HTTPProvider(url))
            result = web3.eth.accounts
        else:
            result = self._key_chain.address_list
        return result

    def export_account_json(self, address, password, url=None):
        if url:
            web3 = Web3(HTTPProvider(url))
            raw_data = web3.manager.request_blocking('parity_exportAccount', [address, password])
            result = json.dumps(raw_data, default=as_attrdict)
        else:
            result = json.dumps(self._key_chain.get_key(address))
        return result

    def export_account_key(self, address, password, url=None):
        if url:
            web3 = Web3(HTTPProvider(url))
            raw_data = web3.manager.request_blocking('parity_exportAccount', [address, password])
            key_json = json.dumps(raw_data, default=as_attrdict)
        else:
            key_json = json.dumps(self._key_chain.get_key(address))
        return EthAccount.decrypt(key_json, password)

    def import_account_json(self, json_text, password, url=None):
        if url:
            web3 = Web3(HTTPProvider(url))
            web3.manager.request_blocking('parity_newAccountFromWallet', [json_text, password])
        else:
            data = json.loads(json_text)
            address = Web3.toChecksumAddress(data["address"])
            self._key_chain.set_key(address, data)
            self._key_chain.save()

    def import_account_key(self, address, raw_key, password, url=None):
        if url:
            web3 = Web3(HTTPProvider(url))
            address = web3.manager.request_blocking('parity_newAccountFromSecret', [raw_key, password])
        else:
            self._key_chain.set_key(address, EthAccount.encrypt(raw_key, password))
            self._key_chain.save()
        return address

    def balance_ether(self, address, url):
        web3 = Web3(HTTPProvider(url))
        return web3.fromWei(web3.eth.getBalance(address), 'ether')

    def send_ether(self, from_address, password, to_address, amount, url=None, timeout=120, is_local=False):
        web3 = Web3(HTTPProvider(url))

        if is_local:
            key_json = json.dumps(self._key_chain.get_key(from_address))
            raw_key = EthAccount.decrypt(key_json, password)
            gas_price = web3.manager.request_blocking('eth_gasPrice', [])
            transaction = {
                'from': from_address,
                'to': to_address,
                'value': Web3.toWei(amount, 'ether'),
                'gasPrice': gas_price,
                'gas': 30000,
                'nonce': 0,
            }
            signed = web3.eth.account.signTransaction(transaction, raw_key)
            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

        else:
            from_address = Web3.toChecksumAddress(from_address)
            to_address =  Web3.toChecksumAddress(to_address)
            web3.personal.unlockAccount(from_address, password)
            tx_hash = web3.personal.sendTransaction( {
                'from': from_address,
                'to': to_address,
                'value': Web3.toWei(amount, 'ether'),
            }, password)

        return web3.eth.waitForTransactionReceipt(tx_hash, timeout=timeout)

    def get_ether(self, address, url):
        data  = {
            'address': address,
            'agent': 'server',
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json = data, headers=headers)
        logger.debug(f'response {response.text} {response.status_code}')
        if response.status_code != 200:
            raise ValueError(f'{response.status_code} {response.text}')
