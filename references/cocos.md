# Cocos Creator Mini Games

## Contents

- Runtime chain
- Plugin localization
- Module resolution
- Bundles and scenes
- Storage and data
- Frequent failures

## Runtime Chain

Identify the Cocos version from settings, engine constants, or cached plugin metadata. Do not assume the version declared in `game.json` matches the cached engine file.

Verify all of these where applicable:

- `adapter-min.js`
- `__globalAdapter.init()`
- engine/plugin bootstrap
- `__globalAdapter.adaptEngine()`
- `ccRequire.js`
- `src/settings.js`
- `main.js`
- `window.boot()`

The exact working order depends on the generated version. Preserve the original ordering unless a stack trace proves it is broken.

## Plugin Localization

When the original host references an unavailable Cocos game plugin:

1. Locate the exact cached plugin version.
2. Preserve its module registry and engine payload.
3. Load it from a normal physical directory such as `local-plugins/`.
4. Keep virtual module IDs expected by the registry.
5. Remove the online `gamePlugins` declaration only after every required plugin behavior has a local implementation.

Example distinction:

```text
physical path: local-plugins/cocos.js          allowed
virtual ID:    __plugin__/wx.../cocos2d-js.js required by registry
physical path: __plugin__/...                  rejected by preview upload
```

Moving a wrapper changes the relative base used by WeChat's `require()`. Normalize the virtual request explicitly and verify the resulting module ID.

## Module Resolution

For `module __plugin__ is not defined` or doubled prefixes:

- inspect the calling module ID;
- inspect the exact `define("...")` registrations in the plugin bundle;
- resolve the requested path relative to the caller;
- change one wrapper path, not the entire generated bundle.

Use filesystem checks for physical files and string inspection for virtual registrations. They are different namespaces.

## Bundles And Scenes

Confirm:

- every bundle root exists;
- bundle configuration matches extracted assets;
- the initial `.fire` scene exists;
- bundle loaders use local or expected remote URLs;
- missing remote bundles are localized or explicitly disabled.

When an item or prefab is missing, verify its UUID/config ID and bundle membership. Do not choose arbitrary existing assets just to silence an error.

## Storage And Data

Seed state only after `settings` and game configuration load. If a scene or board was cached before data injection:

1. patch before preload;
2. preload referenced prefabs;
3. invalidate or refresh the runtime cache;
4. bump the local snapshot version.

For merge/board games, construct cells from real configuration relationships and clear stale locks, recovery state, orders, or backend-only fields deliberately.

## Frequent Failures

- `cc is not defined`: engine/bootstrap order is wrong.
- `module ... is not defined`: caller-relative module ID is wrong or bundle did not register it.
- initial scene missing: settings or asset root is incomplete.
- screen renders but touch fails: inspect exceptions in the same touch event before changing input code.
- reload loses local changes: authoritative storage write path was not patched.
- DevTools runs but preview rejects files: inspect reserved directories, package roots, size, and plugin declarations.

