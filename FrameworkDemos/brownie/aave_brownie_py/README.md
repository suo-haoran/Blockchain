1. Swap eth into weth(wrapped ether)
2. Deposit some ETH into Aave
3. Borrow some asset with the ETH collateral
    1. (OPTIONAL) Sell that borrowed asset. (Short selling)
4. Repay everything back


Testing:

Integration test: Kovan
Unit test: Mainnet-fork

NOTE: If you have no oracles, it's better to test on mainnet-fork. If you have oracles, it's better to mock those contract and interactions on local net.