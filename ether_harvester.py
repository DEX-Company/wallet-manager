#!/usr/bin/env python3

"""
    ether harvester

"""

import time

from wallet_manager.wallet_manager import WalletManager

PASSWORD = 'bill_test_12345'
NODE_URL='http://localhost:8545'
FAUCET_URL = 'https://faucet.nile.dev-ocean.com/faucet'
STORAGE_ADDRESS = '0x02354A1F160A3fd7ac8b02ee91F04104440B28E7'

address_list = []
def main():

    wallet = WalletManager()
    while True:
        address = wallet.new_account(PASSWORD, NODE_URL )
        print(f' new address {address}')
        address_list.append({'address': address, 'is_done': False})
        wallet.get_ether(address, FAUCET_URL)
        for item in address_list:
            if not item['is_done']:
                balance = wallet.balance_ether(item['address'], NODE_URL)
                if balance > 0:
                    print('sending ether')
                    print(wallet.send_ether(address, PASSWORD, STORAGE_ADDRESS, balance - 0.00001, NODE_URL, 480))
                    item['is_done'] = True
if __name__ == '__main__':
    main()
