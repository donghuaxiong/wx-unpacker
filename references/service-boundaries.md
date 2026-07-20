# Local Service Boundaries

## Contents

- Design rules
- Response contracts
- Login and backend
- Ads
- Analytics
- Plugins and cloud features
- Storage

## Design Rules

Keep replacements behind one named local-mode switch. Load them early enough to intercept integrations but after the platform object exists.

Prefer one bootstrap file over edits scattered through generated bundles. Log local substitutions with a stable prefix such as `[local-mode]`.

Trace each caller and record:

- method name and arguments
- synchronous return value
- Promise behavior
- callback registration/removal
- event order
- nested response fields
- persistence side effects

## Response Contracts

A common service wrapper expects more than a status code:

```js
function localResponse(data) {
    return {
        code: 0,
        error: "",
        rawData: data,
        getData: function() { return data; }
    };
}
```

Match the actual project instead of copying this shape blindly. If callers chain `.then()`, return a Promise. If they access synchronously, do not substitute a Promise.

## Login And Backend

A DevTools login code for a different AppID will not authenticate against the original backend. Separate:

- platform login success;
- session exchange;
- account/role bootstrap;
- later gameplay APIs.

Return structurally correct local data only for flows in scope. Never attempt to obtain or reuse another user's session, OpenID, token, or protected data.

## Ads

Implement the API surface callers use:

- `load`, `show`, `hide`, `destroy`
- `onLoad/offLoad`
- `onClose/offClose`
- `onError/offError`
- `onResize/offResize`
- `style` when expected

For an authorized ad-free local build that explicitly retains rewards, resolve `show()` and invoke close listeners with `{isEnded: true}`. For an ordinary offline build where rewards must not be granted, return a failure/no-op shape instead. Do not make reward policy implicit.

Block banner, interstitial, custom, grid, and other rendered ads without creating visible nodes. Test delayed verification calls after a rewarded callback; they may target an online plugin even after the ad itself is mocked.

## Analytics

Skipping SDK construction is insufficient when game code later calls convenience methods. Mirror the public surface actually used, for example:

- `track`, `report`, `flush`
- `onAppStart`, `onAppQuit`
- `onEnterForeground`, `onEnterBackground`
- `onRegister`, `onCreateRole`, `onTutorialFinish`
- identifier setters

Return a stable success result and avoid network access. A missing analytics method inside a touch handler can interrupt movement or navigation.

## Plugins And Cloud Features

Mock plugins by provider/alias only when the online declaration is removed or unavailable. Preserve expected `default` exports and method contracts. Unknown-method fallbacks should be narrowly scoped and logged; a Proxy that makes every property truthy can change feature detection.

Disable rather than fake:

- payments
- protected rankings/account transfers
- authorization grants
- subscription enrollment
- cloud writes with external impact

## Storage

Wrap storage APIs using bound native functions. Avoid recursion after replacing methods. For persistent debug values:

1. transform reads;
2. transform writes;
3. preserve unrelated keys;
4. validate serialized and object forms;
5. migrate existing data explicitly.

