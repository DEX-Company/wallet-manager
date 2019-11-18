import os.path
import json


class KeyChain():
    def __init__(self, filename):
        """

        Keychain to save local account encrypted private keys.

        :param str filename: Filename of the keychain file.

        """
        self._filename = filename
        self._key_list = {}
        self.load()

    def load(self):
        """

        Load the keychain into memory from the provided filename.

        """
        if os.path.exists(self._filename):
            with open(self._filename, 'r') as fp:
                self._key_list = json.load(fp)

    def save(self):
        """

        Save the keychain data to file, using the provided filename on class init.

        """
        with open(self._filename, 'w') as fp:
            json.dump(self._key_list, fp)

    def get_key(self, address):
        """
        Return a JSON account details from the account address.

        :param str address: Address of the account.

        :return: JSON object of the account.

        """
        return self._key_list.get(address, None)

    def set_key(self, address, key_item):
        """

        Set the account JSON object.

        :param str address: Address of the account to set.
        :param str key_item: JSON object to assign to this account.

        """
        self._key_list[address] = key_item

    def delete_key(self, address):
        """

        Delete an account based on it's address.

        :param str address: Address of the account to delete.

        """
        del self._key_list[address]

    def is_key(self, address):
        """

        Return True if the address is being held in this Keychain.

        :param str address: Address of the account to check.

        :return: bool True if the address is in this Keychain.

        """"
        return address in self._key_list

    @property
    def address_list(self):
        """

        Return a list of addresses held in this keychain.

        :return: List of addresses.
        :type: list
        
        """
        return list(self._key_list.keys())
