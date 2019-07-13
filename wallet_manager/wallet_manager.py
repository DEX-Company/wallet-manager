
from web3 import (
    Web3,
    HTTPProvider
)
from eth_account import Account as EthAccount

from wallet_manager.key_chain import KeyChain

class WalletManager():

    def __init__(self, key_chain_filename=None):
        self._key_chain = KeyChain(key_chain_filename)

    def new_account_local(self, password):
        local_account = web3.eth.account.create(password)
        address = local_account.address
        key_value = EthAccount.encrypt(local_account.privateKey, password)
        self._key_chain.set_key(address, key_value)
        self._key_chain.save()
        return address

    def new_account_host(self, password, url):
        web3 = Web3(HTTPProvider(url))
        address = web3.personal.newAccount(password)
        return address
