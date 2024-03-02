import { HardhatRuntimeEnvironment } from 'hardhat/types';
import { DeployFunction } from 'hardhat-deploy/types';
import { network } from 'hardhat';
import { developmentChains, networkConfig } from '../helper-hardhat-config';
import { verify } from '../utils/verify';

const deployFundme: DeployFunction = async function (
    hre: HardhatRuntimeEnvironment
) {
    const { getNamedAccounts, deployments } = hre;
    const { deploy, log } = deployments;
    const { deployer } = await getNamedAccounts();
    const isDevelopment: boolean = developmentChains.includes(network.name);
    let ethUsdPriceFeedAddress: string;
    if (isDevelopment) {
        const ethUsdAggregator = await deployments.get('MockV3Aggregator');
        ethUsdPriceFeedAddress = ethUsdAggregator.address;
    } else {
        ethUsdPriceFeedAddress = networkConfig[network.name].ethUsdPriceFeed!;
    }
    const args = [ethUsdPriceFeedAddress];
    const fundMe = await deploy('FundMe', {
        from: deployer,
        args: args,
        log: true,
        waitConfirmations: networkConfig[network.name].blockConfirmations || 0,
    });

    // verify contract
    if (!isDevelopment && process.env.ETHERSCAN_API_KEY) {
        await verify(fundMe.address, args);
    }
};
export default deployFundme;
deployFundme.tags = ['all', 'fundme'];
