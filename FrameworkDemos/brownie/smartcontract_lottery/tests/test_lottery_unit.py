import time
from brownie import Lottery, accounts, config, network, exceptions
import pytest
from web3 import Web3
from scripts.utils import (
    get_account,
    fund_contract_with_link,
    get_contract,
)
from scripts.deploy_lottery import deploy_lottery


def test_get_entrance_fee(check_local_blockchain_envs, lottery_contract):
    # Arrange (by fixtures)

    # Act
    # 2,000 eth / usd
    # usdEntryFee is 50
    # 2000/1 == 50/x == 0.025
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery_contract.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started(check_local_blockchain_envs, lottery_contract):
    # Arrange (by fixtures)

    # Act / Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery_contract.enter(
            {"from": get_account(), "value": lottery_contract.getEntranceFee()}
        )


def test_can_start_and_enter_lottery(check_local_blockchain_envs, lottery_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottery_contract.startLottery({"from": account})
    # Act
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    # Assert
    assert lottery_contract.players(0) == account


def test_can_end_lottery(check_local_blockchain_envs, lottery_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    fund_contract_with_link(lottery_contract)
    lottery_contract.endLottery({"from": account})
    assert lottery_contract.lotteryState() == 2


def test_can_pick_winner_correctly(check_local_blockchain_envs, lottery_contract):
    # Arrange (by fixtures)

    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enter(
        {"from": account, "value": lottery_contract.getEntranceFee()}
    )
    lottery_contract.enter(
        {"from": get_account(index=1), "value": lottery_contract.getEntranceFee()}
    )
    lottery_contract.enter(
        {"from": get_account(index=2), "value": lottery_contract.getEntranceFee()}
    )
    fund_contract_with_link(lottery_contract)
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery_contract.balance()
    transaction = lottery_contract.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery_contract.address, {"from": account}
    )
    # 777 % 3 = 0
    assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery