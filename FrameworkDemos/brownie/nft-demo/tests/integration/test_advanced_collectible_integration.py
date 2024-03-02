import pytest
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time

# run on rinkeby
def test_can_create_simple_collectible_on_rinkeby():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")

    advanced_collectible, creation_txn = deploy_and_create()
    time.sleep(60)
    assert advanced_collectible.tokenCounter() == 1