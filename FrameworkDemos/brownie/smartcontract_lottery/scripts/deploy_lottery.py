from scripts.utils import fund_contract_with_link, get_account, get_contract
from brownie import Lottery, config, network
import time

def deploy_lottery():
    active_network = network.show_active()
    account = get_account()
    print(active_network)
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][active_network]["fee"],
        config["networks"][active_network]["keyhash"],
        {"from": account},
        publish_source=config["networks"][active_network].get(
            "verify", False
        ),  # Default false unless found verify key
    )
    print("deployed lottery")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_txn = lottery.startLottery({"from": account})
    starting_txn.wait(1)
    print("The lottery is started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10000000
    txn = lottery.enter({"from": account, "value": value})
    txn.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund contract with LINK token.
    txn = fund_contract_with_link(lottery.address)
    txn.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()