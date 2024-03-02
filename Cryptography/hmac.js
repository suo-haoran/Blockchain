const { createHmac } = require("crypto");

const key = "super-secret";
const message = "🎃 hello jack";

const hmac = createHmac("sha256", key).update(message).digest("hex");
console.log(hmac);
