# Wallet Manager
Provide account and wallet management on the Ocean Network

There are two types of account/key storage: local or host

*Local key* is saved as a JSON file and all transactions need to be signed by the app.

*Host key* is saved on the Parity node, and all transactions can be signed on the Parity node via the ethereum xmlprc calls.

## Possible Commands to implement

*  Create account local and host
```
    _cmd_ add <password>
    _cmd_ add <network_name or url> <password>
```

*  Delete account on local and host
```
    _cmd_ delete <address> <password>
    _cmd_ delete <network_name or url> <address> <password>
```

*  Copy local account to host
```
    _cmd_ copy <local_address> <password> <network_name or url>
```

*  Copy host account to local
```
    _cmd_ copy <network_name or url> <host_address> <password>
```

*  Export local and host account to private key
```
    _cmd_ export <address> <password>  --as_key
    _cmd_ export <network_name or url> <address> <password> --as_key
```

*  Export local and host account to JSON
```
    _cmd_ export <address> <password>  --as_json
    _cmd_ export <network_name or url> <address> <password> --as_json
```

*  Import local and host account from private key
```
    _cmd_ import <private_key> <password>
    _cmd_ import <private_key> <password> <network_name or url>
```

*  Import local and host account from JSON key file
```
    _cmd_ import <json_file> <password>
    _cmd_ import <json_file> <password> <network_name or url>
```

*  Change account password on local and host
```
    _cmd_ password <address> <old_password> <new_password>
    _cmd_ password <network_name or url> <address> <old_password> <new_password>
```

*  Request ether from faucet
```
    _cmd_ request_ether <address>
    _cmd_ request_ether <network_name or url> <address>
```

*  Request Ocean tokens on test networks
```
    _cmd_ request_tokens <address> <password> <amount>
    _cmd_ request_tokens <network_name or url> <address> <password> <amount>
```

*  Transfer Ocean tokens to another account
```
    _cmd_ send_tokens <from_address> <password> <to_address>
    _cmd_ send_tokens <network_name or url> <from_address> <password> <to_address>
```

*  Transfer Ocean ether to another account
```
    _cmd_ send_ether <from_address> <password> <to_address>
    _cmd_ send_ether <network_name or url> <from_address> <password> <to_address>
```


