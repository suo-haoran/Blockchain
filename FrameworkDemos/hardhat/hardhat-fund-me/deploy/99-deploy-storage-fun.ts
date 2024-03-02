import { HardhatRuntimeEnvironment } from 'hardhat/types';
import { DeployFunction } from 'hardhat-deploy/types';
import { ethers, network } from 'hardhat';
import { developmentChains, networkConfig } from '../helper-hardhat-config';
import { verify } from '../utils/verify';
const deployFunWithStorage: DeployFunction = async function (
    hre: HardhatRuntimeEnvironment
) {
    const { getNamedAccounts, deployments } = hre;
    const { deploy, log } = deployments;
    const { deployer } = await getNamedAccounts();
    log('----------------------------------------------------');
    log('Deploying FunWithStorage and waiting for confirmations...');
    const funWithStorage = await deploy('FunWithStorage', {
        from: deployer,
        args: [],
        log: true,
        // we need to wait if on a live network so we can verify properly
        waitConfirmations: networkConfig[network.name].blockConfirmations || 1,
    });
    log('Logging storage...');
    for (let i = 0; i < 10; i++) {
        log(
            `Location ${i}: ${await ethers.provider.getStorageAt(
                funWithStorage.address,
                i
            )}`
        );
    }
};

export default deployFunWithStorage;
deployFunWithStorage.tags = ['storage'];
