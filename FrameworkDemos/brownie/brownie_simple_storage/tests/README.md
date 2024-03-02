# Testing
We should test contracts in brownie. More options to automate.

Make sure to prefix your file with `test_`, it's required by pytest. E.g. `test_simple_storage.py`

Do follow the **Arrange, Act, Assert** principle in testing.

Run all tests with `brownie test`.

Test one function `brownie test -k functionName`.

When a test fails, it puts you in a pdb(python) shell, you can check variable states in there. Type `quit()` to exit the shell.

See pytest for more info.


### Where should I run my tests?
1. Brownie Ganache Chain with Mocks: Always
2. Testnet: Always (only for integration testing)
3. Brownie Mainnet Fork: Optional