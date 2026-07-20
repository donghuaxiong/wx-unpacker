#!/usr/bin/env python3

"""Inspect an unpacked WeChat mini program or mini game without modifying it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


RESERVED_DIR_RE = re.compile(r"^__.*__$")
RELATIVE_REQUIRE_RE = re.compile(r"\brequire\(\s*['\"](\.{1,2}/[^'\"]+)['\"]\s*\)")


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # diagnostic tool: report exact file and continue
        errors.append(f"invalid JSON {path}: {exc}")
        return None


def resolve_local_module(source: Path, request: str) -> bool:
    target = (source.parent / request).resolve()
    candidates = [target, Path(str(target) + ".js"), target / "index.js", Path(str(target) + ".json")]
    return any(candidate.is_file() for candidate in candidates)


def inspect(root: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    root = root.resolve()

    app_json = root / "app.json"
    game_json = root / "game.json"
    app_js = root / "app.js"
    game_js = root / "game.js"

    if app_json.exists() or app_js.exists():
        project_type = "mini-program"
        manifest_path = app_json
    elif game_json.exists() or game_js.exists():
        project_type = "mini-game"
        manifest_path = game_json
    else:
        project_type = "unknown"
        manifest_path = None
        errors.append("no app.json/app.js or game.json/game.js found at project root")

    manifest = load_json(manifest_path, errors) if manifest_path and manifest_path.exists() else {}
    if manifest_path and not manifest_path.exists():
        errors.append(f"missing manifest: {manifest_path.name}")

    config_path = root / "project.config.json"
    config = load_json(config_path, errors) if config_path.exists() else {}
    if not config_path.exists():
        warnings.append("project.config.json is missing")

    subpackages = []
    plugins = {}
    pages = []
    if isinstance(manifest, dict):
        pages = manifest.get("pages", []) if isinstance(manifest.get("pages", []), list) else []
        raw_subpackages = manifest.get("subPackages", manifest.get("subpackages", []))
        subpackages = raw_subpackages if isinstance(raw_subpackages, list) else []
        raw_plugins = manifest.get("plugins", manifest.get("gamePlugins", {}))
        plugins = raw_plugins if isinstance(raw_plugins, dict) else {}

    missing_roots = []
    for item in subpackages:
        if not isinstance(item, dict) or not isinstance(item.get("root"), str):
            warnings.append(f"invalid subpackage declaration: {item!r}")
            continue
        package_root = root / item["root"]
        if not package_root.exists():
            missing_roots.append(item["root"])
            errors.append(f"missing subpackage root: {item['root']}")

    reserved_dirs = [str(path.relative_to(root)) for path in root.rglob("*") if path.is_dir() and RESERVED_DIR_RE.match(path.name)]
    for item in reserved_dirs:
        errors.append(f"preview-reserved physical directory: {item}")

    duplicate_subpackage_paths = []
    for path in root.rglob("*"):
        if not path.is_dir():
            continue
        parts = path.relative_to(root).parts
        if len(parts) >= 4:
            for index in range(len(parts) - 3):
                if parts[index] == "subpackages" and parts[index + 2] == "subpackages" and parts[index + 1] == parts[index + 3]:
                    duplicate_subpackage_paths.append(str(path.relative_to(root)))
                    warnings.append(f"possible duplicated subpackage nesting: {path.relative_to(root)}")

    launcher_files = [path for path in (app_js, game_js) if path.exists()]
    missing_requires = []
    for launcher in launcher_files:
        try:
            source = launcher.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"cannot read launcher {launcher}: {exc}")
            continue
        for request in RELATIVE_REQUIRE_RE.findall(source):
            if not resolve_local_module(launcher, request):
                missing_requires.append({"source": str(launcher.relative_to(root)), "request": request})
                errors.append(f"missing launcher require target: {launcher.name} -> {request}")

    indicators = {
        "cocos": any((root / name).exists() for name in ("adapter-min.js", "ccRequire.js", "cocos")),
        "laya": any("laya" in path.name.lower() for path in root.glob("*.js")),
        "egret": any("egret" in path.name.lower() for path in root.glob("*.js")),
        "open_data_context": (root / "openDataContext").exists() or (root / "subContext").exists(),
        "cloud_functions": (root / "cloudfunctions").exists(),
    }

    return {
        "root": str(root),
        "type": project_type,
        "appid": config.get("appid") if isinstance(config, dict) else None,
        "entry": "app.js" if app_js.exists() else "game.js" if game_js.exists() else None,
        "manifest": manifest_path.name if manifest_path else None,
        "pages": len(pages),
        "subpackages": subpackages,
        "plugins": plugins,
        "indicators": indicators,
        "reserved_directories": reserved_dirs,
        "duplicate_subpackage_paths": sorted(set(duplicate_subpackage_paths)),
        "missing_subpackage_roots": missing_roots,
        "missing_launcher_requires": missing_requires,
        "errors": errors,
        "warnings": warnings,
    }


def print_text(report: dict) -> None:
    print(f"Root: {report['root']}")
    print(f"Type: {report['type']}")
    print(f"AppID: {report['appid'] or '(unknown)'}")
    print(f"Entry: {report['entry'] or '(missing)'}")
    print(f"Manifest: {report['manifest'] or '(missing)'}")
    print(f"Pages: {report['pages']}")
    print(f"Subpackages: {len(report['subpackages'])}")
    print(f"Plugins: {len(report['plugins'])}")
    print("Indicators: " + ", ".join(name for name, enabled in report["indicators"].items() if enabled) if any(report["indicators"].values()) else "Indicators: none")
    for warning in report["warnings"]:
        print("WARN: " + warning)
    for error in report["errors"]:
        print("ERROR: " + error)
    print(f"Result: {len(report['errors'])} error(s), {len(report['warnings'])} warning(s)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--strict", action="store_true", help="exit non-zero when errors are found")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"not a directory: {args.root}")
    report = inspect(args.root)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text(report)
    return 1 if args.strict and report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())

