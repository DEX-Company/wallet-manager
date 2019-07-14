
import json

from web3 import (
    Web3,
    HTTPProvider
)
from eth_account import Account as EthAccount

from wallet_manager.key_chain import KeyChain

def as_attrdict(val):
    return dict(val)

class WalletManager():

    def __init__(self, key_chain_filename=None):
        self._key_chain = KeyChain(key_chain_filename)

    def new_account(self, password, url=None):
        address = None
        if url:
            web3 = Web3(HTTPProvider(url))
            address = web3.personal.newAccount(password)
        else:
            local_account = EthAccount.create(password)
            address = local_account.address
            key_value = EthAccount.encrypt(local_account.privateKey, password)
            self._key_chain.set_key(address, key_value)
            self._key_chain.save()
        return address


    def delete_account(address, password, url=None):
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

    def import_account_json (self, json_text, password, url=None):
        if url:
            web3 = Web3(HTTPProvider(url))
            web3.manager.request_blocking('parity_newAccountFromWallet', [json_text, password])
        else:
            data = json.loads(json_text)
            self._key_chain.set_key(data['address'], data)
            self._key_chain.save()
