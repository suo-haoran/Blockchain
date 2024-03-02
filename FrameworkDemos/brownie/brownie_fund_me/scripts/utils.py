from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

# copy a chain and put it in local environment. We have control of the chain.
# Changes made to the forked chain will not have any effect on the original chains.
# Go to alchemy
# To fork chain: brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=<mainnetUrl> accounts=10 mnemonic=brownie port=8545
FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local-test']

DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    active_network = network.show_active()
    if active_network in LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS or active_network in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        print(f'The active network is {network.show_active()}')
        print('Deploying mocks')
        MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {'from': get_account()})
        print("Mocks Deployed")