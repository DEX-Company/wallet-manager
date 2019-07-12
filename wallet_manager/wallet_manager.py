


class WalletManager():

    def __init__(self):
        self._errorMessage = None
        self._commands = None

    def document_new(sef):
        return {
            'description': 'Create account local and host',
            'params' :[
                'new <password> [local]',
                'new <password> <network_name or url>',
            ],
        }
    def command_new(self):
        password = self._validatePassword(1)
        network_name = self._validateNetworkName(2, 'local')
        print(password, network_name)

    def command_test(self):
        print(self._commands)


    def process(self, commands):
        self._commands = commands
        method_name = f'command_{commands[0]}'
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method()
        else:
            self._errorMessage = f'cannot find method "{method_name}"'

    @property
    def errorMessage(self):
        return self._errorMessage

    @property
    def isError(self):
        return not self._errorMessage is None

    def _validatePassword(self, index,):
        password = None
        if index < len(self._commands):
            password = self._commands[index]
        if not isinstance(password, str):
            self._errorMessage = 'please provide a password'
        return password

    def _validateNetworkName(self, index, default=None):
        network_name = default
        if index < len(self._commands):
            network_name = self._commands[index]
        if network_name:
            network_name = network_name.lower()
        return network_name
