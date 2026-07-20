# Acquisition, Decryption, And Unpacking

## Contents

- Evidence layout
- Locating packages
- Identifying package format
- Decrypting V1MMWX
- Using wxappUnpacker
- Main and subpackage handling
- Unpacker failure modes

## Evidence Layout

Create a case directory that keeps immutable inputs separate from derived output:

```text
case/<appid>/<timestamp>/
├── original/          encrypted packages copied from cache
├── decrypted/         decrypted wxapkg files
├── raw/               untouched unpacker output
├── project/           reconstructed runnable copy
├── hashes.sha256
└── NOTES.md
```

Hash before processing:

```bash
shasum -a 256 original/*.wxapkg > hashes.sha256
```

Never run repair scripts directly in `original/` or `raw/`.

## Locating Packages

Search by exact AppID and verify metadata. WeChat cache locations vary by client version, account, architecture, and macOS sandbox layout. Inspect current directories rather than hard-coding a single path.

Useful discovery patterns:

```bash
rg --files "$candidate_root" | rg '<appid>|\.wxapkg$'
find "$candidate_root" -type f -name '*.wxapkg' -size +1k
```

Do not select a package solely because it is newest. A target may have a main package, multiple subpackages, plugin code, and old cached versions. Record sizes and magic headers, then correlate package metadata and runtime configuration.

## Identifying Package Format

- `V1MMWX` at byte zero: encrypted cache package; decrypt first.
- byte `0xBE` at offset 0 and `0xED` at offset 13: typical plaintext wxapkg accepted by legacy unpackers.
- anything else: do not force a decoder. Verify that the file is complete and identify its format.

Inspect safely:

```bash
xxd -l 32 package.wxapkg
```

## Decrypting V1MMWX

Use the bundled script:

```bash
node scripts/decrypt_wxapkg.js \
  --appid wx1234567890abcdef \
  --input original/package.wxapkg \
  --output decrypted/package.wxapkg
```

The script refuses to overwrite output unless `--force` is supplied and verifies the decrypted wxapkg magic. A bad AppID normally produces an AES/padding or header validation failure.

## Using wxappUnpacker

This skill does not vendor wxappUnpacker. A known legacy implementation is `qwerty472123/wxappUnpacker` (`wxapp-unpacker` in its `package.json`). Pin and document the exact commit or local copy used.

Typical commands from the unpacker directory:

```bash
npm install
node wuWxapkg.js -d /absolute/path/decrypted/main.wxapkg
node wuWxapkg.js -o /absolute/path/decrypted/main.wxapkg
node wuWxapkg.js -s=/absolute/path/raw/main /absolute/path/decrypted/subpackage.wxapkg
```

- `-d` keeps transformed intermediate files and is useful for forensic recovery.
- `-o` extracts files without post-processing and is useful when transformation fails.
- `-s=<main-dir>` supplies the main source directory while processing subpackages.

Legacy unpackers may require an older compatible Node dependency set. Do not blindly update dependencies: modern `cheerio`, `glob`, or `vm2` versions can change behavior or require newer Node versions. Keep the working lockfile with the case notes.

## Main And Subpackage Handling

1. Unpack the main package first.
2. Read `app-config.json`, reconstructed `app.json`, or `game.json`.
3. Map every configured subpackage `root` to its package.
4. Unpack each subpackage with main context when the unpacker requires it.
5. Preserve raw results, then assemble `project/` according to configured roots.
6. Check for duplicated output paths created by splitters.
7. Locate plugin caches separately; a plugin AppID is not the host AppID.

For a mini game, the main package may contain only bootstrap code while most game code and assets live in independent subpackages. For a normal mini program, page logic may be split from `app-service.js` and view layers from `page-frame.html`, `page-frame.js`, or `app-wxss.js`.

## Unpacker Failure Modes

### VM2 marker leakage

Generated files may contain identifiers such as `VM2_INTERNAL_STATE_DO_NOT_USE_OR_PROGRAM_WILL_FAIL`. Treat this as unpacker transformation damage. Compare the raw extraction and transformed output before removing anything.

### One-line or obfuscated bundles

Do not assume unpacking failed because a generated bundle remains minified. Preserve it and repair narrow integration boundaries around it.

### Missing page-frame-like file

Use raw extraction mode, identify the client format, and determine whether view code lives in another package. Do not fabricate WXML before confirming the corresponding runtime resources.

### Subpackage detected without main directory

Supply the correct main extraction directory. If the result nests the subpackage root twice, determine which copy the runtime launcher actually loads before editing.

