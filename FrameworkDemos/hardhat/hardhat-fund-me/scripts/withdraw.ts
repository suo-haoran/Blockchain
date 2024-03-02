import { ethers } from 'hardhat';

// try running this on a local node
async function main() {
    const deployer = (await ethers.getSigners())[0];
    const fundMe = await ethers.getContract('FundMe', deployer);
    console.log('Withdrawing');
    const transactionResponse = await fundMe.withdraw();
    await transactionResponse.wait(1);
    console.log('Withdrawn!');
}

main()
    .then(() => process.exit(0))
    .catch((err) => {
        console.error(err);
        process.exit(1);
    });
