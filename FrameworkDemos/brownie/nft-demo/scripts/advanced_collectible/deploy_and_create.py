from scripts.utils import fund_with_link, get_account, OPENSEA_URL,get_contract
from brownie import AdvancedCollectible, network, config


def deploy_and_create():
    account = get_account()
    active_network = network.show_active()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract('vrf_coordinator'),
        get_contract('link_token'),
        config["networks"][active_network]['keyhash'],
        config["networks"][active_network]['fee'],
        {"from": account}
    )
    # Need to fund contract with link to pay for the random ness functions.
    fund_with_link(advanced_collectible.address)
    creating_txn = advanced_collectible.createCollectible({"from": account})
    creating_txn.wait(1)
    print("New token has been created!")
    return advanced_collectible, creating_txn


def main():
    deploy_and_create()
