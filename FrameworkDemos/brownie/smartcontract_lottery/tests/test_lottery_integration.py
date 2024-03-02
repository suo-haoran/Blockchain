import pytest
from scripts.utils import (
    LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_contract_with_link,
)
import time
from brownie import network

# it wont run on local chains
def test_can_pick_winner(lottery_contract):
    if network.show_active() in LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    fund_contract_with_link(lottery_contract)
    lottery_contract.endLottery({"from": account})
    time.sleep(180)
    assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() == 0