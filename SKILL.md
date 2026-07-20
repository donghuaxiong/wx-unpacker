---
name: wx-unpacker-skill
description: Locate, decrypt, unpack, inspect, reconstruct, and validate authorized WeChat mini programs and WeChat mini games from wxapkg packages. Use when Codex must locate packages by AppID, decrypt V1MMWX containers, drive wxappUnpacker, reconstruct main and subpackage topology, distinguish normal mini programs from mini games, resolve launchers and Cocos/plugin paths, or prepare an unpacked project for basic import and preview checks in WeChat DevTools.
---

# WeChat Package Unpacking And Reconstruction

Work only on software the user owns or is authorized to inspect. Preserve every source package and perform modifications in a separate working copy.

## Route The Task

1. Record the AppID, package paths, requested outcome, and allowed modification scope.
2. Run `python3 scripts/inspect_project.py <path>` on an unpacked directory when available.
3. Classify the target:
   - `app.json`, pages, WXML/WXSS: normal mini program. Read `references/mini-program.md`.
   - `game.json`, `game.js`, Cocos/Laya/Egret assets: mini game. Read `references/mini-game.md`.
   - `cc`, `adapter-min.js`, `plugin-bundle.js`: also read `references/cocos.md`.
4. Read `references/unpacking.md` before locating, decrypting, or unpacking packages.
5. Read `references/verification.md` before declaring the unpacking and reconstruction work complete.
6. Use `references/troubleshooting.md` for concrete import, startup, or preview errors.

## Required Workflow

### 1. Acquire Without Destroying Evidence

- Locate packages by exact AppID; do not guess from modification time alone.
- Copy encrypted packages into a timestamped case directory.
- Record size and SHA-256 for every source package.
- Never modify the only copy of a wxapkg.
- Treat account identifiers, OpenIDs, tokens, and cached responses as sensitive; do not print or transmit them unnecessarily.

### 2. Decrypt And Unpack

- Detect `V1MMWX` before decrypting.
- Use `node scripts/decrypt_wxapkg.js --appid <appid> --input <input> --output <output>`.
- Verify the decrypted wxapkg header before unpacking.
- Use a compatible external unpacker such as qwerty472123/wxappUnpacker; the skill does not vendor that GPL project.
- Unpack the main package first. Unpack subpackages with the unpacker's main-directory option when required.
- Preserve raw extraction output separately from the runnable reconstruction.

### 3. Reconstruct Package Topology

- Identify the real main package, subpackages, independent subpackages, plugins, workers, and open-data context.
- Read `app.json` or `game.json` before merging anything.
- Put each subpackage under the configured `root`; do not flatten by filename alone.
- Detect duplicate nesting such as `subpackages/main/subpackages/main/`.
- Keep one canonical editable copy for every runtime file and document any synchronized copies.

### 4. Verify The Reconstructed Entry Chain

- Trace the launcher from `app.js` or `game.js` into the actual runtime entry.
- Verify every relative `require()` and referenced package root exists.
- Repair engine, adapter, settings, bootstrap, and scene load order as one dependency chain.
- Distinguish physical paths from virtual module IDs. Never globally replace `__plugin__/...` strings merely because physical `__plugin__` directories are forbidden during preview upload.
- Import the exact reconstructed root into WeChat DevTools and capture the first fatal stack trace before further path repairs.
- Stop at package reconstruction and basic startup verification. Do not modify business data, rewards, advertising behavior, login, backend services, or other post-unpack product behavior as part of this skill.

### 5. Validate In Layers

Run static checks first:

```bash
python3 scripts/inspect_project.py <project-root> --strict
python3 scripts/validate_project.py <project-root>
```

Then validate in WeChat DevTools:

1. Clear the appropriate compile cache after changing entry files or package paths.
2. Compile with zero fatal errors.
3. Open the initial page or scene.
4. Confirm required main-package, subpackage, plugin, and resource paths resolve.
5. Generate a preview package and test on a real device when requested or when platform differences matter.

Do not suppress exceptions to make the console look clean. Classify known warnings explicitly.

## Editing Rules

- Keep originals, decrypted packages, raw extraction, and working project in distinct directories.
- Make focused edits and run syntax checks after each edited JavaScript file.
- Avoid mass replacement in minified bundles unless a unique, counted pattern and rollback path are established.
- Prefer wrapper/bootstrap patches over invasive edits to multi-megabyte generated bundles.
- Record the exact imported root, AppID used for debugging, package topology, modified reconstruction files, and validation results.

## Completion Standard

Call the unpacking work complete only when the recovered package structure is demonstrated. A reconstructed package normally requires:

- source packages preserved and hashed;
- package topology reconstructed;
- launcher and relative modules resolved;
- no forbidden physical directory names;
- static validation completed;
- zero fatal startup errors and the initial screen visible when runnable reconstruction is in scope;
- preview/real-device behavior checked when in scope.
