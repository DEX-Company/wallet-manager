![](https://github.com/DEX-Company/wallet-manage/workflows/testing/badge.svg)

# Wallet Manager

**Provide account and wallet management on the Ocean Network**

There are two types of account/key storage: local or host

*Local key* is saved as a JSON file and all transactions need to be signed by the app.

*Host key* is saved on the Parity node, and all transactions can be signed on the Parity node via the ethereum xmlprc calls.


## Possible Commands to implement

*  Create account local and host
```
    wallet_manager.py add <password> [local]
    wallet_manager.py add <password> <network_name or url>
```

*  Delete account on local and host
```
    wallet_manager.py delete <address> <password> [local]
    wallet_manager.py delete <address> <password> <network_name or url>
```

*  List accounts on local and host
```
    wallet_manager.py list [local]
    wallet_manager.py list <network_name or url>
```

*  Copy local account to host
```
    wallet_manager.py copy local <local_address> <password> <network_name or url>
```

*  Copy host account to local
```
    wallet_manager.py copy <network_name or url> <host_address> <password> local
```

*  Export local and host account to JSON ( default export mode )
```
    wallet_manager.py export <address> <password> [local]
    wallet_manager.py export <address> <password> <network_name or url>
```

*  Export local and host account to private key
```
    wallet_manager.py export <address> <password> [local] --as_key
    wallet_manager.py export <address> <password> <network_name or url> --as_key
```

*  Import local and host account from JSON key file ( default import mode )
```
    wallet_manager.py import <json_file or string> <password> [local]
    wallet_manager.py import <json_file or string> <password> <network_name or url>
```

*  Import local and host account from private key
```
    wallet_manager.py import <private_key> <password> [local] --as_key
    wallet_manager.py import <private_key> <password> <network_name or url> --as_key
```

*  Change account password on local and host
```
    wallet_manager.py password <address> <old_password> <new_password> [local]
    wallet_manager.py password <address> <old_password> <new_password> <network_name or url>
```

*  Request ether from faucet
```
    wallet_manager.py get ether <address> [local]
    wallet_manager.py get ether <address> <network_name or url>
```

*  Request Ocean tokens on test networks
```
    wallet_manager.py get tokens <address> <password> <amount> [local]
    wallet_manager.py get tokens <address> <password> <amount> <network_name or url>
```

*  Transfer Ocean tokens to another account
```
    wallet_manager.py send tokens <from_address> <password> [local] <to_address>
    wallet_manager.py send tokens <from_address> <password> <network_name or url> <to_address>
```

*  Transfer Ocean ether to another account
```
    wallet_manager.py send ether <from_address> <password> <to_address>
    wallet_manager.py send ether <from_address> <password> <network_name or url> <to_address>
```


### Command Parameters

Any field name within a `<field_name>` must be entered.
Any field name within a `[field_name]` can be an option.

*  `<address>` is any valid ethereum address, starting with optional _0x_.
*  `<password>` is the acount password or key phrase.
*  `<local_address>` is the account address saved in the local wallet.
*  `<host_address>` is the account saved on the host Parity node.
*  `<network_name or url>` can be a predifined url nodes using a network name such as:

    *  `spree`   : http://localhost:8545
    *  `nile`    : https://nile.dev-ocean.com
    *  `pacific` : https://pacific.oceanprotocol.com
    *  `host`    : http://localhost:8545
    *  `local`   : Use the local address and private key

or the actual URL of the Parity Node to access, such as `http://192.168.1.1:8545`.
or a the network name `local` which directs the app to use the local address on disk.

*  `<amount>` amount of ocean tokens.
*  `[local]` optional `local` keyword that can be omitted to imply the local address/key.
