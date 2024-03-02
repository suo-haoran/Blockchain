from scripts.utils import encode_function_data, get_account, upgrade
from brownie import Contract, network, Box, ProxyAdmin, TransparentUpgradableProxy, BoxV2

def main():
    account = get_account()
    print(f"Deploying to network {network.show_active()}")
    box = Box.deploy({"from": account})
   
    proxy_admin = ProxyAdmin.deploy({"from": account})
    initializer = box.store, 1

    # Read more on https://github.com/PatrickAlphaC/upgrades-mix
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradableProxy.deploy(box.address, proxy_admin.address, box_encoded_initializer_function, {"from": account, "gas_limit": 1000000})
    print(f"Proxy deployed to {proxy}, you can upgrade to v2!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    
    box_v2 = BoxV2.deploy({"from": account})
    upgrade_transaction = upgrade(account, proxy, box_v2.address, proxy_admin)
    upgrade_transaction.wait(1)
    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve()) # Output is 2 because previous value is stored and then incremented.