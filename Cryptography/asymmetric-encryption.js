const { publicEncrypt, privateDecrypt } = require("crypto");
const { publicKey, privateKey } = require("./keypair");

// Asymmetric encryption
// very practical

const message = "the british are coming";

// Like dropping letter to a letter box.
const encryptedData = publicEncrypt(publicKey, Buffer.from(message));

console.log(encryptedData.toString("hex"));

// Use your key to open the letter box and take the letter out.
const decryptedData = privateDecrypt(privateKey, encryptedData);

console.log(decryptedData.toString("utf8"));

// How u gonna verify whether the sender is legit?
// Checkout signing