#!/usr/bin/env node

"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

function usage(message) {
    if (message) console.error(message);
    console.error("Usage: node decrypt_wxapkg.js --appid <wx...> --input <encrypted.wxapkg> --output <decrypted.wxapkg> [--force]");
    process.exit(2);
}

function parseArgs(argv) {
    const options = { force: false };
    for (let index = 0; index < argv.length; index += 1) {
        const arg = argv[index];
        if (arg === "--force") {
            options.force = true;
        } else if (arg === "--appid" || arg === "--input" || arg === "--output") {
            const value = argv[index + 1];
            if (!value || value.startsWith("--")) usage("Missing value for " + arg);
            options[arg.slice(2)] = value;
            index += 1;
        } else if (arg === "--help" || arg === "-h") {
            usage();
        } else {
            usage("Unknown argument: " + arg);
        }
    }
    if (!options.appid || !options.input || !options.output) usage("--appid, --input and --output are required");
    if (!/^wx[a-zA-Z0-9]+$/.test(options.appid)) usage("AppID must start with wx");
    return options;
}

function isPlainWxapkg(buffer) {
    return buffer.length >= 14 && buffer[0] === 0xbe && buffer[13] === 0xed;
}

function main() {
    const options = parseArgs(process.argv.slice(2));
    const input = path.resolve(options.input);
    const output = path.resolve(options.output);

    if (input === output) throw new Error("Input and output must be different files");
    if (!fs.existsSync(input) || !fs.statSync(input).isFile()) throw new Error("Input file does not exist: " + input);
    if (fs.existsSync(output) && !options.force) throw new Error("Output already exists; use --force to replace it: " + output);

    const encrypted = fs.readFileSync(input);
    if (encrypted.length < 1030) throw new Error("Input is too small to be a V1MMWX package");
    if (encrypted.subarray(0, 6).toString("ascii") !== "V1MMWX") {
        if (isPlainWxapkg(encrypted)) throw new Error("Input already appears to be a decrypted wxapkg");
        throw new Error("Unsupported package header; expected V1MMWX");
    }

    const key = crypto.pbkdf2Sync(options.appid, "saltiest", 1000, 32, "sha1");
    const iv = Buffer.from("the iv: 16 bytes");
    const decipher = crypto.createDecipheriv("aes-256-cbc", key, iv);
    const decryptedHead = Buffer.concat([
        decipher.update(encrypted.subarray(6, 6 + 1024)),
        decipher.final()
    ]);
    const xorKey = options.appid.charCodeAt(options.appid.length - 2) || 0x66;
    const tail = Buffer.from(encrypted.subarray(6 + 1024));
    for (let index = 0; index < tail.length; index += 1) tail[index] ^= xorKey;

    const decrypted = Buffer.concat([decryptedHead, tail]);
    if (!isPlainWxapkg(decrypted)) throw new Error("Decryption completed but wxapkg magic is invalid; verify the AppID");

    fs.mkdirSync(path.dirname(output), { recursive: true });
    fs.writeFileSync(output, decrypted, { flag: options.force ? "w" : "wx" });
    console.log(JSON.stringify({ input, output, bytes: decrypted.length, header: "BE...ED" }, null, 2));
}

try {
    main();
} catch (error) {
    console.error("decrypt_wxapkg: " + error.message);
    process.exit(1);
}

