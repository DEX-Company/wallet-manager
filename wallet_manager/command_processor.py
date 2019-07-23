import inspect
import re
import os.path
import json

from web3 import (
    Web3,
    HTTPProvider
)
from eth_account import Account as EthAccount
from starfish import Ocean
from starfish.account import Account as OceanAccount

from wallet_manager.wallet_manager import WalletManager


class CommandProcessError(Exception):
    pass

class CommandProcessor():

    NETWORK_NAMES = {
        'spree': {
            'url': 'http://localhost:8545',
            'faucet_account' : ['0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0', 'secret'],
        },
        'nile': {
            'url': 'https://nile.dev-ocean.com',
            'faucet_url' : 'https://nile.dev-ocean.com/faucet',
        },
        'pacific': {
            'url': 'https://pacific.oceanprotocol.com',
            'faucet_url' : 'https://faucet.oceanprotocol.com/faucet',
        },
        'duero': {
            'url': 'https://duero.dev-ocean.com',
            'faucet_url' : 'https://faucet.duero.dev-ocean.com/faucet',
        },
        'host': {
            'url': 'http://localhost:8545',
        }
    }

    def __init__(self, key_chain_filename=None):
        self._commands = None
        self._output = []
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
        password = self._validate_password(1)
        network_name = self._validate_network_name_url(2, 'local')
        if network_name == 'local':
            address = self._wallet.new_account(password)
        else:
            node_url = self._validate_network_name_to_value(network_name)
            address = self._wallet.new_account(password, node_url)
        self._add_output(f'new account address {address}')

    def document_delete(self):
        return {
            'description': 'Delete account on local and host',
            'params': [
                'delete <address> <password> [local]',
                'delete <address> <password> <network_name or url>',
            ]
        }

    def command_delete(self):
        address = self._validate_address(1)
        password = self._validate_password(2)
        network_name = self._validate_network_name_url(3, 'local')
        if network_name == 'local':
            result = self._wallet.delete_account(address, password)
        else:
            node_url = self._validate_network_name_to_value(network_name)
            self._wallet.delete_account(address, password, node_url)
        self._add_output(f'delete account {address}')

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
        result = None
        network_name = self._validate_network_name_url(1, 'local')
        if network_name == 'local':
            result = self._wallet.list_accounts()
        else:
            node_url = self._validate_network_name_to_value(network_name)
            result = self._wallet.list_accounts(node_url)
        self._add_output(result)

    def document_export(self):
        return {
            'description': 'Export local and host account to JSON or private key',
            'params': [
                '[--as_json] [--as_key] export <address> <password> [local]',
                '[--as_json] [--as_key] export <address> <password> <network_name or url>',
            ],
        }

    def command_export(self):
        address = self._validate_address(1)
        password = self._validate_password(2)
        network_name = self._validate_network_name_url(3, 'local')

        if network_name == 'local':
            result = self._wallet.export_account_json(address, password)
        else:
            node_url = self._validate_network_name_to_value(network_name)
            result = self._wallet.export_account_json(address, password, node_url)

        self._add_output(f'Address {address} key:')
        self._add_output(result)


    def document_import(self):
        return {
            'description': 'Import local and host account from JSON key file, or private key',
            'params': [
                '[--as_json] [--as_key] import <json_file or string> <password> [local]',
                '[--as_json] [--as_key] import <json_file or string> <password> <network_name or url>',
            ],
        }

    def command_import(self):
        json_text = self._validate_json_text(1)
        password = self._validate_password(2)
        network_name = self._validate_network_name_url(3, 'local')
        if network_name == 'local':
            result = self._wallet.import_account_json(json_text, password)
        else:
            node_url = self._validate_network_name_to_value(network_name)
            result = self._wallet.import_account_json(json_text, password, node_url)


    def document_password(self):
        return {
            'description': 'Change account password on local and host',
            'params': [
                'password <address> <old_password> <new_password> [local]',
                'password <address> <old_password> <new_password> <network_name or url>',
            ],
        }

    def command_password(self):
        pass

    def document_get(self):
        return [
            {
                'description': 'Request ether from faucet',
                'params': [
                    'get ether <address> <network_name or faucet url>',
                ],
            },
            {
                'description': 'Request Ocean tokens on test networks',
                'params': [
                    'get tokens <address> <password> <network_name or url> [amount]',
                ],
            }
        ]
    def command_get(self):
        sub_command = self._validate_sub_command(1, ['ether', 'tokens'])
        address = self._validate_address(2)
        if sub_command == 'tokens':
            password = self._validate_password(3)
            network_name = self._validate_network_name_url(4)
            amount = self._validate_amount(5, 10)
            node_url = self._validate_network_name_to_value(network_name)
            ocean = Ocean(keeper_url=node_url)
            account = OceanAccount(ocean, address)
            account.unlock(password)
            account.request_tokens(amount)
            self._add_output(f'{address}  ocean tokens: {account.ocean_balance}')
        elif sub_command == 'ether':
            network_name = self._validate_network_name_url(3)
            faucet_url = self._validate_network_name_to_value(network_name, False, 'faucet_url')
            if faucet_url:
                self._wallet.get_ether(address, faucet_url)
                return
            faucet_account = self._validate_network_name_to_value(network_name, False, 'faucet_account')
            if faucet_account:
                # if list then it's a address/password of an account that has ether
                node_url = self._validate_network_name_to_value(network_name)
                self._wallet.send_ether(faucet_account[0], faucet_account[1], address, 3, node_url)
                return
            raise CommandProcessError(f'Warning: The network name {network_name} does not have a faucet')

    def document_balance(self):
        return {
            'description': 'Show the ether and Ocean token balance',
            'params': [
                'balance <address> <network_name or faucet url>',
            ],
        }
    def command_balance(self):
        address = self._validate_address(1)
        network_name = self._validate_network_name_url(2)
        node_url = self._validate_network_name_to_value(network_name)
        ocean = Ocean(keeper_url=node_url)
        account = OceanAccount(ocean, address)
        self._add_output(f'{address}  ocean tokens: {account.ocean_balance}')
        self._add_output(f'{address} ether: {account.ether_balance}')

    def document_send(self):
        return [
            {
                'description': 'Transfer Ocean tokens to another account',
                'params': [
                    'send tokens <from_address> <password> <network_name or url> <to_address> <amount>',
                ],
            },
            {
                'description': 'Transfer Ocean ether to another account',
                'params': [
                    'send ether <from_address> <password> <network_name or url> <to_address> <amount>',
                ],
            }
        ]
    def command_send(self):
        sub_command = self._validate_sub_command(1, ['ether', 'tokens'])

        from_address = self._validate_address(2, field_name='from_address')
        password = self._validate_password(3)
        network_name = self._validate_network_name_url(4)
        node_url = self._validate_network_name_to_value(network_name)
        to_address = self._validate_address(5, field_name='to_address')
        amount = self._validate_amount(6)

        if sub_command == 'tokens':
            ocean = Ocean(keeper_url=node_url)
            account = OceanAccount(ocean, from_address)
            account.unlock(password)
            account.transfer_token(to_address, amount)
        elif sub_command == 'ether':
            self._wallet.send_ether(from_address, password, to_address, amount, node_url)
