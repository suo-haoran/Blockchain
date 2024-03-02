`brownie run scripts/<scriptname>` in terminal to run scripts.

`brownie run scripts/<scriptname> --network <networkName>` to run scripts on a network

Brownie will launch a ganache chain when running scripts.

If you want to work with testnet account, type in terminal `brownie accounts new <accountName>`

If you want to delete an account in brownie, type in
`brownie accounts delete <accountName>`

List all accounts: `brownie accounts list`

NOTE: On linux, export `ganache-cli` path by adding in `.bashrc`.
```bash
export PATH="$PATH:~/.yarn/bin"
```
In this case, I've installed ganache-cli in yarn.

**DON'T PUT LIVE WALLET PRIVATE KEYS IN .env FILES! USE BROWNIE! IT'S SAFER**