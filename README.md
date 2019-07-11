# Wallet Manager
Provide account and wallet management on the Ocean Network

There are two types of account/key storage: local or host

*Local key* is saved as a JSON file and all transactions need to be signed by the app.

*Host key* is saved on the Parity node, and all transactions can be signed on the Parity node via the ethereum xmlprc calls.

## Possible Commands to implement

*  Create account local and host
```
    wallet_manager.py add <password>
    wallet_manager.py add <network_name or url> <password>
```

*  Delete account on local and host
```
    wallet_manager.py delete <address> <password>
    wallet_manager.py delete <network_name or url> <address> <password>
```

*  Copy local account to host
```
    wallet_manager.py copy <local_address> <password> <network_name or url>
```

*  Copy host account to local
```
    wallet_manager.py copy <network_name or url> <host_address> <password>
```

*  Export local and host account to private key
```
    wallet_manager.py export <address> <password>  --as_key
    wallet_manager.py export <network_name or url> <address> <password> --as_key
```

*  Export local and host account to JSON
```
    wallet_manager.py export <address> <password>  --as_json
    wallet_manager.py export <network_name or url> <address> <password> --as_json
```

*  Import local and host account from private key
```
    wallet_manager.py import <private_key> <password>
    wallet_manager.py import <private_key> <password> <network_name or url>
```

*  Import local and host account from JSON key file
```
    wallet_manager.py import <json_file> <password>
    wallet_manager.py import <json_file> <password> <network_name or url>
```

*  Change account password on local and host
```
    wallet_manager.py password <address> <old_password> <new_password>
    wallet_manager.py password <network_name or url> <address> <old_password> <new_password>
```

*  Request ether from faucet
```
    wallet_manager.py request_ether <address>
    wallet_manager.py request_ether <network_name or url> <address>
```

*  Request Ocean tokens on test networks
```
    wallet_manager.py request_tokens <address> <password> <amount>
    wallet_manager.py request_tokens <network_name or url> <address> <password> <amount>
```

*  Transfer Ocean tokens to another account
```
    wallet_manager.py send_tokens <from_address> <password> <to_address>
    wallet_manager.py send_tokens <network_name or url> <from_address> <password> <to_address>
```

*  Transfer Ocean ether to another account
```
    wallet_manager.py send_ether <from_address> <password> <to_address>
    wallet_manager.py send_ether <network_name or url> <from_address> <password> <to_address>
```


