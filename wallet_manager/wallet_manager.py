
from web3 import (
    Web3,
    HTTPProvider
)
from eth_account import Account as EthAccount

from wallet_manager.key_chain import KeyChain

class WalletManager():

    NETWORK_NAMES = {
        'spree': 'http://localhost:8545',
        'nile': 'https://nile.dev-ocean.com',
        'pacific': 'https://pacific.oceanprotocol.com',
        'host': 'http://localhost:8545',
    }

    def __init__(self, key_chain_filename=None):
        self._errorMessage = None
        self._commands = None
        self._key_chain = KeyChain(key_chain_filename)

    def document_new(sef):
        return {
            'description': 'Create account local and host',
            'params' :[
                'new <password> [local]',
                'new <password> <network_name or url>',
            ],
        }
    def command_new(self):
        address = ''
        password = self._validatePassword(1)
        network_name = self._validateNetworkName(2, 'local')
        if network_name == 'local':
            local_account = web3.eth.account.create(password)
            address = local_account.address
            key_value = EthAccount.encrypt(local_account.privateKey, password)
            self._key_chain.set_key(address, key_value)
            self._key_chain.save()
        else:
            node_url = self._network_name_to_url(network_name)
            if self._is_node_url_valid(node_url):
                web3 = Web3(HTTPProvider(node_url))
                address = web3.personal.newAccount(password)
        return address

    def command_test(self):
        print(self._commands)


    def process(self, commands):
        self._commands = commands
        method_name = f'command_{commands[0]}'
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method()
        else:
            self._errorMessage = f'cannot find method "{method_name}"'

    @property
    def errorMessage(self):
        return self._errorMessage

    @property
    def isError(self):
        return not self._errorMessage is None

    def _validatePassword(self, index,):
        password = None
        if index < len(self._commands):
            password = self._commands[index]
        if not isinstance(password, str):
            self._errorMessage = 'please provide a password'
        return password

    def _validateNetworkName(self, index, default=None):
        network_name = default
        if index < len(self._commands):
            network_name = self._commands[index]
        if network_name:
            network_name = network_name.lower()
        return network_name

    def _network_name_to_url(self, network_name):
        if network_name in self.NETWORK_NAMES:
            return self.NETWORK_NAME[network_name]

    def _is_node_url_valid(self, node_url):
        if node_url is None:
            self._errorMessage = f'Cannot find network name "{network_name}"'
            return False
        return True
