
import json
import requests
import logging

from web3 import (
    Web3,
    HTTPProvider,
    gas_strategies,
)

from eth_account import Account as EthAccount
from wallet_manager.key_chain import KeyChain
from wallet_manager import logger


def as_attrdict(val):
    return dict(val)

class WalletManager():
    def __init__(self, key_chain_filename=None):
        """
        Create the wallet manager class.

        :param str key_chain_filename: Optional key chain filename
            that can be used for local access.

        """

        if key_chain_filename:
            self._key_chain = KeyChain(key_chain_filename)


    def new_account(self, password, url=None):
        """

        Create a new account using the provided password, with a remote node or
        if no URL provided as a local public/private key

        :param str password: Password of the new account.
        :param str url: URL of the remote parity node to connect and register the new

        """

        address = None
        if url:
            web3 = Web3(HTTPProvider(url))
            address = web3.personal.newAccount(password)
            accounts = web3.personal.listAccounts
            if not address in accounts:
                raise NameError(f'Unable to create a new account')
        else:
            local_account = EthAccount.create(password)
            address = local_account.address
            key_value = EthAccount.encrypt(local_account.privateKey, password)
            self._key_chain.set_key(address, key_value)
            self._key_chain.save()
        return address


    def get_chain_status(self, url):
        """

        Get the current chain status.

        :param str url: URL of the node on the block chain.
        :return: The parity chain status.

        """
        web3 = Web3(HTTPProvider(url))
        return web3.manager.request_blocking('parity_chainStatus', [])

    def get_chain_name(self, url):
        """

        Get the parity block chain name.

        :param str url: URL of the parity block chain node.
        :return: The parity chain name.

        """
        web3 = Web3(HTTPProvider(url))
        return web3.manager.request_blocking('parity_chain', [])

    def delete_account(self, address, password, url=None):
        """

        Delete an account locally or on the parity node.

        :param str address: Address of the account to delete.
        :param str password: Password of the account to delete.
        :param str url: URL of the parity node to delete on.

        """
        if url:
            web3 = Web3(HTTPProvider(url))
            web3.manager.request_blocking('parity_killAccount', [address, password])
        else:
            self._key_chain.delete_key(address)
            self._key_chain.save()

    def list_accounts(self, url=None):
        """

        List the accounts on the node or locally saved in the key chain.

        :param str url: URL of the parity node to list the accounts, if this
            parameter is None then return the list of accounts in the key chain.

        :return: List of accounts
        :type: list

        """
        result = None
        if url:
            web3 = Web3(HTTPProvider(url))
            result = web3.eth.accounts
        else:
            result = self._key_chain.address_list
        return result

    def export_account_json(self, address, password, url=None):
        """
        Export the account details as a JSON record.

        :param str address: Address of the account to export.
        :param str password: Passmord of the account to export.
        :param str url: URL of the node to export from, else if None then export
            from the keychain.

        :return: JSON object containing information about the account, including
            the encrypted priwate key.

        """
        if url:
            web3 = Web3(HTTPProvider(url))
            raw_data = web3.manager.request_blocking('parity_exportAccount', [address, password])
            result = json.dumps(raw_data, default=as_attrdict)
        else:
            result = json.dumps(self._key_chain.get_key(address))
        return result

    def export_account_key(self, address, password, url=None):
        """
        Export the accounts private key. This is the best way to export
        keys, as this exposes the private key and it can be easilly stolen.

        :param str address: Address of the account to get the private key.
        :param str password: Account password.
        :param str url: URL of the parity node, or if None then use the key chain.

        :return: Private key of the account.

        """
        if url:
            web3 = Web3(HTTPProvider(url))
            raw_data = web3.manager.request_blocking('parity_exportAccount', [address, password])
            key_json = json.dumps(raw_data, default=as_attrdict)
        else:
            key_json = json.dumps(self._key_chain.get_key(address))
        return EthAccount.decrypt(key_json, password)

    def import_account_json(self, json_text, password, url=None):
        """

        Import an account into the partiy node or local keychaain.

        :param str json_text: JSON object of an account that has been exported.
        :param str password: Password of the account that you wish to import.
        :param str url: URL of the parity network you wish to import the account too.
            If the URL is None, then import to the local keychain.

        """
        if url:
            web3 = Web3(HTTPProvider(url))
            web3.manager.request_blocking('parity_newAccountFromWallet', [json_text, password])
        else:
            data = json.loads(json_text)
            address = Web3.toChecksumAddress(data["address"])
            self._key_chain.set_key(address, data)
            self._key_chain.save()

    def import_account_key(self, address, raw_key, password, url=None):
        """

        Import an account's private key. This is not a surggested solution, since passing an
        account's private key is a security risk.

        :param str address: Address of the account to import.
        :param str raw_key: The raw private key of the account to import.
        :param str password: The password to use for saving and importing the account.
        :param str url: URL of the parity node of if None then import the account in the local
            KeyChain.
        """
        if url:
            web3 = Web3(HTTPProvider(url))
            address = web3.manager.request_blocking('parity_newAccountFromSecret', [raw_key, password])
        else:
            self._key_chain.set_key(address, EthAccount.encrypt(raw_key, password))
            self._key_chain.save()
        return address

    def balance_ether(self, address, url):
        """

        Retun the ether balance for an account.

        :param str address: The address of the account.
        :param str url: URL of the parity node to find the balance.

        :return: The account balance.

        """
        web3 = Web3(HTTPProvider(url))
        return web3.fromWei(web3.eth.getBalance(address), 'ether')

    def send_ether(self, from_address, password, to_address, amount, url=None, timeout=120, is_local=False):
        """

        Send some between two valid accounts. Remember the `to_address`, must be a known address,
        if you send ether or Ocean tokens to a random or unkown address you cannot get
        it back again.

        :param str from_address: The address of the account to send ether from.
        :param str password: Password of the from_address account that is sending the ether.
        :param double amount: Amount to send in ether.
        :param str url: URL of the node to use for sending ether.
        :param int timeout: Timeout seconds to wait for transaction to complete ( defaults to 20 seconds).
        :param bool is_local: Sign the transaction locally.

        :return: Transaction receipt number.
        """
        web3 = Web3(HTTPProvider(url))

        if is_local:
            key_json = json.dumps(self._key_chain.get_key(from_address))
            raw_key = EthAccount.decrypt(key_json, password)
            gas_price = web3.manager.request_blocking('eth_gasPrice', [])
            transaction = {
                'from': from_address,
                'to': to_address,
                'value': Web3.toWei(amount, 'ether'),
                'gasPrice': gas_price,
                'gas': 30000,
                'nonce': 0,
            }
            signed = web3.eth.account.signTransaction(transaction, raw_key)
            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

        else:
            from_address = Web3.toChecksumAddress(from_address)
            to_address =  Web3.toChecksumAddress(to_address)
            web3.personal.unlockAccount(from_address, password)
            tx_hash = web3.personal.sendTransaction( {
                'from': from_address,
                'to': to_address,
                'value': Web3.toWei(amount, 'ether'),
            }, password)

        return web3.eth.waitForTransactionReceipt(tx_hash, timeout=timeout)

    def get_ether(self, address, url):
        """

        Get ether from a farucet.

        :param str address: Address for the account to get ether for.
        :param str url: URL of the faucet to obtain ether.

        """
        data  = {
            'address': address,
            'agent': 'server',
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json = data, headers=headers)
        logger.debug(f'response {response.text} {response.status_code}')
        if response.status_code != 200:
            raise ValueError(f'{response.status_code} {response.text}')
