import { ethers } from 'hardhat';

// try running this on a local node
async function main() {
    const deployer = (await ethers.getSigners())[0];
    const fundMe = await ethers.getContract('FundMe', deployer);
    console.log('Funding contract');
    const transactionResponse = await fundMe.fund({
        value: ethers.utils.parseEther('0.1'),
    });
    await transactionResponse.wait(1);
    console.log('Funded!');
}

main()
    .then(() => process.exit(0))
    .catch((err) => {
        console.error(err);
        process.exit(1);
    });
