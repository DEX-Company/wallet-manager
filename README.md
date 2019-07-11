# wallet-manager
Provide account and wallet management on the Ocean Network

There are two types of account/key storage: local or host

Local key is saved as a JSON file and all transactions need to be signed by the app.
Host key is saved on the Parity node, and all transactions can be signed on the node via the ethereum xmlprc calls. 

## Possible Commands to implement

*  Create account local
*  Create account host
*  Import local account to host
*  Export host account to local
*  Export local account to JSON
*  Export host account to JSON
*  Import local account from private key
*  Import host account from priavte key
*  Delete account on host
*  Delete account on local
*  Change account password on local and host
*  Request ether from faucet
*  Request Ocean tokens on test networks
