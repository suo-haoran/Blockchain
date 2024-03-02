from ctypes import addressof
from lib2to3.pytree import convert
from logging import error
from brownie import network, config, interface
from scripts.utils import LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.get_weth import get_weth
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    active_network = network.show_active()
    print(active_network)
    account = get_account()
    erc20_address = config["networks"][active_network]["weth_token"]
    if active_network in LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS:
        get_weth()
    lending_pool = get_lending_pool()

    approve_erc20(amount, lending_pool.address, erc20_address, account)
    print("Depositing...")
    txn = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    txn.wait(1)
    print("Deposited!")
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("Let's borrow some DAI!")
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][active_network]["dai_eth_price_feed"]
    )
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    try:
        dai_address = config["networks"][active_network]["dai_token"]
        borrow_txn = lending_pool.borrow(
            dai_address,
            Web3.toWei(amount_dai_to_borrow, "ether"),
            1,
            0,
            account.address,
            {"from": account},
        )
        borrow_txn.wait(1)
        print("borrowed some dai!")
    except Exception as e:
        if active_network == "kovan":
            print(
                "Dai address might be changed, check out https://docs.aave.com/developers/v/2.0/deployed-contracts/deployed-contracts, \nselect kovan and scroll to the bottom for list of updated addresses."
            )
        else:
            raise e
    get_borrowable_data(lending_pool, account)
    repay_all(amount, lending_pool, account)
    print("You just deposited, borrowed and repayed with aave, brownie and chainlink")

def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):
    """
    Approve sending out ERC20 tokens
    """
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    txn = erc20.approve(spender, amount, {"from": account})
    txn.wait(1)
    print("Approved!")
    return txn


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"DAI/ETH price: {converted_latest_price}")
    return float(converted_latest_price)


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_txn = lending_pool.repay(config["networks"][network.show_active()]["dai_token"],amount,1,account.address, {'from': account})
    repay_txn.wait(1)
    print("Repaid!")

