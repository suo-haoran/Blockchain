from brownie import (
    Contract,
    network,
    accounts,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    interface
)

# copy a chain and put it in local environment. We have control of the chain.
# Changes made to the forked chain will not have any effect on the original chains.
# Go to alchemy
# To fork chain: brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=<mainnetUrl> accounts=10 mnemonic=brownie port=8545
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local-test"]

DECIMALS = 8
STARTING_PRICE = 200000000000




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


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(name: str):
    """
    This function will grab the contract addresses from the brownie config if defined,
    otherwise, it will dpeloy a mock version of that contract and return
    that mock contract

    Args:
        contract_name (string)
    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed version of
        this contract
    """
    active_network = network.show_active()
    contract_type = contract_to_mock[name]
    if active_network in LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][active_network][name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")


def fund_contract_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    txn = link_token.transfer(contract_address, amount, {'from': account})
    # Brownie can work with interface, know which function to call
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # txn = link_token_contract.transfer(contract_address, amount, {'from': account})
    txn.wait(1)
    print("Funded contract!")
    return txn
