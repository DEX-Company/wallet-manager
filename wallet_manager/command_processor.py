import inspect
import re

from web3 import (
    Web3,
    HTTPProvider
)
from eth_account import Account as EthAccount

from wallet_manager.wallet_manager import WalletManager

class CommandProcessor():

    NETWORK_NAMES = {
        'spree': 'http://localhost:8545',
        'nile': 'https://nile.dev-ocean.com',
        'pacific': 'https://pacific.oceanprotocol.com',
        'host': 'http://localhost:8545',
    }

    def __init__(self, key_chain_filename=None):
        self._errorMessage = None
        self._commands = None
        self._wallet = WalletManager(key_chain_filename=key_chain_filename)

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
            address = self._wallet.new_account_local(password)
        else:
            node_url = self._network_name_to_url(network_name)
            if self._is_node_url_valid(node_url):
                address = self._wallet.new_account_host(password, node_url)
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

    def command_list(self):
        items = []
        for name in dir(self):
            if re.match('^document_', name):
                method = getattr(self, name)
                values = method()
                items.append(f'\n{values["description"]}')
                for param in values['params']:
                    items.append(f'    {param}')
        return items

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
