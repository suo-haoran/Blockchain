// iv = initial vector
const { createCipheriv, randomBytes, createDecipheriv } = require("crypto");

// Cipher

const message = "i like turtles";
const key = randomBytes(32);
// randomizes cipher text each time
const iv = randomBytes(16);

const cipher = createCipheriv("aes256", key, iv);

// Encrypt

const encryptedMessage =
  cipher.update(message, "utf8", " hex") + cipher.final("hex");

// Decrypt

const decipher = createDecipheriv("aes256", key, iv);
const decryptedMessage =
  decipher.update(encryptedMessage, "hex", "utf8") + decipher.final("utf8");

console.log(`Encrypted: ${encryptedMessage}`);
console.log(`Deciphered: ${decryptedMessage.toString("utf-8")}`);

// Encrypt and Decrypt requires same password, not so practical.