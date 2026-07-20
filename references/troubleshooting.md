# Troubleshooting Catalog

## Package And Import

### Invalid wxapkg magic

- Check for `V1MMWX` encryption.
- Verify the AppID used for decryption.
- Confirm the package is complete and not a cache index/blob wrapper.

### Imported project has no entry

- Confirm the selected directory directly contains `app.json`/`app.js` or `game.json`/`game.js`.
- Inspect nested unpacker output before moving files.

### Subpackage asks for `-s`

- Unpack the main package first.
- Supply the absolute main extraction directory.
- Recheck configured subpackage roots after transformation.

## Module And Engine

### `cc is not defined`

Repair the engine/bootstrap/adapter load chain. Do not create a fake `cc` global.

### `module ... is not defined`

- Identify the calling module ID.
- Resolve relative paths from that caller.
- Confirm a physical file exists or a virtual registry defines the normalized ID.
- Avoid adding the same directory prefix twice.

### Plugin works in DevTools but preview rejects `__plugin__`

Move the physical wrapper to a normal directory. Preserve virtual `__plugin__/...` IDs registered inside JavaScript. Adjust declarations only when required for the reconstructed package topology.

## Assets And Data

### Bundle does not contain an asset

Verify bundle membership, UUID/config ID, and whether the asset was remote or in another package. Do not silence the error by inventing an unrelated asset.

## Preview And Device

### DevTools runs, preview upload fails

Check reserved directories, package size, ignored files, plugin declarations, invalid JSON, missing subpackage roots, and case-sensitive paths. Run `validate_project.py` before retrying.

### New code works locally but phone shows old behavior

Compile after clearing the relevant cache, create a new preview package, and rescan the new QR. Remove stale recent-development entries only when necessary.
