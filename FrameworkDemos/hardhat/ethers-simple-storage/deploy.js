const ethers = require("ethers");
const fs = require("fs-extra");
require("dotenv").config();

async function main() {
  // start up ganache ui
  const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
  // const wallet = new ethers.Wallet(
  //   // Dont put private keys in source code.
  //   process.env.PRIVATE_KEY,
  //   provider
  // );
  const encryptedJson = fs.readFileSync("./.encryptedKey.json", "utf8");
  const wallet = await new ethers.Wallet.fromEncryptedJsonSync(
    encryptedJson,
    process.env.PRIVATE_KEY_PASSWORD
  ).connect(provider);
  const abi = fs.readFileSync("./SimpleStorage_sol_SimpleStorage.abi", "utf8");
  const binary = fs.readFileSync(
    "./SimpleStorage_sol_SimpleStorage.bin",
    "utf8"
  );
  const contractFactory = new ethers.ContractFactory(abi, binary, wallet);
  console.log("Deploying, please wait...");
  // Stop here! Wait for contract to deploy.
  const contract = await contractFactory.deploy();
  await contract.deployTransaction.wait(1);
  console.log(`Contract Address: ${contract.address}`);
  // use transaction data to deploy
  // console.log("let's deploy with only transaction data!");
  // const nonce = await wallet.getTransactionCount();
  // const txn = {
  //   // current transaction count, refer to ganache (current block), use number (current block + 1)
  //   nonce: nonce,
  //   gasPrice: 20000000000,
  //   gasLimit: 1000000,
  //   to: null,
  //   value: 0,
  //   data: "Copy the SimpleStorage bin here, append 0x infront",
  //   chainId: 1337, // Ganache
  // };

  // sendTransaction will automatically sign it for you.
  // const sentTxnResponse = await wallet.sendTransaction(txn);
  // await sentTxnResponse.wait(1);
  // console.log(sentTxnResponse);
  const currentFavoriteNumber = await contract.retrieve();
  console.log(currentFavoriteNumber); // Big number, why? cuz js can't handle big numbers.
  console.log(`Current Favorite Number: ${currentFavoriteNumber.toString()}`); // Need toString to display the number, why? cuz js can't handle big numbers.
  const transactionResponse = await contract.store("7");
  const transactionReceipt = await transactionResponse.wait(1);
  const updatedFavoriteNumber = await contract.retrieve();
  console.log(`Updated Favorite Number: ${updatedFavoriteNumber.toString()}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
  });
