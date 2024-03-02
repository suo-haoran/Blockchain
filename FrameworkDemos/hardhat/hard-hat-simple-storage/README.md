# Basic Sample Hardhat Project

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, a sample script that deploys that contract, and an example of a task implementation, which simply lists the available accounts.

Try running some of the following tasks:

```shell
npx hardhat accounts
npx hardhat compile
npx hardhat clean
npx hardhat test
npx hardhat node
node scripts/sample-script.js
npx hardhat help
```
change npx to yarn.
Checkout https://hardhat.org/plugins for hardhat plugins.

Run hardhat scripts `yarn hardhat run scripts/<scriptName>.js` with/without `--network <network>`.

If something's funky like no such file or directory, try `yarn hardhat clean`.

To use the hardhat console, run `yarn hardhat console --network <networkName>`

Gas reporter is useful when you want to know how much your transaction costs. It will give you a report every time you test. To install, run `yarn add hardhat-gas-reporter --dev`, and enable/disable inside `hardhat.config.js`. Checkout their [github repo](https://github.com/cgewecke/hardhat-gas-reporter).

Solidity coverage will give some insights about test code coverage. Run `yarn add solidity-coverage --dev` to install. Run `yarn hardhat coverage` to trigger it. Checkout their [github repo](https://github.com/sc-forks/solidity-coverage). 

Hardhat waffle is a testing framework, read more on https://hardhat.org/plugins/nomiclabs-hardhat-waffle.

Hardhat etherscan helps verify contracts on etherscan, read more on https://hardhat.org/plugins/nomiclabs-hardhat-etherscan.

## Typescript
To use typescript, we must install some additional dependencies
```shell
yarn add --dev @typechain/ethers-v5 @typechain/hardhat @types/chai @types/node @types/mocha ts-node typechain typescript
```

And add a `tsconfig.json` in the project root.
```json
{
    "compilerOptions": {
        "target": "es2018",
        "module": "commonjs",
        "strict": true,
        "esModuleInterop": true,
        "outDir": "dist"
    },
    "include": ["./scripts", "./test"],
    "files": ["./hardhat.config.ts"]
}

```
There's a small problem of typescript not able to figure out your contract code. [Typechain](https://github.com/dethcrypto/TypeChain) goin' sort this out for you.
1. `import "@typechain/hardhat";` in `hardhat.config.ts` 
2. Run `yarn hardhat typechain` in console. It will make a dir `typechain-types`.
    - This will generate your contract's function signatures in typescript.
3. `import "typechain-types/<yourContractName>`

For more detailed stuff, checkout https://hardhat.org/guides/typescript