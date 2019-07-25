#!/usr/bin/env python3

import argparse

from wallet_manager.command_processor import (
    CommandProcessor,
    CommandProcessError,
)

DEFAULT_KEY_CHAIN_FILENAME = 'key_chain.json'

APP_NAME = 'wallet_manager.py'

def show_command_help(processor):
    items = processor.command_document_list(APP_NAME)
    print('\nThe following commands can be used:\n')
#    for name, item in COMMAND_LIST.items():
#        print(f'\n{item["description"]}')
#        for param in item['params']:
#            print(f'    {BIN_NAME} {param}')
    print("\n".join(items))
    print('\nPossible network names can be one of the following:')
    print('local               : Local key storage')
    for name, item in CommandProcessor.NETWORK_NAMES.items():
        print(f'{name:20}: {item["url"]}')

def main():
    parser = argparse.ArgumentParser('Ocean Drop')
#    command_list_text = '","'.join(COMMAND_LIST)
    parser.add_argument(
        'commands',
        nargs = '*',
        type = str,
        help = f'The type of commands',
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
    processor = CommandProcessor(key_chain_filename=args.key_chain)

    if args.help_commands:
        show_command_help(processor)
        return

    if len(args.commands) == 0:
        show_command_help(processor)
        return


    try:
        processor.process(args.commands)
    except CommandProcessError as e:
        print(e)
        print('\n--help-commands to view the full command list')
    except Exception as e:
        print(e)
    else:
        print("\n".join(processor.output))

if __name__ == '__main__':
    main()
