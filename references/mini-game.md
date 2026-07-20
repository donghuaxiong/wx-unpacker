# WeChat Mini Games

## Contents

- Recognition
- Engine detection
- Package topology
- Startup repair
- Game state
- Interaction validation

## Recognition

A mini game normally has `game.js` and `game.json` at the import root. It may use a custom engine or a generated runtime such as Cocos, Laya, Egret, Unity WebGL-derived tooling, or another framework.

Common engine indicators:

- Cocos: `cc`, `adapter-min.js`, `ccRequire.js`, `settings.js`, `plugin-bundle.js`
- Laya: `laya.*.js`, `Laya`, `game.js` loaders
- Egret: `egret`, `manifest.js`, `main.min.js`

Do not apply Cocos fixes to another engine.

## Package Topology

Record:

- main package entry and bootstrap files
- ordinary and independent subpackages
- asset bundles and remote bundles
- open-data context/shared canvas
- engine plugins and service plugins
- plugin AppIDs and cached versions

A page-like folder name does not prove it is the configured subpackage root. Read `game.json` and bootstrap module registrations.

## Startup Repair

Trace the actual dependency chain:

```text
game.js
→ platform adapter/bootstrap
→ engine runtime or plugin bundle
→ settings/module registry
→ main entry
→ first scene
```

Fix module resolution and load order before patching missing globals one by one. If `cc` or another engine global is undefined, identify where the engine should be initialized.

Generated launchers often contain virtual module registries. A string such as `__plugin__/appid/module.js` may identify a virtual module, while a physical directory named `__plugin__` can be rejected by preview upload. Preserve the virtual ID and move only the physical wrapper when necessary.

## Interaction Validation

Rendering is not enough. Exercise:

- first touch/click after entering a scene
- movement or drag controls
- one combat/action loop
- one scene transition

An analytics or plugin exception inside a touch-begin handler can look like a movement bug. Follow the entire stack before modifying movement code.
