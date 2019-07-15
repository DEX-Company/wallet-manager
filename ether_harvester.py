#!/usr/bin/env python3

"""
    ether harvester

"""

import time

from wallet_manager.wallet_manager import WalletManager

PASSWORD = 'bill_test_12345'
NODE_URL='http://localhost:8545'
# FAUCET_URL = 'https://faucet.nile.dev-ocean.com/faucet'
FAUCET_URL = 'https://faucet.oceanprotocol.com/faucet'
STORAGE_ADDRESS = '0x02354A1F160A3fd7ac8b02ee91F04104440B28E7'

def main():

    wallet = WalletManager()
    while True:
        address = wallet.new_account(PASSWORD, NODE_URL )
        print(f' new address {address}')
        if wallet.get_ether(address, FAUCET_URL):
            balance = 0
            while balance == 0:
                balance = wallet.balance_ether(address, NODE_URL)
            print('sending ether')
            print(wallet.send_ether(address, PASSWORD, STORAGE_ADDRESS, 2.999999, NODE_URL, 480))

if __name__ == '__main__':
    main()
