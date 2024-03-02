from scripts.utils import get_account
from brownie import interface,config,network

def main():
    get_weth()


def get_weth():
    """
    Mint weth by depositing ETH.
    """
    account = get_account()
    weth = interface.IWeth(config['networks'][network.show_active()]['weth_token'])
    txn = weth.deposit({"from": account, "value": 0.1 * 10**18})
    txn.wait(1)
    print(f"Received 0.1 WETH")