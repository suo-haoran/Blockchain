import "@nomiclabs/hardhat-waffle";
import "dotenv/config";
import "@nomiclabs/hardhat-etherscan"; // will add a verify task, run yarn hardhat, verity is at the bottom!
import "./tasks/block-number";
import "hardhat-gas-reporter";
import "solidity-coverage";
import "@nomiclabs/hardhat-ethers"; 
import "@typechain/hardhat";

// You need to export an object to set up your config
// Go to https://hardhat.org/config/ to learn more

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
const RINKEBY_RPC_URL = process.env.RINKEBY_RPC_URL || "https//eth-rinkeby";
const PRIVATE_KEY = process.env.PRIVATE_KEY || "0xkey";
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY || "key";
module.exports = {
    // uncomment to config defaultNetwork.
    // defaultNetwork: "rinkeby",
    networks: {
        rinkeby: {
            url: RINKEBY_RPC_URL,
            accounts: [PRIVATE_KEY],
            chainId: 4, // checkout chainlist.org
        },
        // run yarn hardhat node in a separate terminal
        localhost: {
            url: "http://127.0.0.1:8545",
            // accounts: Hardhat already populate this field for us.
            chainId: 31337,
        },
    },
    solidity: "0.8.8",
    etherscan: {
        apiKey: ETHERSCAN_API_KEY,
    },
    gasReporter: {
        enabled: true,
        outputFile: "gas-report.txt",
        noColors: true,
        // Need to register coinmarketcap account and get api key
        // It will use live feed to determine currency conversion
        // currency: "USD",
        // coinmarketcap: COINMARKETCAP_API_KEY
    },
};
