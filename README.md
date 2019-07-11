# Wallet Manager
Provide account and wallet management on the Ocean Network

There are two types of account/key storage: local or host

*Local key* is saved as a JSON file and all transactions need to be signed by the app.

*Host key* is saved on the Parity node, and all transactions can be signed on the Parity node via the ethereum xmlprc calls. 

## Possible Commands to implement

*  Create account local and host
*  Delete account on local and host
*  Copy local account to host
*  Copy host account to local
*  Export local and host account to private key
*  Export local and host account to JSON
*  Import local and host account from private key
*  Import local and host account from JSON key file
*  Change account password on local and host
*  Request ether from faucet
*  Request Ocean tokens on test networks
*  Transfer Ocean tokens and ether between accounts
