import { readFileSync, writeFileSync } from "fs";
import { ethers, network } from "hardhat";
import { DeployFunction } from "hardhat-deploy/types";
import { HardhatRuntimeEnvironment } from "hardhat/types";


const FRONT_END_PATH = "../nextjs-lottery/constants";
const FRONT_END_ADDRESSES_FILE = `${FRONT_END_PATH}/contract-addressses.json`;
const FRONT_END_ABI_FILE = `${FRONT_END_PATH}/abi.json`;

const update: DeployFunction = async function (hre: HardhatRuntimeEnvironment) {
  if (process.env.UPDATE_FRONT_END) {
    console.log("Updating Front End...");
    console.log("current path: " + process.cwd());
    updateContractAddresses();
    updateAbi();
  }
};

async function updateContractAddresses() {
  const lottery = await ethers.getContract("Lottery");
  const chainId = network.config.chainId!.toString();
  const currentAddresses = JSON.parse(
    readFileSync(FRONT_END_ADDRESSES_FILE, "utf8")
  );
  if (chainId in currentAddresses) {
    if (!currentAddresses[chainId].includes(lottery.address)) {
      currentAddresses[chainId].push(lottery.address);
    }
  } else {
    currentAddresses[chainId] = [lottery.address];
  }
  writeFileSync(FRONT_END_ADDRESSES_FILE, JSON.stringify(currentAddresses));
}

async function updateAbi() {
    const lottery = await ethers.getContract("Lottery");
    const jsonAbi = lottery.interface.format(ethers.utils.FormatTypes.json).toString()
    writeFileSync(FRONT_END_ABI_FILE, JSON.stringify(JSON.parse(jsonAbi)))
}

export default update;
update.tags = ["all", "frontend"];
