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

    def document_delete(self):
        return {
            'description': 'Delete account on local and host',
            'params': [
                'delete <address> <password> [local]',
                'delete <address> <password> <network_name or url>',
            ]
        }

    def command_delete(self):
        pass

    def document_copy(self):
        return [
            {
                'description': 'Copy local account to host',
                'params': [
                    'copy local <local_address> <password> <network_name or url>',
                ],
            },
            {
                'description': 'Copy host account to local',
                'params': [
                    'copy <network_name or url> <host_address> <password> [local]',
                ],
            }
        ]
    def command_copy(self):
        pass

    def document_list(self):
        return {
            'description': 'List accounts on local and host',
            'params': [
                'list [local]',
                'list <network_name or url>',
            ],
        }
    def command_list(self):
        pass

    def document_export(self):
        return {
            'description': 'Export local and host account to JSON or private key',
            'params': [
                '[--as_json] [--as_key] export <address> <password> [local]',
                '[--as_json] [--as_key] export <address> <password> <network_name or url>',
            ],
        }

    def document_import(self):
        return {
            'description': 'Import local and host account from JSON key file, or private key',
            'params': [
                '[--as_json] [--as_key] import <json_file or string> <password> [local]',
                '[--as_json] [--as_key] import <json_file or string> <password> <network_name or url>',
            ],
        }
    def command_import(self):
        pass

    def document_password(self):
        return {
            'description': 'Change account password on local and host',
            'params': [
                'password <address> <old_password> <new_password> [local]',
                'password <address> <old_password> <new_password> <network_name or url>',
            ],
        }

    def document_get(self):
        return [
            {
                'description': 'Request ether from faucet',
                'params': [
                    'get ether <address> [local]',
                    'get ether <address> <network_name or url>',
                ],
            },
            {
                'description': 'Request Ocean tokens on test networks',
                'params': [
                    'get tokens <address> <password> [local] [amount]',
                    'get tokens <address> <password> <network_name or url> [amount]',
                ],
            }
        ]
    def command_get(self):
        pass

    def document_send(self):
        return [
            {
                'description': 'Transfer Ocean tokens to another account',
                'params': [
                    'send tokens <from_address> <password> [local] <to_address>',
                    'send tokens <from_address> <password> <network_name or url> <to_address>',
                ],
            },
            {
                'description': 'Transfer Ocean ether to another account',
                'params': [
                    'send ether <from_address> <password> <to_address>',
                    'send ether <from_address> <password> <network_name or url> <to_address>',
                ],
            }
        ]
    def command_send(self):
        pass
        
    def command_password(self):
        pass


    def command_export(self):
        pass



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
                if isinstance(values, list):
                    for value in values:
                        items += self._expand_document_item(value)
                else:
                    items += self._expand_document_item(values)
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

    def _expand_document_item(self, value):
        items = []
        items.append(f'\n{value["description"]}')
        for param in value['params']:
            items.append(f'    {param}')
        return items
