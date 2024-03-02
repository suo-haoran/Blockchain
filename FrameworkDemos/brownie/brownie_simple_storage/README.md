To use brownie, check out https://github.com/eth-brownie/brownie

brownie-config.yaml tells brownie to load stuff when initializing. E.g. in the first line, load .env files when running scripts.

Run `brownie console` to interact with contracts. First deploy the contract and then interact with it. See `deploy.py -> deploy_simple_storage()`

Run `brownie networks list` to see a list of networks. Under the `development` section, the networks will be torn down after the scripts complete. 
However in other networks, the contract will persist on the networks like `Rinkeby, Kovan` etc.

Brownie will not remember which contracts are deployed to non-persistent networks, but we can tell it to remember each deployments by using `brownie networks add <chainName> <networkName> host=<host> chainid=<networkId>`. Then run `brownie run scripts/deploy.py --network <networkName>`. We can use this method to add new live networks as well.

You can check the deployed contracts in `/brownie_fund_me/build/contracts` (They are deployed to non-persistent networks, but are still remembered because we ran the networks add command, but you have to manually delete the build folder each time you close the local chain).

NOTE: `<chainName>` is the tree roots when you run `brownie networks list`, i.e. Ethereum, Ethereum Classic,.., XDai, Development. `<networkName>` is what you want to call the network.

