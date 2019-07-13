#!/usr/bin/env python3

import argparse

from wallet_manager.wallet_manager import WalletManager

DEFAULT_KEY_CHAIN_FILENAME = 'key_chain.json'

BIN_NAME = 'wallet_manager.py'

COMMAND_LIST = {
    'new': {
        'description': 'Create account local and host',
        'params' :[
            'new <password> [local]',
            'new <password> <network_name or url>',
        ],
    },
    'delete': {
        'description': 'Delete account on local and host',
        'params': [
            'delete <address> <password> [local]',
            'delete <address> <password> <network_name or url>',
        ],
    },
    'list': {
        'description': 'List accounts on local and host',
        'params': [
            'list [local]',
            'list <network_name or url>',
        ],
    },
    'copy_local': {
        'description': 'Copy local account to host',
        'params': [
            'local <local_address> <password> <network_name or url>',
        ],
    },
    'copy_host': {
        'description': 'Copy host account to local',
        'params': [
            'copy <network_name or url> <host_address> <password> [local]',
        ],
    },
    'export': {
        'description': 'Export local and host account to JSON or private key',
        'params': [
            '[--as_json] [--as_key] export <address> <password> [local]',
            '[--as_json] [--as_key] export <address> <password> <network_name or url>',
        ],
    },
    'import': {
        'description': 'Import local and host account from JSON key file, or private key',
        'params': [
            '[--as_json] [--as_key] import <json_file or string> <password> [local]',
            '[--as_json] [--as_key] import <json_file or string> <password> <network_name or url>',
        ],
    },
    'password': {
        'description': 'Change account password on local and host',
        'params': [
            'password <address> <old_password> <new_password> [local]',
            'password <address> <old_password> <new_password> <network_name or url>',
        ],
    },
    'get_ether': {
        'description': 'Request ether from faucet',
        'params': [
            'get ether <address> [local]',
            'get ether <address> <network_name or url>',
        ],
    },
    'get_tokens': {
        'description': 'Request Ocean tokens on test networks',
        'params': [
            'get tokens <address> <password> [local] [amount]',
            'get tokens <address> <password> <network_name or url> [amount]',
        ],
    },
    'send_tokens': {
        'description': 'Transfer Ocean tokens to another account',
        'params': [
            'send tokens <from_address> <password> [local] <to_address>',
            'send tokens <from_address> <password> <network_name or url> <to_address>',
        ],
    },
    'send_ether': {
        'description': 'Transfer Ocean ether to another account',
        'params': [
            'send ether <from_address> <password> <to_address>',
            'send ether <from_address> <password> <network_name or url> <to_address>',
        ],
    }
}

def show_command_help():
    print('\nThe following commands can be used:\n')
    for name, item in COMMAND_LIST.items():
        print(f'\n{item["description"]}')
        for param in item['params']:
            print(f'    {BIN_NAME} {param}')

    print('\nPossible network names:')
    print('local               : Local key storage')
    for name, url in WalletManager.NETWORK_NAMES.items():
        print(f'{name:20}: {url}')

def main():
    parser = argparse.ArgumentParser('Ocean Drop')
    command_list_text = '","'.join(COMMAND_LIST)
    parser.add_argument(
        'commands',
        nargs = '*',
        type = str,
        help = f'The type of commands: "{command_list_text}"',
    )

    parser.add_argument(
        '-d', '--debug',
        action = 'store_true',
        help = 'show debug log',
    )

    parser.add_argument(
        '--help-commands',
        action = 'store_true',
        help = 'show the help for the possible commands'
    )

    parser.add_argument(
        '-k', '--key-chain',
        help = f'Key chain file to save and read local keys. Default {DEFAULT_KEY_CHAIN_FILENAME}',
        default = DEFAULT_KEY_CHAIN_FILENAME
    )

    args = parser.parse_args()

    if args.help_commands:
        show_command_help()
        return

    if len(args.commands) == 0:
        show_command_help()
        return

    manager = WalletManager(key_chain_filename=args.key_chain)
    manager.process(args.commands)
    if manager.isError:
        print(manager.errorMessage)
        show_command_help()

if __name__ == '__main__':
    main()
