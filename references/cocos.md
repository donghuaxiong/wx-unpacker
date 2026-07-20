# Cocos Creator Mini Games

## Contents

- Runtime chain
- Plugin recovery
- Module resolution
- Bundles and scenes
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

## Plugin Recovery

When the original host references an unavailable Cocos game plugin:

1. Locate the exact cached plugin version.
2. Preserve its module registry and engine payload.
3. Load it from a normal physical directory such as `local-plugins/`.
4. Keep virtual module IDs expected by the registry.
5. Adjust the online `gamePlugins` declaration only after the recovered engine payload loads from its reconstructed path.

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
- missing remote bundles are recovered from an authorized package source or reported as unavailable.

When an item or prefab is missing, verify its UUID/config ID and bundle membership. Do not choose arbitrary existing assets just to silence an error.

## Frequent Failures

- `cc is not defined`: engine/bootstrap order is wrong.
- `module ... is not defined`: caller-relative module ID is wrong or bundle did not register it.
- initial scene missing: settings or asset root is incomplete.
- DevTools runs but preview rejects files: inspect reserved directories, package roots, size, and plugin declarations.
