from brownie import (
    network,
    accounts,
    config,
)

# copy a chain and put it in local environment. We have control of the chain.
# Changes made to the forked chain will not have any effect on the original chains.
# Go to alchemy
# To fork chain: brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=<mainnetUrl> accounts=10 mnemonic=brownie port=8545
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local-test"]

def get_account(index=None, id=None):
    active_network = network.show_active()
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        active_network in LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS
        or active_network in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

