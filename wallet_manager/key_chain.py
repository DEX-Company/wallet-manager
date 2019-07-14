import os.path
import json


class KeyChain():
    def __init__(self, filename):
        self._filename = filename
        self._key_list = {}
        self.load()

    def load(self):
        if os.path.exists(self._filename):
            with open(self._filename, 'r') as fp:
                self._key_list = json.load(fp)

    def save(self):
        with open(self._filename, 'w') as fp:
            json.dump(self._key_list, fp)

    def get_key(self, address):
        return self._key_list.get(address, None)

    def set_key(self, address, key_item):
        self._key_list[address] = key_item

    def delete_key(self, address):
        del self._key_list[address]

    @property
    def address_list(self):
        return list(self._key_list.keys())
