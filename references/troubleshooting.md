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

Move the physical wrapper to a normal directory. Preserve virtual `__plugin__/...` IDs registered inside JavaScript. Remove online plugin declarations only after local behavior is complete.

## Services And Interaction

### Invalid login code

The debug AppID cannot authenticate against the original backend. Gate a local login/bootstrap path rather than retrying indefinitely.

### `getData is not a function`

The mock response shape is incomplete. Trace the caller and return the service wrapper object it expects.

### Reward callback succeeds, then a delayed error appears

The game is probably calling an online verification/plugin method after the ad closes. Mock that separate boundary and reproduce after its timer delay.

### Screen renders but touch, navigation, or movement fails

Inspect the first exception from touch-begin/click dispatch. Analytics, tutorial, or plugin calls can interrupt the same event before movement logic runs.

### State resets after reload

Patch the authoritative write path as well as the read path, and verify the actual storage key/schema.

## Assets And Data

### Bundle does not contain an asset

Verify bundle membership, UUID/config ID, and whether the asset was remote or in another package. Do not silence the error by inventing an unrelated asset.

### Board/scene is blank after seeding data

- seed after configuration load;
- preload referenced prefabs;
- clear locks only when intended;
- invalidate stale caches;
- bump the local snapshot version.

## Preview And Device

### DevTools runs, preview upload fails

Check reserved directories, package size, ignored files, plugin declarations, invalid JSON, missing subpackage roots, and case-sensitive paths. Run `validate_project.py` before retrying.

### New code works locally but phone shows old behavior

Compile after clearing the relevant cache, create a new preview package, and rescan the new QR. Remove stale recent-development entries only when necessary.