#            ocean = Ocean(keeper_url=node_url)
#            account = OceanAccount(ocean, from_address)
#            account.unlock(password)
#            account.transfer_ether(to_address, amount)

    def command_test(self):
        print(self._commands)

    def process(self, commands):
        self._commands = commands
        method_name = f'command_{commands[0]}'
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method()
        else:
            raise CommandProcessError(f'Invalid comamnd "{commands[0]}"')

    def list_commands(self):
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

    def _validate_password(self, index,):
        password = None
        if index < len(self._commands):
            password = self._commands[index]
        if not isinstance(password, str):
            raise CommandProcessError(f'Please provide a password')
        return password

    def _validate_network_name_url(self, index, default=None):
        network_name = default
        if index < len(self._commands):
            network_name = self._commands[index]
        else:
            raise CommandProcessError(f'Please provide a network name')
        return network_name

    def _validate_address(self, index, field_name=None):
        if field_name is None:
            field_name = 'address'
        if index < len(self._commands):
            address = self._commands[index]
            if Web3.isAddress(address):
                return address
            else:
                raise CommandProcessError(f'"{address}" is not a vaild account {field_name}')
        else:
            raise CommandProcessError(f'Please provide an address name')

    def _validate_json_text(self, index):
        if index < len(self._commands):
            json_text = self._commands[index]
            if os.path.exists(json_text):
                with open(json_text, 'r') as fp:
                    json_text = fp.read()
            try:
                data = json.loads(json_text)
            except json.decoder.JSONDecodeError:
                raise CommandProcessError(f'Please provide valid json key file or text')

            return json_text
        else:
            raise CommandProcessError(f'Please provide json text or filename')

    def _validate_network_name_to_value(self, network_name, validate=True, name=None):
        value = None
        if name is None:
            name = 'url'
        if network_name.lower() in self.NETWORK_NAMES:
            value = self.NETWORK_NAMES[network_name.lower()][name]
        if re.match('^http', network_name) or re.match('^/w+\.', network_name):
            value = network_name
        if value is None and validate:
            raise CommandProcessError(f'Cannot resolve network name "{network_name}" to a value')
        return value

    def _validate_sub_command(self, index, command_list):
        command_list_text = ','.join(command_list)
        if index < len(self._commands):
            sub_command = self._commands[index]
            if sub_command in command_list:
                return sub_command
            raise CommandProcessError(f'Invalid command "{sub_command}", one of the following commands "{command_list_text}"')
        else:
            raise CommandProcessError(f'Please provide one of the following commands "{command_list_text}"')

    def _validate_amount(self, index, default_value=None):
        amount = default_value
        if index < len(self._commands):
            amount = int(self._commands[index])

        if amount is None:
            raise CommandProcessError(f'Please provide an  "{command_list_text}"')
        return amount

    def _expand_document_item(self, value):
        items = []
        items.append(f'\n{value["description"]}')
        for param in value['params']:
            items.append(f'    {param}')
        return items

    def _add_output(self, text):
        if isinstance(text, str):
            self._output.append(text)
        else:
            for value in text:
                self._output.append(value)

    @property
    def output(self):
        return self._output
