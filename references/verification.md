# Verification And Handoff

## Static Checks

Run from the skill root or use absolute script paths:

```bash
python3 scripts/inspect_project.py /path/to/project --strict
python3 scripts/validate_project.py /path/to/project
```

Also inspect focused patterns:

```bash
rg -n "require\(|subPackages|subpackages|plugins|gamePlugins" /path/to/project
rg -n "wx\.login|wx\.request|wx\.cloud|create.*Ad|requirePlugin" /path/to/project
find /path/to/project -type d -name '__*__' -print
```

Treat zero script errors as a precondition, not proof of runtime correctness.

## DevTools Matrix

Verify each applicable row:

| Layer | Evidence |
|---|---|
| Import | exact root and debug AppID recorded |
| Compile | zero fatal build/runtime errors |
| Bootstrap | first page or scene visible |
| Packages | requested subpackages/bundles load |
| Interaction | click, drag, movement, or form action works |
| Local services | requested login/backend/ad/plugin path works |
| Persistence | reload retains intended local state |
| Preview | package generation has no forbidden paths |
| Real device | requested flow works under the target base library |

## Cache Discipline

After changing launchers, manifests, package roots, or plugin paths:

1. use the appropriate DevTools clear-cache action;
2. compile again;
3. verify the resource explorer reflects physical changes;
4. generate a new preview QR rather than reusing an older development build.

Do not clear local storage automatically if persistence behavior is under test. Record when storage is intentionally reset.

## Console Discipline

- Never hide exceptions.
- Separate fatal errors from known non-blocking warnings.
- Capture the first stack for each distinct error.
- After fixing one error, reproduce the original interaction that triggered it.
- Watch for delayed callbacks and timer errors after the visible action completes.

## Handoff Record

Document:

- original and debug AppIDs;
- source package hashes;
- decrypted/raw/project paths;
- unpacker name, commit/version, Node version;
- project type and engine version;
- main entry and package roots;
- local-mode flag and bootstrap file;
- edited files and reason;
- exact validation performed;
- remaining online-only features and known warnings.

