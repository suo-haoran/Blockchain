import { ethers, network } from "hardhat";
import { DeployFunction } from "hardhat-deploy/types";
import { HardhatRuntimeEnvironment } from "hardhat/types";
import { developmentChains } from "../helper-hardhat-config";

const BASE_FEE = ethers.utils.parseEther("0.25"); // 0.25 is premium, it costs 0.25 LINK.
const GAS_PRICE_LINK = 1e9; // Calculated value based on the gas of the chain

const deployMocks: DeployFunction = async function (
  hre: HardhatRuntimeEnvironment
) {
  const { getNamedAccounts, deployments } = hre;
  const { deploy, log } = deployments;
  const { deployer } = await getNamedAccounts();
  const networkName = network.name;
  const args = [BASE_FEE, GAS_PRICE_LINK];

  if (developmentChains.includes(networkName)) {
    log("Local Network Detected! Deploying mocks...");
    await deploy("VRFCoordinatorV2Mock", {
      from: deployer,
      log: true,
      args: args,
    });
    log("Mocks deployed!");
    log("---------------------------------------------");
  }
};

export default deployMocks;
deployMocks.tags = ["all", "mocks"];
