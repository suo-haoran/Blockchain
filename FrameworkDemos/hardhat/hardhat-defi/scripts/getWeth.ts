import { ethers, getNamedAccounts } from "hardhat";

export const AMOUNT = ethers.utils.parseEther("0.02").toString();

export async function getWeth() {
    const {deployer} = await getNamedAccounts();
    const iWeth = await ethers.getContractAt("IWeth", "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", deployer)
    const txn = await iWeth.deposit({value: AMOUNT});
    await txn.wait(1)
    const wethBalance = await iWeth.balanceOf(deployer);
    console.log(`Got ${wethBalance.toString()} WETH`);
}