from scripts.utils import get_account, LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

def test_can_fund_and_withdraw():
    if network.show_active() not in LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
   
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    fund_txn = fund_me.fund({'from': account, 'value': entrance_fee})
    fund_txn.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    withdraw_txn = fund_me.withdraw({'from': account})
    withdraw_txn.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # Expect pytest to raise virtual machine error
    with pytest.raises(exceptions.VirtualMachineError):
        # this should not be working because in our contract,
        # we appended the onlyOwner modifier. No one else should withdraw.
        fund_me.withdraw({'from': bad_actor})