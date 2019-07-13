import os.path
import json


class KeyChain():
    def __init__(self, filename):
        self._filename = filename
        self._key_list = {}

    def load(self):
        if os.path.exists(_filename):
            with open(_filename, 'r') as fp:
                self._key_list = json.load(fp)

    def save(self):
        with open(_filename, 'w') as fp:
            json.dump(self._key_list, fp)

    def get_key(self, address):
        return self._key_list.get(address, None)

    def set_key(self, address, key_item):
        self._key_list[address] = key_item

    def delete_key(slef, address):
        del self._key_list[address]
        
    def address_list(self):
        return self._key_list.names()
