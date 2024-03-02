Course video: https://www.youtube.com/watch?v=gyMwXuJrbJQ&t=7287s
Course github: https://github.com/smartcontractkit/full-blockchain-solidity-course-js

# Solidity Style
https://docs.soliditylang.org/en/latest/style-guide.html

# Yarn
Prefer `yarn` over `npm`.
Install `yarn` by `npm install -g yarn`.

- To install things from package.json, simply run `yarn`. (this is equivalent to `npm i` or `npm install`)
- To install new dependencies: `yarn add <pkgName>`(this is equivalent to `npm install <pkgName>`)
- To install new devDependencies: `yarn add <pkgName> --dev` (this is equivalent to `npm install --save-dev <pkgName>`)

# Setup a Hardhat Project
1. `mkdir project`
2. `cd project`
3. `yarn add hardhat`
4. `yarn hardhat`
    1. Choose `Create an advanced sample project that uses Typescript`
    2. hit tab
    3. hit enter
    4. hit enter
5. You're done.

Checkout `hardhat-simple-storage` for a simple sample project.

Checkout `hardhat-fund-me` for an advanced sample project.

# Hardhat Typescript Support
Checkout https://hardhat.org/guides/typescript. 

# Linting
Run `yarn solhint contracts/*.sol` to lint solidity contracts.

# Imports in Solidity
We need to manually install the packages from npm.
For example, we imported several contracts from chainlink/contracts. We need to run `yarn add --dev @chainlink/contracts`.

# Deploy
Hardhat deployments don't save any abi or bins like we did in ethers.

To workaround this, we install [hardhat-deploy](https://github.com/wighawag/hardhat-deploy)plugin. 

1.  Install dependencies
```shell
yarn add --dev hardhat-deploy
yarn add --dev @nomiclabs/hardhat-ethers@npm:hardhat-deploy-ethers ethers
```
2. Add the following statement to your hardhat.config.ts
```typescript
import "hardhat-deploy";
```
3. Create a folder called `deploy/` in project root
4. Add `./deploy` and `./hardhat.config.ts` in the `tsconfig.json` include array.
5. Write deploy scripts in `deploy/` folder
6. Run `yarn hardhat deploy` once you finish composing your deploy scripts
7. NOTE: when you run `yarn hardhat node` the deploy scripts will automatically run and the contracts will be loaded to the nodes.

# Testing
Run `yarn hardhat test --network <networkName>` network defaults to hardhat.

## Unit Tests
- Test every bit of your solidity code.
- Declare a gas reporter variable in your .env to see the gas cost.
- Use `yarn hardhat coverage` to see how much your test covers the contract.

## Staging Tests
See how the codes perform in testnet before launch.
