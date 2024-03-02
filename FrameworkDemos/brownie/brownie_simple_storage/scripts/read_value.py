from brownie import SimpleStorage, accounts, config

def read_contract():
    # most recent deployment: -1
    simple_storage = SimpleStorage[-1]
    # ABI
    # Address
    print(simple_storage.retrieve())

def main():
    read_contract()