# Wallet Manager
Provide account and wallet management on the Ocean Network

There are two types of account/key storage: local or host

*Local key* is saved as a JSON file and all transactions need to be signed by the app.

*Host key* is saved on the Parity node, and all transactions can be signed on the Parity node via the ethereum xmlprc calls. 

## Possible Commands to implement

*  Create account local and host
        add <password>
        add <network_name or url> <password>
        
*  Delete account on local and host
        delete <address> <password>
        delete <network_name or url> <address> <password>
        
*  Copy local account to host
        copy <local_address> <password> <network_name or url>
        
*  Copy host account to local
        copy <network_name or url> <host_address> <password>

*  Export local and host account to private key
        export <address> <password>  --as_key
        export <network_name or url> <address> <password> --as_key

*  Export local and host account to JSON
        export <address> <password>  --as_json
        export <network_name or url> <address> <password> --as_json

*  Import local and host account from private key
        import <private_key> <password>
        import <private_key> <password> <network_name or url>

*  Import local and host account from JSON key file
        import <json_file> <password>
        import <json_file> <password> <network_name or url>

*  Change account password on local and host
        set_password <address> <old_password> <new_password>
        set_password <network_name or url> <address> <old_password> <new_password>

*  Request ether from faucet
        request_ether <address>
        request_ether <network_name or url> <address>
        
*  Request Ocean tokens on test networks
        request_tokens <address> <password> <amount>
        request_tokens <network_name or url> <address> <password> <amount>
        
*  Transfer Ocean tokens to another account
        send_tokens <from_address> <password> <to_address>
        send_tokens <network_name or url> <from_address> <password> <to_address>

*  Transfer Ocean ether to another account
        send_ether <from_address> <password> <to_address>
        send_ether <network_name or url> <from_address> <password> <to_address>


