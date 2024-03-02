import os
from solcx import compile_standard
import json
from web3 import Web3
from dotenv import load_dotenv

# load dot env file.
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]


# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# deploy to fake chain ganache
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/bb9ebcfd88f64744981614721e9da2a7"))
# google for chain_id
chain_id = 4
my_addr = "0xf5F647383F753272F11461DF17B2e5ACA14824C6"
# append 0x at the front of private key. 
# Never hardcode private keys.
# export PRIVATE_KEY=private_key
private_key = os.getenv('PRIVATE_KEY')
print(private_key)
# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
# this nonce is different from the other nonce in cryptography.
nonce = w3.eth.getTransactionCount(my_addr)
print(nonce)

# Steps:
# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction({
    # need to add gas price.
    "gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_addr, "nonce": nonce
})
# 2. Sign a transaction 
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# 3. Send a transaction
print("Deploying Contract...")
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for block confirmation
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Deployed!")

# Working with the contract, we need:
# Contract Address
# Contract ABI
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)
# call -> simulate making the call and getting a return value (use it on view functions)
# transact -> actually make a state change (use it for state changes)
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction({
    "gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_addr, "nonce": nonce + 1
})
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("Updated!")
print(simple_storage.functions.retrieve().call())