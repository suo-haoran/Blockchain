const { createHash } = require("crypto");

function hash(input) {
  return createHash("sha256").update(input).digest("hex");
}

let password = "Hi-mom!";
const hash1 = hash(password);
console.log(hash1);

// some time later..
password = "Hi-mom!";
const hash2 = hash(password);
const match = hash1 === hash2;
console.log(match ? "✔ Good Password" : "✘ Password does not match");
