import pytest
from scripts.utils import encode_function_data, get_account, upgrade
from brownie import (
    Box,
    Contract,
    ProxyAdmin,
    TransparentUpgradableProxy,
    BoxV2,
    exceptions,
)


def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    box_v2 = BoxV2.deploy({"from": account})

    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    upgrade_transaction = upgrade(account, proxy, box_v2.address, proxy_admin)
    upgrade_transaction.wait(1)
    assert proxy_box.retrieve() == 0
    print("Proxy has been upgraded!")
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
