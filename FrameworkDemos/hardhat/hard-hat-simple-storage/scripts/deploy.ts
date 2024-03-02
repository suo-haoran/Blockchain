import { ethers, run, network } from "hardhat";

async function main() {
    // We get the contract to deploy
    const SimpleStorageFactory = await ethers.getContractFactory(
        "SimpleStorage"
    );
    const simpleStorage = await SimpleStorageFactory.deploy();

    await simpleStorage.deployed();
    console.log("SimpleStorage deployed to:", simpleStorage.address);
    console.log(network.config);
    if (network.config.chainId === 4 && process.env.ETHERSCAN_API_KEY) {
        await simpleStorage.deployTransaction.wait(6); // wait 6 blocks.
        verify(simpleStorage.address, []);
    }

    const currentValue = await simpleStorage.retrieve()
    console.log(`Current value is ${currentValue}`);
    const transactionResponse = await simpleStorage.store(7);
    await transactionResponse.wait(1)
    const updatedValue = await simpleStorage.retrieve()
    console.log(`Updated value is ${updatedValue}`);
}

async function verify(contractAddress: String, args: any[]) {
    console.log("Verifying contract...");
    // verify task added by etherscan
    try {
        await run("verify:verify", {
            address: contractAddress,
            constructorArguments: args,
        });
    } catch (e: any) {
        if (e.message.toLowerCase().includes("already verified")) {
            console.log("Already verified!");
        } else {
            console.log(e);
        }
    }
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
