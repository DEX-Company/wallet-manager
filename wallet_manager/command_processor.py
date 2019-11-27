"""

Command processor, to control the command line arguments.

This module then call the walletmanager library.

"""

import inspect
import re
import os.path
import json
import secrets
import time
import logging
import sys

from web3 import (
    Web3,
    HTTPProvider
)
from eth_account import Account as EthAccount
from starfish import Ocean
from starfish.account import Account as OceanAccount

from wallet_manager.wallet_manager import WalletManager
from wallet_manager import logger

DEFAULT_REQUEST_TOKEN_AMOUNT = 10

class CommandProcessError(Exception):
    pass

class CommandProcessor():

    NETWORK_NAMES = {
        'local': {
            'description': 'No network, only access to local account setup',
        },
        'spree': {
            'description': 'Spree network running on a local barge',
            'url': 'http://localhost:8545',
            'faucet_account' : ['0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0', 'secret'],
        },
        'nile': {
            'description': 'Nile network access to remote network node',
            'url': 'https://nile.dev-ocean.com',
            'faucet_url' : 'https://faucet.nile.dev-ocean.com/faucet',
        },
        'pacific': {
            'description': 'Pacific network access to remote network node',
            'url': 'https://pacific.oceanprotocol.com',
            'faucet_url' : 'https://faucet.oceanprotocol.com/faucet',
        },
        'duero': {
            'description': 'Duero network access to remote network node',
            'url': 'https://duero.dev-ocean.com',
            'faucet_url' : 'https://faucet.duero.dev-ocean.com/faucet',
        },
        'host': {
            'description': 'Local node running on barge',
            'url': 'http://localhost:8545',
        }
    }

    def __init__(self, key_chain_filename=None):
        """

        Start up the command line library.

        :param str key_chain_filename: Optional key chain storage file that holds
            the local private keys.


        """
        self._commands = None
        self._output = []
        self._wallet = WalletManager(key_chain_filename=key_chain_filename)


    def document_new(sef):
        """

        Document a new account comand.

        """
        return {
            'description': 'Create account local and host',
            'params' :[
                'new <password> [local]',
                'new <password> <network_name or url>',
            ],
        }

    def command_new(self):
        """

        Create a new account.

        """
        address = ''
        password = self._validate_password(1)
        network_name = self._validate_network_name_url(2, 'local')
        if network_name == 'local':
            address = self._wallet.new_account(password)
        else:
            node_url = self._validate_network_name_to_value(network_name)
            address = self._wallet.new_account(password, node_url)
        self._add_output(address)

    def document_delete(self):
        return {
            'description': 'Delete account on local and host',
            'params': [
                'delete <address> <password> [local]',
                'delete <address> <password> <network_name or url>',
            ]
        }

    def command_delete(self):
        """

        Delete an account.

        """
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
        """

        Copy an account.

        TODO: No Implemented!

        """
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
        """

        List accounts.

        """
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
        """

        Export an account.

        """
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
        """

        Import an account

        """
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
        """

        Change an account password.

        """
        pass

    def document_get(self):
        return [
            {
                'description': 'Get ether from faucet. The amount is only used in local spree network',
                'params': [
                    'get ether <address> <network_name or faucet url> [amount]',
                ],
            },
            {
                'description': 'Get Ocean tokens on test networks, using a temporary transfer account to request tokens',
                'params': [
                    'get tokens <address> <network_name or url> [amount]',
                ],
            }
        ]
    def command_get(self):
        """

        Get ether or Ocean tokens for an account.

        """

        # test to see if this is a get token or get ether
        sub_command = self._validate_sub_command(1, ['ether', 'tokens'])
        # get the address to send the ether or tokens too
        address = self._validate_address(2)
        # get the network name / type
        network_name = self._validate_network_name_url(3)
        # get the optional amount to get.
        amount = self._validate_amount(4, DEFAULT_REQUEST_TOKEN_AMOUNT)

        # do the get Ocean tokens
        if sub_command == 'tokens':

            # first create a new account to request tokesn into
            node_url = self._validate_network_name_to_value(network_name)
            password = secrets.token_hex(32)
            request_address = self._wallet.new_account(password, node_url)
            node_status = self._wallet.get_chain_status(node_url)

            if node_status and not node_status['blockGap'] is None:
                self._add_output(f'Please wait: The local node is not yet in sync')
                return

            # after creating a temp account, no request tokens for this account.
            logger.info(f'created temp account {request_address}')
            ocean = Ocean(keeper_url=node_url)
            account = OceanAccount(ocean, request_address, password)
            chain_name = self._wallet.get_chain_name(node_url)
            logger.debug(f'chain name is {chain_name}')
            faucet_url = self._validate_network_name_to_value(chain_name, False, 'faucet_url')
            logger.debug(f'requesting ether from faucet at {faucet_url}')
            self._wallet.get_ether(request_address, faucet_url)

            # we need to request some ether for this temp account.
            logger.debug('wating for ether to be available in register account')
            while True:
                account = OceanAccount(ocean, request_address, password)
                if account.ether_balance > 0:
                    break
                time.sleep(1)
            logger.debug(f'{request_address} ether tokens: {account.ether_balance}')

            logger.debug('requesting ocean tokens')
            account.unlock(password)
            account.request_tokens(amount)

            # we need to wait for the transaction to complete to send the Ocean tokens.
            logger.debug('waiting for ocean tokens to be available in request account')
            while True:
                account = OceanAccount(ocean, request_address, password)
                if account.ocean_balance > 0:
                    break
                time.sleep(1)

            logger.debug(f'{request_address} ocean tokens: {account.ocean_balance}')
            logger.debug(f'{request_address} ether: {account.ether_balance}')

            node_status = self._wallet.get_chain_status(node_url)
            if node_status and not node_status['blockGap'] is None:
                self._add_output(f'Please wait: The local node is not yet in sync')
                return

            # now transfer from a new temp account to the given account by this parameter
            logger.debug(f'transfer {amount} from {request_address} to {address}')
            time.sleep(2)
            account.unlock(password)
            account.transfer_token(address, amount)
            ether_amount = 0
            if account.ether_balance > 0:
                ether_amount = float(account.ether_balance) - 0.0000000001
                account.transfer_ether(address, ether_amount)

            # delete the request account
            self._wallet.delete_account(request_address, password, node_url)
            self._add_output(f'sent {amount} ocean tokens and {ether_amount:.4f} ether to account {address}')

        elif sub_command == 'ether':

            # if getting ether then request from a faucet or a dev faucet account.
            node_url = self._validate_network_name_to_value(network_name)
            chain_name = self._wallet.get_chain_name(node_url)
            logger.debug(f'chain name is {chain_name}')
            faucet_url = self._validate_network_name_to_value(chain_name, False, 'faucet_url')
            if faucet_url:
                self._wallet.get_ether(address, faucet_url)
                ocean = Ocean(keeper_url=node_url)
                account = OceanAccount(ocean, address)
                self._add_output(f'{address}  ether : {account.ether_balance}')
                return
            faucet_account = self._validate_network_name_to_value(network_name, False, 'faucet_account')
            if faucet_account:
                # if list then it's a address/password of an account that has ether
                self._wallet.send_ether(faucet_account[0], faucet_account[1], address, amount, node_url)
                self._add_output(f'{address}  ether : {account.ether_balance}')
                return
            raise CommandProcessError(f'Warning: The network name {network_name} does not have a faucet')

    def document_request(self):
        return [
            {
                'description': 'Request Ocean tokens on a test network',
                'params': [
                    'request tokens <address> <password> <network_name or url> [amount]',
                ],
            }
        ]
    def command_request(self):
        """

        Request Ocean tokens for an account.

        """

        # do a basic starfish request tokens.
        sub_command = self._validate_sub_command(1, ['tokens'])
        address = self._validate_address(2)
        password = self._validate_password(3)
        network_name = self._validate_network_name_url(4)
        amount = self._validate_amount(5, DEFAULT_REQUEST_TOKEN_AMOUNT)
        node_url = self._validate_network_name_to_value(network_name)
        ocean = Ocean(keeper_url=node_url)
        account = OceanAccount(ocean, address)
        account.unlock(password)
        account.request_tokens(amount)
        self._add_output(f'{address}  ocean tokens: {account.ocean_balance}')


    def document_balance(self):
        return {
            'description': 'Show the ether and Ocean token balance',
            'params': [
                'balance <address> <network_name or faucet url>',
            ],
        }
    def command_balance(self):
        """

        Get an account balance.

        """
        address = self._validate_address(1)
        network_name = self._validate_network_name_url(2)
        node_url = self._validate_network_name_to_value(network_name)
        ocean = Ocean(keeper_url=node_url)
        account = OceanAccount(ocean, address)
        self._add_output(f'{address} ocean tokens: {account.ocean_balance}')
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
        """

        Send ether or Ocean tokens from one account to another account.

        """
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

    def command_test(self):
        """

        Test out the command line.

        """
        print(self._commands)

    def process(self, commands):
        """

        Process a command line.

        :param list commands: List of commands to process.

        """
        self._commands = commands
        method_name = f'command_{commands[0]}'
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method()
        else:
            raise CommandProcessError(f'Invalid comamnd "{commands[0]}"')

    def command_document_list(self, app_name):
        """

        Show the documentation for a command.

        """
        items = []
        for name in dir(self):
            if re.match('^document_', name):
                method = getattr(self, name)
                values = method()
                if isinstance(values, list):
                    for value in values:
                        items += self._expand_document_item(app_name, value)
                else:
                    items += self._expand_document_item(app_name, values)
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
            raise CommandProcessError(f'Please provide an amount')
        return amount

    def _expand_document_item(self, app_name, value):
        items = []
        items.append(f'\n{value["description"]}')
        for param in value['params']:
            items.append(f'    {app_name} {param}')
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
